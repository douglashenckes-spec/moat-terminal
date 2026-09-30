"""
apply_matrix_and_table_fixes.py
================================
1. Corrige o comportamento dos filtros da Matriz 2x2 para que NUNCA redirecionem para outra pagina.
   Permite filtrar por quadrante e por categorias mantendo o investidor dentro da Matriz.
   Atualiza a barra de filtros da matriz com: Todos, Acima da Curva (Desconto), Abaixo da Curva (Premio),
   Tier 1, Caixa Liquido, Lucro Acelerando, Dividendos e contador de bolhas plotadas.
2. Compacta a Tabela do Scanner B3 (reduz padding de py-2.5 px-3 para py-1.5 px-2,
   logo de w-7 h-7 para w-5 h-5, fontes e espacamentos ajustados para alta densidade institucional).
"""

with open("build_standalone_html.py", "r", encoding="utf-8") as f:
    code = f.read()

# -------------------------------------------------------------
# 1. ATUALIZAR SUB-BARRA DE FILTROS DA MATRIZ 2X2
# -------------------------------------------------------------
old_matrix_subbar = """      <!-- Sub-Barra Ultra-Compacta: Filtros da Curva de Mercado & Legenda Dinâmica -->
      <div class="px-3 py-1.5 border-b border-slate-200 flex flex-wrap items-center justify-between gap-2 bg-slate-50 flex-shrink-0 text-xs font-mono">
        <div class="flex items-center gap-2 flex-wrap">
          <span class="text-[10px] text-slate-600 uppercase font-bold tracking-wider mr-1">Filtros:</span>
          
          <button onclick="filterByQuadrant('ABOVE')" class="inline-flex items-center gap-1.5 px-3 py-0.5 rounded-full glass-pill border-emerald-300 bg-emerald-50 hover:bg-emerald-100 text-emerald-900 font-semibold transition cursor-pointer" title="Filtrar Ativos Acima da Curva (Desconto Relativo)">
            <svg class="w-3.5 h-3.5 stroke-[1.75] text-emerald-700" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/></svg>
            <span>Acima da Curva (Desconto)</span>
            <span class="bg-emerald-200 px-1.5 py-0.2 rounded-full text-[10px] font-bold text-emerald-950" id="stat-above">--</span>
          </button>

          <button onclick="filterByQuadrant('BELOW')" class="inline-flex items-center gap-1.5 px-3 py-0.5 rounded-full glass-pill border-amber-300 bg-amber-50 hover:bg-amber-100 text-amber-900 font-semibold transition cursor-pointer" title="Filtrar Ativos Abaixo da Curva (Prêmio Exigente)">
            <svg class="w-3.5 h-3.5 stroke-[1.75] text-amber-700" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M13 17h8m0 0V9m0 8l-8-8-4 4-6-6"/></svg>
            <span>Abaixo da Curva (Prêmio)</span>
            <span class="bg-amber-200 px-1.5 py-0.2 rounded-full text-[10px] font-bold text-amber-950" id="stat-below">--</span>
          </button>

          <button onclick="filterByCategory('CAT_EXPANSION')" class="inline-flex items-center gap-1.5 px-3 py-0.5 rounded-full glass-pill border-teal-300 bg-teal-50 hover:bg-teal-100 text-teal-900 font-semibold transition cursor-pointer" title="Filtrar Lucro em Expansão 2T26">
            <svg class="w-3.5 h-3.5 stroke-[1.75] text-teal-700" fill="none" stroke="currentColor" viewBox="0 0 24 24"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
            <span>Lucro Acelerando</span>
            <span class="bg-teal-200 px-1.5 py-0.2 rounded-full text-[10px] font-bold text-teal-950" id="stat-expansion">--</span>
          </button>

          <button onclick="filterByCategory('CAT_DIVIDENDS')" class="inline-flex items-center gap-1.5 px-3 py-0.5 rounded-full glass-pill border-cyan-300 bg-cyan-50 hover:bg-cyan-100 text-cyan-900 font-semibold transition cursor-pointer" title="Filtrar Dividendos Consistentes (Dividend Yield &gt; 5%)">
            <svg class="w-3.5 h-3.5 stroke-[1.75] text-cyan-700" fill="none" stroke="currentColor" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path stroke-linecap="round" stroke-linejoin="round" d="M12 7v10m-3-7.5a2.5 2.5 0 015 0c0 2-3 2-3 4h3"/></svg>
            <span>Dividendos &gt; 5%</span>
            <span class="bg-cyan-200 px-1.5 py-0.2 rounded-full text-[10px] font-bold text-cyan-950" id="stat-dividends">--</span>
          </button>
        </div>

        <div class="text-[10px] text-slate-700 font-mono hidden lg:flex items-center gap-2" id="matrixLegendContainer">
          <!-- Legenda dinâmica inserida via JS -->
        </div>

        <div class="text-[10px] text-slate-400 font-sans hidden md:inline">
          💡 Role o mouse para Zoom • Arraste para Pan • Clique em uma bolha para ver no Dossiê
        </div>
      </div>"""

