# -*- coding: utf-8 -*-
with open('build_standalone_html.py', 'r', encoding='utf-8') as f:
    c = f.read()

replacements = [
    # Matrix toolbar axis labels
    ('Eixo X: <b class="text-white" id="lbl-matrix-axis-x">P/L (0-32x)</b> | Eixo Y: <b class="text-white"',
     'Eixo X: <b class="text-slate-900" id="lbl-matrix-axis-x">P/L (0-32x)</b> | Eixo Y: <b class="text-slate-900"'),
    ('bg-emerald-500/20 px-1.5 py-0.2 rounded-full text-[10px] font-bold text-white',
     'bg-emerald-100 px-1.5 py-0.2 rounded-full text-[10px] font-bold text-emerald-900 border border-emerald-300'),
     
    # Portfolio KPIs
    ('<div class="text-base font-bold text-white mt-0.5" id="kp-port-pl">--</div>',
     '<div class="text-base font-bold text-slate-900 mt-0.5" id="kp-port-pl">--</div>'),
    ('<div class="text-base font-bold text-white mt-0.5" id="kp-port-debt">--</div>',
     '<div class="text-base font-bold text-slate-900 mt-0.5" id="kp-port-debt">--</div>'),
     
    # Portfolio Simulator & HHI
    ('<span class="font-bold text-white flex items-center gap-1.5"><span>💵</span> SIMULADOR DE APORTE</span>',
     '<span class="font-bold text-slate-900 flex items-center gap-1.5"><svg class="w-4 h-4 stroke-[1.75] inline-block text-emerald-700" fill="none" stroke="currentColor" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path stroke-linecap="round" stroke-linejoin="round" d="M12 7v10m-3-7.5a2.5 2.5 0 015 0c0 2-3 2-3 4h3"/></svg> SIMULADOR DE APORTE</span>'),
    ('Índice HHI Setorial: <b class="text-white font-mono">0.172</b>',
     'Índice HHI Setorial: <b class="text-slate-900 font-mono">0.172</b>'),
    ('<b class=\\"text-white font-mono\\">${{hhi.toFixed(3)}}</b>',
     '<b class=\\"text-slate-900 font-mono\\">${{hhi.toFixed(3)}}</b>'),
    ('<b class=\\"text-white\\">${{topSector}}</b>',
     '<b class=\\"text-slate-900 font-bold\\">${{topSector}}</b>'),
    ('<b class=\\"text-white\\">${{sortedSectors.length}} setores distintos</b>',
     '<b class=\\"text-slate-900 font-bold\\">${{sortedSectors.length}} setores distintos</b>'),
    ('<b class=\\"text-white\\">${{cashRichCount}} de ${{pStocks.length}} ativos</b>',
     '<b class=\\"text-slate-900 font-bold\\">${{cashRichCount}} de ${{pStocks.length}} ativos</b>'),
    ('<span class="text-slate-300 font-semibold">${{sec}}</span>: <b class="text-white">${{w}}%</b>',
     '<span class="text-slate-700 font-semibold">${{sec}}</span>: <b class="text-slate-900">${{w}}%</b>'),
     
    # Balanço details cards in Dossiê
    ('<span class="text-slate-400 font-sans">Cotação Atual:</span> <b class="text-white">',
     '<span class="text-slate-600 font-sans font-medium">Cotação Atual:</span> <b class="text-slate-900 font-bold">'),
    ('<span class="text-slate-400 font-sans">Liquidez Média (2m):</span> <b class="text-white">',
     '<span class="text-slate-600 font-sans font-medium">Liquidez Média (2m):</span> <b class="text-slate-900 font-bold">'),
    ('<span class="text-slate-400 font-sans">Faixa 52 Semanas:</span> <b class="text-slate-300">',
     '<span class="text-slate-600 font-sans font-medium">Faixa 52 Semanas:</span> <b class="text-slate-800 font-semibold">'),
    ('<span class="text-slate-400 font-sans">Valor de Mercado:</span> <b class="text-white">',
     '<span class="text-slate-600 font-sans font-medium">Valor de Mercado:</span> <b class="text-slate-900 font-bold">'),
    ('<span class="text-slate-400 font-sans">Valor da Firma (EV):</span> <b class="text-white">',
     '<span class="text-slate-600 font-sans font-medium">Valor da Firma (EV):</span> <b class="text-slate-900 font-bold">'),
    ('<span class="text-slate-400 font-sans">P/L (12M LTM):</span>',
     '<span class="text-slate-600 font-sans font-medium">P/L (12M LTM):</span>'),
    ('<span class="text-slate-400 font-sans">P/L Run-Rate (2T26):</span>',
     '<span class="text-slate-600 font-sans font-medium">P/L Run-Rate (2T26):</span>'),
    ('<span class="text-slate-400 font-sans">P/VP:</span> <b class="text-slate-200">',
     '<span class="text-slate-600 font-sans font-medium">P/VP:</span> <b class="text-slate-800 font-bold">'),
    ('<span class="text-slate-400 font-sans">EV / EBITDA:</span> <b class="text-slate-200">',
     '<span class="text-slate-600 font-sans font-medium">EV / EBITDA:</span> <b class="text-slate-800 font-bold">'),
    ('<span class="text-slate-400 font-sans">Dividend Yield:</span>',
     '<span class="text-slate-600 font-sans font-medium">Dividend Yield:</span>'),
     
    # Card 2: Balanço & Solvência
    ('<span class="text-slate-400 font-sans">Ativo Total:</span> <b class="text-white">',
     '<span class="text-slate-600 font-sans font-medium">Ativo Total:</span> <b class="text-slate-900 font-bold">'),
    ('<span class="text-slate-400 font-sans">Ativo Circulante:</span> <b class="text-white">',
     '<span class="text-slate-600 font-sans font-medium">Ativo Circulante:</span> <b class="text-slate-900 font-bold">'),
    ('<span class="text-slate-400 font-sans">Disponibilidades (Caixa):</span>',
     '<span class="text-slate-600 font-sans font-medium">Disponibilidades (Caixa):</span>'),
    ('<span class="text-slate-400 font-sans">Dívida Bruta:</span> <b class="text-slate-200">',
     '<span class="text-slate-600 font-sans font-medium">Dívida Bruta:</span> <b class="text-slate-800 font-bold">'),
    ('<span class="text-slate-400 font-sans">Dívida Líquida:</span>',
     '<span class="text-slate-600 font-sans font-medium">Dívida Líquida:</span>'),
    ('<span class="text-slate-400 font-sans">Dív. Líq. / EBITDA:</span>',
     '<span class="text-slate-600 font-sans font-medium">Dív. Líq. / EBITDA:</span>'),
    ('<span class="text-slate-400 font-sans">Patrimônio Líquido:</span> <b class="text-white">',
     '<span class="text-slate-600 font-sans font-medium">Patrimônio Líquido:</span> <b class="text-slate-900 font-bold">'),
    ('<span class="text-slate-400 font-sans">Valor Patrimonial / Ação:</span> <b class="text-slate-300">',
     '<span class="text-slate-600 font-sans font-medium">Valor Patrimonial / Ação:</span> <b class="text-slate-800 font-bold">'),
    ('<span class="text-slate-400 font-sans">Estrutura de Capital:</span>',
     '<span class="text-slate-600 font-sans font-medium">Estrutura de Capital:</span>'),
     
    # Card 3: DRE & Geração de Resultados
    ('<span class="text-slate-400 font-sans">Receita Líquida (12m):</span> <b class="text-white">',
     '<span class="text-slate-600 font-sans font-medium">Receita Líquida (12m):</span> <b class="text-slate-900 font-bold">'),
    ('<span class="text-slate-400 font-sans">EBIT Operacional (12m):</span> <b class="${{s.details.ebit_12m < 0 ? \'text-rose-400 font-bold\' : \'text-white\'}}">',
     '<span class="text-slate-600 font-sans font-medium">EBIT Operacional (12m):</span> <b class="${{s.details.ebit_12m < 0 ? \'text-rose-700 font-bold\' : \'text-slate-900 font-bold\'}}">'),
    ('<span class="text-slate-400 font-sans">Lucro Líquido (12m):</span>',
     '<span class="text-slate-600 font-sans font-medium">Lucro Líquido (12m):</span>'),
    ('<span class="text-slate-400 font-sans">Lucro Trimestre (2T26):</span>',
     '<span class="text-slate-600 font-sans font-medium">Lucro Trimestre (2T26):</span>'),
    ('<span class="text-slate-400 font-sans">LPA (Lucro por Ação):</span> <b class="text-slate-200">',
     '<span class="text-slate-600 font-sans font-medium">LPA (Lucro por Ação):</span> <b class="text-slate-800 font-bold">'),
    ('<span class="text-slate-400 font-sans">Margem Bruta:</span> <b class="${{s.mrg_bruta < 0 ? \'text-rose-400 font-bold\' : \'text-slate-200\'}}">',
     '<span class="text-slate-600 font-sans font-medium">Margem Bruta:</span> <b class="${{s.mrg_bruta < 0 ? \'text-rose-700 font-bold\' : \'text-slate-800 font-bold\'}}">'),
    ('<span class="text-slate-400 font-sans">Margem Líquida:</span>',
     '<span class="text-slate-600 font-sans font-medium">Margem Líquida:</span>'),
     
    # Card 4: Recorrência
    ('<span class="text-slate-400 font-sans">Lucro 3M (2T26):</span> <b class="${{s.details.lucro_liq_3m < 0 ? \'text-rose-400 font-bold\' : \'text-white\'}}">',
     '<span class="text-slate-600 font-sans font-medium">Lucro 3M (2T26):</span> <b class="${{s.details.lucro_liq_3m < 0 ? \'text-rose-700 font-bold\' : \'text-slate-900 font-bold\'}}">'),
    ('<span class="text-slate-400 font-sans">Lucro 12M (LTM):</span> <b class="${{s.details.lucro_liq_12m < 0 ? \'text-rose-400 font-bold\' : \'text-white\'}}">',
     '<span class="text-slate-600 font-sans font-medium">Lucro 12M (LTM):</span> <b class="${{s.details.lucro_liq_12m < 0 ? \'text-rose-700 font-bold\' : \'text-slate-900 font-bold\'}}">'),
    ('<span class="text-slate-400 font-sans">P/L LTM Histórico:</span>',
     '<span class="text-slate-600 font-sans font-medium">P/L LTM Histórico:</span>'),
    ('<span class="text-slate-400 font-sans">P/L Run-Rate 2T26:</span>',
     '<span class="text-slate-600 font-sans font-medium">P/L Run-Rate 2T26:</span>'),
    ('<div class="text-[10px] text-slate-400 font-sans pt-1 leading-relaxed">',
     '<div class="text-[10px] text-slate-600 font-sans pt-1 leading-relaxed font-medium">'),
     
    # Dossiê Card Headers
    ('font-bold text-amber-300 text-xs flex items-center gap-1.5 border-b border-slate-200 pb-1.5">\n            <span>🏷️</span> Valuation &amp; Mercado',
     'font-bold text-amber-900 text-xs flex items-center gap-1.5 border-b border-slate-200 pb-1.5">\n            <span>' + '<svg class="w-3.5 h-3.5 stroke-[1.75] inline-block text-amber-700" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M20.59 13.41l-7.17 7.17a2 2 0 01-2.83 0L2 12V2h10l8.59 8.59a2 2 0 010 2.82z"/><line x1="7" y1="7" x2="7.01" y2="7"/></svg>' + '</span> Valuation &amp; Mercado'),
    ('font-bold text-sky-300 text-xs flex items-center gap-1.5 border-b border-slate-200 pb-1.5">\n            <span>🛡️</span> Balanço &amp; Solvência',
     'font-bold text-sky-900 text-xs flex items-center gap-1.5 border-b border-slate-200 pb-1.5">\n            <span>' + '<svg class="w-3.5 h-3.5 stroke-[1.75] inline-block text-sky-700" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>' + '</span> Balanço &amp; Solvência'),
    ('font-bold text-emerald-300 text-xs flex items-center gap-1.5 border-b border-slate-200 pb-1.5">\n            <span>📊</span> DRE &amp; Desempenho Operacional',
     'font-bold text-emerald-900 text-xs flex items-center gap-1.5 border-b border-slate-200 pb-1.5">\n            <span>' + '<svg class="w-3.5 h-3.5 stroke-[1.75] inline-block text-emerald-700" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4 4v16h16M4 12h16M12 4v16"/></svg>' + '</span> DRE &amp; Desempenho Operacional'),
    ('font-bold text-purple-300 text-xs flex items-center gap-1.5 font-sans">\n              <span>⚖️</span> Auditoria de Recorrência',
     'font-bold text-indigo-900 text-xs flex items-center gap-1.5 font-sans">\n              <span>' + '<svg class="w-3.5 h-3.5 stroke-[1.75] inline-block text-indigo-700" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 3v18m-7-5l7-13 7 13M5 16h14M3 19h4m10 0h4"/></svg>' + '</span> Auditoria de Recorrência'),
     
    # Dossiê KPI Grid labels
    ('<div class="text-[10px] text-slate-400 uppercase font-semibold">ROIC / ROE</div>',
     '<div class="text-[10px] text-slate-700 uppercase font-bold">ROIC / ROE</div>'),
    ('<div class="text-[10px] text-slate-400 uppercase font-semibold">Spread NTN-B</div>',
     '<div class="text-[10px] text-slate-700 uppercase font-bold">Spread NTN-B</div>'),
    ('<div class="text-[10px] text-slate-400 uppercase font-semibold">Payout</div>',
     '<div class="text-[10px] text-slate-700 uppercase font-bold">Payout</div>'),
    ('<div class="text-[10px] text-slate-400 uppercase font-semibold">Dív.Líq / EBITDA</div>',
     '<div class="text-[10px] text-slate-700 uppercase font-bold">Dív.Líq / EBITDA</div>'),
    ('<div class="text-[10px] text-slate-400 uppercase font-semibold">EBIT / EBITDA</div>',
     '<div class="text-[10px] text-slate-700 uppercase font-bold">EBIT / EBITDA</div>'),
    ('<div class="text-[10px] text-slate-400 uppercase font-semibold">Margem Líq.</div>',
     '<div class="text-[10px] text-slate-700 uppercase font-bold">Margem Líq.</div>'),
     
    # Checklist CFA
    ('<div class="text-[10px] text-slate-400">1. Munger Acid Test</div>',
     '<div class="text-[10px] text-slate-700 font-bold">1. Munger Acid Test</div>'),
    ('<div class="text-[10px] text-slate-400">2. Solvência Anti-Selic</div>',
     '<div class="text-[10px] text-slate-700 font-bold">2. Solvência Anti-Selic</div>'),
    ('<div class="text-[10px] text-slate-400">3. Governança Tag Along</div>',
     '<div class="text-[10px] text-slate-700 font-bold">3. Governança Tag Along</div>'),
    ('<div class="text-[10px] text-slate-400">4. Crescimento 5 Anos</div>',
     '<div class="text-[10px] text-slate-700 font-bold">4. Crescimento 5 Anos</div>'),
    ('<div class="text-[10px] text-slate-400">5. Recorrência 2T26</div>',
     '<div class="text-[10px] text-slate-700 font-bold">5. Recorrência 2T26</div>'),
    ('<div class="text-[10px] text-slate-400">6. Ciclo Commodities</div>',
     '<div class="text-[10px] text-slate-700 font-bold">6. Ciclo Commodities</div>'),
     
    # History 5A
    ('<span class="text-lg font-bold font-mono text-white">${{h.cagr_receita_pct > 0 ? \'+\' : \'\'}}${{h.cagr_receita_pct}}%</span>',
     '<span class="text-lg font-bold font-mono text-slate-900">${{h.cagr_receita_pct > 0 ? \'+\' : \'\'}}${{h.cagr_receita_pct}}%</span>'),
    ('<span class="text-lg font-bold font-mono text-white">${{h.cagr_lucro_pct > 0 ? \'+\' : \'\'}}${{h.cagr_lucro_pct}}%</span>',
     '<span class="text-lg font-bold font-mono text-slate-900">${{h.cagr_lucro_pct > 0 ? \'+\' : \'\'}}${{h.cagr_lucro_pct}}%</span>'),
    ('<div class="text-[10px] text-slate-400 uppercase font-semibold font-mono flex items-center justify-between">\n              <span>CAGR Receita (5A)</span>',
     '<div class="text-[10px] text-slate-700 uppercase font-bold font-mono flex items-center justify-between">\n              <span>CAGR Receita (5A)</span>'),
    ('<div class="text-[10px] text-slate-400 uppercase font-semibold font-mono flex items-center justify-between">\n              <span>Consistência de Lucro</span>',
     '<div class="text-[10px] text-slate-700 uppercase font-bold font-mono flex items-center justify-between">\n              <span>Consistência de Lucro</span>'),
    ('<div class="text-[10px] text-slate-400 uppercase font-semibold font-mono flex items-center justify-between">\n              <span>CAGR Lucro (5A)</span>',
     '<div class="text-[10px] text-slate-700 uppercase font-bold font-mono flex items-center justify-between">\n              <span>CAGR Lucro (5A)</span>'),
     
    # 5-Year Table
    ('<thead class="border-b border-slate-200 text-slate-400 text-[10px] uppercase">',
     '<thead class="border-b border-slate-200 bg-slate-100 text-slate-800 text-[10px] uppercase font-bold">'),
    ('<td class="py-1.5 px-2 font-sans font-medium text-slate-300">Receita Líquida</td>',
     '<td class="py-1.5 px-2 font-sans font-semibold text-slate-800">Receita Líquida</td>'),
    ('<td class="py-1.5 px-2 font-sans font-medium text-slate-300">Lucro Líquido</td>',
     '<td class="py-1.5 px-2 font-sans font-semibold text-slate-800">Lucro Líquido</td>'),
    ('<td class="py-1.5 px-2 font-sans font-medium text-slate-300">Margem Líquida</td>',
     '<td class="py-1.5 px-2 font-sans font-semibold text-slate-800">Margem Líquida</td>'),
    ('<td class="py-1.5 px-2 font-sans font-medium text-slate-300">ROIC / ROE</td>',
     '<td class="py-1.5 px-2 font-sans font-semibold text-slate-800">ROIC / ROE</td>'),
    ('<td class="py-1.5 px-2 font-sans font-medium text-slate-300">Dividend Yield</td>',
     '<td class="py-1.5 px-2 font-sans font-semibold text-slate-800">Dividend Yield</td>'),
    ('${{h.receita.map(r => `<td class="py-1.5 px-2 text-right text-white font-semibold">${{formatBillions(r)}}</td>`).join(\'\')}}',
     '${{h.receita.map(r => `<td class="py-1.5 px-2 text-right text-slate-900 font-bold">${{formatBillions(r)}}</td>`).join(\'\')}}')
]

count = 0
for old, new in replacements:
    if old in c:
        c = c.replace(old, new)
        count += 1
    else:
        # Check if version with single braces matches
        old_s = old.replace('{{', '{').replace('}}', '}')
        if old_s in c:
            c = c.replace(old_s, new)
            count += 1

print(f"Applied {count}/{len(replacements)} contrast and label fixes.")

with open('build_standalone_html.py', 'w', encoding='utf-8') as f:
    f.write(c)
