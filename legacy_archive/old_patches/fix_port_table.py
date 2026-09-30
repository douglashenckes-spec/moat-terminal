with open("build_standalone_html.py", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Título da tabela de carteiras
text = text.replace('<span class="text-sm font-mono font-bold text-white flex items-center gap-1.5" id="portTableTitle">',
                    '<span class="text-sm font-mono font-bold text-slate-900 flex items-center gap-1.5" id="portTableTitle">')

# 2. Subtítulo da tabela de carteiras
text = text.replace('<span class="text-xs text-amber-400 font-mono font-semibold" id="portTableSubtitle">',
                    '<span class="text-xs text-emerald-800 font-mono font-bold" id="portTableSubtitle">')

# 3. Cabeçalho thead da tabela de carteiras
text = text.replace('<th class="py-3 px-3.5">Tese Mungeriana / Racional de Investimento</th>',
                    '<th class="py-3 px-3.5 text-slate-700 font-bold">Tese de Investimento &amp; Racional</th>')

# 4. Tese de investimento nas linhas da tabela de carteiras
text = text.replace('<td class="py-2.5 px-3.5 text-xs text-slate-300 leading-relaxed font-sans max-w-md">',
                    '<td class="py-2.5 px-3.5 text-xs text-slate-700 leading-relaxed font-sans max-w-md">')

text = text.replace('text-slate-300 leading-relaxed', 'text-slate-700 leading-relaxed')

with open("build_standalone_html.py", "w", encoding="utf-8") as f:
    f.write(text)

print("Ajuste da tabela de carteiras aplicado!")