new_matrix_subbar = """      <!-- Sub-Barra Ultra-Compacta: Filtros da Curva de Mercado & Legenda Dinâmica -->
      <div class="px-3 py-1.5 border-b border-slate-200 flex flex-wrap items-center justify-between gap-2 bg-slate-50 flex-shrink-0 text-xs font-mono">
        <div class="flex items-center gap-1.5 flex-wrap">
          <span class="text-[10px] text-slate-500 uppercase font-bold tracking-wider mr-1">Filtros da Matriz:</span>
          
          <button id="btn-mat-ALL" onclick="setMatrixFilter('ALL')" class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full border border-slate-300 bg-white hover:bg-slate-100 text-slate-800 text-[11px] font-semibold transition cursor-pointer" title="Ver todos os ativos">
            <span>Todos</span>
            <span class="bg-slate-100 text-slate-700 px-1.5 py-0.2 rounded-full text-[10px] font-bold" id="stat-mat-all">--</span>
          </button>

          <button id="btn-mat-QUAD_ABOVE" onclick="setMatrixFilter('QUAD_ABOVE')" class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full border border-emerald-300 bg-emerald-50 hover:bg-emerald-100 text-emerald-900 text-[11px] font-semibold transition cursor-pointer" title="Filtrar Ativos Acima da Curva (Desconto Relativo)">
            <svg class="w-3.5 h-3.5 stroke-[1.75] text-emerald-700" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/></svg>
            <span>Acima da Curva (Desconto)</span>
            <span class="bg-emerald-200 px-1.5 py-0.2 rounded-full text-[10px] font-bold text-emerald-950" id="stat-above">--</span>
          </button>

          <button id="btn-mat-QUAD_BELOW" onclick="setMatrixFilter('QUAD_BELOW')" class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full border border-amber-300 bg-amber-50 hover:bg-amber-100 text-amber-900 text-[11px] font-semibold transition cursor-pointer" title="Filtrar Ativos Abaixo da Curva (Prêmio Exigente)">
            <svg class="w-3.5 h-3.5 stroke-[1.75] text-amber-700" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M13 17h8m0 0V9m0 8l-8-8-4 4-6-6"/></svg>
            <span>Abaixo da Curva (Prêmio)</span>
            <span class="bg-amber-200 px-1.5 py-0.2 rounded-full text-[10px] font-bold text-amber-950" id="stat-below">--</span>
          </button>

          <button id="btn-mat-CAT_TIER1" onclick="setMatrixFilter('CAT_TIER1')" class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full border border-emerald-300 bg-emerald-50 hover:bg-emerald-100 text-emerald-900 text-[11px] font-semibold transition cursor-pointer" title="Filtrar Líderes Tier 1">
            <span>🏆</span>
            <span>Tier 1</span>
            <span class="bg-emerald-200 px-1.5 py-0.2 rounded-full text-[10px] font-bold text-emerald-950" id="stat-mat-tier1">--</span>
          </button>

          <button id="btn-mat-CAT_NET_CASH" onclick="setMatrixFilter('CAT_NET_CASH')" class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full border border-emerald-300 bg-emerald-50 hover:bg-emerald-100 text-emerald-900 text-[11px] font-semibold transition cursor-pointer" title="Filtrar Balanço com Caixa Líquido">
            <span>🛡️</span>
            <span>Caixa Líquido</span>
            <span class="bg-emerald-200 px-1.5 py-0.2 rounded-full text-[10px] font-bold text-emerald-950" id="stat-mat-cash">--</span>
          </button>

          <button id="btn-mat-CAT_EXPANSION" onclick="setMatrixFilter('CAT_EXPANSION')" class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full border border-teal-300 bg-teal-50 hover:bg-teal-100 text-teal-900 text-[11px] font-semibold transition cursor-pointer" title="Filtrar Lucro em Expansão 2T26">
            <svg class="w-3.5 h-3.5 stroke-[1.75] text-teal-700" fill="none" stroke="currentColor" viewBox="0 0 24 24"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
            <span>Lucro Acelerando</span>
            <span class="bg-teal-200 px-1.5 py-0.2 rounded-full text-[10px] font-bold text-teal-950" id="stat-expansion">--</span>
          </button>

          <button id="btn-mat-CAT_DIVIDENDS" onclick="setMatrixFilter('CAT_DIVIDENDS')" class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full border border-cyan-300 bg-cyan-50 hover:bg-cyan-100 text-cyan-900 text-[11px] font-semibold transition cursor-pointer" title="Filtrar Dividendos Consistentes (Dividend Yield &gt; 5%)">
            <svg class="w-3.5 h-3.5 stroke-[1.75] text-cyan-700" fill="none" stroke="currentColor" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path stroke-linecap="round" stroke-linejoin="round" d="M12 7v10m-3-7.5a2.5 2.5 0 015 0c0 2-3 2-3 4h3"/></svg>
            <span>Dividendos &gt; 5%</span>
            <span class="bg-cyan-200 px-1.5 py-0.2 rounded-full text-[10px] font-bold text-cyan-950" id="stat-dividends">--</span>
          </button>
        </div>

        <div class="text-[10px] text-slate-700 font-mono hidden lg:flex items-center gap-2" id="matrixLegendContainer">
          <!-- Legenda dinâmica inserida via JS -->
        </div>

        <div class="text-[10px] text-slate-500 font-mono flex items-center gap-1.5 bg-slate-100 px-2.5 py-0.5 rounded-full border border-slate-200">
          <span>Plotados:</span> <b class="text-emerald-700 font-bold" id="matrixPlotCount">--</b>
        </div>
      </div>"""

