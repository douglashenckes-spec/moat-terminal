import json
import math
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

def generate_moat_decomposition_html(s):
    if not s:
        return ""
    qs = float(s.get("quality_score") or 50.0)
    is_fin = bool(s.get("is_financial"))
    subs = s.get("sub_scores", {}) or {}

    s_ret = float(subs.get("roe" if is_fin else "roic", s.get("pilar_rentabilidade", 50)))
    s_mrg = float(subs.get("mrg_liq", 50)) if is_fin else (float(subs.get("mrg_bruta", 50)) * 0.5 + float(subs.get("mrg_liq", 50)) * 0.5)
    s_cons = float(s.get("pilar_consistencia", 50))
    s_sol = float(s.get("pilar_solidez", 50))

    raw_p1 = (s_ret / 100.0) * 30.0
    raw_p2 = (s_mrg / 100.0) * 25.0
    raw_p3 = (s_cons / 100.0) * 25.0
    raw_p4 = (s_sol / 100.0) * 20.0

    raw_sum = raw_p1 + raw_p2 + raw_p3 + raw_p4
    scale = (qs / raw_sum) if raw_sum > 0 else 1.0

    p1 = round(min(30.0, max(1.0, raw_p1 * scale)), 1)
    p2 = round(min(25.0, max(1.0, raw_p2 * scale)), 1)
    p3 = round(min(25.0, max(1.0, raw_p3 * scale)), 1)
    p4 = round(qs - (p1 + p2 + p3), 1)
    if p4 < 0:
        p4 = 0.5
        p1 = round(qs - (p2 + p3 + p4), 1)

    pct1 = min(100, max(5, (p1 / 30.0) * 100))
    pct2 = min(100, max(5, (p2 / 25.0) * 100))
    pct3 = min(100, max(5, (p3 / 25.0) * 100))
    pct4 = min(100, max(5, (p4 / 20.0) * 100))

    def get_style(pct):
        if pct >= 75:
            return "bg-emerald-500", "text-emerald-700", "bg-[#00A887]"
        if pct >= 55:
            return "bg-teal-500", "text-teal-700", "bg-teal-600"
        if pct >= 40:
            return "bg-amber-500", "text-amber-700", "bg-amber-500"
        return "bg-rose-500", "text-rose-700", "bg-rose-500"

    dot1, txt1, bar1 = get_style(pct1)
    dot2, txt2, bar2 = get_style(pct2)
    dot3, txt3, bar3 = get_style(pct3)
    dot4, txt4, bar4 = get_style(pct4)

    if is_fin:
        sector_badge_html = """
          <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[10px] font-mono font-bold bg-indigo-50 text-indigo-900 border border-indigo-200 shadow-2xs">
            <span>⚖️</span> Metodologia Ajustada: Setor Financeiro/Seguros
          </span>"""
        title1 = "Retorno Patrimonial (Spread ROE vs NTN-B)"
        title2 = "Eficiência Operacional &amp; Margem de Conversão"
        title3 = "Consistência de Resultados &amp; Payout (5 Anos)"
        title4 = "Escala &amp; Solvência Institucional (Patrimônio Líquido)"

        roe = float(s.get("roe") or 0)
        roe_str = format_pct(roe)
        if roe >= 0.20:
            desc1 = f"ROE de {roe_str} comprova rentabilidade patrimonial excepcional e forte capacidade de composição de lucros dos sócios."
        elif roe >= 0.14:
            desc1 = f"ROE de {roe_str} reflete rentabilidade sólida e resiliente para os padrões de exigência de capital regulatório."
        elif roe >= 0.08:
            desc1 = f"ROE de {roe_str} situa-se em nível mediano frente ao custo de oportunidade da economia brasileira."
        else:
            desc1 = f"ROE de {roe_str} é modesto frente aos riscos de crédito e mercado, reduzindo a criação de valor econômico."

        if p2 >= 20.0:
            desc2 = "Estrutura operacional de ponta com captação a custo controlado e excelente geração de receitas de serviços e tarifas."
        elif p2 >= 15.0:
            desc2 = "Eficiência operacional e conversão dentro dos padrões auditados de bancos múltiplos e seguradoras líderes da B3."
        else:
            desc2 = "Custos operacionais e despesas de intermediação/sinistros pressionam a margem líquida final da operação."

        if p3 >= 20.0:
            desc3 = "Histórico auditado de 5 anos de lucros contínuos (2022-2026), sem distorções graves, prejuízos ou one-offs artificiais."
        elif p3 >= 15.0:
            desc3 = "Geração de resultados estável na maior parte do quinquênio, assegurando boa previsibilidade aos dividendos."
        else:
            desc3 = "Oscilações relevantes de resultados históricos ou quebra recente de lucratividade penalizam a previsibilidade."

        if p4 >= 17.0:
            desc4 = "Escala patrimonial de grande porte com sólida folga sobre os limites regulatórios de Basileia/Susep e captação competitiva."
        elif p4 >= 13.0:
            desc4 = "Estrutura patrimonial suficiente e aderente com segurança às métricas de solvência e liquidez regulamentares."
        else:
            desc4 = "Porte patrimonial menor impõe custo de captação relativamente superior frente aos grandes conglomerados."
    else:
        sector_badge_html = """
          <span class="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-[10px] font-mono font-bold bg-slate-100 text-slate-700 border border-slate-200">
            <span>🛡️</span> Modelo Munger de Fosso Econômico
          </span>"""
        title1 = "Retorno sobre Capital (Spread ROIC vs NTN-B)"
        title2 = "Poder de Precificação &amp; Margens (Proteção Moat)"
        title3 = "Consistência Histórica &amp; Lucro Limpo (5 Anos)"
        title4 = "Solidez Financeira &amp; Desalavancagem (Anti-Crise)"

        roic = float(s.get("roic") or 0)
        roic_str = format_pct(roic)
        if roic >= 0.20:
            desc1 = f"ROIC auditado de {roic_str} supera amplamente o juro real soberano (NTN-B 6,5%), gerando alto valor econômico (EVA)."
        elif roic >= 0.12:
            desc1 = f"ROIC de {roic_str} entrega retorno saudável e consistente acima do custo de oportunidade da economia brasileira."
        elif roic >= 0.06:
            desc1 = f"ROIC de {roic_str} opera em patamar moderado, com spread estreito sobre os títulos soberanos da NTN-B."
        else:
            desc1 = f"ROIC de {roic_str} fica abaixo do custo de oportunidade soberano (NTN-B 6,5%), consumindo valor econômico dos acionistas."

        mrg = float(s.get("mrg_liq") or 0)
        mrg_str = format_pct(mrg)
        if mrg >= 0.15:
            desc2 = f"Margem líquida de {mrg_str} comprova forte poder de precificação contra pressões inflacionárias de custos."
        elif mrg >= 0.07:
            desc2 = f"Margem líquida de {mrg_str} preserva conversão operacional equilibrada dentro da média do setor."
        else:
            desc2 = f"Margem líquida comprimida ({mrg_str}) expõe a operação a variações de insumos e competição predatória."

        if p3 >= 20.0:
            desc3 = "Histórico ininterrupto de lucros no quinquênio (2022-2026), sem distorções contábeis graves ou prejuízos recentes."
        elif p3 >= 15.0:
            desc3 = "Geração de resultados estável na maior parte do quinquênio, assegurando boa previsibilidade aos fluxos operacionais."
        else:
            desc3 = "Oscilações relevantes de resultados históricos ou quebra recente de lucratividade reduzem a previsibilidade projetada."

        dl = s.get("div_liq_ebitda")
        if dl is not None and float(dl) <= 0:
            desc4 = "Empresa opera com caixa líquido positivo (sem endividamento líquido), conferindo blindagem máxima com Selic alta."
        elif dl is not None and float(dl) <= 1.5:
            dl_f = f"{float(dl):.1f}".replace(".", ",")
            desc4 = f"Alavancagem prudente de {dl_f}x EBITDA mantém o balanço confortável e imune a choques de liquidez."
        elif dl is not None and float(dl) <= 2.5:
            dl_f = f"{float(dl):.1f}".replace(".", ",")
            desc4 = f"Alavancagem moderada de {dl_f}x EBITDA exige acompanhamento da cobertura de juros."
        elif dl is not None:
            dl_f = f"{float(dl):.1f}".replace(".", ",")
            desc4 = f"Alavancagem elevada de {dl_f}x EBITDA onera o fluxo de caixa com serviço da dívida sob juros altos."
        else:
            desc4 = "Estrutura patrimonial sem passivos financeiros onerosos que comprometam a continuidade dos negócios."

    p1_str = f"{p1:.1f}".replace(".", ",")
    p2_str = f"{p2:.1f}".replace(".", ",")
    p3_str = f"{p3:.1f}".replace(".", ",")
    p4_str = f"{p4:.1f}".replace(".", ",")
    qs_str = f"{qs:.1f}".replace(".", ",")
    tier_str = s.get("quality_tier", "Tier de Qualidade")

    return f"""
        <!-- DECOMPOSIÇÃO DO MOAT SCORE (RAIO-X DE QUALIDADE INSTITUCIONAL) -->
        <div class="mt-5 p-5 sm:p-6 bg-slate-50/70 border border-slate-200/90 rounded-2xl space-y-4">
          <div class="flex flex-wrap items-center justify-between gap-2 border-b border-slate-200/80 pb-3">
            <div class="flex items-center gap-2.5">
              <div class="w-7 h-7 rounded-lg bg-[#004B49] text-white flex items-center justify-center font-mono text-xs font-bold shadow-2xs">
                RX
              </div>
              <div>
                <h3 class="text-xs sm:text-sm font-bold font-mono text-slate-900 uppercase tracking-wider">
                  Decomposição do Moat Score • Raio-X de Qualidade
                </h3>
                <p class="text-[11px] text-slate-500 font-sans mt-0.5">
                  Auditoria transparente dos 4 pilares quantitativos que formam a nota final de 0 a 100
                </p>
              </div>
            </div>
            {sector_badge_html}
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-3.5 pt-1">
            <!-- Pilar 1 -->
            <div class="p-3.5 rounded-xl bg-white border border-slate-200/80 shadow-3xs space-y-2">
              <div class="flex items-center justify-between text-xs font-mono">
                <span class="font-bold text-slate-800 flex items-center gap-1.5">
                  <span class="w-2 h-2 rounded-full {dot1}"></span>
                  {title1}
                </span>
                <span class="font-bold {txt1}">{p1_str} / 30 pts</span>
              </div>
              <div class="w-full h-1.5 bg-slate-100 rounded-full overflow-hidden">
                <div class="h-full {bar1} rounded-full transition-all duration-500" style="width: {pct1:.0f}%"></div>
              </div>
              <p class="text-[11px] text-slate-600 font-sans leading-relaxed">
                {desc1}
              </p>
            </div>

            <!-- Pilar 2 -->
            <div class="p-3.5 rounded-xl bg-white border border-slate-200/80 shadow-3xs space-y-2">
              <div class="flex items-center justify-between text-xs font-mono">
                <span class="font-bold text-slate-800 flex items-center gap-1.5">
                  <span class="w-2 h-2 rounded-full {dot2}"></span>
                  {title2}
                </span>
                <span class="font-bold {txt2}">{p2_str} / 25 pts</span>
              </div>
              <div class="w-full h-1.5 bg-slate-100 rounded-full overflow-hidden">
                <div class="h-full {bar2} rounded-full transition-all duration-500" style="width: {pct2:.0f}%"></div>
              </div>
              <p class="text-[11px] text-slate-600 font-sans leading-relaxed">
                {desc2}
              </p>
            </div>

            <!-- Pilar 3 -->
            <div class="p-3.5 rounded-xl bg-white border border-slate-200/80 shadow-3xs space-y-2">
              <div class="flex items-center justify-between text-xs font-mono">
                <span class="font-bold text-slate-800 flex items-center gap-1.5">
                  <span class="w-2 h-2 rounded-full {dot3}"></span>
                  {title3}
                </span>
                <span class="font-bold {txt3}">{p3_str} / 25 pts</span>
              </div>
              <div class="w-full h-1.5 bg-slate-100 rounded-full overflow-hidden">
                <div class="h-full {bar3} rounded-full transition-all duration-500" style="width: {pct3:.0f}%"></div>
              </div>
              <p class="text-[11px] text-slate-600 font-sans leading-relaxed">
                {desc3}
              </p>
            </div>

            <!-- Pilar 4 -->
            <div class="p-3.5 rounded-xl bg-white border border-slate-200/80 shadow-3xs space-y-2">
              <div class="flex items-center justify-between text-xs font-mono">
                <span class="font-bold text-slate-800 flex items-center gap-1.5">
                  <span class="w-2 h-2 rounded-full {dot4}"></span>
                  {title4}
                </span>
                <span class="font-bold {txt4}">{p4_str} / 20 pts</span>
              </div>
              <div class="w-full h-1.5 bg-slate-100 rounded-full overflow-hidden">
                <div class="h-full {bar4} rounded-full transition-all duration-500" style="width: {pct4:.0f}%"></div>
              </div>
              <p class="text-[11px] text-slate-600 font-sans leading-relaxed">
                {desc4}
              </p>
            </div>
          </div>

          <div class="pt-2 border-t border-slate-200/70 flex flex-wrap items-center justify-between gap-2 text-[11px] font-mono text-slate-500">
            <span>Soma dos Pilares: <b class="text-slate-900">{qs_str} / 100 pts</b> ({tier_str})</span>
            <span class="text-slate-400">Metodologia Auditada CVM 2T26 • Sem Caixa-Preta</span>
          </div>
        </div>
    """

