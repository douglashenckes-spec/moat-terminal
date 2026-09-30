import re
import subprocess
import shutil

TARGET = "build_company_page.py"

with open(TARGET, "r", encoding="utf-8") as f:
    text = f.read()

# 1. CSS da info-badge
old_style_end = """    .custom-scrollbar::-webkit-scrollbar-thumb:hover {{
      background: #94A3B8;
    }}
  </style>"""

new_style_end = """    .custom-scrollbar::-webkit-scrollbar-thumb:hover {{
      background: #94A3B8;
    }}
    .info-badge {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 14px;
      height: 14px;
      border-radius: 9999px;
      font-size: 10px;
      font-weight: 700;
      color: #64748B;
      background-color: #F1F5F9;
      border: 1px solid #CBD5E1;
      cursor: help;
      transition: all 0.15s ease;
      vertical-align: middle;
      margin-left: 3px;
    }}
    .info-badge:hover {{
      color: #0F172A;
      background-color: #E2E8F0;
      border-color: #94A3B8;
      transform: scale(1.1);
    }}
  </style>"""

text = text.replace(old_style_end, new_style_end)

# 2. Markup do Global Tooltip no body
old_body_start = '<body class="bg-[#F8FAFC] text-slate-800 antialiased min-h-screen flex flex-col justify-between selection:bg-emerald-100 selection:text-emerald-900">'
new_body_start = """<body class="bg-[#F8FAFC] text-slate-800 antialiased min-h-screen flex flex-col justify-between selection:bg-emerald-100 selection:text-emerald-900">

  <!-- GLOBAL INTERACTIVE EDUCATIONAL TOOLTIP (BALÃOZINHO INSTITUCIONAL) -->
  <div id="globalTooltip" class="fixed hidden z-[999999] max-w-xs sm:max-w-sm bg-slate-900 text-white p-3 rounded-xl shadow-2xl border border-slate-700 pointer-events-none transition-opacity duration-150 text-xs font-sans">
    <div class="font-bold text-amber-300 font-mono text-xs flex items-center gap-1.5 border-b border-slate-700/80 pb-1 mb-1.5" id="gtTitle"></div>
    <div class="text-slate-200 text-[11px] leading-relaxed font-sans" id="gtDesc"></div>
    <div class="text-slate-400 text-[10px] font-mono mt-1.5 pt-1 border-t border-slate-800 flex items-center justify-between" id="gtFoot"></div>
  </div>"""

text = text.replace(old_body_start, new_body_start)

# 3. Resumo Executivo em renderCompanyHeader
old_header_badges = """        <!-- Rótulos de Enquadramento Estratégico & Momento -->
        <div class="mt-4 pt-3.5 border-t border-slate-100 flex flex-wrap items-center gap-2">
          <span class="text-[11px] font-mono font-bold uppercase tracking-wider text-slate-500 mr-1 flex items-center gap-1.5">
            <svg class="w-3.5 h-3.5 stroke-[1.75] text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"/></svg>
            Enquadramentos &amp; Momento:
          </span>
          ${{catBadgesHtml}}
        </div>
      `;"""

new_header_badges = """        <!-- Box de Resumo Executivo Didático para o Investidor -->
        <div class="mt-4 p-4 bg-emerald-50/70 border border-emerald-200/80 rounded-2xl flex items-start gap-3.5 text-xs font-sans text-slate-800 leading-relaxed shadow-2xs">
          <span class="text-xl mt-0.5">💡</span>
          <div>
            <div class="font-bold text-emerald-950 font-mono text-[11px] uppercase tracking-wider mb-1 flex items-center gap-2">
              <span>Diagnóstico Executivo para o Investidor</span>
              <span class="px-2 py-0.2 rounded-full text-[9px] font-bold bg-white text-emerald-800 border border-emerald-300">Linguagem Simples</span>
            </div>
            <p class="text-slate-700 text-xs leading-relaxed font-sans">${{generateHumanExecutiveSummary(s)}}</p>
          </div>
        </div>

        <!-- Rótulos de Enquadramento Estratégico & Momento -->
        <div class="mt-3.5 pt-3 border-t border-slate-100 flex flex-wrap items-center gap-2">
          <span class="text-[11px] font-mono font-bold uppercase tracking-wider text-slate-500 mr-1 flex items-center gap-1.5">
            <svg class="w-3.5 h-3.5 stroke-[1.75] text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"/></svg>
            Enquadramentos &amp; Momento:
          </span>
          ${{catBadgesHtml}}
        </div>
      `;"""

