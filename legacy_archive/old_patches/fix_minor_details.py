with open("build_standalone_html.py", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Indicadores médios ponderados texto
text = text.replace('text-xs font-mono font-bold text-slate-200 uppercase tracking-wider flex items-center gap-1.5',
                    'text-xs font-mono font-bold text-slate-800 uppercase tracking-wider flex items-center gap-1.5')

# 2. Input do simulador
text = text.replace('class="w-full bg-slate-900/80 border border-white/10 focus:border-emerald-400 rounded-full pl-10 pr-4 py-2 text-white font-bold text-sm tracking-wide transition"',
                    'class="w-full bg-slate-50 border border-slate-200 focus:bg-white focus:border-emerald-500 rounded-full pl-10 pr-4 py-2 text-slate-900 font-bold text-sm tracking-wide transition"')

# 3. ROIC 11,0% no 3º card da home
text = text.replace('elRoic.className = \'text-2xl font-bold font-mono \' + getColorRoe(medianRoic);',
                    'elRoic.className = \'text-2xl font-bold font-mono text-emerald-800\';')

with open("build_standalone_html.py", "w", encoding="utf-8") as f:
    f.write(text)

print("Ajustes pontuais aplicados com sucesso!")