def generate_acoes_directory(stocks, base_dir, today_str):
    """
    Gera a página central de diretório /acoes/index.html
    com todas as 201 ações da B3 categorizadas por setor e com links diretos
    para acelerar a indexação do Googlebot e resolver a fila de páginas detectadas.
    """
    acoes_root = os.path.join(base_dir, "acoes")
    os.makedirs(acoes_root, exist_ok=True)
    directory_path = os.path.join(acoes_root, "index.html")

    # Agrupar ações por setor
    sectors_map = {}
    for s in stocks:
        sec = s.get("setor", "Outros").strip() or "Outros"
        if sec not in sectors_map:
            sectors_map[sec] = []
        sectors_map[sec].append(s)

    # Ordenar setores pelo número de ações (decrescente)
    sorted_sectors = sorted(sectors_map.items(), key=lambda x: len(x[1]), reverse=True)

    # Construir os cartões pré-renderizados para cada setor
    sectors_html_parts = []
    category_pills_html = []
    
    # Pill "Todos"
    category_pills_html.append(
        f'<button onclick="filterSector(\'ALL\')" class="sec-pill active px-3 py-1.5 rounded-xl text-xs font-mono font-bold transition border border-[#004B49] bg-[#004B49] text-white cursor-pointer shadow-xs whitespace-nowrap">'
        f'Todos ({len(stocks)})'
        f'</button>'
    )

    for sec_name, sec_stocks in sorted_sectors:
        # Ordenar ações dentro do setor por Moat Score (decrescente)
        sec_stocks_sorted = sorted(sec_stocks, key=lambda x: float(x.get("quality_score", 0) or 0), reverse=True)
        
        slug_id = re.sub(r'[^a-zA-Z0-9]', '', sec_name).lower()
        category_pills_html.append(
            f'<button onclick="filterSector(\'{slug_id}\')" class="sec-pill px-3 py-1.5 rounded-xl text-xs font-mono font-medium transition border border-slate-200 bg-white hover:bg-slate-100 text-slate-700 cursor-pointer shadow-2xs whitespace-nowrap">'
            f'{sec_name} ({len(sec_stocks)})'
            f'</button>'
        )

        cards_html_list = []
        for s in sec_stocks_sorted:
            t = s.get("ticker", "").upper().strip()
            emp = s.get("empresa", t).strip()
            cot = float(s.get("cotacao", 0) or 0)
            cot_str = format_curr(cot)
            score = float(s.get("quality_score", 0) or 0)
            tier = s.get("quality_tier", "TIER 2")
            roic_val = s.get("roic") or s.get("roe") or 0
            roic_str = format_pct(roic_val)
            pl_val = s.get("pl")
            pl_str = format_mult(pl_val) if pl_val is not None else "N/D"
            dy_val = s.get("div_yield") or 0
            dy_str = format_pct(dy_val)
            det = s.get("details", {}) or {}
            lpa = float(det.get("lpa")) if det.get("lpa") not in [None, ""] else None
            vpa = float(det.get("vpa")) if det.get("vpa") not in [None, ""] else None
            
            graham_price = None
            if lpa and vpa and lpa > 0 and vpa > 0:
                graham_price = math.sqrt(22.5 * lpa * vpa)
            graham_str = format_curr(graham_price) if graham_price else "N/D"

            bazin_price = None
            if dy_val and dy_val > 0 and cot > 0:
                bazin_price = (cot * dy_val) / 0.06
            bazin_str = format_curr(bazin_price) if bazin_price else "N/D"

            tier_badge = "bg-emerald-50 text-emerald-800 border-emerald-200" if "TIER 1" in tier else ("bg-blue-50 text-blue-800 border-blue-200" if "TIER 2" in tier else "bg-slate-100 text-slate-700 border-slate-200")

            cards_html_list.append(f"""
            <div class="stock-dir-card bg-white rounded-2xl p-4 sm:p-5 border border-slate-200 shadow-2xs hover:shadow-md hover:border-[#004B49] transition flex flex-col justify-between group" data-ticker="{t}" data-name="{emp.lower()}" data-sector="{slug_id}">
              <div>
                <div class="flex items-center justify-between gap-3 mb-2.5">
                  <div class="flex items-center gap-2.5 min-w-0">
                    <div class="w-9 h-9 rounded-xl flex items-center justify-center overflow-hidden flex-shrink-0 bg-slate-50 border border-slate-200 p-0.5">
                      <img src="https://raw.githubusercontent.com/thefintz/icones-b3/main/icones/{t}.png" alt="{t}" class="w-full h-full object-contain" onerror="this.style.display='none';" />
                    </div>
                    <div class="min-w-0">
                      <a href="/acoes/{t.lower()}/" class="text-base font-bold font-mono text-slate-900 group-hover:text-[#004B49] transition truncate block">
                        {t}
                      </a>
                      <span class="text-[11px] text-slate-500 font-sans truncate block">{emp}</span>
                    </div>
                  </div>
                  <span class="text-[10px] font-mono px-2 py-0.5 rounded-full font-bold border {tier_badge} flex-shrink-0">
                    Moat {f"{score:.1f}".replace(".", ",")}
                  </span>
                </div>

                <div class="grid grid-cols-3 gap-1.5 py-2.5 border-y border-slate-100 font-mono text-xs">
                  <div>
                    <span class="text-[10px] text-slate-600 block uppercase font-sans">Cotação</span>
                    <b class="text-slate-900">{cot_str}</b>
                  </div>
                  <div>
                    <span class="text-[10px] text-slate-600 block uppercase font-sans">ROIC / ROE</span>
                    <b class="text-emerald-700">{roic_str}</b>
                  </div>
                  <div>
                    <span class="text-[10px] text-slate-600 block uppercase font-sans">Div. Yield</span>
                    <b class="text-indigo-700">{dy_str}</b>
                  </div>
                </div>

                <div class="grid grid-cols-2 gap-2 mt-2.5 text-[11px] font-mono bg-slate-50/70 p-2 rounded-xl border border-slate-100">
                  <div>
                    <span class="text-[10px] text-slate-600 block font-sans">Preço Graham:</span>
                    <span class="font-bold text-slate-800">{graham_str}</span>
                  </div>
                  <div>
                    <span class="text-[10px] text-slate-600 block font-sans">Teto Bazin (6%):</span>
                    <span class="font-bold text-slate-800">{bazin_str}</span>
                  </div>
                </div>
              </div>

              <a href="/acoes/{t.lower()}/" class="mt-3.5 w-full py-1.5 px-3 rounded-xl bg-slate-100 hover:bg-[#004B49] hover:text-white text-slate-700 text-xs font-sans font-semibold transition text-center flex items-center justify-center gap-1.5 group-hover:bg-[#004B49] group-hover:text-white">
                <span>Ver Dossiê {t}</span>
                <span class="text-[10px] font-mono">→</span>
              </a>
            </div>
            """)

        cards_joined = "\n".join(cards_html_list)
        sectors_html_parts.append(f"""
        <section class="sector-group mb-10" id="sector-{slug_id}" data-sector="{slug_id}">
          <div class="flex items-center justify-between mb-4 border-b border-slate-200 pb-2.5">
            <h2 class="text-lg sm:text-xl font-bold font-editorial text-slate-900 flex items-center gap-2">
              <span>{sec_name}</span>
              <span class="text-xs font-mono font-semibold px-2.5 py-0.5 rounded-full bg-slate-100 text-slate-600 border border-slate-200">
                {len(sec_stocks)} ações
              </span>
            </h2>
            <a href="#topo" class="text-xs font-sans text-slate-400 hover:text-[#004B49] transition">Voltar ao topo ↑</a>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {cards_joined}
          </div>
        </section>
        """)

    all_sectors_html = "\n".join(sectors_html_parts)
    category_pills_joined = "\n".join(category_pills_html)

    # Schema.org ItemList para SEO de diretório
    item_list_elements = []
    for idx, s in enumerate(stocks, 1):
        t = s.get("ticker", "").upper().strip()
        item_list_elements.append({
            "@type": "ListItem",
            "position": idx,
            "name": f"{t} - {s.get('empresa', t)}",
            "url": f"https://moatterminal.com.br/acoes/{t.lower()}/"
        })

    schema_directory = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Moat Terminal", "item": "https://moatterminal.com.br/"},
                    {"@type": "ListItem", "position": 2, "name": "Ações B3", "item": "https://moatterminal.com.br/acoes/"}
                ]
            },
            {
                "@type": "CollectionPage",
                "name": "Ações B3: Diretório Completo de Empresas, Setores e Valuation 2026",
                "description": f"Diretório institucional com todas as {len(stocks)} ações da B3 categorizadas por setor econômico, múltiplos de Graham, Preço Teto de Bazin, rentabilidade sobre capital e classificação de Fosso Econômico (Economic Moat).",
                "url": "https://moatterminal.com.br/acoes/",
                "mainEntity": {
                    "@type": "ItemList",
                    "numberOfItems": len(stocks),
                    "itemListElement": item_list_elements[:50] # Top 50 para payload equilibrado
                }
            }
        ]
    }
    schema_dir_json = json.dumps(schema_directory, ensure_ascii=False, indent=2)

    directory_html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Ações B3: Lista Completa de Empresas, Setores e Valuation 2026 • Moat Terminal</title>
  <meta name="description" content="Diretório completo de ações da B3: lista com todas as {len(stocks)} empresas organizadas por setor com Preço Justo de Graham, Preço Teto Bazin, ROIC e Economic Moat.">
  <meta name="keywords" content="ações B3, lista de ações, empresas da bolsa, setores B3, valuation, Graham, Bazin, ROIC, dividendos, fosso econômico">
  <meta name="author" content="MOAT TERMINAL">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="https://moatterminal.com.br/acoes/">

  <!-- Open Graph -->
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://moatterminal.com.br/acoes/">
  <meta property="og:title" content="Ações B3: Lista Completa de Empresas, Setores e Valuation 2026 • Moat Terminal">
  <meta property="og:description" content="Guia completo de {len(stocks)} ações listadas na bolsa brasileira B3 com múltiplos de Graham, Bazin, ROIC e Moat Score.">
  <meta property="og:site_name" content="MOAT TERMINAL">
  <meta property="og:locale" content="pt_BR">

  <!-- Twitter / X -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Ações B3: Diretório Completo de Empresas • Moat Terminal">
  <meta name="twitter:description" content="Consulte todas as ações da B3 organizadas por setor com análise de valor intrínseco Graham e Preço Teto Bazin.">

  <!-- Schema.org JSON-LD -->
  <script type="application/ld+json">
{schema_dir_json}
  </script>

  <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32' fill='none'%3E%3Ccircle cx='16' cy='16' r='14' stroke='%2300A887' stroke-width='1.5'/%3E%3Cpath d='M16 4.6 L18.4 8.2 L22.4 7.6 L25.8 10.4 L24.2 14.4 L26.4 16 L24.2 17.6 L25.8 21.6 L22.4 24.4 L18.4 23.8 L16 27.4 L13.6 23.8 L9.6 24.4 L6.2 21.6 L7.8 17.6 L5.6 16 L7.8 14.4 L6.2 10.4 L9.6 7.6 L13.6 8.2 Z' stroke='%2300A887' stroke-width='1.5' fill='rgba(0,168,135,0.2)'/%3E%3Cpolygon points='16,10.6 19.6,16 16,21.4 12.4,16' fill='%2300A887'/%3E%3Cpolygon points='16,12.2 18.2,16 16,19.8 13.8,16' fill='%23FFFFFF'/%3E%3C/svg%3E">

  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;0,6..72,700;1,6..72,400&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">

  <!-- GOOGLE ADSENSE -->
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8661500874049196" crossorigin="anonymous"></script>

  <!-- Google Analytics 4 -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-QJPB4NM5PW"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-QJPB4NM5PW');
  </script>

  <!-- Tailwind CSS -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {{
      theme: {{
        extend: {{
          fontFamily: {{
            serif: ['Newsreader', 'Georgia', 'serif'],
            sans: ['Plus Jakarta Sans', 'Inter', 'sans-serif'],
            mono: ['JetBrains Mono', 'monospace'],
          }},
          colors: {{
            bcgForest: '#004B49',
            bcgDeep: '#003836',
            bcgMint: '#00A887',
            bcgLightMint: '#E6F4F1',
            bcgWarmBg: '#FBFBF9',
            bcgCard: '#FFFFFF',
            bcgBorder: '#E7E7E2',
          }}
        }}
      }}
    }}
  </script>
  <style>
    body {{
      background-color: #FBFBF9;
      background-image: 
        radial-gradient(circle at 10% 15%, rgba(0, 75, 73, 0.025) 0%, transparent 45%),
        radial-gradient(circle at 90% 80%, rgba(0, 168, 135, 0.025) 0%, transparent 45%);
      background-attachment: fixed;
      color: #1A202C;
      font-family: 'Plus Jakarta Sans', 'Inter', sans-serif;
    }}
    .font-editorial {{
      font-family: 'Newsreader', Georgia, serif;
    }}
    .no-scrollbar::-webkit-scrollbar {{
      display: none;
    }}
    .no-scrollbar {{
      -ms-overflow-style: none;
      scrollbar-width: none;
    }}
  </style>
