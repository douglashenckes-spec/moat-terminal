with open('build_standalone_html.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Panorama Geral cards
old_pane_home_cards = """          <!-- Radar de Virada de Ciclo -->
          <div class="glass-card rounded-xl flex flex-col overflow-hidden">
            <div class="p-3 border-b border-slate-200 bg-slate-50 flex items-center justify-between">
              <div class="flex items-center gap-1.5">
                <span class="text-base">⚡</span>
                <span class="text-xs font-mono font-bold text-purple-400 uppercase">Radar de Virada de Ciclo (Run-Rate 2T26)</span>
              </div>
              <span class="text-[10px] font-mono text-purple-300 bg-purple-500/10 border border-purple-500/30 px-2 py-0.5 rounded-full">Lucro 2T26 x 4 vs LTM</span>
            </div>
            <div class="p-3 grid grid-cols-1 sm:grid-cols-2 gap-2.5 text-xs font-mono">
              <div>
                <div class="text-[11px] font-bold text-emerald-800 mb-1.5 flex items-center justify-between">
                  <span class="flex items-center gap-1"><span>🟢</span> Lucro em Expansão</span>
                  <button onclick="filterByCategory('CAT_EXPANSION')" id="btn-cat-accel" class="text-[9px] font-mono font-bold text-emerald-300 hover:text-slate-900 glass-pill border-emerald-500/30 px-2 py-0.5 rounded-full transition cursor-pointer" title="Ver todas as empresas com Lucro em Expansão">
                    <span>Todas</span> <span id="cnt-cat-accel">(--)</span> <span>➜</span>
                  </button>
                </div>
                <div class="space-y-1.5" id="home-list-accelerating">
                  <!-- Renderizado via JS -->
                </div>
              </div>
              <div>
                <div class="text-[11px] font-bold text-amber-800 mb-1.5 flex items-center justify-between">
                  <span class="flex items-center gap-1"><span>⚠️</span> Alerta de Compressão</span>
                  <button onclick="filterByCategory('CAT_DECELERATION')" id="btn-cat-decel" class="text-[9px] font-mono font-bold text-amber-300 hover:text-slate-900 glass-pill border-amber-500/30 px-2 py-0.5 rounded-full transition cursor-pointer" title="Ver todas as empresas com Alerta de Compressão">
                    <span>Todas</span> <span id="cnt-cat-decel">(--)</span> <span>➜</span>
                  </button>
                </div>
                <div class="space-y-1.5" id="home-list-decelerating">
                  <!-- Renderizado via JS -->
                </div>
              </div>
            </div>
          </div>

          <!-- Solvência & Anti-Fragilidade -->
          <div class="glass-card rounded-xl flex flex-col overflow-hidden">
            <div class="p-3 border-b border-slate-200 bg-slate-50 flex items-center justify-between">
              <div class="flex items-center gap-1.5">
                <span class="text-base">🛡️</span>
                <span class="text-xs font-mono font-bold text-indigo-800 uppercase">Solvência &amp; Anti-Fragilidade (Selic Alta)</span>
              </div>
              <span class="text-[10px] font-mono text-sky-300 bg-sky-500/10 border border-sky-500/30 px-2 py-0.5 rounded-full">Dívida Líq. / EBITDA</span>
            </div>
            <div class="p-3 grid grid-cols-1 sm:grid-cols-2 gap-2.5 text-xs font-mono">
              <div>
                <div class="text-[11px] font-bold text-emerald-800 mb-1.5 flex items-center justify-between">
                  <span class="flex items-center gap-1"><span>🛡️</span> Balanços Fortes</span>
                  <button onclick="filterByCategory('CAT_NET_CASH')" id="btn-cat-netcash" class="text-[9px] font-mono font-bold text-emerald-300 hover:text-slate-900 glass-pill border-emerald-500/30 px-2 py-0.5 rounded-full transition cursor-pointer" title="Ver todas as empresas com Caixa Líquido">
                    <span>Todas</span> <span id="cnt-cat-netcash">(--)</span> <span>➜</span>
                  </button>
                </div>
                <div class="space-y-1.5" id="home-list-netcash">
                  <!-- Renderizado via JS -->
                </div>
              </div>
              <div>
                <div class="text-[11px] font-bold text-rose-400 mb-1.5 flex items-center justify-between">
                  <span class="flex items-center gap-1"><span>🚨</span> Alavancagem Crítica</span>
                  <button onclick="filterByCategory('CAT_HIGH_DEBT')" id="btn-cat-highdebt" class="text-[9px] font-mono font-bold text-rose-300 hover:text-slate-900 glass-pill border-rose-500/30 px-2 py-0.5 rounded-full transition cursor-pointer" title="Ver todas as empresas com Alavancagem Crítica">
                    <span>Todas</span> <span id="cnt-cat-highdebt">(--)</span> <span>➜</span>
                  </button>
                </div>
                <div class="space-y-1.5" id="home-list-highdebt">
                  <!-- Renderizado via JS -->
                </div>
              </div>
            </div>
          </div>"""

new_pane_home_cards = """          <!-- Radar de Virada de Ciclo -->
          <div class="glass-card rounded-xl flex flex-col overflow-hidden border border-slate-200 bg-white">
            <div class="p-3 border-b border-slate-200 bg-slate-50 flex items-center justify-between">
              <div class="flex items-center gap-1.5">
                <span class="text-base">⚡</span>
                <span class="text-xs font-mono font-bold text-purple-900 uppercase">Radar de Virada de Ciclo (Run-Rate 2T26)</span>
              </div>
              <span class="text-[10px] font-mono font-bold text-purple-900 bg-purple-100 border border-purple-300 px-2 py-0.5 rounded-full">Lucro 2T26 x 4 vs LTM</span>
            </div>
            <div class="p-3 grid grid-cols-1 sm:grid-cols-2 gap-2.5 text-xs font-mono">
              <div>
                <div class="text-[11px] font-bold text-emerald-900 mb-1.5 flex items-center justify-between">
                  <span class="flex items-center gap-1"><span>🟢</span> Lucro em Expansão</span>
                  <button onclick="filterByCategory('CAT_EXPANSION')" id="btn-cat-accel" class="text-[9px] font-mono font-bold text-emerald-800 hover:text-slate-900 bg-emerald-50 hover:bg-emerald-100 border border-emerald-300 px-2 py-0.5 rounded-full transition cursor-pointer" title="Ver todas as empresas com Lucro em Expansão">
                    <span>Todas</span> <span id="cnt-cat-accel">(--)</span> <span>➜</span>
                  </button>
                </div>
                <div class="space-y-1.5" id="home-list-accelerating">
                  <!-- Renderizado via JS -->
                </div>
              </div>
              <div>
                <div class="text-[11px] font-bold text-amber-900 mb-1.5 flex items-center justify-between">
                  <span class="flex items-center gap-1"><span>⚠️</span> Alerta de Compressão</span>
                  <button onclick="filterByCategory('CAT_DECELERATION')" id="btn-cat-decel" class="text-[9px] font-mono font-bold text-amber-900 hover:text-slate-900 bg-amber-50 hover:bg-amber-100 border border-amber-300 px-2 py-0.5 rounded-full transition cursor-pointer" title="Ver todas as empresas com Alerta de Compressão">
                    <span>Todas</span> <span id="cnt-cat-decel">(--)</span> <span>➜</span>
                  </button>
                </div>
                <div class="space-y-1.5" id="home-list-decelerating">
                  <!-- Renderizado via JS -->
                </div>
              </div>
            </div>
          </div>

          <!-- Solvência & Anti-Fragilidade -->
          <div class="glass-card rounded-xl flex flex-col overflow-hidden border border-slate-200 bg-white">
            <div class="p-3 border-b border-slate-200 bg-slate-50 flex items-center justify-between">
              <div class="flex items-center gap-1.5">
                <span class="text-base">🛡️</span>
                <span class="text-xs font-mono font-bold text-indigo-900 uppercase">Solvência &amp; Anti-Fragilidade (Selic Alta)</span>
              </div>
              <span class="text-[10px] font-mono font-bold text-sky-900 bg-sky-100 border border-sky-300 px-2 py-0.5 rounded-full">Dívida Líq. / EBITDA</span>
            </div>
            <div class="p-3 grid grid-cols-1 sm:grid-cols-2 gap-2.5 text-xs font-mono">
              <div>
                <div class="text-[11px] font-bold text-emerald-900 mb-1.5 flex items-center justify-between">
                  <span class="flex items-center gap-1"><span>🛡️</span> Balanços Fortes</span>
                  <button onclick="filterByCategory('CAT_NET_CASH')" id="btn-cat-netcash" class="text-[9px] font-mono font-bold text-emerald-800 hover:text-slate-900 bg-emerald-50 hover:bg-emerald-100 border border-emerald-300 px-2 py-0.5 rounded-full transition cursor-pointer" title="Ver todas as empresas com Caixa Líquido">
                    <span>Todas</span> <span id="cnt-cat-netcash">(--)</span> <span>➜</span>
                  </button>
                </div>
                <div class="space-y-1.5" id="home-list-netcash">
                  <!-- Renderizado via JS -->
                </div>
              </div>
              <div>
                <div class="text-[11px] font-bold text-rose-900 mb-1.5 flex items-center justify-between">
                  <span class="flex items-center gap-1"><span>🚨</span> Alavancagem Crítica</span>
                  <button onclick="filterByCategory('CAT_HIGH_DEBT')" id="btn-cat-highdebt" class="text-[9px] font-mono font-bold text-rose-800 hover:text-slate-900 bg-rose-50 hover:bg-rose-100 border border-rose-300 px-2 py-0.5 rounded-full transition cursor-pointer" title="Ver todas as empresas com Alavancagem Crítica">
                    <span>Todas</span> <span id="cnt-cat-highdebt">(--)</span> <span>➜</span>
                  </button>
                </div>
                <div class="space-y-1.5" id="home-list-highdebt">
                  <!-- Renderizado via JS -->
                </div>
              </div>
            </div>
          </div>"""

assert old_pane_home_cards in code, "Failed to find old_pane_home_cards"
code = code.replace(old_pane_home_cards, new_pane_home_cards, 1)

# 2. Matrix Tooltip HTML definition (line 695)
old_tt_def = """<div id="matrixTooltip" class="absolute pointer-events-none hidden bg-slate-900 rounded-xl p-3.5 text-xs text-white shadow-2xl z-50 font-mono border border-slate-700"></div>"""
new_tt_def = """<div id="matrixTooltip" class="absolute pointer-events-none hidden bg-white/95 backdrop-blur-md rounded-xl p-3.5 text-xs text-slate-900 shadow-2xl z-50 font-mono border border-slate-300"></div>"""
assert old_tt_def in code, "Failed to find old_tt_def"
code = code.replace(old_tt_def, new_tt_def, 1)

# 3. Matrix Tooltip JS rendering
old_tt_js = """      let curveBadge = '';
      if (s.entry_tag === 'PASSIVO_DESCOBERTO') {{
        curveBadge = '<span class="px-2 py-0.5 rounded bg-red-950 text-red-300 border border-red-700 font-bold text-[10px]">🛑 Passivo Descoberto</span>';
      }} else if (isAbove) {{
        curveBadge = `<span class="px-2 py-0.5 rounded bg-emerald-950 text-emerald-300 border border-emerald-500 font-bold text-[10px]">📈 Acima da Curva (Desconto ${{Math.abs(deltaPL).toFixed(1)}}x P/L)</span>`;
      }} else {{
        const deltaStr = deltaPL !== null ? `+${{Math.abs(deltaPL).toFixed(1)}}x` : 'N/D';
        curveBadge = `<span class="px-2 py-0.5 rounded bg-amber-950 text-amber-300 border border-amber-500 font-bold text-[10px]">📉 Abaixo da Curva (Prêmio ${{deltaStr}})</span>`;
      }}

      // Tag de Momento
      let momTag = '';
      if (s.run_rate_div_pct !== null && s.run_rate_div_pct !== undefined) {{
        if (s.run_rate_div_pct >= 15.0) momTag = `<span class="text-emerald-700 font-bold">⚡ Lucro Acelerando (+${{s.run_rate_div_pct.toFixed(0)}}%)</span>`;
        else if (s.run_rate_div_pct <= -20.0) momTag = `<span class="text-orange-400 font-bold">⚠️ Lucro Comprimindo (${{s.run_rate_div_pct.toFixed(0)}}%)</span>`;
        else momTag = `<span class="text-slate-300">Estável (${{s.run_rate_div_pct > 0 ? '+' : ''}}${{s.run_rate_div_pct.toFixed(0)}}%)</span>`;
      }}

      let warningBanner = '';
      if (s.is_distorted) {{
        warningBanner = `
          <div class="mt-1.5 p-1.5 bg-purple-950/70 border border-purple-800 rounded text-[10px] text-purple-200">
            ⚠️ <b>Atenção de Valuation:</b> ${{s.distortion_label}}
          </div>
        `;
      }}

      tt.innerHTML = `
        <div class="font-bold text-white text-sm flex items-center justify-between gap-2">
          <span>${{s.ticker}} <span class="font-normal text-slate-400 font-sans text-xs">(${{s.empresa}})</span></span>
          <div class="flex items-center gap-1.5">
            ${{curveBadge}}
            <span class="text-[10px] font-sans px-1.5 py-0.5 rounded bg-slate-800 text-slate-300 font-normal">${{s.setor}}</span>
          </div>
        </div>
        <div class="text-[11px] text-slate-400 font-sans my-1 border-b border-slate-200 pb-1">
          Cap: <b class="text-slate-200">${{mcapStr}}</b> • Vol: <b class="text-slate-200">R$ ${{volStr}}/d</b> • Bal: <b class="text-slate-200">${{s.ult_balanco}}</b>
        </div>
        <div>• Quality Score: <b class="text-white">${{s.quality_score.toFixed(1)}}/100</b> (${{s.quality_tier.split(':')[0]}})</div>
        <div>• P/L (12m): <b>${{formatMultiple(s.pl)}}</b> (Fair Value de Mercado: <b class="text-sky-300">${{expPL.toFixed(1)}}x</b>)</div>
        <div>• Momento 2T26: ${{momTag}}</div>
        <div>• Earnings Yield: <b>${{formatPercent(s.earnings_yield_pct/100)}}</b> (Spread NTN-B: <b>${{spreadStr}}</b>)</div>
        <div>• ROIC: <b>${{formatPercent(s.roic || s.roe)}}</b> | DY: <b>${{formatPercent(s.div_yield)}}</b></div>
        <div class="mt-1 text-[11px] font-sans font-semibold text-emerald-800">${{s.entry_status}}</div>
        ${{warningBanner}}
        <div class="mt-2 pt-1.5 border-t border-slate-200 flex items-center justify-between text-[10px] text-slate-400 font-sans">
          <span>Clique p/ selecionar ativo</span>
          <span class="text-amber-800 font-bold font-mono">Ver Dossiê ➜</span>
        </div>
      `;"""

new_tt_js = """      let curveBadge = '';
      if (s.entry_tag === 'PASSIVO_DESCOBERTO') {{
        curveBadge = '<span class="px-2 py-0.5 rounded bg-rose-100 text-rose-900 border border-rose-300 font-bold text-[10px]">🛑 Passivo Descoberto</span>';
      }} else if (isAbove) {{
        curveBadge = `<span class="px-2 py-0.5 rounded bg-emerald-100 text-emerald-900 border border-emerald-300 font-bold text-[10px]">📈 Acima da Curva (Desconto ${{Math.abs(deltaPL).toFixed(1)}}x P/L)</span>`;
      }} else {{
        const deltaStr = deltaPL !== null ? `+${{Math.abs(deltaPL).toFixed(1)}}x` : 'N/D';
        curveBadge = `<span class="px-2 py-0.5 rounded bg-amber-100 text-amber-900 border border-amber-300 font-bold text-[10px]">📉 Abaixo da Curva (Prêmio ${{deltaStr}})</span>`;
      }}

      // Tag de Momento
      let momTag = '';
      if (s.run_rate_div_pct !== null && s.run_rate_div_pct !== undefined) {{
        if (s.run_rate_div_pct >= 15.0) momTag = `<span class="text-emerald-800 font-bold">⚡ Lucro Acelerando (+${{s.run_rate_div_pct.toFixed(0)}}%)</span>`;
        else if (s.run_rate_div_pct <= -20.0) momTag = `<span class="text-amber-800 font-bold">⚠️ Lucro Comprimindo (${{s.run_rate_div_pct.toFixed(0)}}%)</span>`;
        else momTag = `<span class="text-slate-600 font-medium">Estável (${{s.run_rate_div_pct > 0 ? '+' : ''}}${{s.run_rate_div_pct.toFixed(0)}}%)</span>`;
      }}

      let warningBanner = '';
      if (s.is_distorted) {{
        warningBanner = `
          <div class="mt-1.5 p-1.5 bg-purple-50 border border-purple-200 rounded text-[10px] text-purple-900 font-sans">
            ⚠️ <b>Atenção de Valuation:</b> ${{s.distortion_label}}
          </div>
        `;
      }}

      tt.innerHTML = `
        <div class="font-bold text-slate-900 text-sm flex items-center justify-between gap-2">
          <span>${{s.ticker}} <span class="font-normal text-slate-600 font-sans text-xs">(${{s.empresa}})</span></span>
          <div class="flex items-center gap-1.5">
            ${{curveBadge}}
            <span class="text-[10px] font-sans px-1.5 py-0.5 rounded bg-slate-100 text-slate-700 font-medium border border-slate-200">${{s.setor}}</span>
          </div>
        </div>
        <div class="text-[11px] text-slate-600 font-sans my-1 border-b border-slate-200 pb-1">
          Cap: <b class="text-slate-900 font-bold">${{mcapStr}}</b> • Vol: <b class="text-slate-900 font-bold">R$ ${{volStr}}/d</b> • Bal: <b class="text-slate-800 font-semibold">${{s.ult_balanco}}</b>
        </div>
        <div class="text-slate-700">• Quality Score: <b class="text-slate-900 font-bold">${{s.quality_score.toFixed(1)}}/100</b> (${{s.quality_tier.split(':')[0]}})</div>
        <div class="text-slate-700">• P/L (12m): <b class="text-slate-900 font-bold">${{formatMultiple(s.pl)}}</b> (Fair Value: <b class="text-emerald-800 font-bold">${{expPL.toFixed(1)}}x</b>)</div>
        <div class="text-slate-700">• Momento 2T26: ${{momTag}}</div>
        <div class="text-slate-700">• Earnings Yield: <b class="text-slate-900 font-bold">${{formatPercent(s.earnings_yield_pct/100)}}</b> (Spread NTN-B: <b class="${{getColorSpread(s.ey_spread)}}">${{spreadStr}}</b>)</div>
        <div class="text-slate-700">• ROIC: <b class="text-slate-900 font-bold">${{formatPercent(s.roic || s.roe)}}</b> | DY: <b class="text-emerald-800 font-bold">${{formatPercent(s.div_yield)}}</b></div>
        <div class="mt-1 text-[11px] font-sans font-semibold text-emerald-800">${{s.entry_status}}</div>
        ${{warningBanner}}
        <div class="mt-2 pt-1.5 border-t border-slate-200 flex items-center justify-between text-[10px] text-slate-500 font-sans">
          <span>Clique p/ selecionar ativo</span>
          <span class="text-emerald-700 font-bold font-mono">Ver Dossiê ➜</span>
        </div>
      `;"""

assert old_tt_js in code, "Failed to find old_tt_js"
code = code.replace(old_tt_js, new_tt_js, 1)

# 4. Payout in Drawer
old_payout = """      let payoutColor = 'text-slate-400';
      if (s.payout_implicito !== null) {{
        const pVal = Number(s.payout_implicito);
        if (pVal > 100) payoutColor = 'text-rose-400 font-bold';
        else if (pVal >= 30 && pVal <= 85) payoutColor = 'text-emerald-700 font-bold';
        else if (pVal > 85) payoutColor = 'text-amber-800 font-semibold';
        else payoutColor = 'text-indigo-800 font-semibold';
      }}"""

new_payout = """      let payoutColor = 'text-slate-500';
      if (s.payout_implicito !== null) {{
        const pVal = Number(s.payout_implicito);
        if (pVal > 100) payoutColor = 'text-rose-700 font-bold';
        else if (pVal >= 30 && pVal <= 85) payoutColor = 'text-emerald-700 font-bold';
        else if (pVal > 85) payoutColor = 'text-amber-800 font-semibold';
        else payoutColor = 'text-indigo-800 font-semibold';
      }}"""

assert old_payout in code, "Failed to find old_payout"
code = code.replace(old_payout, new_payout, 1)

# 5. Toast notifications
old_toast = """      if (type === 'success') bg = 'bg-emerald-950/80 border-emerald-800 text-emerald-300';
      if (type === 'error') bg = 'bg-rose-950/80 border-rose-800 text-rose-300';"""

new_toast = """      if (type === 'success') bg = 'bg-emerald-50 border border-emerald-300 text-emerald-900 shadow-lg';
      if (type === 'error') bg = 'bg-rose-50 border border-rose-300 text-rose-900 shadow-lg';"""

assert old_toast in code, "Failed to find old_toast"
code = code.replace(old_toast, new_toast, 1)

with open('build_standalone_html.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Final polish applied successfully!")