if old_matrix_subbar in code:
    code = code.replace(old_matrix_subbar, new_matrix_subbar)
    print("[OK] Sub-barra da Matriz 2x2 atualizada com sucesso!")
else:
    print("! Aviso: old_matrix_subbar nao encontrada exatamente.")

# -------------------------------------------------------------
# 2. ATUALIZAR FUNÇÕES DE FILTRO DA MATRIZ NO JAVASCRIPT
# -------------------------------------------------------------
old_filter_quad = """    function filterByQuadrant(q) {{
      if (q === 'ABOVE' || q === 'FILE' || q === 'BARGAIN') {{
        setFilter('QUAD_ABOVE');
      }} else if (q === 'BELOW' || q === 'EXPENSIVE' || q === 'TRAP') {{
        setFilter('QUAD_BELOW');
      }} else {{
        setFilter('ALL');
      }}
      switchWorkspace('table');
    }}

    function filterByCategory(cat) {{
      setFilter(cat);
      switchWorkspace('table');
    }}"""

new_filter_quad = """    function setMatrixFilter(f) {{
      if (currentFilter === f) {{
        currentFilter = 'ALL';
      }} else {{
        currentFilter = f;
      }}
      renderMatrix();
      updateMatrixFilterButtons();
      updateFilterCounts();
    }}

    function updateMatrixFilterButtons() {{
      const btnKeys = ['ALL', 'QUAD_ABOVE', 'QUAD_BELOW', 'CAT_TIER1', 'CAT_NET_CASH', 'CAT_EXPANSION', 'CAT_DIVIDENDS'];
      btnKeys.forEach(k => {{
        const btn = document.getElementById('btn-mat-' + k);
        if (btn) {{
          if (currentFilter === k || (k === 'ALL' && currentFilter === 'ALL')) {{
            btn.classList.add('ring-2', 'ring-emerald-600', 'font-bold', 'bg-emerald-100/90');
          }} else {{
            btn.classList.remove('ring-2', 'ring-emerald-600', 'font-bold', 'bg-emerald-100/90');
          }}
        }}
      }});
    }}

    function filterByQuadrant(q) {{
      let target = 'ALL';
      if (q === 'ABOVE' || q === 'FILE' || q === 'BARGAIN') {{
        target = 'QUAD_ABOVE';
      }} else if (q === 'BELOW' || q === 'EXPENSIVE' || q === 'TRAP') {{
        target = 'QUAD_BELOW';
      }}
      if (currentWorkspace === 'matrix') {{
        setMatrixFilter(target);
      }} else {{
        setFilter(target);
        switchWorkspace('table');
      }}
    }}

    function filterByCategory(cat) {{
      if (currentWorkspace === 'matrix') {{
        setMatrixFilter(cat);
      }} else {{
        setFilter(cat);
        switchWorkspace('table');
      }}
    }}"""

