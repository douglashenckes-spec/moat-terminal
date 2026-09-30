with open('build_standalone_html.py', 'r', encoding='utf-8') as f:
    c = f.read()

replacements = [
    # Table Filter pill Ultra-Crítico -> Máxima Solvência
    ("💎 Ultra-Crítico (<span id=\"cnt-CAT_ULTRA_CRITIC\">--</span>)", "💎 Máxima Solvência (<span id=\"cnt-CAT_ULTRA_CRITIC\">--</span>)"),
    
    # Gatekeeper pill checkboxes and text
    ('<span class="text-slate-200">Liq &ge; R$ 1M</span>', '<span class="text-slate-700 font-medium">Liq &ge; R$ 1M</span>'),
    ('<span class="text-slate-200">Balanço 2T26</span>', '<span class="text-slate-700 font-medium">Balanço 2T26</span>'),
    ('<span class="text-slate-200">Só Recorrente</span>', '<span class="text-slate-700 font-medium">Só Recorrente</span>'),
    ('<span class="text-slate-200">Acid Test &ge; 75%</span>', '<span class="text-slate-700 font-medium">Acid Test &ge; 75%</span>'),
    ('<span class="text-slate-200">Só Ações ON</span>', '<span class="text-slate-700 font-medium">Só Ações ON</span>'),
    
    ('w-3.5 h-3.5 rounded text-emerald-500 bg-slate-800 border-slate-700', 'w-3.5 h-3.5 rounded text-emerald-600 bg-white border-slate-300'),
    ('w-3.5 h-3.5 rounded text-purple-400 bg-slate-800 border-slate-700', 'w-3.5 h-3.5 rounded text-purple-600 bg-white border-slate-300'),
    ('w-3.5 h-3.5 rounded text-yellow-400 bg-slate-800 border-slate-700', 'w-3.5 h-3.5 rounded text-amber-600 bg-white border-slate-300'),
    ('w-3.5 h-3.5 rounded text-indigo-400 bg-slate-800 border-slate-700', 'w-3.5 h-3.5 rounded text-indigo-600 bg-white border-slate-300'),
    
    # Home bottom 4 cards
    ('<span class="text-xl font-bold text-white group-hover:text-emerald-800 transition" id="home-quad-above-cnt">--</span>',
     '<span class="text-xl font-bold text-slate-900 group-hover:text-emerald-700 transition" id="home-quad-above-cnt">--</span>'),
     
    ('<span class="text-xl font-bold text-white group-hover:text-amber-800 transition" id="home-quad-below-cnt">--</span>',
     '<span class="text-xl font-bold text-slate-900 group-hover:text-amber-700 transition" id="home-quad-below-cnt">--</span>'),
     
    ('<span class="text-xs font-bold text-teal-300 flex items-center gap-1"><span>⚡</span> MOMENTO EM ALTA</span>',
     '<span class="text-xs font-bold text-teal-800 flex items-center gap-1"><span>⚡</span> MOMENTO EM ALTA</span>'),
    ('<span class="text-xl font-bold text-white group-hover:text-teal-300 transition" id="home-quad-accel-cnt">--</span>',
     '<span class="text-xl font-bold text-slate-900 group-hover:text-teal-700 transition" id="home-quad-accel-cnt">--</span>'),
    ('<div class="text-[10px] text-teal-300 font-bold mt-2">Filtrar na Tabela ➜</div>',
     '<div class="text-[10px] text-teal-700 font-bold mt-2">Filtrar na Tabela ➜</div>'),
     
    ('<span class="text-xs font-bold text-cyan-300 flex items-center gap-1"><span>💰</span> DIVIDENDOS CONSISTENTES</span>',
     '<span class="text-xs font-bold text-cyan-800 flex items-center gap-1"><span>💰</span> DIVIDENDOS CONSISTENTES</span>'),
    ('<span class="text-xl font-bold text-white group-hover:text-cyan-300 transition" id="home-quad-div-cnt">--</span>',
     '<span class="text-xl font-bold text-slate-900 group-hover:text-cyan-700 transition" id="home-quad-div-cnt">--</span>'),
    ('<div class="text-[10px] text-cyan-300 font-bold mt-2">Filtrar na Tabela ➜</div>',
     '<div class="text-[10px] text-cyan-700 font-bold mt-2">Filtrar na Tabela ➜</div>'),
     
    # Card descriptions in bottom 4 cards
    ('<p class="text-[11px] text-slate-400 font-sans mt-1">Desconto Relativo', '<p class="text-[11px] text-slate-600 font-sans mt-1">Desconto Relativo'),
    ('<p class="text-[11px] text-slate-400 font-sans mt-1">Prêmio Exigente', '<p class="text-[11px] text-slate-600 font-sans mt-1">Prêmio Exigente'),
    ('<p class="text-[11px] text-slate-400 font-sans mt-1">Run-Rate 2T26', '<p class="text-[11px] text-slate-600 font-sans mt-1">Run-Rate 2T26'),
    ('<p class="text-[11px] text-slate-400 font-sans mt-1">Dividend Yield &ge; 5%', '<p class="text-[11px] text-slate-600 font-sans mt-1">Dividend Yield &ge; 5%')
]

count = 0
for old, new in replacements:
    if old in c:
        c = c.replace(old, new)
        count += 1
    else:
        print(f'MISSED: {old[:50]}...')

print(f'Applied {count}/{len(replacements)} replacements.')
with open('build_standalone_html.py', 'w', encoding='utf-8') as f:
    f.write(c)
