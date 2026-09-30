import re

# 1. UPDATE build_standalone_html.py
with open('build_standalone_html.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Add getColorRoic alongside getColorRoe
old_get_color_roe = """    function getColorRoe(val) {{
      if (val === null || val === undefined) return 'text-slate-500';
      const num = Math.abs(val) < 2.0 ? val * 100 : val;
      if (num >= 15.0) return 'text-emerald-700 font-bold';
      if (num >= 8.0) return 'text-slate-700 font-medium';
      if (num >= 0.0) return 'text-amber-800 font-medium';
      return 'text-rose-700 font-bold';
    }}"""

new_get_color_roe = """    function getColorRoic(val, isFin = false) {{
      if (isFin) return 'text-slate-400 font-normal';
      if (val === null || val === undefined) return 'text-slate-500';
      const num = Math.abs(val) < 2.0 ? val * 100 : val;
      if (num >= 15.0) return 'text-emerald-700 font-bold';
      if (num >= 8.0) return 'text-slate-700 font-medium';
      if (num >= 0.0) return 'text-amber-800 font-medium';
      return 'text-rose-700 font-bold';
    }}

    function getColorRoe(val) {{
      if (val === null || val === undefined) return 'text-slate-500';
      const num = Math.abs(val) < 2.0 ? val * 100 : val;
      if (num >= 15.0) return 'text-emerald-700 font-bold';
      if (num >= 8.0) return 'text-slate-700 font-medium';
      if (num >= 0.0) return 'text-amber-800 font-medium';
      return 'text-rose-700 font-bold';
    }}"""

assert old_get_color_roe in code, "Failed to find old_get_color_roe"
code = code.replace(old_get_color_roe, new_get_color_roe, 1)

# Update Scanner B3 thead
old_scanner_th = """                <th onclick="sortTable('ev_ebitda')" class="py-2 px-2 cursor-pointer hover:text-emerald-700 text-right" title="Valor da Firma sobre EBITDA">EV / EBITDA ⬍</th>
                <th onclick="sortTable('roic')" class="py-2 px-2 cursor-pointer hover:text-emerald-700 text-right" title="Retorno sobre Capital Empregado (ROIC / ROE)">ROIC / ROE ⬍</th>
                <th onclick="sortTable('mrg_liq')" class="py-2 px-2 cursor-pointer hover:text-emerald-700 text-right" title="Margem Líquida">Margem Líq. ⬍</th>"""

new_scanner_th = """                <th onclick="sortTable('ev_ebitda')" class="py-2 px-2 cursor-pointer hover:text-emerald-700 text-right" title="Valor da Firma sobre EBITDA (Múltiplo da Firma)">EV / EBITDA ⬍</th>
                <th onclick="sortTable('roic')" class="py-2 px-2 cursor-pointer hover:text-emerald-700 text-right" title="Retorno sobre Capital Investido (Eficiência Operacional NOPAT/CI)">ROIC ⬍</th>
                <th onclick="sortTable('roe')" class="py-2 px-2 cursor-pointer hover:text-emerald-700 text-right" title="Retorno sobre o Patrimônio Líquido (Retorno do Acionista Lucro/PL)">ROE ⬍</th>
                <th onclick="sortTable('mrg_liq')" class="py-2 px-2 cursor-pointer hover:text-emerald-700 text-right" title="Margem Líquida">Margem Líq. ⬍</th>"""

assert old_scanner_th in code, "Failed to find old_scanner_th"
code = code.replace(old_scanner_th, new_scanner_th, 1)

# Update Categorias B3 thead
old_cat_th = """                <th class="py-3 px-3 text-right">ROIC / ROE</th>"""
new_cat_th = """                <th class="py-2 px-2 text-right" title="Retorno sobre Capital Investido">ROIC</th>
                <th class="py-2 px-2 text-right" title="Retorno sobre Patrimônio Líquido">ROE</th>"""
assert old_cat_th in code, "Failed to find old_cat_th"
code = code.replace(old_cat_th, new_cat_th, 1)

# Update Categorias empty state colspan
code = code.replace('colspan="9" class="py-8 text-center text-slate-500 font-mono text-xs"', 'colspan="10" class="py-8 text-center text-slate-500 font-mono text-xs"')

# Update sortTable in JS
old_sort_logic = """      stocks.sort((a, b) => {{
        let vA = currentSortCol === 'roic' ? (a.roic || a.roe) : a[currentSortCol];
        let vB = currentSortCol === 'roic' ? (b.roic || b.roe) : b[currentSortCol];
        if (vA === null || vA === undefined) return 1;
        if (vB === null || vB === undefined) return -1;"""

new_sort_logic = """      stocks.sort((a, b) => {{
        let vA, vB;
        if (currentSortCol === 'roic') {{
          vA = a.is_financial ? -999 : (a.roic !== null && a.roic !== undefined ? a.roic : -999);
          vB = b.is_financial ? -999 : (b.roic !== null && b.roic !== undefined ? b.roic : -999);
          return currentSortAsc ? vA - vB : vB - vA;
        }} else if (currentSortCol === 'roe') {{
          vA = a.roe !== null && a.roe !== undefined ? a.roe : -999;
          vB = b.roe !== null && b.roe !== undefined ? b.roe : -999;
          return currentSortAsc ? vA - vB : vB - vA;
        }} else {{
          vA = a[currentSortCol];
          vB = b[currentSortCol];
        }}
        if (vA === null || vA === undefined) return 1;
        if (vB === null || vB === undefined) return -1;"""

assert old_sort_logic in code, "Failed to find old_sort_logic"
code = code.replace(old_sort_logic, new_sort_logic, 1)

# Update Scanner B3 row rendering
old_scanner_row_roic = """        // 3. ROIC / ROE Real
        const roicVal = s.roic || s.roe;
        const roicColor = getColorRoe(roicVal);"""

new_scanner_row_roic = """        // 3. ROIC (Operacional) e ROE (Acionista)
        const roicDisplay = s.is_financial ? '<span class="text-[10px] text-slate-400 font-sans font-normal">N/A (Bancos)</span>' : formatPercent(s.roic);
        const roicColor = s.is_financial ? 'text-slate-400' : getColorRoic(s.roic);
        const roeDisplay = formatPercent(s.roe);
        const roeColor = getColorRoe(s.roe);"""

assert old_scanner_row_roic in code, "Failed to find old_scanner_row_roic"
code = code.replace(old_scanner_row_roic, new_scanner_row_roic, 1)

# Update Scanner B3 row innerHTML using regex or exact substring
old_td_target = '          <td class="py-1.5 px-2 text-xs text-right font-medium text-slate-700 font-mono border-b border-slate-100">${{s.is_financial ? \'N/A\' : (s.ev_ebitda !== null ? formatMultiple(s.ev_ebitda) : \'N/D\')}}</td>\n          <td class="py-1.5 px-2 text-xs text-right font-semibold ${{roicColor}} font-mono border-b border-slate-100">${{formatPercent(roicVal)}}${{s.is_financial ? \' <span class=\\"text-[9px] text-indigo-800 font-normal\\">(ROE)</span>\' : \'\'}}</td>\n          <td class="py-1.5 px-2 text-xs text-right font-medium ${{mrgColor}} font-mono border-b border-slate-100">${{formatPercent(s.mrg_liq)}}</td>'

new_td_target = '          <td class="py-1.5 px-2 text-xs text-right font-medium text-slate-700 font-mono border-b border-slate-100">${{s.is_financial ? \'N/A\' : (s.ev_ebitda !== null ? formatMultiple(s.ev_ebitda) : \'N/D\')}}</td>\n          <td class="py-1.5 px-2 text-xs text-right font-semibold ${{roicColor}} font-mono border-b border-slate-100" title="ROIC: Retorno sobre Capital Investido (Operacional)">${{roicDisplay}}</td>\n          <td class="py-1.5 px-2 text-xs text-right font-semibold ${{roeColor}} font-mono border-b border-slate-100" title="ROE: Retorno sobre Patrimônio Líquido (Acionista)">${{roeDisplay}}</td>\n          <td class="py-1.5 px-2 text-xs text-right font-medium ${{mrgColor}} font-mono border-b border-slate-100">${{formatPercent(s.mrg_liq)}}</td>'

assert old_td_target in code, "Failed to find old_td_target"
code = code.replace(old_td_target, new_td_target, 1)

# Update Categorias table row rendering
old_cat_row_tds = """          <td class="py-1.5 px-2 text-xs text-right font-mono font-semibold border-b border-slate-100 ${{getColorPl(s.pl)}}">${{formatMultiple(s.pl)}}</td>
          <td class="py-1.5 px-2 text-xs text-right font-mono font-semibold border-b border-slate-100 ${{getColorRoe(s.roic || s.roe)}}">${{formatPercent(s.roic || s.roe)}}${{s.is_financial ? ' <span class="text-[9px] text-indigo-800 font-normal">(ROE)</span>' : ''}}</td>
          <td class="py-1.5 px-2 text-xs text-right font-mono font-bold border-b border-slate-100 ${{getColorDy(s.div_yield)}}">${{formatPercent(s.div_yield)}}</td>"""

new_cat_row_tds = """          <td class="py-1.5 px-2 text-xs text-right font-mono font-semibold border-b border-slate-100 ${{getColorPl(s.pl)}}">${{formatMultiple(s.pl)}}</td>
          <td class="py-1.5 px-2 text-xs text-right font-mono font-semibold border-b border-slate-100 ${{s.is_financial ? 'text-slate-400' : getColorRoic(s.roic)}}">${{s.is_financial ? 'N/A' : formatPercent(s.roic)}}</td>
          <td class="py-1.5 px-2 text-xs text-right font-mono font-semibold border-b border-slate-100 ${{getColorRoe(s.roe)}}">${{formatPercent(s.roe)}}</td>
          <td class="py-1.5 px-2 text-xs text-right font-mono font-bold border-b border-slate-100 ${{getColorDy(s.div_yield)}}">${{formatPercent(s.div_yield)}}</td>"""

assert old_cat_row_tds in code, "Failed to find old_cat_row_tds"
code = code.replace(old_cat_row_tds, new_cat_row_tds, 1)

# Update Dossiê Gauge 1
old_gauge_roe = """      // Renderizar os 3 Semicircular Gauges Bloomberg Calibrados com Benchmarks
      const roicOrRoe = s.roic !== null ? s.roic : (s.roe !== null ? s.roe : 0);
      renderAnalogGauge('gaugeRoe', roicOrRoe, 0.0, 0.30, s.is_financial ? 'ROE Auditado' : 'ROIC Auditado', {{
        isPercent: true,
        displayVal: formatPercent(s.roic || s.roe),
        refVal: 0.15,
        refText: 'Ref: ≥ 15%'
      }});"""

new_gauge_roe = """      // Renderizar os 3 Semicircular Gauges Bloomberg Calibrados com Benchmarks
      const gaugeMetricVal = s.is_financial ? (s.roe !== null ? s.roe : 0) : (s.roic !== null ? s.roic : (s.roe || 0));
      const gaugeMetricLabel = s.is_financial ? 'ROE do Acionista' : 'ROIC Operacional';
      const gaugeMetricRef = s.is_financial ? 'Ref ROE: ≥ 15%' : 'Ref ROIC: ≥ 15%';
      renderAnalogGauge('gaugeRoe', gaugeMetricVal, 0.0, 0.35, gaugeMetricLabel, {{
        isPercent: true,
        displayVal: formatPercent(gaugeMetricVal),
        refVal: 0.15,
        refText: gaugeMetricRef
      }});"""

assert old_gauge_roe in code, "Failed to find old_gauge_roe"
code = code.replace(old_gauge_roe, new_gauge_roe, 1)

# Update Dossiê kpiGrid to show ROIC and ROE as distinct cards
old_kpi_grid = """      // KPI Grid com Hierarquia de Cores
      const spreadStr = s.ey_spread !== null ? (s.ey_spread > 0 ? '+' : '') + s.ey_spread.toFixed(1) + '%' : 'N/D';
      const spreadColor = getColorSpread(s.ey_spread);
      const roicValActual = s.roic || s.roe;
      const roicColor = getColorRoe(roicValActual);
      const mrgColor = getColorMrgLiq(s.mrg_liq);
      const capStr = s.capital_intensity !== null ? (s.capital_intensity * 100).toFixed(0) + '%' : 'N/D';
      const capColor = s.is_financial ? 'text-indigo-800 font-semibold' : getColorAcidTest(s.capital_intensity);
      const debtColor = getColorDebt(s.div_liq_ebitda, s.is_financial);
      const debtVal = s.div_liq_ebitda;
      const debtStr = s.is_financial ? 'Bancos' : (debtVal !== null ? (debtVal < 0 ? 'Caixa Líq. 🛡️' : debtVal.toFixed(2) + 'x') : 'N/D');

      const payoutStr = s.payout_implicito !== null ? s.payout_implicito.toFixed(0) + '%' : 'N/D';
      let payoutColor = 'text-slate-500';
      if (s.payout_implicito !== null) {{
        const pVal = Number(s.payout_implicito);
        if (pVal > 100) payoutColor = 'text-rose-700 font-bold';
        else if (pVal >= 30 && pVal <= 85) payoutColor = 'text-emerald-700 font-bold';
        else if (pVal > 85) payoutColor = 'text-amber-800 font-semibold';
        else payoutColor = 'text-indigo-800 font-semibold';
      }}

      document.getElementById('kpiGrid').innerHTML = `
        <div class="glass-card rounded-xl border border-slate-200 p-2.5 text-center">
          <div class="text-[10px] text-slate-700 uppercase font-bold">ROIC / ROE</div>
          <div class="text-sm font-bold ${{roicColor}} mt-0.5">${{formatPercent(roicValActual)}}</div>
          <div class="text-[9px] text-slate-500 font-sans mt-0.5">Score: ${{s.sub_scores.roic.toFixed(0)}}/100</div>
        </div>
        <div class="glass-card rounded-xl border border-slate-200 p-2.5 text-center">
          <div class="text-[10px] text-slate-700 uppercase font-bold">Spread NTN-B</div>
          <div class="text-sm font-bold ${{spreadColor}} mt-0.5">${{spreadStr}}</div>
          <div class="text-[9px] text-slate-500 font-sans mt-0.5">Ref: 6,5% a.a.</div>
        </div>
        <div class="glass-card rounded-xl border border-slate-200 p-2.5 text-center">
          <div class="text-[10px] text-slate-700 uppercase font-bold">Payout</div>
          <div class="text-sm font-bold ${{payoutColor}} mt-0.5">${{payoutStr}}</div>
          <div class="text-[9px] text-slate-500 font-sans mt-0.5">${{s.payout_tag ? s.payout_tag.split(' ')[1] || 'Normal' : 'Normal'}}</div>
        </div>
        <div class="glass-card rounded-xl border border-slate-200 p-2.5 text-center">
          <div class="text-[10px] text-slate-700 uppercase font-bold">Dív.Líq / EBITDA</div>
          <div class="text-sm font-bold ${{debtColor}} mt-0.5">${{debtStr}}</div>
          <div class="text-[9px] text-slate-500 font-sans mt-0.5">Score: ${{s.sub_scores.div_liq_ebitda.toFixed(0)}}/100</div>
        </div>
        <div class="glass-card rounded-xl border border-slate-200 p-2.5 text-center">
          <div class="text-[10px] text-slate-700 uppercase font-bold">EBIT / EBITDA</div>
          <div class="text-sm font-bold ${{capColor}} mt-0.5">${{capStr}}</div>
          <div class="text-[9px] text-slate-500 font-sans mt-0.5">Munger Acid Test</div>
        </div>
        <div class="glass-card rounded-xl border border-slate-200 p-2.5 text-center">
          <div class="text-[10px] text-slate-700 uppercase font-bold">Margem Líq.</div>
          <div class="text-sm font-bold ${{mrgColor}} mt-0.5">${{formatPercent(s.mrg_liq)}}</div>
          <div class="text-[9px] text-slate-500 font-sans mt-0.5">Score: ${{s.sub_scores.mrg_liq.toFixed(0)}}/100</div>
        </div>
      `;"""

new_kpi_grid = """      // KPI Grid com Distinção Rigorosa entre ROIC e ROE
      const spreadStr = s.ey_spread !== null ? (s.ey_spread > 0 ? '+' : '') + s.ey_spread.toFixed(1) + '%' : 'N/D';
      const spreadColor = getColorSpread(s.ey_spread);
      const roicColor = s.is_financial ? 'text-slate-400' : getColorRoic(s.roic);
      const roeColor = getColorRoe(s.roe);
      const mrgColor = getColorMrgLiq(s.mrg_liq);
      const debtColor = getColorDebt(s.div_liq_ebitda, s.is_financial);
      const debtVal = s.div_liq_ebitda;
      const debtStr = s.is_financial ? 'Bancos' : (debtVal !== null ? (debtVal < 0 ? 'Caixa Líq. 🛡️' : debtVal.toFixed(2) + 'x') : 'N/D');

      const payoutStr = s.payout_implicito !== null ? s.payout_implicito.toFixed(0) + '%' : 'N/D';
      let payoutColor = 'text-slate-500';
      if (s.payout_implicito !== null) {{
        const pVal = Number(s.payout_implicito);
        if (pVal > 100) payoutColor = 'text-rose-700 font-bold';
        else if (pVal >= 30 && pVal <= 85) payoutColor = 'text-emerald-700 font-bold';
        else if (pVal > 85) payoutColor = 'text-amber-800 font-semibold';
        else payoutColor = 'text-indigo-800 font-semibold';
      }}

      document.getElementById('kpiGrid').innerHTML = `
        <div class="glass-card rounded-xl border border-slate-200 p-2.5 text-center">
          <div class="text-[10px] text-slate-700 uppercase font-bold flex items-center justify-center gap-1">
            <span>ROIC (Operacional)</span>
          </div>
          <div class="text-sm font-bold ${{roicColor}} mt-0.5">${{s.is_financial ? 'N/A (Bancos)' : formatPercent(s.roic)}}</div>
          <div class="text-[9px] text-slate-500 font-sans mt-0.5">${{s.is_financial ? 'Inaplicável a bancos' : 'Capital Investido'}}</div>
        </div>
        <div class="glass-card rounded-xl border border-slate-200 p-2.5 text-center">
          <div class="text-[10px] text-slate-700 uppercase font-bold flex items-center justify-center gap-1">
            <span>ROE (do Acionista)</span>
          </div>
          <div class="text-sm font-bold ${{roeColor}} mt-0.5">${{formatPercent(s.roe)}}</div>
          <div class="text-[9px] text-slate-500 font-sans mt-0.5">Retorno s/ Patrimônio</div>
        </div>
        <div class="glass-card rounded-xl border border-slate-200 p-2.5 text-center">
          <div class="text-[10px] text-slate-700 uppercase font-bold">Spread NTN-B</div>
          <div class="text-sm font-bold ${{spreadColor}} mt-0.5">${{spreadStr}}</div>
          <div class="text-[9px] text-slate-500 font-sans mt-0.5">Ref: 6,5% a.a.</div>
        </div>
        <div class="glass-card rounded-xl border border-slate-200 p-2.5 text-center">
          <div class="text-[10px] text-slate-700 uppercase font-bold">Dív.Líq / EBITDA</div>
          <div class="text-sm font-bold ${{debtColor}} mt-0.5">${{debtStr}}</div>
          <div class="text-[9px] text-slate-500 font-sans mt-0.5">${{s.is_financial ? 'Regulação Bacen' : 'Solvência Auditada'}}</div>
        </div>
        <div class="glass-card rounded-xl border border-slate-200 p-2.5 text-center">
          <div class="text-[10px] text-slate-700 uppercase font-bold">Margem Líq.</div>
          <div class="text-sm font-bold ${{mrgColor}} mt-0.5">${{formatPercent(s.mrg_liq)}}</div>
          <div class="text-[9px] text-slate-500 font-sans mt-0.5">Conversão em Lucro</div>
        </div>
        <div class="glass-card rounded-xl border border-slate-200 p-2.5 text-center">
          <div class="text-[10px] text-slate-700 uppercase font-bold">Payout Implícito</div>
          <div class="text-sm font-bold ${{payoutColor}} mt-0.5">${{payoutStr}}</div>
          <div class="text-[9px] text-slate-500 font-sans mt-0.5">${{s.payout_tag ? s.payout_tag.split(' ')[1] || 'Normal' : 'Normal'}}</div>
        </div>
      `;"""

assert old_kpi_grid in code, "Failed to find old_kpi_grid"
code = code.replace(old_kpi_grid, new_kpi_grid, 1)

# Update Balanço Card 1 to include both ROIC and ROE
old_bal_rows = """            <div class="flex justify-between py-0.5 border-b border-slate-200/60"><span class="text-slate-600 font-sans font-medium">EV / EBITDA:</span> <b class="text-slate-800 font-bold">${{s.is_financial ? 'N/A (Bancos)' : formatMultiple(s.ev_ebitda)}}</b></div>
            <div class="flex justify-between py-0.5"><span class="text-slate-600 font-sans font-medium">Dividend Yield:</span> <b class="${{getColorDy(s.div_yield)}} font-bold">${{formatPercent(s.div_yield)}}</b></div>"""

new_bal_rows = """            <div class="flex justify-between py-0.5 border-b border-slate-200/60"><span class="text-slate-600 font-sans font-medium">EV / EBITDA:</span> <b class="text-slate-800 font-bold">${{s.is_financial ? 'N/A (Bancos)' : formatMultiple(s.ev_ebitda)}}</b></div>
            <div class="flex justify-between py-0.5 border-b border-slate-200/60"><span class="text-slate-600 font-sans font-medium">ROIC (Capital Investido):</span> <b class="${{s.is_financial ? 'text-slate-400 font-normal' : getColorRoic(s.roic)}} font-bold">${{s.is_financial ? 'N/A (Bancos)' : formatPercent(s.roic)}}</b></div>
            <div class="flex justify-between py-0.5 border-b border-slate-200/60"><span class="text-slate-600 font-sans font-medium">ROE (Patrimônio Líquido):</span> <b class="${{getColorRoe(s.roe)}} font-bold">${{formatPercent(s.roe)}}</b></div>
            <div class="flex justify-between py-0.5"><span class="text-slate-600 font-sans font-medium">Dividend Yield:</span> <b class="${{getColorDy(s.div_yield)}} font-bold">${{formatPercent(s.div_yield)}}</b></div>"""

assert old_bal_rows in code, "Failed to find old_bal_rows"
code = code.replace(old_bal_rows, new_bal_rows, 1)

# Update Matrix Tooltip to show both ROIC and ROE
old_tt_roic = """<div class="text-slate-700">• ROIC: <b class="text-slate-900 font-bold">${{formatPercent(s.roic || s.roe)}}</b> | DY: <b class="text-emerald-800 font-bold">${{formatPercent(s.div_yield)}}</b></div>"""
new_tt_roic = """<div class="text-slate-700">• ROIC: <b class="text-slate-900 font-bold">${{s.is_financial ? 'N/A' : formatPercent(s.roic)}}</b> | ROE: <b class="text-slate-900 font-bold">${{formatPercent(s.roe)}}</b> | DY: <b class="text-emerald-800 font-bold">${{formatPercent(s.div_yield)}}</b></div>"""

assert old_tt_roic in code, "Failed to find old_tt_roic"
code = code.replace(old_tt_roic, new_tt_roic, 1)

with open('build_standalone_html.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("build_standalone_html.py successfully updated with ROIC and ROE separation!")

# 2. UPDATE build_company_page.py
with open('build_company_page.py', 'r', encoding='utf-8') as f:
    c_code = f.read()

# Update essentialMultiplesGrid
old_comp_multiples = """      const items = [
        {{ label: 'P/L Histórico', val: formatMultiple(s.pl), desc: 'Preço sobre Lucro LTM', color: 'text-slate-900' }},
        {{ label: 'P/L Run-Rate', val: s.pl_run_rate ? formatMultiple(s.pl_run_rate) : 'N/D', desc: 'Ritmo anualizado 2T26', color: s.pl_run_rate && s.pl && s.pl_run_rate < s.pl ? 'text-emerald-800 font-bold' : 'text-slate-900' }},
        {{ label: 'P / VP', val: formatMultiple(s.pvp), desc: 'Preço sobre Valor Patrimonial', color: 'text-slate-900' }},
        {{ label: 'EV / EBITDA', val: s.is_financial ? 'N/A' : (s.ev_ebitda !== null ? formatMultiple(s.ev_ebitda) : 'N/D'), desc: 'Múltiplo da Firma', color: 'text-slate-900' }},
        {{ label: 'ROIC / ROE', val: formatPercent(roicVal), desc: s.is_financial ? 'Retorno s/ Patrimônio' : 'Retorno Capital Investido', color: roicVal >= 0.15 ? 'text-emerald-800 font-bold' : 'text-slate-900' }},
        {{ label: 'Margem Líquida', val: formatPercent(s.mrg_liq), desc: 'Conversão em Lucro Líquido', color: s.mrg_liq >= 0.15 ? 'text-emerald-800 font-bold' : 'text-slate-900' }},
        {{ label: 'Dividend Yield', val: formatPercent(s.div_yield), desc: 'Proventos pagos 12m', color: s.div_yield >= 0.06 ? 'text-emerald-800 font-bold' : 'text-slate-900' }},
        {{ label: 'Alavancagem', val: debtText, desc: 'Dívida Líquida / EBITDA', color: dlVal !== null && dlVal <= 0 ? 'text-emerald-800 font-bold' : 'text-slate-900' }}
      ];"""

new_comp_multiples = """      const items = [
        {{ label: 'P/L Histórico', val: formatMultiple(s.pl), desc: 'Preço sobre Lucro LTM', color: 'text-slate-900' }},
        {{ label: 'P/L Run-Rate', val: s.pl_run_rate ? formatMultiple(s.pl_run_rate) : 'N/D', desc: 'Ritmo anualizado 2T26', color: s.pl_run_rate && s.pl && s.pl_run_rate < s.pl ? 'text-emerald-800 font-bold' : 'text-slate-900' }},
        {{ label: 'P / VP', val: formatMultiple(s.pvp), desc: 'Preço sobre Patrimônio', color: 'text-slate-900' }},
        {{ label: 'EV / EBITDA', val: s.is_financial ? 'N/A' : (s.ev_ebitda !== null ? formatMultiple(s.ev_ebitda) : 'N/D'), desc: 'Múltiplo da Firma', color: 'text-slate-900' }},
        {{ label: 'ROIC Operacional', val: s.is_financial ? 'N/A (Bancos)' : formatPercent(s.roic), desc: 'Retorno Capital Investido (NOPAT/CI)', color: (!s.is_financial && s.roic >= 0.15) ? 'text-emerald-800 font-bold' : 'text-slate-900' }},
        {{ label: 'ROE do Acionista', val: formatPercent(s.roe), desc: 'Retorno s/ Patrimônio Líquido', color: s.roe >= 0.15 ? 'text-emerald-800 font-bold' : 'text-slate-900' }},
        {{ label: 'Margem Líquida', val: formatPercent(s.mrg_liq), desc: 'Conversão em Lucro Líquido', color: s.mrg_liq >= 0.15 ? 'text-emerald-800 font-bold' : 'text-slate-900' }},
        {{ label: 'Dividend Yield', val: formatPercent(s.div_yield), desc: 'Proventos pagos 12m', color: s.div_yield >= 0.06 ? 'text-emerald-800 font-bold' : 'text-slate-900' }}
      ];"""

assert old_comp_multiples in c_code, "Failed to find old_comp_multiples"
c_code = c_code.replace(old_comp_multiples, new_comp_multiples, 1)

# In Peer comparison table header
old_peer_th = """                <th class="py-3 px-2 text-right">ROIC/ROE</th>"""
new_peer_th = """                <th class="py-3 px-2 text-right">ROIC</th>
                <th class="py-3 px-2 text-right">ROE</th>"""
assert old_peer_th in c_code, "Failed to find old_peer_th"
c_code = c_code.replace(old_peer_th, new_peer_th, 1)

# In Peer comparison table rows
old_peer_td = """          <td class="py-3 px-2 text-right font-semibold ${{s.roic || s.roe >= 0.15 ? 'text-emerald-800 font-bold' : 'text-slate-700'}}">${{formatPercent(s.roic || s.roe)}}</td>"""
new_peer_td = """          <td class="py-3 px-2 text-right font-semibold ${{!s.is_financial && s.roic >= 0.15 ? 'text-emerald-800 font-bold' : 'text-slate-700'}}">${{s.is_financial ? 'N/A' : formatPercent(s.roic)}}</td>
          <td class="py-3 px-2 text-right font-semibold ${{s.roe >= 0.15 ? 'text-emerald-800 font-bold' : 'text-slate-700'}}">${{formatPercent(s.roe)}}</td>"""
assert old_peer_td in c_code, "Failed to find old_peer_td"
c_code = c_code.replace(old_peer_td, new_peer_td, 1)

with open('build_company_page.py', 'w', encoding='utf-8') as f:
    f.write(c_code)

print("build_company_page.py successfully updated with ROIC and ROE separation!")