if old_filter_quad in code:
    code = code.replace(old_filter_quad, new_filter_quad)
    print("[OK] Funcoes setMatrixFilter e filterByQuadrant atualizadas!")
else:
    print("! Aviso: old_filter_quad nao encontrada exatamente.")

# -------------------------------------------------------------
# 3. ATUALIZAR CONTADORES DA MATRIZ EM updateFilterCounts
# -------------------------------------------------------------
old_mat_counts = """      const elAbove = document.getElementById('stat-above');
      if (elAbove) elAbove.innerText = cntAbove;
      const elBelow = document.getElementById('stat-below');
      if (elBelow) elBelow.innerText = cntBelow;
      const elExp = document.getElementById('stat-expansion');
      if (elExp) elExp.innerText = cntExpansion;
      const elDivs = document.getElementById('stat-dividends');
      if (elDivs) elDivs.innerText = cntDivs;"""

new_mat_counts = """      const elAbove = document.getElementById('stat-above');
      if (elAbove) elAbove.innerText = cntAbove;
      const elBelow = document.getElementById('stat-below');
      if (elBelow) elBelow.innerText = cntBelow;
      const elExp = document.getElementById('stat-expansion');
      if (elExp) elExp.innerText = cntExpansion;
      const elDivs = document.getElementById('stat-dividends');
      if (elDivs) elDivs.innerText = cntDivs;

      const elMatAll = document.getElementById('stat-mat-all');
      if (elMatAll) elMatAll.innerText = basePool.length;
      const elMatT1 = document.getElementById('stat-mat-tier1');
      if (elMatT1) elMatT1.innerText = cntT1;
      const elMatCash = document.getElementById('stat-mat-cash');
      if (elMatCash) elMatCash.innerText = cntCash;

      const elPlotCount = document.getElementById('matrixPlotCount');
      if (elPlotCount) {{
        const plotted = getFilteredStocks().filter(s => s.pl !== null && s.pl > 0 && s.pl <= 35.0).length;
        elPlotCount.innerText = `${{plotted}} / ${{basePool.length}}`;
      }}
      if (typeof updateMatrixFilterButtons === 'function') {{
        updateMatrixFilterButtons();
      }}"""

if old_mat_counts in code:
    code = code.replace(old_mat_counts, new_mat_counts)
    print("[OK] Contadores da Matriz 2x2 atualizados em updateFilterCounts!")
else:
    print("! Aviso: old_mat_counts nao encontrada.")