text = text.replace(old_header_badges, new_header_badges)

# 4. Tooltips nos múltiplos essenciais
old_items = """      const items = [
        {{ label: 'P/L Histórico', val: formatMultiple(s.pl), desc: 'Preço sobre Lucro LTM', color: 'text-slate-900' }},
        {{ label: 'P/L Run-Rate', val: s.pl_run_rate ? formatMultiple(s.pl_run_rate) : 'N/D', desc: 'Ritmo anualizado 2T26', color: s.pl_run_rate && s.pl && s.pl_run_rate < s.pl ? 'text-emerald-800 font-bold' : 'text-slate-900' }},
        {{ label: 'P / VP', val: formatMultiple(s.pvp), desc: 'Preço sobre Patrimônio', color: 'text-slate-900' }},
        {{ label: 'EV / EBITDA', val: s.is_financial ? 'N/A' : (s.ev_ebitda !== null ? formatMultiple(s.ev_ebitda) : 'N/D'), desc: 'Múltiplo da Firma', color: 'text-slate-900' }},
        {{ label: 'ROIC Operacional', val: s.is_financial ? 'N/A (Bancos)' : formatPercent(s.roic), desc: 'Retorno Capital Investido (NOPAT/CI)', color: (!s.is_financial && s.roic >= 0.15) ? 'text-emerald-800 font-bold' : 'text-slate-900' }},
        {{ label: 'ROE do Acionista', val: formatPercent(s.roe), desc: 'Retorno s/ Patrimônio Líquido', color: s.roe >= 0.15 ? 'text-emerald-800 font-bold' : 'text-slate-900' }},
        {{ label: 'Margem Líquida', val: formatPercent(s.mrg_liq), desc: 'Conversão em Lucro Líquido', color: s.mrg_liq >= 0.15 ? 'text-emerald-800 font-bold' : 'text-slate-900' }},
        {{ label: 'Dividend Yield', val: formatPercent(s.div_yield), desc: 'Proventos pagos 12m', color: s.div_yield >= 0.06 ? 'text-emerald-800 font-bold' : 'text-slate-900' }}
      ];

      document.getElementById('essentialMultiplesGrid').innerHTML = items.map(c => `
        <div class="glass-card rounded-xl p-3 border border-slate-200 text-center flex flex-col justify-between">
          <div class="text-[10px] text-slate-500 uppercase font-mono font-semibold">${{c.label}}</div>
          <div class="text-sm sm:text-base font-mono font-bold ${{c.color}} my-1">${{c.val}}</div>
          <div class="text-[9px] text-slate-500 font-sans truncate" title="${{c.desc}}">${{c.desc}}</div>
        </div>
      `).join('');"""

