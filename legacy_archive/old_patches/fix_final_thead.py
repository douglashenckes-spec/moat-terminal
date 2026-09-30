with open("build_standalone_html.py", "r", encoding="utf-8") as f:
    text = f.read()

# 1. thead da tabela de carteiras
text = text.replace('class="bg-[#0A0E1A]/95 backdrop-blur-md border-b border-slate-200 font-mono text-slate-400 uppercase text-[11px]"',
                    'class="bg-slate-100 border-b border-slate-200 font-mono text-slate-700 uppercase text-[11px] font-bold"')

# 2. Qtd ações e Tese nas linhas da tabela de carteiras
text = text.replace('<td class="py-2.5 px-3 text-right font-mono font-bold text-white bg-amber-500/10">${{simQty.toLocaleString(\'pt-BR\')}} <span class="text-[10px] text-slate-400 font-normal">ações</span></td>',
                    '<td class="py-2.5 px-3 text-right font-mono font-bold text-emerald-900 bg-emerald-50 border-r border-emerald-200">${{simQty.toLocaleString(\'pt-BR\')}} <span class="text-[10px] text-emerald-700 font-normal">ações</span></td>')

text = text.replace('<div class="text-[11px] text-slate-300 font-sans max-w-[340px] leading-relaxed">${{s.thesis}}</div>',
                    '<div class="text-[11px] text-slate-700 font-sans font-medium max-w-[340px] leading-relaxed">${{s.thesis}}</div>')

with open("build_standalone_html.py", "w", encoding="utf-8") as f:
    f.write(text)

print("Ajuste final do thead e tese da carteira aplicado!")