# -------------------------------------------------------------
# 4. ATUALIZAR PRESETS DO SCANNER TOOLBAR (COM NOVAS CATEGORIAS)
# -------------------------------------------------------------
old_scanner_presets = """          <!-- Presets Munger -->
          <div class="inline-flex bg-slate-100 border border-slate-200 rounded-full p-1 gap-1">
            <button onclick="setFilter('ALL')" id="flt-ALL" class="filter-btn active rounded-full px-3 py-1 text-xs font-mono font-medium hover:text-slate-900">Todos (<span id="cnt-ALL">--</span>)</button>
            <button onclick="setFilter('CAT_ULTRA_CRITIC')" id="flt-CAT_ULTRA_CRITIC" class="filter-btn rounded-full px-3 py-1 text-xs font-mono font-bold hover:text-slate-900 text-amber-800">💎 Máxima Solvência (<span id="cnt-CAT_ULTRA_CRITIC">--</span>)</button>
            <button onclick="setFilter('TIER1')" id="flt-TIER1" class="filter-btn rounded-full px-3 py-1 text-xs font-mono font-bold hover:text-slate-900 text-amber-800">Tier 1 (<span id="cnt-TIER1">--</span>)</button>
            <button onclick="setFilter('ASYMMETRY')" id="flt-ASYMMETRY" class="filter-btn rounded-full px-3 py-1 text-xs font-mono font-bold hover:text-slate-900 text-emerald-800">Assimetria (<span id="cnt-ASYMMETRY">--</span>)</button>
            <button onclick="setFilter('NTNB')" id="flt-NTNB" class="filter-btn rounded-full px-3 py-1 text-xs font-mono font-bold hover:text-slate-900 text-sky-800">Spread NTN-B (<span id="cnt-NTNB">--</span>)</button>
            <button onclick="setFilter('NET_CASH')" id="flt-NET_CASH" class="filter-btn rounded-full px-3 py-1 text-xs font-mono font-bold hover:text-slate-900 text-indigo-800">Caixa Líq (<span id="cnt-NET_CASH">--</span>)</button>
          </div>"""

new_scanner_presets = """          <!-- Presets de Categorias e Fatores B3 -->
          <div class="inline-flex bg-slate-100 border border-slate-200 rounded-full p-0.5 gap-1">
            <button onclick="setFilter('ALL')" id="flt-ALL" class="filter-btn active rounded-full px-2.5 py-0.5 text-xs font-mono font-medium hover:text-slate-900">Todos (<span id="cnt-ALL">--</span>)</button>
            <button onclick="setFilter('CAT_TIER1')" id="flt-CAT_TIER1" class="filter-btn rounded-full px-2.5 py-0.5 text-xs font-mono font-bold hover:text-slate-900 text-amber-800">🏆 Tier 1 (<span id="cnt-TIER1">--</span>)</button>
            <button onclick="setFilter('CAT_NET_CASH')" id="flt-CAT_NET_CASH" class="filter-btn rounded-full px-2.5 py-0.5 text-xs font-mono font-bold hover:text-slate-900 text-emerald-800">🛡️ Caixa Líq (<span id="cnt-NET_CASH">--</span>)</button>
            <button onclick="setFilter('CAT_EXPANSION')" id="flt-CAT_EXPANSION" class="filter-btn rounded-full px-2.5 py-0.5 text-xs font-mono font-bold hover:text-slate-900 text-emerald-800">🟢 Expansão (<span id="sb-cnt-exp">--</span>)</button>
            <button onclick="setFilter('CAT_DIVIDENDS')" id="flt-CAT_DIVIDENDS" class="filter-btn rounded-full px-2.5 py-0.5 text-xs font-mono font-bold hover:text-slate-900 text-teal-800">💰 Dividendos (<span id="sb-cnt-div">--</span>)</button>
            <button onclick="setFilter('CAT_GRAHAM')" id="flt-CAT_GRAHAM" class="filter-btn rounded-full px-2.5 py-0.5 text-xs font-mono font-bold hover:text-slate-900 text-sky-800">📐 Graham (<span id="sb-cnt-graham">--</span>)</button>
            <button onclick="setFilter('CAT_SPREAD_NTNB')" id="flt-CAT_SPREAD_NTNB" class="filter-btn rounded-full px-2.5 py-0.5 text-xs font-mono font-bold hover:text-slate-900 text-indigo-800">📈 Spread NTN-B (<span id="sb-cnt-spread">--</span>)</button>
          </div>"""

if old_scanner_presets in code:
    code = code.replace(old_scanner_presets, new_scanner_presets)
    print("[OK] Presets do Scanner atualizados para novas categorias!")
else:
    print("! Aviso: old_scanner_presets nao encontrado.")

