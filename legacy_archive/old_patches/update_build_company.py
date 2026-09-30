with open('build_company_page.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update essential multiples
old_m = """      const items = [
        {{ label: 'P/L Histórico', val: formatMultiple(s.pl), desc: 'Preço sobre Lucro LTM', color: 'text-slate-900' }},
        {{ label: 'P/L Run-Rate', val: s.pl_run_rate ? formatMultiple(s.pl_run_rate) : 'N/D', desc: 'Ritmo anualizado 2T26', color: s.pl_run_rate && s.pl && s.pl_run_rate < s.pl ? 'text-emerald-800 font-bold' : 'text-slate-900' }},
        {{ label: 'P / VP', val: formatMultiple(s.pvp), desc: 'Preço sobre Valor Patrimonial', color: 'text-slate-900' }},
        {{ label: 'EV / EBITDA', val: s.is_financial ? 'N/A' : (s.ev_ebitda !== null ? formatMultiple(s.ev_ebitda) : 'N/D'), desc: 'Múltiplo da Firma', color: 'text-slate-900' }},
        {{ label: 'ROIC / ROE', val: formatPercent(roicVal), desc: s.is_financial ? 'Retorno s/ Patrimônio' : 'Retorno Capital Investido', color: roicVal >= 0.15 ? 'text-emerald-800 font-bold' : 'text-slate-900' }},
        {{ label: 'Margem Líquida', val: formatPercent(s.mrg_liq), desc: 'Conversão em Lucro Líquido', color: s.mrg_liq >= 0.15 ? 'text-emerald-800 font-bold' : 'text-slate-900' }},
        {{ label: 'Dividend Yield', val: formatPercent(s.div_yield), desc: 'Proventos pagos 12m', color: s.div_yield >= 0.06 ? 'text-emerald-800 font-bold' : 'text-slate-900' }},
        {{ label: 'Alavancagem', val: debtText, desc: 'Dívida Líquida / EBITDA', color: dlVal !== null && dlVal <= 0 ? 'text-emerald-800 font-bold' : 'text-slate-900' }}
      ];"""

new_m = """      const items = [
        {{ label: 'P/L Histórico', val: formatMultiple(s.pl), desc: 'Preço sobre Lucro LTM', color: 'text-slate-900' }},
        {{ label: 'P/L Run-Rate', val: s.pl_run_rate ? formatMultiple(s.pl_run_rate) : 'N/D', desc: 'Ritmo anualizado 2T26', color: s.pl_run_rate && s.pl && s.pl_run_rate < s.pl ? 'text-emerald-800 font-bold' : 'text-slate-900' }},
        {{ label: 'P / VP', val: formatMultiple(s.pvp), desc: 'Preço sobre Patrimônio', color: 'text-slate-900' }},
        {{ label: 'EV / EBITDA', val: s.is_financial ? 'N/A' : (s.ev_ebitda !== null ? formatMultiple(s.ev_ebitda) : 'N/D'), desc: 'Múltiplo da Firma', color: 'text-slate-900' }},
        {{ label: 'ROIC Operacional', val: s.is_financial ? 'N/A (Bancos)' : formatPercent(s.roic), desc: 'Retorno Capital Investido (NOPAT/CI)', color: (!s.is_financial && s.roic >= 0.15) ? 'text-emerald-800 font-bold' : 'text-slate-900' }},
        {{ label: 'ROE do Acionista', val: formatPercent(s.roe), desc: 'Retorno s/ Patrimônio Líquido', color: s.roe >= 0.15 ? 'text-emerald-800 font-bold' : 'text-slate-900' }},
        {{ label: 'Margem Líquida', val: formatPercent(s.mrg_liq), desc: 'Conversão em Lucro Líquido', color: s.mrg_liq >= 0.15 ? 'text-emerald-800 font-bold' : 'text-slate-900' }},
        {{ label: 'Dividend Yield', val: formatPercent(s.div_yield), desc: 'Proventos pagos 12m', color: s.div_yield >= 0.06 ? 'text-emerald-800 font-bold' : 'text-slate-900' }}
      ];"""

assert old_m in code, 'old_m not found'
code = code.replace(old_m, new_m, 1)

# 2. Update peers table header
old_p_th = """              <th class="py-3 px-2 text-right">ROIC/ROE</th>"""
new_p_th = """              <th class="py-3 px-2 text-right" title="Retorno sobre Capital Investido">ROIC</th>
              <th class="py-3 px-2 text-right" title="Retorno sobre Patrimônio Líquido">ROE</th>"""
assert old_p_th in code, 'old_p_th not found'
code = code.replace(old_p_th, new_p_th, 1)

# 3. Update peers table td
old_p_td = """          <td class="py-2.5 px-2 text-right font-mono font-semibold text-emerald-800">${{formatPercent(p.roic || p.roe)}}</td>"""
new_p_td = """          <td class="py-2.5 px-2 text-right font-mono font-semibold text-slate-800">${{p.is_financial ? 'N/A' : formatPercent(p.roic)}}</td>
          <td class="py-2.5 px-2 text-right font-mono font-semibold text-emerald-800">${{formatPercent(p.roe)}}</td>"""
assert old_p_td in code, 'old_p_td not found'
code = code.replace(old_p_td, new_p_td, 1)

with open('build_company_page.py', 'w', encoding='utf-8') as f:
    f.write(code)

print('build_company_page.py updated successfully!')