</head>
<body class="min-h-screen flex flex-col bg-[#FBFBF9] text-[#1A202C]" id="topo">

  <!-- TOPBAR INSTITUCIONAL -->
  <header class="sticky top-0 z-40 bg-white/95 backdrop-blur-md border-b border-[#E7E7E2] text-slate-900 shadow-xs">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-14 sm:h-[68px] flex items-center justify-between gap-4">
      
      <!-- Logo Moat Terminal -->
      <a href="/index.html" class="flex items-center gap-2 sm:gap-3.5 group cursor-pointer flex-shrink-0" title="Moat Terminal - Home">
        <div class="w-8 h-8 sm:w-10 sm:h-10 rounded-xl bg-[#003836] border border-[#004B49] flex items-center justify-center text-white shadow-xs group-hover:scale-105 transition-all">
          <svg class="w-5 h-5 sm:w-6 sm:h-6 text-[#00A887]" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="16" cy="16" r="14.2" stroke="currentColor" stroke-width="1.2" opacity="0.65" />
            <circle cx="16" cy="16" r="12.6" stroke="currentColor" stroke-width="0.75" stroke-dasharray="1.5 1.5" opacity="0.4" />
            <path d="M16 4.6 L18.4 8.2 L22.4 7.6 L25.8 10.4 L24.2 14.4 L26.4 16 L24.2 17.6 L25.8 21.6 L22.4 24.4 L18.4 23.8 L16 27.4 L13.6 23.8 L9.6 24.4 L6.2 21.6 L7.8 17.6 L5.6 16 L7.8 14.4 L6.2 10.4 L9.6 7.6 L13.6 8.2 Z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round" fill="rgba(0, 168, 135, 0.12)" />
            <circle cx="16" cy="16" r="6.6" stroke="currentColor" stroke-width="1.1" opacity="0.85" />
            <polygon points="16,10.6 19.6,16 16,21.4 12.4,16" fill="currentColor" />
            <polygon points="16,12.2 18.2,16 16,19.8 13.8,16" fill="#FFFFFF" opacity="0.95" />
          </svg>
        </div>
        <div class="flex flex-col">
          <div class="flex items-center gap-1.5 sm:gap-2">
            <span class="font-bold text-slate-900 text-xs sm:text-base tracking-[0.10em] sm:tracking-[0.14em] font-['Cinzel',serif] leading-none group-hover:text-[#004B49] transition-colors whitespace-nowrap">MOAT TERMINAL</span>
            <span class="px-1 py-0.2 sm:px-1.5 sm:py-0.5 text-[7.5px] sm:text-[8px] bg-[#E6F4F1] text-[#004B49] border border-[#BCE5DC] font-bold font-mono rounded tracking-wider flex-shrink-0">EMPRESAS</span>
          </div>
          <span class="text-[10px] text-slate-500 font-sans mt-0.5 hidden sm:inline">Lista Completa de Empresas B3</span>
        </div>
      </a>

      <!-- Navegação Superior -->
      <nav class="flex items-center gap-2 text-xs font-sans">
        <a href="/index.html" class="px-3 py-1.5 rounded-xl text-slate-700 hover:text-slate-900 hover:bg-slate-100 transition font-medium">Panorama Geral</a>
        <a href="/index.html" class="hidden sm:inline-block px-3 py-1.5 rounded-xl text-slate-700 hover:text-slate-900 hover:bg-slate-100 transition font-medium">Scanner</a>
        <a href="/sobre.html" class="hidden md:inline-block px-3 py-1.5 rounded-xl text-slate-700 hover:text-slate-900 hover:bg-slate-100 transition font-medium">Metodologia</a>
        <a href="/acoes/" class="px-3 py-1.5 rounded-xl bg-[#004B49] text-white font-semibold shadow-xs">Empresas</a>
      </nav>

    </div>
  </header>

  <!-- CONTEÚDO PRINCIPAL -->
  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 flex-1 w-full space-y-8">
    
    <!-- BREADCRUMB -->
    <nav aria-label="breadcrumb" class="flex items-center gap-1.5 text-xs font-sans text-slate-500">
      <a href="/index.html" class="hover:text-[#004B49] transition">Home</a>
      <span>›</span>
      <span class="font-bold text-slate-900">Empresas B3 (Diretório Completo)</span>
    </nav>

    <!-- HERO HEADER DO DIRETÓRIO -->
    <div class="bg-white rounded-3xl p-6 sm:p-10 border border-slate-200 shadow-sm space-y-4">
      <div class="flex flex-wrap items-center justify-between gap-3 border-b border-slate-100 pb-4">
        <div class="space-y-1">
          <span class="text-xs font-mono font-bold uppercase tracking-wider text-[#004B49] bg-[#E6F4F1] border border-[#BCE5DC] px-2.5 py-0.5 rounded-full inline-block">
            Base CVM 2T26 Auditada
          </span>
          <h1 class="text-2xl sm:text-4xl font-bold font-editorial text-slate-900">
            Ações da B3: Diretório Completo de Empresas e Setores
          </h1>
        </div>
        <div class="flex items-center gap-2">
          <span class="text-xs font-mono font-bold text-emerald-700 bg-emerald-50 border border-emerald-200 px-3 py-1.5 rounded-xl">
            {len(stocks)} Ações Cobertas
          </span>
        </div>
      </div>

      <p class="text-sm sm:text-base text-slate-600 leading-relaxed font-sans max-w-4xl">
        Consulte todas as <b>{len(stocks)} companhias abertas negociadas na B3</b> (bolsa de valores brasileira). Acesse dossiês analíticos individuais com múltiplos auditados de valuation clássico (<b>Valor Intrínseco de Graham</b> e <b>Preço Teto de Décio Bazin 6%</b>), rentabilidade sobre capital investido (<b>ROIC</b> e <b>ROE</b>) e classificação quantitativa de <b>Fosso Econômico (Economic Moat)</b>.
      </p>

      <!-- KPI Pills -->
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-2">
        <div class="p-3 rounded-2xl bg-slate-50 border border-slate-200">
          <span class="text-[10px] font-mono uppercase text-slate-600 block">Total de Empresas</span>
          <b class="text-xl font-mono text-slate-900">{len(stocks)} Ações</b>
        </div>
        <div class="p-3 rounded-2xl bg-slate-50 border border-slate-200">
          <span class="text-[10px] font-mono uppercase text-slate-600 block">Setores Cobertos</span>
          <b class="text-xl font-mono text-slate-900">{len(sorted_sectors)} Setores</b>
        </div>
        <div class="p-3 rounded-2xl bg-slate-50 border border-slate-200">
          <span class="text-[10px] font-mono uppercase text-slate-600 block">Metodologia</span>
          <b class="text-xl font-mono text-slate-900">Value Investing</b>
        </div>
        <div class="p-3 rounded-2xl bg-slate-50 border border-slate-200">
          <span class="text-[10px] font-mono uppercase text-slate-600 block">Acesso</span>
          <b class="text-xl font-mono text-emerald-700">100% Gratuito</b>
        </div>
      </div>
    </div>

    <!-- BARRA DE PESQUISA & FILTRO POR SETOR -->
    <div class="sticky top-14 sm:top-[68px] z-30 bg-[#FBFBF9]/95 backdrop-blur-md py-3 space-y-3">
      <!-- Input de Busca Rápida -->
      <div class="relative max-w-2xl">
        <span class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
          <svg class="w-4 h-4 stroke-[2]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-4.35-4.35"/></svg>
        </span>
        <input type="text" id="dirSearchInput" oninput="handleDirectorySearch(this.value)" placeholder="Buscar por ticker, empresa ou setor (ex: WEGE3, Vale, Elétricas, Bancos)..." class="w-full bg-white border border-slate-300 focus:border-[#004B49] focus:ring-2 focus:ring-[#004B49]/20 rounded-2xl pl-10 pr-4 py-2.5 text-xs sm:text-sm font-sans text-slate-900 placeholder-slate-400 focus:outline-none transition shadow-xs" autocomplete="off" />
      </div>

      <!-- Pills de Filtro Setorial com Scroll Lateral -->
      <div class="flex items-center gap-1.5 overflow-x-auto no-scrollbar pb-1 select-none" id="sectorPillsWrapper">
        {category_pills_joined}
      </div>
    </div>

    <!-- LISTAGEM POR SETOR -->
    <div id="directoryGridContainer">
      {all_sectors_html}
    </div>

    <!-- SEÇÃO DIDÁTICA E EDITORIAL DE VALUATION & VALUE INVESTING -->
    <section class="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-sm space-y-6">
      <div class="border-b border-slate-100 pb-4">
        <h2 class="text-xl sm:text-2xl font-bold font-editorial text-slate-900">
          Como Analisar Ações com o Modelo Moat Terminal
        </h2>
        <p class="text-xs sm:text-sm text-slate-500 font-sans mt-1">
          Guia prático para interpretar os múltiplos de valuation, a rentabilidade sobre capital e o fosso econômico.
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 text-xs sm:text-sm leading-relaxed text-slate-700">
        <div class="p-5 rounded-2xl bg-slate-50 border border-slate-200 space-y-2">
          <h3 class="font-bold font-mono text-slate-900 text-sm flex items-center gap-2">
            <span class="w-2.5 h-2.5 rounded-full bg-[#00A887]"></span>
            Fosso Econômico (Economic Moat) & ROIC
          </h3>
          <p>
            Inspirado nos ensinamentos de <b>Charlie Munger</b> e <b>Warren Buffett</b>, o Moat Terminal avalia se uma empresa possui barreiras de entrada capazes de proteger seus lucros da concorrência a longo prazo. O principal termômetro contábil é o <b>ROIC (Retorno sobre o Capital Investido)</b>: companhias com ROIC consistentemente superior a 15% ao ano demonstram capacidade superior de alocação de capital e composição de valor para o acionista.
          </p>
        </div>

        <div class="p-5 rounded-2xl bg-slate-50 border border-slate-200 space-y-2">
          <h3 class="font-bold font-mono text-slate-900 text-sm flex items-center gap-2">
            <span class="w-2.5 h-2.5 rounded-full bg-emerald-600"></span>
            Valor Intrínseco de Benjamin Graham
          </h3>
          <p>
            Desenvolvido por <b>Benjamin Graham</b> em <i>O Investidor Inteligente</i>, o modelo calcula o Preço Justo através da fórmula: <code>V = √(22,5 × LPA × VPA)</code>. O método pondera tanto o patrimônio líquido tangível por ação (VPA) quanto a capacidade histórica de geração de lucro por ação (LPA), estabelecendo um referencial teórico conservador com margem de segurança.
          </p>
        </div>

        <div class="p-5 rounded-2xl bg-slate-50 border border-slate-200 space-y-2">
          <h3 class="font-bold font-mono text-slate-900 text-sm flex items-center gap-2">
            <span class="w-2.5 h-2.5 rounded-full bg-indigo-600"></span>
            Preço Teto de Décio Bazin (Yield 6%)
          </h3>
          <p>
            Baseado no clássico brasileiro <i>Faça Fortuna com Ações</i> de <b>Décio Bazin</b>, o preço teto determina a cotação máxima a ser paga por um papel para obter no mínimo <b>6,0% de Dividend Yield anual</b> em proventos (DPA / 0,06). É um método quantitativo consagrado por investidores focados em renda passiva e carteiras previdenciárias de dividendos na B3.
          </p>
        </div>

        <div class="p-5 rounded-2xl bg-slate-50 border border-slate-200 space-y-2">
          <h3 class="font-bold font-mono text-slate-900 text-sm flex items-center gap-2">
            <span class="w-2.5 h-2.5 rounded-full bg-amber-600"></span>
            Spread Real sobre o Tesouro IPCA+ (NTN-B)
          </h3>
          <p>
            Compara o <b>Earnings Yield (Inverso do P/L)</b> da ação com o rendimento do título público soberano livre de risco do governo brasileiro (Tesouro IPCA+ 2035). Investir em empresas na bolsa só se justifica matematicamente quando o retorno esperado oferece um <b>prêmio real de risco positivo</b> sobre a renda fixa atrelada à inflação.
          </p>
        </div>
      </div>
    </section>

    <!-- CONFORMIDADE REGULATÓRIA CVM -->
    <div class="p-5 rounded-2xl bg-slate-100 border border-slate-200 text-slate-600 text-xs leading-relaxed space-y-1.5">
      <div class="font-mono font-bold text-slate-800 flex items-center gap-2 text-[11px]">
        <span>⚖️</span> CONFORMIDADE REGULATÓRIA (RESOLUÇÃO CVM Nº 20/2021)
      </div>
      <p>
        O <b>MOAT TERMINAL</b> é uma ferramenta estritamente computacional, didática e de pesquisa quantitativa independente. As métricas, scores e dados compilados refletem cálculos matemáticos sobre demonstrativos contábeis públicos oficiais divulgados pelas companhias abertas na CVM e B3. <b>Este conteúdo tem finalidade estritamente educacional e informativa</b>, não constituindo consultoria, relatório de análise ou recomendação individualizada de compra ou venda de valores mobiliários.
      </p>
    </div>

  </main>

  <!-- RODAPÉ INSTITUCIONAL -->
  <footer class="bg-white border-t border-slate-200 py-8 px-4 text-center text-xs text-slate-500 font-sans space-y-3 mt-12">
    <div class="flex items-center justify-center gap-4 sm:gap-6 flex-wrap text-xs">
      <a href="/index.html" class="hover:text-[#004B49] transition font-medium">Terminal Scanner</a>
      <span>•</span>
      <a href="/acoes/" class="text-slate-900 font-bold">Empresas</a>
      <span>•</span>
      <a href="/sobre.html" class="hover:text-[#004B49] transition font-medium">Sobre &amp; Metodologia</a>
      <span>•</span>
      <a href="/contato.html" class="hover:text-[#004B49] transition font-medium">Contato</a>
      <span>•</span>
      <a href="/termos.html" class="hover:text-[#004B49] transition font-medium">Termos de Uso</a>
      <span>•</span>
      <a href="/privacidade.html" class="hover:text-[#004B49] transition font-medium">Política de Privacidade</a>
    </div>
    <p class="text-[11px] text-slate-400 font-mono">
      © 2026 MOAT TERMINAL • Economic Moats &amp; Capital Compounding • Todos os direitos reservados.
    </p>
  </footer>

  <!-- SCRIPT DE FILTRAGEM RÁPIDA NO CLIENTE -->
  <script>
    let activeSector = 'ALL';

    function filterSector(slug) {{
      activeSector = slug;
      // Atualizar estilo das pills
      document.querySelectorAll('.sec-pill').forEach(btn => {{
        btn.classList.remove('active', 'bg-[#004B49]', 'text-white', 'border-[#004B49]');
        btn.classList.add('bg-white', 'text-slate-700', 'border-slate-200');
      }});
      event.target.classList.add('active', 'bg-[#004B49]', 'text-white', 'border-[#004B49]');
      event.target.classList.remove('bg-white', 'text-slate-700', 'border-slate-200');

      applyFilters();
    }}

    function handleDirectorySearch(query) {{
      applyFilters();
    }}

    function applyFilters() {{
      const query = (document.getElementById('dirSearchInput').value || '').toLowerCase().trim();
      const sectorGroups = document.querySelectorAll('.sector-group');

      sectorGroups.forEach(group => {{
        const groupSector = group.getAttribute('data-sector');
        const cards = group.querySelectorAll('.stock-dir-card');
        let visibleInGroup = 0;

        cards.forEach(card => {{
          const ticker = card.getAttribute('data-ticker').toLowerCase();
          const name = card.getAttribute('data-name').toLowerCase();
          const matchSector = (activeSector === 'ALL' || groupSector === activeSector);
          const matchSearch = (!query || ticker.includes(query) || name.includes(query));

          if (matchSector && matchSearch) {{
            card.style.display = '';
            visibleInGroup++;
          }} else {{
            card.style.display = 'none';
          }}
        }});

        if (visibleInGroup > 0) {{
          group.style.display = '';
        }} else {{
          group.style.display = 'none';
        }}
      }});
    }}
  </script>