new_items = """      const items = [
        {{ label: 'P/L Histórico', val: formatMultiple(s.pl), desc: 'Preço sobre Lucro LTM', color: 'text-slate-900', tip: 'pl_run_rate' }},
        {{ label: 'P/L Run-Rate', val: s.pl_run_rate ? formatMultiple(s.pl_run_rate) : 'N/D', desc: 'Ritmo anualizado 2T26', color: s.pl_run_rate && s.pl && s.pl_run_rate < s.pl ? 'text-emerald-800 font-bold' : 'text-slate-900', tip: 'pl_run_rate' }},
        {{ label: 'P / VP', val: formatMultiple(s.pvp), desc: 'Preço sobre Patrimônio', color: 'text-slate-900', tip: 'graham' }},
        {{ label: 'EV / EBITDA', val: s.is_financial ? 'N/A' : (s.ev_ebitda !== null ? formatMultiple(s.ev_ebitda) : 'N/D'), desc: 'Múltiplo da Firma', color: 'text-slate-900', tip: 'ev_ebitda' }},
        {{ label: 'ROIC Operacional', val: s.is_financial ? 'N/A (Bancos)' : formatPercent(s.roic), desc: 'Retorno Capital Investido (NOPAT/CI)', color: (!s.is_financial && s.roic >= 0.15) ? 'text-emerald-800 font-bold' : 'text-slate-900', tip: 'roic' }},
        {{ label: 'ROE do Acionista', val: formatPercent(s.roe), desc: 'Retorno s/ Patrimônio Líquido', color: s.roe >= 0.15 ? 'text-emerald-800 font-bold' : 'text-slate-900', tip: 'roe' }},
        {{ label: 'Margem Líquida', val: formatPercent(s.mrg_liq), desc: 'Conversão em Lucro Líquido', color: s.mrg_liq >= 0.15 ? 'text-emerald-800 font-bold' : 'text-slate-900', tip: 'mrg_liq' }},
        {{ label: 'Dividend Yield', val: formatPercent(s.div_yield), desc: 'Proventos pagos 12m', color: s.div_yield >= 0.06 ? 'text-emerald-800 font-bold' : 'text-slate-900', tip: 'payout' }}
      ];

      document.getElementById('essentialMultiplesGrid').innerHTML = items.map(c => `
        <div class="glass-card rounded-xl p-3 border border-slate-200 text-center flex flex-col justify-between">
          <div class="text-[10px] text-slate-500 uppercase font-mono font-semibold flex items-center justify-center gap-1">
            <span>${{c.label}}</span>
            ${{c.tip ? `<span class="info-badge" data-tooltip="${{c.tip}}">ⓘ</span>` : ''}}
          </div>
          <div class="text-sm sm:text-base font-mono font-bold ${{c.color}} my-1">${{c.val}}</div>
          <div class="text-[9px] text-slate-500 font-sans truncate" title="${{c.desc}}">${{c.desc}}</div>
        </div>
      `).join('');"""

text = text.replace(old_items, new_items)

# 5. Guia Didático de Conciliação dos Métodos de Valuation
old_val_end = """        <!-- Nota Explicativa -->
        <div class="p-3 bg-slate-50 rounded-xl border border-slate-200 text-[10px] text-slate-500 font-sans leading-relaxed">
          <b>Metodologia Institucional:</b> Graham busca segurança patrimonial baseada em ativos tangíveis; Bazin exige fluxo de dividendos presente; NTN-B compara diretamente contra a taxa livre de risco soberana do Brasil (IPCA + 6,5%).
        </div>
      `;"""

new_val_end = """        <!-- Guia Didático de Conciliação dos 3 Métodos de Valuation -->
        <div class="p-4 bg-white rounded-xl border border-slate-200 text-xs font-sans text-slate-700 space-y-2.5 shadow-2xs mt-3">
          <div class="font-bold text-slate-900 font-mono text-xs flex items-center gap-1.5 border-b border-slate-100 pb-2">
            <span>📚</span> Como interpretar as divergências entre os métodos de Valuation?
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 text-[11px] text-slate-600 leading-relaxed">
            <div class="p-3 rounded-xl bg-slate-50 border border-slate-100 flex flex-col justify-between">
              <div>
                <b class="text-slate-900 font-mono block mb-1">📐 Benjamin Graham:</b>
                Avalia o valor patrimonial e lucros médios (foco em proteção patrimonial). Ideal para indústrias maduras com ativos físicos tangíveis.
              </div>
              <span class="text-[10px] text-sky-800 font-bold font-mono mt-2">Proteção Patrimonial</span>
            </div>
            <div class="p-3 rounded-xl bg-slate-50 border border-slate-100 flex flex-col justify-between">
              <div>
                <b class="text-slate-900 font-mono block mb-1">💵 Décio Bazin:</b>
                Avalia a geração imediata de proventos com yield mínimo exigido de 6,0% a.a. Foco estrito em geração de fluxo de caixa passivo.
              </div>
              <span class="text-[10px] text-emerald-800 font-bold font-mono mt-2">Renda Passiva Imediata</span>
            </div>
            <div class="p-3 rounded-xl bg-slate-50 border border-slate-100 flex flex-col justify-between">
              <div>
                <b class="text-slate-900 font-mono block mb-1">💎 Charlie Munger:</b>
                Avalia a capacidade de reinvestir lucros a taxas elevadas de retorno (ROIC/ROE). Aceita pagar prêmio por empresas de classe mundial.
              </div>
              <span class="text-[10px] text-indigo-800 font-bold font-mono mt-2">Fosso &amp; Qualidade</span>
            </div>
          </div>
        </div>
      `;"""