# -------------------------------------------------------------
# 5. COMPACTAR CABEÇALHO DA TABELA DO SCANNER
# -------------------------------------------------------------
old_scanner_thead = """            <thead class="sticky top-0 bg-slate-100 z-10 border-b border-slate-200 shadow-xs">
              <tr class="text-slate-700 text-xs font-bold uppercase tracking-wider select-none">
                <th onclick="sortTable('ticker')" class="py-3 px-3.5 cursor-pointer hover:text-emerald-700" title="Ticker e Nome da Empresa">Ativo ⬍</th>
                <th onclick="sortTable('cotacao')" class="py-3 px-3 cursor-pointer hover:text-emerald-700 text-right" title="Cotação Atual">Cotação ⬍</th>
                <th onclick="sortTable('quality_score')" class="py-3 px-3 cursor-pointer hover:text-emerald-700 text-center" title="Score de Qualidade Fundamentalista (0 a 100)">Score ⬍</th>
                <th onclick="sortTable('ey_spread')" class="py-3 px-3 cursor-pointer hover:text-emerald-700 text-right" title="Prêmio Real sobre NTN-B 6,50%">Spread NTN-B ⬍</th>
                <th onclick="sortTable('pl')" class="py-3 px-3 cursor-pointer hover:text-emerald-700 text-right" title="P/L LTM e P/L Run-Rate Anualizado (2T26)">P/L &amp; Run-Rate ⬍</th>
                <th onclick="sortTable('ev_ebitda')" class="py-3 px-3 cursor-pointer hover:text-emerald-700 text-right" title="Valor da Firma sobre EBITDA">EV / EBITDA ⬍</th>
                <th onclick="sortTable('roic')" class="py-3 px-3 cursor-pointer hover:text-emerald-700 text-right" title="Retorno sobre Capital Empregado (ROIC / ROE)">ROIC / ROE ⬍</th>
                <th onclick="sortTable('mrg_liq')" class="py-3 px-3 cursor-pointer hover:text-emerald-700 text-right" title="Margem Líquida">Margem Líq. ⬍</th>
                <th onclick="sortTable('div_liq_ebitda')" class="py-3 px-3 cursor-pointer hover:text-emerald-700 text-right" title="Dívida Líquida / EBITDA">Dív. / EBITDA ⬍</th>
                <th onclick="sortTable('div_yield')" class="py-3 px-3 cursor-pointer hover:text-emerald-700 text-right" title="Dividend Yield e Payout">DY &amp; Payout ⬍</th>
              </tr>
            </thead>"""

new_scanner_thead = """            <thead class="sticky top-0 bg-slate-100/95 backdrop-blur-sm z-10 border-b border-slate-200 shadow-2xs">
              <tr class="text-slate-600 text-[11px] font-bold uppercase tracking-wider select-none">
                <th onclick="sortTable('ticker')" class="py-2 px-2.5 cursor-pointer hover:text-emerald-700" title="Ticker e Nome da Empresa">Ativo ⬍</th>
                <th onclick="sortTable('cotacao')" class="py-2 px-2 cursor-pointer hover:text-emerald-700 text-right" title="Cotação Atual">Cotação ⬍</th>
                <th onclick="sortTable('quality_score')" class="py-2 px-1.5 cursor-pointer hover:text-emerald-700 text-center" title="Score de Qualidade Fundamentalista (0 a 100)">Score ⬍</th>
                <th onclick="sortTable('ey_spread')" class="py-2 px-2 cursor-pointer hover:text-emerald-700 text-right" title="Prêmio Real sobre NTN-B 6,50%">Spread NTN-B ⬍</th>
                <th onclick="sortTable('pl')" class="py-2 px-2 cursor-pointer hover:text-emerald-700 text-right" title="P/L LTM e P/L Run-Rate Anualizado (2T26)">P/L &amp; Run-Rate ⬍</th>
                <th onclick="sortTable('ev_ebitda')" class="py-2 px-2 cursor-pointer hover:text-emerald-700 text-right" title="Valor da Firma sobre EBITDA">EV / EBITDA ⬍</th>
                <th onclick="sortTable('roic')" class="py-2 px-2 cursor-pointer hover:text-emerald-700 text-right" title="Retorno sobre Capital Empregado (ROIC / ROE)">ROIC / ROE ⬍</th>
                <th onclick="sortTable('mrg_liq')" class="py-2 px-2 cursor-pointer hover:text-emerald-700 text-right" title="Margem Líquida">Margem Líq. ⬍</th>
                <th onclick="sortTable('div_liq_ebitda')" class="py-2 px-2 cursor-pointer hover:text-emerald-700 text-right" title="Dívida Líquida / EBITDA">Dív. / EBITDA ⬍</th>
                <th onclick="sortTable('div_yield')" class="py-2 px-2.5 cursor-pointer hover:text-emerald-700 text-right" title="Dividend Yield e Payout">DY &amp; Payout ⬍</th>
              </tr>
            </thead>"""

