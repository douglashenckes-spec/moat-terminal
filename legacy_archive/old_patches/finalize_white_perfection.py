"""
finalize_white_perfection.py
============================
Perfeição total do tema branco institucional:
1. Scanner B3:
   - Presets bar: fundo slate-100, borda slate-200, texto slate-700/slate-900.
   - Cabeçalho da tabela: bg-slate-100, texto slate-700 font-bold.
   - Linhas da tabela: tickers em slate-900, cotações em slate-900, EV/EBITDA em slate-700, bordas suaves slate-100.
   - Badges de score: pastel com texto nítido (bg-emerald-50 text-emerald-800 / bg-amber-50 text-amber-800).
2. Carteiras Recomendadas:
   - Tabela: thead bg-slate-100 text-slate-700, tickers em slate-900, cotações em slate-900.
   - Simulador de Aporte: input com texto slate-900, botões 10k/25k/50k em slate-100 hover:bg-slate-200.
3. Dossiê Drawer:
   - Header do drawer com texto slate-900 e fechar em slate-600.
   - Gráficos de 5 anos com títulos em slate-900 e dados da tabela histórica em slate-900 e emerald-700.
"""

with open("build_standalone_html.py", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Scanner Toolbar: Presets container e inputs
text = text.replace('class="inline-flex bg-slate-900/80 border border-slate-200 rounded-full p-1 shadow-inner gap-1"',
                    'class="inline-flex bg-slate-100 border border-slate-200 rounded-full p-1 gap-1"')

text = text.replace('class="bg-slate-900/80 border border-slate-200 rounded-full px-3.5 py-1.5 text-xs text-white font-mono focus:outline-none focus:border-emerald-400 cursor-pointer"',
                    'class="bg-slate-50 border border-slate-200 rounded-full px-3.5 py-1.5 text-xs text-slate-900 font-mono focus:outline-none focus:border-emerald-500 cursor-pointer"')

text = text.replace('<span class="text-xs font-mono text-slate-300 bg-slate-900/80 px-3 py-1 rounded-full border border-slate-200" id="tableCountBadge">',
                    '<span class="text-xs font-mono text-slate-700 bg-slate-100 px-3 py-1 rounded-full border border-slate-200 font-bold" id="tableCountBadge">')

text = text.replace('text-yellow-300', 'text-amber-800')
text = text.replace('text-amber-400', 'text-amber-800')
text = text.replace('text-emerald-400', 'text-emerald-800')
text = text.replace('text-cyan-400', 'text-sky-800')
text = text.replace('text-sky-400', 'text-indigo-800')
text = text.replace('hover:text-white', 'hover:text-slate-900')

# Tabela do Scanner: Header e cores de linhas
text = text.replace('<thead class="sticky top-0 bg-[#0A0E1A]/95 backdrop-blur-md z-10 border-b border-white/10 shadow-sm">',
                    '<thead class="sticky top-0 bg-slate-100 z-10 border-b border-slate-200 shadow-xs">')

text = text.replace('<span class="text-sm font-bold text-amber-300 tracking-wide font-mono">${s.ticker}</span>',
                    '<span class="text-sm font-bold text-slate-900 tracking-wide font-mono">${s.ticker}</span>')

text = text.replace('<td class="py-2.5 px-3 text-xs text-right font-semibold text-white font-mono" title="Liquidez Média: ${formatBillions(s.liq_2m)}/d">${formatCurrency(s.cotacao)}</td>',
                    '<td class="py-2.5 px-3 text-xs text-right font-bold text-slate-900 font-mono" title="Liquidez Média: ${formatBillions(s.liq_2m)}/d">${formatCurrency(s.cotacao)}</td>')

text = text.replace('text-medium text-slate-200 font-mono">${s.is_financial ? \'N/A\' : (s.ev_ebitda !== null ? formatMultiple(s.ev_ebitda) : \'N/D\')}',
                    'text-medium text-slate-700 font-mono">${s.is_financial ? \'N/A\' : (s.ev_ebitda !== null ? formatMultiple(s.ev_ebitda) : \'N/D\')}')

# Score badges
text = text.replace("const scoreBadgeClass = s.quality_score >= 80 ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40' : (s.quality_score >= 65 ? 'bg-amber-500/20 text-amber-300 border border-amber-500/40' : (s.quality_score < 50 ? 'bg-rose-500/20 text-rose-300 border border-rose-500/40' : 'bg-white/10 text-slate-300 border border-slate-200'));",
                    "const scoreBadgeClass = s.quality_score >= 80 ? 'bg-emerald-50 text-emerald-800 border border-emerald-300 font-bold' : (s.quality_score >= 65 ? 'bg-amber-50 text-amber-800 border border-amber-300 font-bold' : (s.quality_score < 50 ? 'bg-rose-50 text-rose-800 border border-rose-300 font-bold' : 'bg-slate-100 text-slate-700 border border-slate-200'));")

# 2. Carteiras Recomendadas
text = text.replace('<thead class="bg-[#0A0E1A]/95 backdrop-blur-md border-b border-white/10 font-mono text-slate-400 uppercase text-[11px]">',
                    '<thead class="bg-slate-100 border-b border-slate-200 font-mono text-slate-700 uppercase text-[11px] font-bold">')

text = text.replace('<th class="py-3 px-3.5 text-right bg-amber-500/10 text-amber-300 font-bold">Aporte Simulado</th>',
                    '<th class="py-3 px-3.5 text-right bg-amber-50 text-amber-900 font-bold border-l border-r border-amber-200">Aporte Simulado</th>')

text = text.replace('<th class="py-3 px-3 text-right bg-amber-500/10 text-amber-300 font-bold">Qtd Ações</th>',
                    '<th class="py-3 px-3 text-right bg-amber-50 text-amber-900 font-bold border-r border-amber-200">Qtd Ações</th>')

text = text.replace('<tbody id="portStocksTableBody" class="divide-y divide-white/5 font-sans">',
                    '<tbody id="portStocksTableBody" class="divide-y divide-slate-100 font-sans">')

text = text.replace("const rowBg = idx % 2 === 0 ? 'bg-white/[0.01]' : 'bg-transparent';",
                    "const rowBg = idx % 2 === 0 ? 'bg-white' : 'bg-slate-50/50';")

text = text.replace('<span class="text-sm font-bold text-amber-300 tracking-wide font-mono">${s.ticker}</span>',
                    '<span class="text-sm font-bold text-slate-900 tracking-wide font-mono">${s.ticker}</span>')

text = text.replace('<td class="py-2.5 px-3 text-right font-mono font-semibold text-white">${formatCurrency(s.cotacao)}</td>',
                    '<td class="py-2.5 px-3 text-right font-mono font-bold text-slate-900">${formatCurrency(s.cotacao)}</td>')

text = text.replace('<input type="number" id="simCapitalInput" value="50000" step="5000" min="1000" oninput="updateSimulationCapital(this.value)" class="w-full bg-slate-900/80 border border-white/10 focus:border-emerald-400 rounded-full pl-10 pr-4 py-2 text-white font-bold text-sm tracking-wide transition" />',
                    '<input type="number" id="simCapitalInput" value="50000" step="5000" min="1000" oninput="updateSimulationCapital(this.value)" class="w-full bg-slate-50 border border-slate-200 focus:bg-white focus:border-emerald-500 rounded-full pl-10 pr-4 py-2 text-slate-900 font-bold text-sm tracking-wide transition" />')

text = text.replace('glass-pill hover:bg-white/10 text-slate-300', 'bg-slate-100 hover:bg-slate-200 border border-slate-200 text-slate-700 font-medium')
text = text.replace('glass-pill bg-amber-500/20 border-amber-500/50 text-amber-300', 'bg-emerald-50 border border-emerald-300 text-emerald-800 font-bold')

# 3. Dossiê Drawer
text = text.replace('<span class="font-mono font-bold text-xs text-white uppercase tracking-wider">Dossiê Fundamentalista 360°</span>',
                    '<span class="font-mono font-bold text-xs text-slate-900 uppercase tracking-wider">Dossiê Fundamentalista 360°</span>')

text = text.replace('<div class="text-2xl font-bold font-mono text-white tracking-tight flex items-center gap-2">',
                    '<div class="text-2xl font-bold font-mono text-slate-900 tracking-tight flex items-center gap-2">')

text = text.replace('<div class="text-sm font-medium text-slate-200 truncate max-w-[260px] mt-0.5">${s.empresa}</div>',
                    '<div class="text-sm font-semibold text-slate-700 truncate max-w-[260px] mt-0.5">${s.empresa}</div>')

text = text.replace('<b class="text-slate-200 font-mono">${formatCurrency(s.cotacao)}</b>',
                    '<b class="text-slate-900 font-mono">${formatCurrency(s.cotacao)}</b>')

# Gráfico Histórico 5 anos no Drawer
text = text.replace('<div class="font-mono font-bold text-xs text-white flex items-center gap-1.5">',
                    '<div class="font-mono font-bold text-xs text-slate-900 flex items-center gap-1.5">')

text = text.replace('<span class="text-slate-300 font-semibold">Receita</span>',
                    '<span class="text-slate-700 font-semibold">Receita</span>')

text = text.replace('<span class="text-slate-300 font-semibold">Lucro Líquido</span>',
                    '<span class="text-slate-700 font-semibold">Lucro Líquido</span>')

text = text.replace('<text-white font-semibold">${formatBillions(r)}</td>',
                    '<text-slate-900 font-semibold">${formatBillions(r)}</td>')

text = text.replace('stroke="rgba(255,255,255,0.06)"', 'stroke="#E2E8F0"')
text = text.replace('stroke="rgba(255,255,255,0.12)"', 'stroke="#CBD5E1"')

with open("build_standalone_html.py", "w", encoding="utf-8") as f:
    f.write(text)

print("Perfeição total aplicada em build_standalone_html.py!")