</body>
</html>
"""
    with open(directory_path, "w", encoding="utf-8") as f:
        f.write(directory_html_content)

    print(f"[pSEO] Gerado com sucesso o Diretório Geral /acoes/index.html com {len(stocks)} ações!")

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

    # Ler empresa.html como base template
    empresa_path = os.path.join(base_dir, "empresa.html")
    with open(empresa_path, "r", encoding="utf-8") as f:
        base_html_template = f.read()

    today_str = datetime.now().strftime("%Y-%m-%d")
    sitemap_urls = [
        ('https://moatterminal.com.br/', today_str, 'daily', '1.0'),
        ('https://moatterminal.com.br/acoes/', today_str, 'daily', '0.9'),
        ('https://moatterminal.com.br/sobre.html', today_str, 'weekly', '0.7'),
        ('https://moatterminal.com.br/contato.html', today_str, 'monthly', '0.5'),
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
        cotacao = float(s.get("cotacao", 0) or 0)
        quality_score = float(s.get("quality_score", 0) or 0)
        quality_tier = s.get("quality_tier", "TIER 2")
        quality_tag = s.get("quality_tag", "EQUILIBRADA")
        entry_status = s.get("entry_status", "Neutro")
        entry_tag = s.get("entry_tag", "NEUTRO")
        roic_val = s.get("roic") or s.get("roe") or 0
        roe_val = s.get("roe") or 0
        pl_val = s.get("pl")
        pvp_val = s.get("pvp")
        dy_val = float(s.get("div_yield") or 0)
        ey_spread = float(s.get("ey_spread") or 0)
        div_liq_ebitda = s.get("div_liq_ebitda")
        det = s.get("details", {}) or {}
        val_mercado = det.get("valor_mercado")
        val_firma = det.get("valor_firma")
        lpa = float(det.get("lpa")) if det.get("lpa") not in [None, ""] else None
        vpa = float(det.get("vpa")) if det.get("vpa") not in [None, ""] else None
        
        roic_str = format_pct(roic_val)
        roe_str = format_pct(roe_val)
        pl_str = format_mult(pl_val) if pl_val is not None else "N/D"
        pvp_str = format_mult(pvp_val) if pvp_val is not None else "N/D"
        dy_str = format_pct(dy_val)
        cot_str = format_curr(cotacao)
        val_merc_str = format_billions(val_mercado)
        val_firma_str = format_billions(val_firma)
        div_str = f"{div_liq_ebitda:.2f}x".replace(".", ",") if div_liq_ebitda is not None else "N/D"

        # Modelos Clássicos de Valuation: Graham e Bazin
        graham_price = None
        graham_margin = None
        if lpa and vpa and lpa > 0 and vpa > 0:
            graham_price = math.sqrt(22.5 * lpa * vpa)
            if cotacao > 0:
                graham_margin = ((graham_price - cotacao) / cotacao) * 100

        bazin_price = None
        bazin_margin = None
        if dy_val > 0 and cotacao > 0:
            bazin_price = (cotacao * dy_val) / 0.06
            bazin_margin = ((bazin_price - cotacao) / cotacao) * 100

        graham_str = format_curr(graham_price) if graham_price else "N/D"
        bazin_str = format_curr(bazin_price) if bazin_price else "N/D"
        score_str = f"{quality_score:.1f}".replace(".", ",")
        graham_badge = f"{graham_margin:+.1f}%".replace(".", ",") + " vs cotação" if graham_margin is not None else "LPA/VPA Inválido"
        bazin_badge = f"{bazin_margin:+.1f}%".replace(".", ",") + " vs cotação" if bazin_margin is not None else "Sem Proventos"
        ey_spread_str = f"{ey_spread:+.1f}%".replace(".", ",")

        # Pares setoriais para o gráfico comparativo e interlinking SEO (top 6 do mesmo setor)
        peers = [p for p in stocks if p.get("setor") == setor and p.get("ticker") != ticker and p.get("is_liquid_1m")]
        peers.sort(key=lambda x: x.get("quality_score", 0), reverse=True)
        peers = peers[:6]

        # Meta tags ricas de SEO focadas em alta intenção de busca (High-CTR)
        canonical_url = f"https://moatterminal.com.br/acoes/{ticker_lower}/"
        page_title = f"{ticker} Vale a Pena em 2026? Preço Teto Bazin, Graham e Indicadores • Moat Terminal"
        meta_desc = f"Análise fundamentalista de {empresa} ({ticker}): Preço Justo de Graham ({graham_str}), Preço Teto Bazin 6% ({bazin_str}), Moat Score {score_str}/100 ({quality_tier}), ROIC {roic_str} e dividendos. Veja se {ticker} vale a pena em 2026."
        og_title = f"{ticker} Vale a Pena em 2026? Preço Teto Bazin & Graham • Moat Terminal"
        og_desc = f"Análise de {empresa} ({ticker}): Preço Graham {graham_str}, Preço Bazin {bazin_str}, Moat Score {score_str}/100 ({quality_tier}), ROIC {roic_str}. Indicadores e valuation da B3."

        # Textos das 4 perguntas e respostas para o FAQ Schema.org
        faq_q1 = f"Qual é o Fosso Econômico (Economic Moat) da {empresa} ({ticker})?"
        faq_a1 = f"A {empresa} ({ticker}) possui um Moat Score de {score_str}/100, classificado no {quality_tier} ({quality_tag}). A empresa atua no setor de {setor} ({subsetor}) com indicadores auditados de rentabilidade sobre capital e consistência de balanço no Moat Terminal."

        faq_q2 = f"Qual é a rentabilidade e o ROIC de {ticker}?"
        faq_a2 = f"{ticker} entrega atualmente um ROIC de {roic_str} e um ROE de {roe_str}. No Moat Terminal, o Retorno sobre Capital Investido avalia a capacidade da diretoria de compor valor econômico acima do custo de capital da economia."

        faq_q3 = f"Quanto {ticker} paga de dividendos e qual o Preço Teto Bazin?"
        faq_a3 = f"Atualmente, {ticker} apresenta um Dividend Yield de {dy_str}. Pelo método de Décio Bazin (exigência de 6% de dividendo anual), o Preço Teto calculado é de {bazin_str} (margem de {bazin_badge}). A distribuição de proventos depende da geração de caixa livre e política de payout."

        faq_q4 = f"Qual é o Valor Intrínseco de Graham de {ticker} hoje?"
        faq_a4 = f"Pela fórmula clássica de Benjamin Graham (V = √(22,5 × LPA × VPA)), o Preço Justo estimado para {ticker} é de {graham_str} ({graham_badge}). Negociada a P/L {pl_str} e P/VP {pvp_str}, a ação oferece Spread de Earnings Yield de {ey_spread_str} a.a. sobre o juro real da NTN-B."

        # Schema.org JSON-LD estruturado
        schema_data = {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "BreadcrumbList",
                    "itemListElement": [
                        {"@type": "ListItem", "position": 1, "name": "Moat Terminal", "item": "https://moatterminal.com.br/"},
                        {"@type": "ListItem", "position": 2, "name": "Ações B3", "item": "https://moatterminal.com.br/acoes/"},
                        {"@type": "ListItem", "position": 3, "name": setor, "item": f"https://moatterminal.com.br/acoes/#sector-{re.sub(r'[^a-zA-Z0-9]', '', setor).lower()}"},
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

        # Breadcrumbs HTML semântico com link direto para /acoes/
        breadcrumbs_html = f"""
    <!-- BREADCRUMB SEMÂNTICO (SEO & NAVEGAÇÃO HIERÁRQUICA) -->
    <nav aria-label="breadcrumb" class="flex items-center gap-1.5 text-[11px] font-sans text-slate-500 mb-2">
      <a href="/index.html" class="hover:text-[#004B49] transition">Home</a>
      <span>›</span>
      <a href="/acoes/" class="hover:text-[#004B49] transition font-medium">Empresas</a>
      <span>›</span>
      <a href="/acoes/#sector-{re.sub(r'[^a-zA-Z0-9]', '', setor).lower()}" class="hover:text-[#004B49] transition text-slate-500">{setor}</a>
      <span>›</span>
      <span class="font-bold text-slate-900">{ticker}</span>
    </nav>"""

        # Pre-rendered Hero Card HTML para rastreadores
        entry_badge_bg = "bg-emerald-600 text-white" if entry_tag == "ASSIMETRIA_FAVORAVEL" else ("bg-amber-500 text-white" if entry_tag == "PRECO_JUSTO" else "bg-slate-700 text-white")
        tier_label = "Tier 1 (Wide Moat)" if quality_score >= 80 else ("Tier 2 (Narrow Moat)" if quality_score >= 65 else "Tier 3 (No Moat)")

        decomposition_html = generate_moat_decomposition_html(s)

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
              <span>Setor: <a href="/acoes/#sector-{re.sub(r'[^a-zA-Z0-9]', '', setor).lower()}" class="text-slate-800 hover:text-[#004B49] font-medium underline">{setor}</a></span>
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
            <span class="text-2xl font-bold font-mono leading-none my-0.5 text-slate-900">{score_str}</span>
            <span class="text-[9px] font-mono font-semibold text-slate-700">{tier_label}</span>
          </div>
        </div>
      </div>

      {decomposition_html}
"""

        # Pre-rendered Editorial Valuation & Sector Peers Section (100% visível para o Googlebot e usuários)
        peers_cards_html = []
        for p in peers:
            p_tick = p.get("ticker", "").upper().strip()
            p_emp = p.get("empresa", p_tick).strip()
            p_roic = format_pct(p.get("roic") or p.get("roe"))
            p_pl = format_mult(p.get("pl")) if p.get("pl") is not None else "N/D"
            p_dy = format_pct(p.get("div_yield"))
            p_sc = float(p.get("quality_score", 0) or 0)
            p_sc_str = f"{p_sc:.1f}".replace(".", ",")
            peers_cards_html.append(f"""
            <a href="/acoes/{p_tick.lower()}/" class="p-3.5 rounded-xl border border-slate-200 bg-white hover:border-[#004B49] hover:shadow-xs transition flex flex-col justify-between group">
              <div class="flex items-center justify-between">
                <span class="font-mono font-bold text-sm text-slate-900 group-hover:text-[#004B49]">{p_tick}</span>
                <span class="text-[10px] font-mono px-2 py-0.5 rounded-full bg-slate-100 text-slate-700 font-bold">Moat {p_sc_str}</span>
              </div>
              <div class="text-xs text-slate-600 truncate mt-1">{p_emp}</div>
              <div class="mt-2.5 pt-2 border-t border-slate-100 flex items-center justify-between text-[11px] font-mono text-slate-500">
                <span>ROIC: <b class="text-slate-800">{p_roic}</b></span>
                <span>P/L: <b class="text-slate-800">{p_pl}</b></span>
                <span>DY: <b class="text-emerald-700">{p_dy}</b></span>
              </div>
            </a>
            """)
        peers_cards_joined = "\n".join(peers_cards_html) if peers_cards_html else '<p class="text-xs text-slate-500 font-sans">Nenhum concorrente com liquidez suficiente no mesmo setor.</p>'

        graham_margin_val_str = f"{graham_margin:.1f}%".replace(".", ",") if graham_margin is not None else ""
        graham_interpretation = f"Com cotação atual de {cot_str} contra o valor intrínseco teórico de {graham_str}, o papel negocia com margem de segurança de {graham_margin_val_str} segundo o método clássico de Benjamin Graham." if (graham_margin and graham_margin > 0) else f"Negociada a {cot_str}, acima do valor intrínseco teórico de Graham ({graham_str}), o que é comum em companhias com alto prêmio de qualidade e crescimento sobre o valor contábil."
        bazin_interpretation = f"Com dividendo atual de {dy_str}, o preço teto de Bazin (exigência de 6% a.a.) fica em {bazin_str}, proporcionando margem favorável de proventos frente à cotação atual." if (bazin_margin and bazin_margin > 0) else f"Pelo critério de Décio Bazin (piso de 6% a.a.), o preço teto calculado é de {bazin_str}. Para capturar 6% em dividendos, a cotação de equilíbrio situa-se neste teto."

        editorial_section_html = f"""
    <!-- SEÇÃO EDITORIAL PRE-RENDERIZADA: VEREDITO QUANTITATIVO, GRAHAM, BAZIN & PARES SETORIAIS -->
    <section class="mt-8 pt-8 border-t border-slate-200 space-y-6">
      
      <div class="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-sm space-y-6">
        <div class="flex flex-wrap items-center justify-between gap-3 border-b border-slate-100 pb-4">
          <div>
            <h2 class="text-xl sm:text-2xl font-bold font-editorial text-slate-900">
              Veredito de Valuation &amp; Análise de {empresa} ({ticker})
            </h2>
            <p class="text-xs sm:text-sm text-slate-500 font-sans mt-0.5">
              Consolidação analítica baseada em demonstrativos contábeis oficiais auditados (CVM 2T26).
            </p>
          </div>
          <a href="/acoes/" class="text-xs font-mono font-bold text-[#004B49] bg-[#E6F4F1] border border-[#BCE5DC] px-3 py-1.5 rounded-xl hover:bg-[#DCF0EC] transition flex items-center gap-1.5">
            <span>← Ver Todas as Empresas</span>
          </a>
        </div>

        <!-- Grid de Modelos Clássicos de Valuation -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <!-- Card Graham -->
          <div class="p-4 rounded-2xl bg-slate-50 border border-slate-200 space-y-2">
            <div class="flex items-center justify-between">
              <span class="text-xs font-mono font-bold text-slate-900 uppercase">Preço Justo Graham</span>
              <span class="text-[10px] font-mono px-2 py-0.5 rounded-full font-bold { 'bg-emerald-100 text-emerald-800' if graham_margin and graham_margin > 0 else 'bg-slate-200 text-slate-700' }">
                {graham_badge}
              </span>
            </div>
            <div class="text-xl font-bold font-mono text-slate-900">{graham_str}</div>
            <p class="text-xs text-slate-600 font-sans leading-relaxed">
              {graham_interpretation}
            </p>
          </div>

          <!-- Card Bazin -->
          <div class="p-4 rounded-2xl bg-slate-50 border border-slate-200 space-y-2">
            <div class="flex items-center justify-between">
              <span class="text-xs font-mono font-bold text-slate-900 uppercase">Preço Teto Bazin (6%)</span>
              <span class="text-[10px] font-mono px-2 py-0.5 rounded-full font-bold { 'bg-indigo-100 text-indigo-800' if bazin_margin and bazin_margin > 0 else 'bg-slate-200 text-slate-700' }">
                {bazin_badge}
              </span>
            </div>
            <div class="text-xl font-bold font-mono text-slate-900">{bazin_str}</div>
            <p class="text-xs text-slate-600 font-sans leading-relaxed">
              {bazin_interpretation}
            </p>
          </div>

          <!-- Card NTN-B -->
          <div class="p-4 rounded-2xl bg-slate-50 border border-slate-200 space-y-2">
            <div class="flex items-center justify-between">
              <span class="text-xs font-mono font-bold text-slate-900 uppercase">Spread Real NTN-B</span>
              <span class="text-[10px] font-mono px-2 py-0.5 rounded-full font-bold { 'bg-emerald-100 text-emerald-800' if ey_spread > 0 else 'bg-amber-100 text-amber-800' }">
                { 'Prêmio Positivo' if ey_spread > 0 else 'Abaixo do IPCA+' }
              </span>
            </div>
            <div class="text-xl font-bold font-mono text-slate-900">{ey_spread_str} a.a.</div>
            <p class="text-xs text-slate-600 font-sans leading-relaxed">
              Earnings Yield da companhia contra a taxa real da NTN-B 2035 do Tesouro Direto (~6,5% a.a. acima do IPCA).
            </p>
          </div>
        </div>

        <!-- Comparativo com Concorrentes do Setor -->
        <div class="space-y-3 pt-2">
          <div class="flex items-center justify-between">
            <h3 class="text-sm font-mono font-bold text-slate-900 uppercase">
              Concorrentes Diretos no Setor de {setor}
            </h3>
            <span class="text-xs font-sans text-slate-500">Pares comparativos da B3</span>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
            {peers_cards_joined}
          </div>
        </div>

      </div>

    </section>
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
        
        # Ensure robots is index, follow on individual stock pages
        page_html = re.sub(r'<meta\s+name="robots"\s+content="[^"]*">', '<meta name="robots" content="index, follow">', page_html)

        # Ensure canonical tag is exact, self-referential, lowercase, with trailing slash and without mutation id
        page_html = re.sub(r'<link\s+rel="canonical"[^>]*>', f'<link rel="canonical" href="{canonical_url}">', page_html)

        # Strip out any client-side canonical mutation script from programmatic pages
        page_html = re.sub(
            r'<script>\s*\(function\(\)\s*\{.*?canonicalTag.*?\}\)\(\);\s*</script>\s*',
            '',
            page_html,
            flags=re.DOTALL
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

        # 2. Substituir Schema.org JSON-LD de forma robusta no <head>
        new_schema_block = f"""<!-- Schema.org JSON-LD Estruturado (Breadcrumbs, Corporation, FAQPage) -->\n  <script type="application/ld+json">\n{schema_json_str}\n  </script>"""
        schema_pattern = r'<!-- Schema\.org JSON-LD -->\s*<script type="application/ld\+json">.*?</script>'
        if re.search(schema_pattern, page_html, flags=re.DOTALL):
            page_html = re.sub(schema_pattern, new_schema_block, page_html, count=1, flags=re.DOTALL)
        else:
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
            page_html = page_html.replace(old_schema_str, new_schema_block)

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

        # 4. Inserir Seção Editorial de Valuation & FAQ Accordion antes do footer
        page_html = page_html.replace(
            '</main>',
            f'{editorial_section_html}\n{faq_section_html}\n  </main>'
        )

        # 5. Ajustar links relativos para raiz e garantir link para /acoes/ no rodapé
        page_html = page_html.replace('href="index.html"', 'href="/index.html"')
        page_html = page_html.replace('href="termos.html"', 'href="/termos.html"')
        page_html = page_html.replace('href="privacidade.html"', 'href="/privacidade.html"')
        page_html = page_html.replace(
            '<a href="/sobre.html"',
            '<a href="/acoes/" class="text-slate-600 hover:text-[#004B49] underline underline-offset-2">Empresas</a>\n          <span>•</span>\n          <a href="/sobre.html"'
        )

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

        # Gravar arquivo estatico na pasta acoes/{ticker_lower}/index.html
        stock_dir = os.path.join(acoes_root, ticker_lower)
        os.makedirs(stock_dir, exist_ok=True)
        stock_file = os.path.join(stock_dir, "index.html")
        with open(stock_file, "w", encoding="utf-8") as f:
            f.write(page_html)

        sitemap_urls.append((canonical_url, today_str, 'daily', '0.9'))
        total_generated += 1

    print(f"[pSEO] Geradas com sucesso {total_generated} páginas estáticas em /acoes/{{ticker}}/")

    # Gerar a página central do diretório /acoes/index.html
    generate_acoes_directory(stocks, base_dir, today_str)

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