text = text.replace(old_val_end, new_val_end)

# 6. Adicionar funções auxiliares e dicionário ao final do script
js_footer_add = """
    // =========================================================================
    // DICIONÁRIO DE TOOLTIPS DIDÁTICOS PARA EMPRESA.HTML
    // =========================================================================
    const METRIC_TOOLTIPS = {
      quality_score: {
        title: '🏆 Score de Qualidade Munger (0 a 100)',
        desc: 'Mede a excelência do negócio unindo rentabilidade real histórica (ROIC/ROE), solidez de balanço anti-crise e consistência de lucros sem prejuízos nos últimos 5 anos.',
        foot: 'Tier 1 (≥ 80) = Classe Mundial • Tier 2 (≥ 65) = Saudável'
      },
      ey_spread: {
        title: '📈 Spread vs NTN-B Soberana (6,50% a.a.)',
        desc: 'Compara o rendimento em lucros da ação (Earnings Yield) com o juro real do Tesouro IPCA+ longo. Mostra se a empresa paga prêmio suficiente frente à renda fixa pública.',
        foot: 'Spread > 0% = Ação compensa o risco soberano do Brasil'
      },
      pl_run_rate: {
        title: '⏱️ P/L (12M) vs P/L Run-Rate (2T26)',
        desc: 'O P/L 12M reflete os últimos 4 trimestres. O P/L Run-Rate anualiza o resultado mais recente (4x 2T26). Se for menor (verde), os lucros estão acelerando.',
        foot: 'Permite identificar viradas operacionais antes do mercado'
      },
      ev_ebitda: {
        title: '🏢 EV / EBITDA (Múltiplo da Firma)',
        desc: 'Avalia o custo para comprar todas as ações e quitar todas as dívidas da empresa em relação ao caixa operacional gerado. Inaplicável a bancos.',
        foot: 'Abaixo de 6.0x = Múltiplo atrativo para indústrias e serviços'
      },
      roic: {
        title: '🏭 ROIC (Retorno s/ Capital Investido)',
        desc: 'Mede o lucro gerado estritamente pelas operações fabris e comerciais sobre o dinheiro empatado no negócio. É a métrica favorita de Charlie Munger para avaliar o fosso competitivo (Moat).',
        foot: 'Acima de 15% ao ano = Excelência operacional e barreira de entrada'
      },
      roe: {
        title: '🏛️ ROE (Retorno s/ Patrimônio Líquido)',
        desc: 'Mede quanto lucro a empresa entrega para cada R$ 100 colocados pelos acionistas. É a métrica soberana para instituições financeiras e holdings (como Itaúsa, Itaú e Banco do Brasil).',
        foot: 'Acima de 15% ao ano = Retorno de capital de classe mundial'
      },
      mrg_liq: {
        title: '💧 Margem Líquida (% de Conversão)',
        desc: 'Fatia da receita que sobra como lucro líquido após pagar fornecedores, funcionários, juros da dívida e impostos.',
        foot: 'Acima de 15% = Forte poder de precificação e margem defensiva'
      },
      debt: {
        title: '🛡️ Dívida Líquida / EBITDA (Solvência)',
        desc: 'Quantos anos de caixa operacional a empresa levaria para quitar toda a sua dívida. Valores negativos indicam Caixa Líquido.',
        foot: '< 1.5x = Muito seguro • > 3.0x = Alerta em juros altos'
      },
      payout: {
        title: '💰 Dividend Yield & Payout Implícito',
        desc: 'Dividend Yield é a taxa de proventos pagos em 12 meses. O Payout Implícito indica quanto do lucro foi distribuído aos acionistas.',
        foot: 'DY ≥ 6% = Renda passiva real acima da inflação'
      },
      graham: {
        title: '📐 Preço Justo de Benjamin Graham',
        desc: 'Fórmula clássica de Benjamin Graham (V = √(22,5 × LPA × VPA)) que busca margem de segurança patrimonial equilibrando lucro e valor patrimonial.',
        foot: 'Preço atual abaixo do Graham = Desconto intrínseco'
      }
    };

    function initGlobalTooltips() {
      const tooltip = document.getElementById('globalTooltip');
      const titleEl = document.getElementById('gtTitle');
      const descEl = document.getElementById('gtDesc');
      const footEl = document.getElementById('gtFoot');
      if (!tooltip) return;

      document.body.addEventListener('mouseenter', (e) => {
        const target = e.target.closest('[data-tooltip]');
        if (!target) return;
        const key = target.getAttribute('data-tooltip');
        const item = METRIC_TOOLTIPS[key];
        if (!item) return;

        titleEl.textContent = item.title;
        descEl.textContent = item.desc;
        footEl.textContent = item.foot || '';

        tooltip.classList.remove('hidden');
        positionTooltip(e, target, tooltip);
      }, true);

      document.body.addEventListener('mousemove', (e) => {
        const target = e.target.closest('[data-tooltip]');
        if (!target) return;
        positionTooltip(e, target, tooltip);
      }, true);

      document.body.addEventListener('mouseleave', (e) => {
        const target = e.target.closest('[data-tooltip]');
        if (!target) return;
        tooltip.classList.add('hidden');
      }, true);
    }

    function positionTooltip(e, target, tooltip) {
      const rect = target.getBoundingClientRect();
      const tipRect = tooltip.getBoundingClientRect();
      const padding = 12;

      let top = rect.bottom + 8;
      let left = rect.left + (rect.width / 2) - (tipRect.width / 2);

      if (left + tipRect.width > window.innerWidth - padding) {
        left = window.innerWidth - tipRect.width - padding;
      }
      if (left < padding) left = padding;

      if (top + tipRect.height > window.innerHeight - padding) {
        top = rect.top - tipRect.height - 8;
      }

      tooltip.style.top = `${top}px`;
      tooltip.style.left = `${left}px`;
    }

    function generateHumanExecutiveSummary(s) {
      if (!s) return '';
      const isFin = s.is_financial;
      const roePct = s.roe ? (s.roe * 100).toFixed(1) + '%' : 'N/D';
      const roicPct = s.roic ? (s.roic * 100).toFixed(1) + '%' : null;
      const dyPct = s.div_yield ? (s.div_yield * 100).toFixed(1) + '%' : '0.0%';
      const tierShort = s.quality_score >= 80 ? 'Tier 1 (Classe Mundial)' : (s.quality_score >= 65 ? 'Tier 2 (Sólida)' : 'Tier 3 / Atenção');

      if (isFin) {
        return `<b>${s.empresa} (${s.ticker})</b> é uma instituição financeira/holding regulada pelas métricas do Banco Central, avaliada no <b>${tierShort}</b> com nota <b>${s.quality_score.toFixed(1)}/100</b>. Entrega um retorno patrimonial (ROE) robusto de <b>${roePct}</b> ao ano e distribui dividendos regulares de <b>${dyPct}</b> a.a. Seu valuation atual oferece <b>${s.entry_status}</b> frente à renda fixa pública.`;
      }

      const debtStatus = (s.div_liq_ebitda !== null && s.div_liq_ebitda < 0) ? 'opera com caixa líquido positivo (sem endividamento líquido)' : (s.div_liq_ebitda ? `alavancagem controlada de ${s.div_liq_ebitda.toFixed(1)}x EBITDA` : 'estrutura de capital auditada');
      const returnDesc = roicPct ? `retorno operacional (ROIC) de <b>${roicPct}</b> e retorno patrimonial (ROE) de <b>${roePct}</b>` : `ROE de <b>${roePct}</b>`;

      return `<b>${s.empresa} (${s.ticker})</b> atua no setor de <b>${s.setor || 'Atividade Geral'}</b>, classificada no <b>${tierShort}</b> com Score de <b>${s.quality_score.toFixed(1)}/100</b>. Apresenta ${returnDesc}, ${debtStatus} e remuneração em proventos de <b>${dyPct}</b> a.a., posicionando-se em <b>${s.entry_status}</b>.`;
    }
"""

text = text.replace("    // Inicialização da página", js_footer_add + "\n    // Inicialização da página")
text = text.replace("renderPeerComparison();", "renderPeerComparison();\n      initGlobalTooltips();")

with open(TARGET, "w", encoding="utf-8") as f:
    f.write(text)

print("[OK] build_company_page.py atualizado com sucesso!")
