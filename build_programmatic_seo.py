import json
import os
import re
from datetime import datetime

def format_curr(val):
    if val is None or val == "" or str(val).lower() == "none":
        return "R$ --"
    try:
        return f"R$ {float(val):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return "R$ --"

def format_pct(val):
    if val is None or val == "":
        return "N/D"
    try:
        return f"{float(val)*100:.1f}%".replace(".", ",")
    except Exception:
        return "N/D"

def format_mult(val):
    if val is None or val == "":
        return "N/D"
    try:
        return f"{float(val):.2f}x".replace(".", ",")
    except Exception:
        return "N/D"

def format_billions(val):
    if val is None or val == "":
        return "R$ --"
    try:
        num = float(val)
        if abs(num) >= 1e9:
            return f"R$ {num / 1e9:.2f}".replace(".", ",") + " B"
        if abs(num) >= 1e6:
            return f"R$ {num / 1e6:.1f}".replace(".", ",") + " M"
        return f"R$ {num:,.0f}".replace(",", ".")
    except Exception:
        return "R$ --"

def build_programmatic_seo():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, "cache", "standalone_data.json")
    
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    stocks = data.get("stocks", [])
    print(f"[pSEO] Carregados {len(stocks)} ativos da B3 de cache/standalone_data.json")

    # Criar search_index leve para o autocomplete de busca instantanea
    search_index = []
    for s in stocks:
        search_index.append({
            "ticker": s.get("ticker", ""),
            "empresa": s.get("empresa", ""),
            "setor": s.get("setor", ""),
            "quality_score": s.get("quality_score", 0),
            "pl": s.get("pl"),
            "div_yield": s.get("div_yield"),
            "tri_balanco": s.get("tri_balanco", "2T26"),
            "is_latest_balanco": s.get("is_latest_balanco", True)
        })

    # Ler empresa.html como base template (que já tem todas as chaves avaliadas pelo Python)
    empresa_path = os.path.join(base_dir, "empresa.html")
    with open(empresa_path, "r", encoding="utf-8") as f:
        base_html_template = f.read()

    today_str = datetime.now().strftime("%Y-%m-%d")
    sitemap_urls = [
        ('https://moatterminal.com.br/', today_str, 'daily', '1.0'),
        ('https://moatterminal.com.br/empresa.html', today_str, 'daily', '0.5'),
        ('https://moatterminal.com.br/privacidade.html', today_str, 'monthly', '0.3'),
        ('https://moatterminal.com.br/termos.html', today_str, 'monthly', '0.3'),
    ]

    total_generated = 0
    acoes_root = os.path.join(base_dir, "acoes")
    os.makedirs(acoes_root, exist_ok=True)

    for s in stocks:
        ticker = s.get("ticker", "").upper().strip()
        if not ticker:
            continue
            
        ticker_lower = ticker.lower()
        empresa = s.get("empresa", ticker).strip()
        setor = s.get("setor", "Geral").strip()
        subsetor = s.get("subsetor", s.get("sub_setor", "")).strip() or setor
        cotacao = s.get("cotacao", 0)
        quality_score = float(s.get("quality_score", 0) or 0)
        quality_tier = s.get("quality_tier", "TIER 2")
        quality_tag = s.get("quality_tag", "EQUILIBRADA")
        entry_status = s.get("entry_status", "Neutro")
        entry_tag = s.get("entry_tag", "NEUTRO")
        roic_val = s.get("roic") or s.get("roe") or 0
        roe_val = s.get("roe") or 0
        pl_val = s.get("pl")
        pvp_val = s.get("pvp")
        dy_val = s.get("div_yield") or 0
        ey_spread = s.get("ey_spread") or 0
        div_liq_ebitda = s.get("div_liq_ebitda")
        det = s.get("details", {}) or {}
        val_mercado = det.get("valor_mercado")
        val_firma = det.get("valor_firma")
        rationale = s.get("rationale", "").strip() or f"Avaliação quantitativa de qualidade do modelo Moat Terminal para {empresa}."
        
        roic_str = format_pct(roic_val)
        roe_str = format_pct(roe_val)
        pl_str = format_mult(pl_val) if pl_val is not None else "N/D"
        pvp_str = format_mult(pvp_val) if pvp_val is not None else "N/D"
        dy_str = format_pct(dy_val)
        cot_str = format_curr(cotacao)
        val_merc_str = format_billions(val_mercado)
        val_firma_str = format_billions(val_firma)
        div_str = f"{div_liq_ebitda:.2f}x".replace(".", ",") if div_liq_ebitda is not None else "N/D"
        
        # Meta tags ricas de SEO
        canonical_url = f"https://moatterminal.com.br/acoes/{ticker_lower}/"
        page_title = f"{ticker} • {empresa} — Análise Fundamentalista, Fosso Econômico e ROIC | Moat Terminal"
        meta_desc = f"Análise fundamentalista de {empresa} ({ticker}): Fosso Econômico (Moat Score: {quality_score:.1f}/100 - {quality_tier}), ROIC de {roic_str}, P/L {pl_str}, Dividend Yield {dy_str}, valuation de Graham e alocação de capital na B3."
        og_title = f"{ticker} ({empresa}) • Fosso Econômico e Indicadores B3 | Moat Terminal"
        og_desc = f"Moat Score: {quality_score:.1f}/100 ({quality_tier}) | ROIC: {roic_str} | P/L: {pl_str} | DY: {dy_str}. Análise auditada de alocação de capital na B3."

        # Textos das 4 perguntas e respostas para o FAQ Schema.org
        faq_q1 = f"Qual é o Fosso Econômico (Economic Moat) da {empresa} ({ticker})?"
        faq_a1 = f"A {empresa} ({ticker}) possui um Moat Score de {quality_score:.1f}/100, classificado no {quality_tier} ({quality_tag}). A empresa atua no setor de {setor} ({subsetor}) com indicadores auditados de rentabilidade sobre capital e consistência de balanço no Moat Terminal."

        faq_q2 = f"Qual é a rentabilidade e o ROIC de {ticker}?"
        faq_a2 = f"{ticker} entrega atualmente um ROIC de {roic_str} e um ROE de {roe_str}. No Moat Terminal, o Retorno sobre Capital Investido avalia a capacidade da diretoria de compor valor econômico acima do custo de capital da economia."

        faq_q3 = f"Quanto {ticker} paga de dividendos (Dividend Yield)?"
        faq_a3 = f"Atualmente, {ticker} apresenta um Dividend Yield de {dy_str}. A distribuição de dividendos e JCP depende da geração de caixa livre, da política de payout da companhia e das oportunidades de reinvestimento no próprio negócio."

        faq_q4 = f"Qual é o valuation e preço sobre lucro de {ticker} hoje?"
        faq_a4 = f"Negociada a um múltiplo P/L de {pl_str} e P/VP de {pvp_str}, {ticker} oferece um Spread de Earnings Yield de {ey_spread:+.1f}% sobre o juro real da NTN-B (Tesouro IPCA+). O modelo de Graham e a curva de dispersão indicam o enquadramento de entrada no mercado."

        # Schema.org JSON-LD estruturado
        schema_data = {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "BreadcrumbList",
                    "itemListElement": [
                        {"@type": "ListItem", "position": 1, "name": "Moat Terminal", "item": "https://moatterminal.com.br/"},
                        {"@type": "ListItem", "position": 2, "name": "Ações B3", "item": "https://moatterminal.com.br/index.html"},
                        {"@type": "ListItem", "position": 3, "name": setor, "item": f"https://moatterminal.com.br/index.html?sector={setor}"},
                        {"@type": "ListItem", "position": 4, "name": ticker, "item": canonical_url}
                    ]
                },
                {
                    "@type": "Corporation",
                    "name": empresa,
                    "tickerSymbol": ticker,
                    "url": canonical_url,
                    "description": f"Análise fundamentalista e vantagens competitivas (Economic Moat) de {empresa} ({ticker}) na B3."
                },
                {
                    "@type": "FinancialProduct",
                    "name": f"Ação {ticker} - {empresa}",
                    "description": meta_desc,
                    "provider": {
                        "@type": "Organization",
                        "name": "MOAT TERMINAL",
                        "url": "https://moatterminal.com.br"
                    }
                },
                {
                    "@type": "FAQPage",
                    "mainEntity": [
                        {
                            "@type": "Question",
                            "name": faq_q1,
                            "acceptedAnswer": {"@type": "Answer", "text": faq_a1}
                        },
                        {
                            "@type": "Question",
                            "name": faq_q2,
                            "acceptedAnswer": {"@type": "Answer", "text": faq_a2}
                        },
                        {
                            "@type": "Question",
                            "name": faq_q3,
                            "acceptedAnswer": {"@type": "Answer", "text": faq_a3}
                        },
                        {
                            "@type": "Question",
                            "name": faq_q4,
                            "acceptedAnswer": {"@type": "Answer", "text": faq_a4}
                        }
                    ]
                }
            ]
        }
        schema_json_str = json.dumps(schema_data, ensure_ascii=False, indent=2)

        # Breadcrumbs HTML semantico
        breadcrumbs_html = f"""
    <!-- BREADCRUMB SEMÂNTICO (SEO & NAVEGAÇÃO HIERÁRQUICA) -->
    <nav aria-label="breadcrumb" class="flex items-center gap-1.5 text-[11px] font-sans text-slate-500 mb-2">
      <a href="/index.html" class="hover:text-[#004B49] transition">Home</a>
      <span>›</span>
      <a href="/index.html" class="hover:text-[#004B49] transition">Ações B3</a>
      <span>›</span>
      <span class="text-slate-400">{setor}</span>
      <span>›</span>
      <span class="font-bold text-slate-900">{ticker}</span>
    </nav>"""

        # Pre-rendered Hero Card HTML para rastreadores
        entry_badge_bg = "bg-emerald-600 text-white" if entry_tag == "ASSIMETRIA_FAVORAVEL" else ("bg-amber-500 text-white" if entry_tag == "PRECO_JUSTO" else "bg-slate-700 text-white")
        tier_label = "Tier 1 (Wide Moat)" if quality_score >= 80 else ("Tier 2 (Narrow Moat)" if quality_score >= 65 else "Tier 3 (No Moat)")

        prerendered_hero_html = f"""
      <div class="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-6">
        <div class="flex items-center gap-4 min-w-0">
          <div class="w-16 h-16 rounded-2xl flex items-center justify-center overflow-hidden flex-shrink-0 bg-slate-100 border border-slate-200 shadow-xs relative">
            <img src="https://raw.githubusercontent.com/thefintz/icones-b3/main/icones/{ticker}.png" alt="{ticker}" class="w-full h-full object-contain p-1" onerror="this.style.display='none';" />
          </div>
          <div class="flex flex-col min-w-0">
            <div class="flex flex-wrap items-center gap-2">
              <h1 class="text-2xl sm:text-3xl font-bold font-editorial text-slate-900 tracking-wide">{ticker}</h1>
              <span class="text-xs px-2.5 py-0.5 rounded-full font-mono font-bold bg-white text-slate-800 border border-slate-200">2T26 Auditado</span>
              <span class="text-xs px-3 py-0.5 rounded-full font-sans font-semibold {entry_badge_bg}">{entry_status}</span>
              <span class="text-xs px-2.5 py-0.5 rounded-full font-mono font-bold bg-white text-slate-800 border border-slate-200">{quality_tier}</span>
            </div>
            <div class="text-base font-medium font-editorial text-slate-800 mt-1 truncate">{empresa}</div>
            <div class="text-xs text-slate-500 font-sans mt-0.5 flex flex-wrap items-center gap-2">
              <span>Setor: <b class="text-slate-800">{setor}</b></span>
              <span>•</span>
              <span>Segmento: <b class="text-slate-800">{subsetor}</b></span>
              <span>•</span>
              <span>Liquidez: <b class="text-slate-800">{format_billions(s.get('liq_2m'))}/dia</b></span>
            </div>
          </div>
        </div>

        <div class="flex flex-wrap items-center gap-4 sm:gap-6 self-stretch lg:self-auto justify-between lg:justify-end border-t lg:border-t-0 pt-4 lg:pt-0 border-slate-100">
          <div class="flex flex-col text-left lg:text-right">
            <span class="text-[11px] text-slate-500 uppercase font-mono font-semibold">Cotação Atual</span>
            <span class="text-2xl font-bold font-mono text-slate-900 mt-0.5">{cot_str}</span>
            <span class="text-[10px] text-slate-500 font-sans">Mercado B3 à vista</span>
          </div>

          <div class="flex flex-col text-left lg:text-right">
            <span class="text-[11px] text-slate-500 uppercase font-mono font-semibold">Valor de Mercado</span>
            <span class="text-lg font-bold font-mono text-slate-800 mt-0.5">{val_merc_str}</span>
            <span class="text-[10px] text-slate-500 font-sans">EV: {val_firma_str}</span>
          </div>

          <div class="flex flex-col items-center justify-center p-3 rounded-2xl border bg-white border-slate-300 min-w-[95px] shadow-2xs">
            <span class="text-[10px] font-mono font-bold uppercase tracking-wider text-slate-500">Qualidade</span>
            <span class="text-2xl font-bold font-mono leading-none my-0.5 text-slate-900">{quality_score:.1f}</span>
            <span class="text-[9px] font-mono font-semibold text-slate-700">{tier_label}</span>
          </div>
        </div>
      </div>
"""

        # Pre-rendered FAQ Accordion HTML
        faq_section_html = f"""
    <!-- SEÇÃO DIDÁTICA DE PERGUNTAS FREQUENTES (FAQ & RESPOSTAS ESTRUTURADAS PARA O GOOGLE E IA) -->
    <section class="mt-8 pt-8 border-t border-slate-200 space-y-4">
      <div class="flex items-center justify-between">
        <div>
          <h2 class="text-lg font-serif font-bold text-slate-900">Perguntas Frequentes sobre {empresa} ({ticker})</h2>
          <p class="text-xs text-slate-500 font-sans mt-0.5">Respostas fundamentadas nos demonstrativos contábeis e no modelo de vantagens competitivas.</p>
        </div>
        <span class="text-[10px] font-mono text-[#004B49] bg-[#E6F4F1] border border-[#BCE5DC] px-2.5 py-1 rounded-full font-bold">2T26 CVM Auditado</span>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="p-4 rounded-2xl bg-white border border-slate-200 shadow-2xs space-y-2">
          <h3 class="text-xs font-mono font-bold text-slate-900 flex items-center gap-1.5">
            <span class="w-2 h-2 rounded-full bg-[#00A887] flex-shrink-0"></span>
            {faq_q1}
          </h3>
          <p class="text-xs text-slate-600 leading-relaxed font-sans">{faq_a1}</p>
        </div>

        <div class="p-4 rounded-2xl bg-white border border-slate-200 shadow-2xs space-y-2">
          <h3 class="text-xs font-mono font-bold text-slate-900 flex items-center gap-1.5">
            <span class="w-2 h-2 rounded-full bg-emerald-600 flex-shrink-0"></span>
            {faq_q2}
          </h3>
          <p class="text-xs text-slate-600 leading-relaxed font-sans">{faq_a2}</p>
        </div>

        <div class="p-4 rounded-2xl bg-white border border-slate-200 shadow-2xs space-y-2">
          <h3 class="text-xs font-mono font-bold text-slate-900 flex items-center gap-1.5">
            <span class="w-2 h-2 rounded-full bg-indigo-600 flex-shrink-0"></span>
            {faq_q3}
          </h3>
          <p class="text-xs text-slate-600 leading-relaxed font-sans">{faq_a3}</p>
        </div>

        <div class="p-4 rounded-2xl bg-white border border-slate-200 shadow-2xs space-y-2">
          <h3 class="text-xs font-mono font-bold text-slate-900 flex items-center gap-1.5">
            <span class="w-2 h-2 rounded-full bg-amber-600 flex-shrink-0"></span>
            {faq_q4}
          </h3>
          <p class="text-xs text-slate-600 leading-relaxed font-sans">{faq_a4}</p>
        </div>
      </div>
    </section>
"""

        # Pares setoriais para o grafico comparativo (top 6 do mesmo setor)
        peers = [p for p in stocks if p.get("setor") == setor and p.get("ticker") != ticker and p.get("is_liquid_1m")]
        peers.sort(key=lambda x: x.get("quality_score", 0), reverse=True)
        peers = peers[:6]

        stock_page_data = {
            "stocks": [s] + peers,
            "searchIndex": search_index
        }
        stock_page_json_str = json.dumps(stock_page_data, ensure_ascii=False)

        # Montar a pagina HTML a partir do template limpo de empresa.html
        page_html = base_html_template

        # 1. Substituir tags de Head (title, meta desc, canonical, og, schema)
        page_html = page_html.replace(
            '<title id="pageTitle">Dossiê de Empresa • Moat Terminal</title>',
            f'<title id="pageTitle">{page_title}</title>'
        )
        page_html = page_html.replace(
            '<meta name="description" content="Dossiê fundamentalista institucional de ações B3: decomposição DuPont, histórico auditado de 5 anos, valuation Graham e Bazin, e análise de fosso econômico (Economic Moat).">',
            f'<meta name="description" content="{meta_desc}">'
        )
        page_html = page_html.replace(
            '<link rel="canonical" id="canonicalTag" href="https://moatterminal.com.br/empresa.html">',
            f'<link rel="canonical" id="canonicalTag" href="{canonical_url}">'
        )
        page_html = page_html.replace(
            '<meta property="og:url" id="ogUrl" content="https://moatterminal.com.br/empresa.html">',
            f'<meta property="og:url" id="ogUrl" content="{canonical_url}">'
        )
        page_html = page_html.replace(
            '<meta property="og:title" id="ogTitle" content="Dossiê de Empresa • Moat Terminal">',
            f'<meta property="og:title" id="ogTitle" content="{og_title}">'
        )
        page_html = page_html.replace(
            '<meta property="og:description" content="Análise fundamentalista institucional e vantagens competitivas (Moats) da B3.">',
            f'<meta property="og:description" content="{og_desc}">'
        )
        page_html = page_html.replace(
            '<meta name="twitter:title" id="twTitle" content="Dossiê de Empresa • Moat Terminal">',
            f'<meta name="twitter:title" id="twTitle" content="{og_title}">'
        )
        page_html = page_html.replace(
            '<meta name="twitter:description" content="Análise fundamentalista completa e vantagens competitivas (Moats) da B3.">',
            f'<meta name="twitter:description" content="{og_desc}">'
        )

        # 2. Substituir Schema.org JSON-LD de forma robusta
        old_schema_str = """  <!-- Schema.org JSON-LD -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "FinancialProduct",
    "name": "Dossiê Fundamentalista B3",
    "description": "Análise quantitativa e qualitativa de vantagens competitivas duradouras (Economic Moats) na B3",
    "provider": {
      "@type": "Organization",
      "name": "MOAT TERMINAL",
      "url": "https://moatterminal.com.br"
    }
  }
  </script>"""
        new_schema_str = f"""  <!-- Schema.org JSON-LD Estruturado (Breadcrumbs, Corporation, FAQPage) -->
  <script type="application/ld+json">
{schema_json_str}
  </script>"""
        page_html = page_html.replace(old_schema_str, new_schema_str)

        # 3. Inserir Breadcrumbs e Hero Pre-renderizado
        old_hero_container = """    <!-- 1. HERO SECTION: CABEÇALHO DO ATIVO -->
    <div id="companyHeroCard" class="glass-card rounded-2xl p-6 shadow-sm border border-slate-200">
      <!-- Renderizado via JS -->
    </div>"""
        new_hero_container = f"""{breadcrumbs_html}

    <!-- 1. HERO SECTION: CABEÇALHO DO ATIVO (PRÉ-RENDERIZADO) -->
    <div id="companyHeroCard" class="glass-card rounded-3xl p-6 sm:p-8 border transition-colors duration-200 shadow-sm bg-white border-slate-200">
{prerendered_hero_html}
    </div>"""
        page_html = page_html.replace(old_hero_container, new_hero_container)

        # 4. Inserir FAQ Accordion antes do footer
        page_html = page_html.replace(
            '</main>',
            f'{faq_section_html}\n  </main>'
        )

        # 5. Ajustar links relativos para raiz
        page_html = page_html.replace('href="index.html"', 'href="/index.html"')
        page_html = page_html.replace('href="termos.html"', 'href="/termos.html"')
        page_html = page_html.replace('href="privacidade.html"', 'href="/privacidade.html"')

        # 6. Substituir a linha única de APP_DATA por regex
        page_html = re.sub(
            r'const APP_DATA = \{.*?\};',
            f'const APP_DATA = {stock_page_json_str};',
            page_html
        )

        # 7. Configurar o ticker padrao deste arquivo
        page_html = page_html.replace(
            "let currentTicker = (urlParams.get('ticker') || 'WEGE3').toUpperCase().trim();",
            f"let currentTicker = (urlParams.get('ticker') || '{ticker}').toUpperCase().trim();"
        )

        # 8. Ajustar busca para utilizar searchIndex completo
        page_html = page_html.replace(
            'companySearchResults = APP_DATA.stocks.map(',
            'companySearchResults = (APP_DATA.searchIndex || APP_DATA.stocks).map('
        )

        # 9. Ajustar links nos resultados de busca para irem para a pagina estatica correspondente
        page_html = page_html.replace(
            'href="empresa.html?ticker=${s.ticker}"',
            'href="/acoes/${s.ticker.toLowerCase()}/"'
        )

        # Gravar arquivo estatico na pasta acoes/{ticker_lower}/index.html
        stock_dir = os.path.join(acoes_root, ticker_lower)
        os.makedirs(stock_dir, exist_ok=True)
        stock_file = os.path.join(stock_dir, "index.html")
        with open(stock_file, "w", encoding="utf-8") as f:
            f.write(page_html)

        sitemap_urls.append((canonical_url, today_str, 'daily', '0.9'))
        total_generated += 1

    print(f"[pSEO] Geradas com sucesso {total_generated} páginas estáticas em /acoes/{{ticker}}/")

    # Gerar Sitemap.xml definitivo e completo
    sitemap_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]
    for loc, lastmod, freq, prio in sitemap_urls:
        sitemap_lines.extend([
            '  <url>',
            f'    <loc>{loc}</loc>',
            f'    <lastmod>{lastmod}</lastmod>',
            f'    <changefreq>{freq}</changefreq>',
            f'    <priority>{prio}</priority>',
            '  </url>'
        ])
    sitemap_lines.append('</urlset>')

    sitemap_content = "\n".join(sitemap_lines)
    sitemap_path = os.path.join(base_dir, "sitemap.xml")
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write(sitemap_content)
    print(f"[pSEO] Atualizado sitemap.xml com {len(sitemap_urls)} URLs indexáveis!")

    # Adicionar acoes/ ao Git stage para ser commitado pelo runner de CI
    import shutil
    import subprocess
    git_bin = shutil.which("git")
    if not git_bin and os.name == "nt":
        for c in [r"C:\Users\dougl\AppData\Local\Programs\MinGit\cmd\git.exe", r"C:\Program Files\Git\cmd\git.exe"]:
            if os.path.exists(c):
                git_bin = c
                break
    if git_bin:
        try:
            subprocess.run([git_bin, "add", "acoes/"], cwd=base_dir, check=False)
            print("[pSEO] Diretório acoes/ adicionado ao stage do Git.")
        except Exception as e:
            print(f"[pSEO] Nota: git add acoes/ ignorado: {e}")

if __name__ == "__main__":
    build_programmatic_seo()
