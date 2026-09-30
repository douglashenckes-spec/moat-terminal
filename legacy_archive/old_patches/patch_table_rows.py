with open("build_standalone_html.py", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Tickers em preto/slate-900
text = text.replace('<span class="text-sm font-bold text-amber-300 tracking-wide font-mono">${{s.ticker}}</span>',
                    '<span class="text-sm font-bold text-slate-900 tracking-wide font-mono">${{s.ticker}}</span>')

# 2. Cotação em slate-900 na tabela scanner
text = text.replace('<td class="py-2.5 px-3 text-xs text-right font-semibold text-white font-mono" title="Liquidez M?dia: ${{formatBillions(s.liq_2m)}}/d">${{formatCurrency(s.cotacao)}}</td>',
                    '<td class="py-2.5 px-3 text-xs text-right font-bold text-slate-900 font-mono" title="Liquidez Média: ${{formatBillions(s.liq_2m)}}/d">${{formatCurrency(s.cotacao)}}</td>')

# Fallback se a interrogação for diferente
import re
text = re.sub(
    r'<td class="py-2\.5 px-3 text-xs text-right font-semibold text-white font-mono"[^>]*>\${{formatCurrency\(s\.cotacao\)\}}</td>',
    '<td class="py-2.5 px-3 text-xs text-right font-bold text-slate-900 font-mono">${{formatCurrency(s.cotacao)}}</td>',
    text
)

# 3. Cotação na tabela de carteiras
text = text.replace('<td class="py-2.5 px-3 text-right font-mono font-semibold text-white">${{formatCurrency(s.cotacao)}}</td>',
                    '<td class="py-2.5 px-3 text-right font-mono font-bold text-slate-900">${{formatCurrency(s.cotacao)}}</td>')

# 4. EV/EBITDA em slate-700
text = text.replace('text-medium text-slate-200 font-mono">${{s.is_financial ? \'N/A\' : (s.ev_ebitda !== null ? formatMultiple(s.ev_ebitda) : \'N/D\')}}',
                    'text-medium text-slate-700 font-mono font-semibold">${{s.is_financial ? \'N/A\' : (s.ev_ebitda !== null ? formatMultiple(s.ev_ebitda) : \'N/D\')}}')

text = text.replace('text-slate-200 font-mono">${{s.is_financial',
                    'text-slate-700 font-mono font-semibold">${{s.is_financial')

# 5. Nome da empresa na tabela scanner
text = text.replace('<div class="text-[11px] text-slate-400 font-sans truncate max-w-[150px]"',
                    '<div class="text-[11px] text-slate-600 font-sans font-medium truncate max-w-[150px]"')

# 6. Aporte simulado na tabela de carteiras
text = text.replace('text-amber-300 bg-amber-500/10">${{formatCurrency(simVal)}}</td>',
                    'text-emerald-900 font-bold bg-emerald-50 border-l border-r border-emerald-200">${{formatCurrency(simVal)}}</td>')

text = text.replace('text-amber-300 bg-amber-500/10">${{simQty.toLocaleString(\'pt-BR\')}}</td>',
                    'text-emerald-900 font-bold bg-emerald-50 border-r border-emerald-200">${{simQty.toLocaleString(\'pt-BR\')}}</td>')

# 7. Peso da carteira badge
text = text.replace('bg-amber-500/20 text-amber-300 border border-amber-500/40',
                    'bg-slate-100 text-slate-800 border border-slate-300 font-bold')

with open("build_standalone_html.py", "w", encoding="utf-8") as f:
    f.write(text)

print("Patch aplicado com sucesso em build_standalone_html.py!")