if old_scanner_thead in code:
    code = code.replace(old_scanner_thead, new_scanner_thead)
    print("[OK] thead do Scanner compactado!")
else:
    print("! Aviso: old_scanner_thead nao encontrado.")

# -------------------------------------------------------------
# 6. COMPACTAR LINHAS DA TABELA EM renderTable()
# -------------------------------------------------------------
old_render_row = """        tr.innerHTML = `
          <td class="py-2.5 px-3">
            <div class="flex items-center gap-2.5">
              ${{getStockLogoHtml(s.ticker, s.empresa, 'w-7 h-7')}}
              <div class="flex flex-col min-w-0">
                <div class="flex items-center gap-1.5">
                  <span class="text-sm font-bold text-slate-900 tracking-wide font-mono">${{s.ticker}}</span>
                  ${{s.is_distorted ? '<span class="text-[9px] px-2 py-0.2 rounded-full bg-amber-100 text-amber-900 border border-amber-300 font-semibold" title="' + (s.distortion_label || 'Distorção Contábil') + '">Dist.</span>' : ''}}
                </div>
                <div class="text-[11px] text-slate-600 font-sans font-medium truncate max-w-[160px]" title="${{s.empresa}} - ${{s.setor || ''}}">${{s.empresa}}</div>
              </div>
            </div>
          </td>
          <td class="py-2.5 px-3 text-xs text-right font-bold text-slate-900 font-mono">${{formatCurrency(s.cotacao)}}</td>
          <td class="py-2.5 px-3 text-center">
            <span class="px-2.5 py-0.5 rounded-full font-bold text-xs ${{scoreBadgeClass}}" title="${{s.entry_tag || s.quality_tag || ''}}">
              ${{s.quality_score.toFixed(1)}}
            </span>
          </td>
          <td class="py-2.5 px-3 text-xs text-right font-bold ${{spreadColor}} font-mono" title="Earnings Yield: ${{s.earnings_yield_pct !== null ? s.earnings_yield_pct.toFixed(1) + '%' : 'N/D'}}">${{spreadStr}}</td>
          <td class="py-2.5 px-3 text-right font-mono">
            <div class="text-xs font-semibold ${{plColor}}">${{formatMultiple(s.pl)}}</div>
            <div class="text-[10px] ${{rrColor}}" title="P/L Run-rate anualizado do 2T26">${{rrStr}}</div>
          </td>
          <td class="py-2.5 px-3 text-xs text-right font-medium text-slate-800 font-mono font-semibold">${{s.is_financial ? 'N/A' : (s.ev_ebitda !== null ? formatMultiple(s.ev_ebitda) : 'N/D')}}</td>
          <td class="py-2.5 px-3 text-xs text-right font-semibold ${{roicColor}} font-mono">${{formatPercent(roicVal)}}${{s.is_financial ? ' <span class=\"text-[10px] text-indigo-800 font-normal\">(ROE)</span>' : ''}}</td>
          <td class="py-2.5 px-3 text-xs text-right font-medium ${{mrgColor}} font-mono">${{formatPercent(s.mrg_liq)}}</td>
          <td class="py-2.5 px-3 text-xs text-right font-medium font-mono ${{debtClass}}">${{debtDisplay}}</td>
          <td class="py-2.5 px-3 text-right font-mono">
            <div class="text-xs font-bold ${{dyColor}}">${{formatPercent(s.div_yield)}}</div>
            <div class="text-[10px] ${{payoutColor}}" title="Payout Implícito (% do Lucro Pago em Proventos)">${{payoutStr}}</div>
          </td>
        `;"""

