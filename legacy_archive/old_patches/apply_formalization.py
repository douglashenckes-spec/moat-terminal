import sys

with open('build_standalone_html.py', 'r', encoding='utf-8') as f:
    c = f.read()

replacements = [
    # Header & Titles in switchWorkspace
    ("<span>📊</span> <span>MATRIZ MUNGER 2X2</span>", "<span>📊</span> <span>MATRIZ ESTRATÉGICA 2X2</span>"),
    ("topSub.innerText = 'Qualidade Charlie Munger vs. Valuation e dispersão do mercado';", "topSub.innerText = 'Score de Qualidade Fundamentalista vs. Valuation e dispersão do mercado';"),
    
    # Portfolio nameMap & shortMap
    ("'munger': '🏆 CARTEIRA CHARLIE MUNGER (COMPOUNDERS &amp; MOATS)',", "'munger': '🏆 CARTEIRA FUNDAMENTALISTA PREMIUM (COMPOUNDERS &amp; MOATS)',"),
    ("'asymmetry': '📈 CARTEIRA ASSIMETRIA REAL (DEEP VALUE &amp; GRAHAM)',", "'asymmetry': '📈 CARTEIRA ASSIMETRIA DE VALUATION (DEEP VALUE &amp; MARGEM DE SEGURANÇA)',"),
    ("'cfa_ultra': '💎 CARTEIRA INSTITUCIONAL CFA ULTRA-CRÍTICA'", "'cfa_ultra': '💎 CARTEIRA MÁXIMA SOLVÊNCIA &amp; RESILIÊNCIA (CRITÉRIO INSTITUCIONAL)'"),
    ("'dividends': 'Vacas Leiteiras • Alocação 100% Ponderada (8 Ativos)',", "'dividends': 'Dividendos Consistentes • Alocação 100% Ponderada (8 Ativos)',"),
    ("'asymmetry': 'Deep Value & Graham • Alocação 100% Ponderada (8 Ativos)',", "'asymmetry': 'Deep Value & Assimetria • Alocação 100% Ponderada (8 Ativos)',"),
    ("'cfa_ultra': 'Régua CFA Ultra-Crítica • Alocação 100% Ponderada (8 Ativos)'", "'cfa_ultra': 'Máxima Solvência & Solidez • Alocação 100% Ponderada (8 Ativos)'"),
    
    # Thesis fallback
    ("Ativo com Munger Score de", "Ativo com Score Fundamentalista de"),
    
    # Badge labels & categories in JS
    ("label: 'Filé Mignon Munger',", "label: 'Líderes de Setor (Tier 1)',"),
    ("shortLabel: 'Filé Mignon',", "shortLabel: 'Tier 1',"),
    ("bgClass: 'bg-amber-950/80 text-amber-300 border border-amber-700/60'", "bgClass: 'bg-amber-50 text-amber-800 border border-amber-300 font-semibold'"),
    ("label: 'Assimetria Real',", "label: 'Assimetria de Valuation',"),
    ("bgClass: 'bg-cyan-950/80 text-cyan-300 border border-cyan-700/60'", "bgClass: 'bg-sky-50 text-sky-800 border border-sky-300 font-semibold'"),
    ("label: 'Vaca Leiteira',", "label: 'Dividendos Consistentes',"),
    ("bgClass: 'bg-emerald-950/80 text-emerald-300 border border-emerald-700/60'", "bgClass: 'bg-emerald-50 text-emerald-800 border border-emerald-300 font-semibold'"),
    ("bgClass: 'bg-yellow-950/90 text-amber-800 border border-yellow-500/70 shadow-sm'", "bgClass: 'bg-amber-50 text-amber-800 border border-amber-300 shadow-sm font-semibold'"),
    
    # Rankings cards tooltips & pills
    ('title="Ver lista completa de empresas Filé Mignon na Tabela"', 'title="Ver lista completa de Líderes de Setor na Tabela"'),
    ('title="Ver lista completa de empresas com Assimetria Real na Tabela"', 'title="Ver lista completa de empresas com Assimetria de Valuation na Tabela"'),
    ('title="Ver lista completa de Vacas Leiteiras na Tabela"', 'title="Ver lista completa de Dividendos Consistentes na Tabela"'),
    ('title="Filtrar Vacas Leiteiras (Dividend Yield &gt; 5%)"', 'title="Filtrar Dividendos Consistentes (Dividend Yield &gt; 5%)"'),
    
    # Pill colors in Home rankings
    ('class="text-[10px] font-mono font-bold text-amber-300 hover:text-slate-900 glass-pill border-amber-500/30 px-2.5 py-0.5 rounded-full transition cursor-pointer flex items-center gap-1"', 'class="text-[10px] font-mono font-semibold text-amber-800 hover:bg-amber-100 bg-amber-50 border border-amber-300 px-2.5 py-0.5 rounded-full transition cursor-pointer flex items-center gap-1"'),
    ('class="text-[10px] font-mono font-bold text-cyan-300 hover:text-slate-900 glass-pill border-cyan-500/30 px-2.5 py-0.5 rounded-full transition cursor-pointer flex items-center gap-1"', 'class="text-[10px] font-mono font-semibold text-sky-800 hover:bg-sky-100 bg-sky-50 border border-sky-300 px-2.5 py-0.5 rounded-full transition cursor-pointer flex items-center gap-1"'),
    ('class="text-[10px] font-mono font-bold text-emerald-300 hover:text-slate-900 glass-pill border-emerald-500/30 px-2.5 py-0.5 rounded-full transition cursor-pointer flex items-center gap-1"', 'class="text-[10px] font-mono font-semibold text-emerald-800 hover:bg-emerald-100 bg-emerald-50 border border-emerald-300 px-2.5 py-0.5 rounded-full transition cursor-pointer flex items-center gap-1"'),
    
    # Matrix filter pills
    ('border-amber-500/40 hover:border-amber-400 text-amber-300 transition cursor-pointer', 'border-amber-300 bg-amber-50 hover:bg-amber-100 text-amber-800 font-semibold transition cursor-pointer'),
    ('border-teal-400/40 hover:border-teal-300 text-teal-200 transition cursor-pointer', 'border-teal-300 bg-teal-50 hover:bg-teal-100 text-teal-800 font-semibold transition cursor-pointer'),
    ('border-cyan-500/40 hover:border-cyan-400 text-cyan-300 transition cursor-pointer', 'border-cyan-300 bg-cyan-50 hover:bg-cyan-100 text-cyan-800 font-semibold transition cursor-pointer'),
    ('bg-amber-500/20 px-1.5 py-0.2 rounded-full text-[10px] font-bold text-white', 'bg-amber-200 px-1.5 py-0.2 rounded-full text-[10px] font-bold text-amber-900'),
    ('bg-teal-500/20 px-1.5 py-0.2 rounded-full text-[10px] font-bold text-white', 'bg-teal-200 px-1.5 py-0.2 rounded-full text-[10px] font-bold text-teal-900'),
    ('bg-cyan-500/20 px-1.5 py-0.2 rounded-full text-[10px] font-bold text-white', 'bg-cyan-200 px-1.5 py-0.2 rounded-full text-[10px] font-bold text-cyan-900')
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