new_render_row = """        // Versão Compacta de Alta Densidade Institucional (Bloomberg Style)
        let debtCompact = debtDisplay;
        if (s.is_financial) {
          debtCompact = '<span class="text-[10px] text-indigo-800 font-medium">Bancos</span>';
        } else if (debtDisplay.includes('Caixa Líq')) {
          debtCompact = '<span class="px-1.5 py-0.2 rounded-full text-[9px] font-bold bg-emerald-50 text-emerald-800 border border-emerald-200">Caixa Líq. 🛡️</span>';
        }

        tr.innerHTML = `
          <td class="py-1.5 px-2.5 border-b border-slate-100">
            <div class="flex items-center gap-2">
              ${{getStockLogoHtml(s.ticker, s.empresa, 'w-5 h-5')}}
              <div class="flex flex-col min-w-0">
                <div class="flex items-center gap-1.5 leading-none">
                  <span class="text-xs font-bold text-slate-900 tracking-wide font-mono">${{s.ticker}}</span>
                  ${{s.is_distorted ? '<span class="text-[8px] px-1.5 py-0.2 rounded-full bg-amber-100 text-amber-900 border border-amber-300 font-semibold" title="' + (s.distortion_label || 'Distorção Contábil') + '">Dist.</span>' : ''}}
                </div>
                <div class="text-[10px] text-slate-500 font-sans font-medium truncate max-w-[130px] leading-tight mt-0.5" title="${{s.empresa}} - ${{s.setor || ''}}">${{s.empresa}}</div>
              </div>
            </div>
          </td>
          <td class="py-1.5 px-2 text-xs text-right font-bold text-slate-900 font-mono border-b border-slate-100">${{formatCurrency(s.cotacao)}}</td>
          <td class="py-1.5 px-1.5 text-center border-b border-slate-100">
            <span class="px-2 py-0.5 rounded-full font-bold text-[11px] ${{scoreBadgeClass}}" title="${{s.entry_tag || s.quality_tag || ''}}">
              ${{s.quality_score.toFixed(1)}}
            </span>
          </td>
          <td class="py-1.5 px-2 text-xs text-right font-bold ${{spreadColor}} font-mono border-b border-slate-100" title="Earnings Yield: ${{s.earnings_yield_pct !== null ? s.earnings_yield_pct.toFixed(1) + '%' : 'N/D'}}">${{spreadStr}}</td>
          <td class="py-1.5 px-2 text-right font-mono border-b border-slate-100">
            <div class="text-xs font-semibold ${{plColor}} leading-tight">${{formatMultiple(s.pl)}}</div>
            <div class="text-[9px] ${{rrColor}} leading-none mt-0.5" title="P/L Run-rate anualizado do 2T26">${{rrStr}}</div>
          </td>
          <td class="py-1.5 px-2 text-xs text-right font-medium text-slate-700 font-mono border-b border-slate-100">${{s.is_financial ? 'N/A' : (s.ev_ebitda !== null ? formatMultiple(s.ev_ebitda) : 'N/D')}}</td>
          <td class="py-1.5 px-2 text-xs text-right font-semibold ${{roicColor}} font-mono border-b border-slate-100">${{formatPercent(roicVal)}}${{s.is_financial ? ' <span class=\"text-[9px] text-indigo-800 font-normal\">(ROE)</span>' : ''}}</td>
          <td class="py-1.5 px-2 text-xs text-right font-medium ${{mrgColor}} font-mono border-b border-slate-100">${{formatPercent(s.mrg_liq)}}</td>
          <td class="py-1.5 px-2 text-xs text-right font-medium font-mono ${{debtClass}} border-b border-slate-100">${{debtCompact}}</td>
          <td class="py-1.5 px-2.5 text-right font-mono border-b border-slate-100">
            <div class="text-xs font-bold ${{dyColor}} leading-tight">${{formatPercent(s.div_yield)}}</div>
            <div class="text-[9px] ${{payoutColor}} leading-none mt-0.5" title="Payout Implícito (% do Lucro Pago em Proventos)">${{payoutStr}}</div>
          </td>
        `;"""

if old_render_row in code:
    code = code.replace(old_render_row, new_render_row)
    print("[OK] Linhas da tabela do Scanner compactadas com sucesso!")
else:
    print("! Aviso: old_render_row nao encontrado.")

with open("build_standalone_html.py", "w", encoding="utf-8") as f:
    f.write(code)

print("\nbuild_standalone_html.py atualizado.")
