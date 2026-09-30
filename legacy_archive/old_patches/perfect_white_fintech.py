"""
perfect_white_fintech.py
========================
Aplica o acabamento perfeito de alto contraste e legibilidade no tema branco institucional:
1. Topbar: Fundo branco puro, borda slate-200, texto escuro de alto contraste.
2. Tabela / Scanner B3: Cabeçalho cinza suave (bg-slate-100), linhas nítidas, textos escuros (slate-900 e slate-700), sem números invisíveis.
3. Home: Contraste perfeito nos 4 cards macro e nas listas de rankings.
4. Matriz: Barra de ferramentas e controles em branco e cinza claro com botões esmeralda.
5. Dossiê Drawer: Cabeçalho com texto preto/slate-900, abas e cards perfeitamente legíveis.
"""

with open("build_standalone_html.py", "r", encoding="utf-8") as f:
    code = f.read()

# 1. TOPBAR: substituir qualquer resquício de fundo escuro
old_topbar_regex = r'<header class="bg-\[#080C14\][^>]+>.*?</header>'
new_topbar_clean = """    <header class="bg-white border-b border-slate-200 px-6 py-3.5 flex items-center justify-between gap-4 z-10 flex-shrink-0 shadow-xs">
      <!-- Título Dinâmico do Workspace Ativo -->
      <div>
        <div class="font-mono font-bold text-sm text-slate-900 flex items-center gap-2" id="topbarTitle">
          <span>🏠</span> <span>PANORAMA GERAL</span>
        </div>
        <div class="text-xs text-slate-500" id="topbarSubtitle">Cockpit executivo e inteligência fundamentalista B3</div>
      </div>

      <!-- Barra de Busca Universal, Ativo Ativo e Ações -->
      <div class="flex items-center gap-3">
        <!-- Input de Busca Rápida -->
        <div class="relative">
          <input type="text" id="searchInput" oninput="handleSearch()" placeholder="Buscar Ticker ou Empresa..." class="w-48 md:w-64 bg-slate-50 border border-slate-200 rounded-full px-4 py-1.5 text-xs text-slate-900 placeholder-slate-400 focus:outline-none focus:bg-white focus:border-emerald-500 font-mono transition">
        </div>

        <!-- Indicador de Ativo Ativo -->
        <div class="text-xs font-mono text-slate-700 hidden md:flex items-center gap-1.5 bg-slate-100 px-3 py-1.5 rounded-full border border-slate-200 shadow-xs">
          <span class="text-slate-500 text-[11px]">Ativo:</span>
          <b class="text-emerald-700 font-bold" id="topSelectedTickerBadge">--</b>
        </div>

        <!-- Contador do Universo -->
        <div class="text-xs font-mono text-slate-600 hidden lg:block bg-slate-100 px-3 py-1.5 rounded-full border border-slate-200 shadow-xs">
          <b class="text-emerald-700 font-bold" id="displayedCount">--</b>/<span id="totalUniverseCount">--</span>
        </div>

        <!-- Botão Atualizar Fundamentus -->
        <button id="btn-refresh-data" onclick="triggerDataRefresh()" class="px-4 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white font-mono font-bold rounded-full text-xs transition flex items-center gap-1.5 cursor-pointer shadow-xs">
          <span id="btn-refresh-icon">🔄</span> <span id="btn-refresh-text">Atualizar</span>
        </button>

        <!-- Botão Reset -->
        <button onclick="resetData()" class="px-3 py-1.5 bg-slate-100 hover:bg-slate-200 border border-slate-200 text-slate-700 rounded-full text-xs font-mono cursor-pointer transition">
          Reset
        </button>
      </div>
    </header>"""

import re
code = re.sub(r'<header class="bg-\[#080C14\].*?</header>', new_topbar_clean, code, flags=re.DOTALL)

# 2. SCANNER B3: Toolbar e Tabela
old_scanner_toolbar = """      <!-- TOOLBAR INTEGRADA DO SCANNER B3 -->
      <div id="global-filters-toolbar" class="glass-panel rounded-2xl p-4 flex flex-wrap items-center justify-between gap-3 shadow-xl">
        <div class="flex flex-wrap items-center gap-3">
          <!-- Setor Dropdown -->
          <div class="flex items-center gap-2">
            <span class="text-xs font-mono text-slate-400 font-semibold uppercase">Setor:</span>
            <select id="sectorSelect" onchange="handleSectorChange(this.value)" class="bg-slate-900/80 border border-white/10 rounded-full px-3.5 py-1.5 text-xs text-white font-mono focus:outline-none focus:border-emerald-400 cursor-pointer">
              <option value="ALL" class="bg-[#0A0E1A]">🏢 Todos os Setores</option>
            </select>
          </div>

          <div class="h-4 w-px bg-white/10 hidden sm:block"></div>

          <!-- Presets Munger -->
          <div class="inline-flex bg-slate-900/80 border border-white/10 rounded-full p-1 shadow-inner gap-1">
            <button onclick="setFilter('ALL')" id="flt-ALL" class="filter-btn active rounded-full px-3 py-1 text-xs font-mono font-medium hover:text-white">Todos (<span id="cnt-ALL">--</span>)</button>
            <button onclick="setFilter('CAT_ULTRA_CRITIC')" id="flt-CAT_ULTRA_CRITIC" class="filter-btn rounded-full px-3 py-1 text-xs font-mono font-bold hover:text-white text-yellow-300">💎 Ultra-Crítico (<span id="cnt-CAT_ULTRA_CRITIC">--</span>)</button>
            <button onclick="setFilter('TIER1')" id="flt-TIER1" class="filter-btn rounded-full px-3 py-1 text-xs font-mono font-bold hover:text-white text-amber-400">Tier 1 (<span id="cnt-TIER1">--</span>)</button>
            <button onclick="setFilter('ASYMMETRY')" id="flt-ASYMMETRY" class="filter-btn rounded-full px-3 py-1 text-xs font-mono font-bold hover:text-white text-emerald-400">Assimetria (<span id="cnt-ASYMMETRY">--</span>)</button>
            <button onclick="setFilter('NTNB')" id="flt-NTNB" class="filter-btn rounded-full px-3 py-1 text-xs font-mono font-bold hover:text-white text-cyan-400">Spread NTN-B (<span id="cnt-NTNB">--</span>)</button>
            <button onclick="setFilter('NET_CASH')" id="flt-NET_CASH" class="filter-btn rounded-full px-3 py-1 text-xs font-mono font-bold hover:text-white text-sky-400">Caixa Líq (<span id="cnt-NET_CASH">--</span>)</button>
          </div>

          <div class="h-4 w-px bg-white/10 hidden sm:block"></div>

          <!-- Gatekeepers -->
          <div class="flex items-center gap-2 flex-wrap">
            <label class="flex items-center gap-1.5 cursor-pointer glass-pill px-3 py-1 rounded-full text-xs select-none hover:border-white/20 transition">
              <input type="checkbox" id="chkLiquidity1M" checked onchange="toggleGatekeeper()" class="w-3.5 h-3.5 rounded text-emerald-500 bg-slate-800 border-slate-700">
              <span class="text-slate-200">Liq &ge; R$ 1M</span>
              <span class="text-[11px] text-emerald-400 font-mono font-bold" id="cnt-liq-badge">--</span>
            </label>
            <label class="flex items-center gap-1.5 cursor-pointer glass-pill px-3 py-1 rounded-full text-xs select-none hover:border-white/20 transition">
              <input type="checkbox" id="chkLatestBalance" checked onchange="toggleGatekeeper()" class="w-3.5 h-3.5 rounded text-emerald-500 bg-slate-800 border-slate-700">
              <span class="text-slate-200">Balanço 2T26</span>
              <span class="text-[11px] text-emerald-400 font-mono font-bold" id="cnt-bal-badge">--</span>
            </label>
            <label class="flex items-center gap-1.5 cursor-pointer glass-pill px-3 py-1 rounded-full text-xs select-none hover:border-white/20 transition">
              <input type="checkbox" id="chkFilterDistortions" onchange="toggleGatekeeper()" class="w-3.5 h-3.5 rounded text-purple-400 bg-slate-800 border-slate-700">
              <span class="text-slate-200">Só Recorrente</span>
              <span class="text-[11px] text-purple-400 font-mono font-bold" id="cnt-rec-badge">--</span>
            </label>
            <label class="flex items-center gap-1.5 cursor-pointer glass-pill px-3 py-1 rounded-full text-xs select-none hover:border-white/20 transition" title="Munger Acid Test: Exige conversão EBIT/EBITDA >= 75% ou Bancos ROE >= 15%">
              <input type="checkbox" id="chkAcidTest" onchange="toggleGatekeeper()" class="w-3.5 h-3.5 rounded text-yellow-400 bg-slate-800 border-slate-700">
              <span class="text-slate-200">Acid Test &ge; 75%</span>
            </label>
            <label class="flex items-center gap-1.5 cursor-pointer glass-pill px-3 py-1 rounded-full text-xs select-none hover:border-white/20 transition" title="Governança: Exige ações ordinárias (ON - 100% Tag Along Legal)">
              <input type="checkbox" id="chkOnlyON" onchange="toggleGatekeeper()" class="w-3.5 h-3.5 rounded text-indigo-400 bg-slate-800 border-slate-700">
              <span class="text-slate-200">Só Ações ON</span>
            </label>
          </div>
        </div>

        <div class="flex items-center gap-3">
          <span class="text-xs font-mono text-slate-300 bg-slate-900/80 px-3 py-1 rounded-full border border-white/10" id="tableCountBadge">-- ativos</span>
          <div id="tableQuadrantFilterBadge" class="hidden items-center gap-1"></div>
        </div>
      </div>"""

new_scanner_toolbar = """      <!-- TOOLBAR INTEGRADA DO SCANNER B3 -->
      <div id="global-filters-toolbar" class="glass-panel rounded-2xl p-4 flex flex-wrap items-center justify-between gap-3 shadow-xs bg-white border border-slate-200">
        <div class="flex flex-wrap items-center gap-3">
          <!-- Setor Dropdown -->
          <div class="flex items-center gap-2">
            <span class="text-xs font-mono text-slate-600 font-semibold uppercase">Setor:</span>
            <select id="sectorSelect" onchange="handleSectorChange(this.value)" class="bg-slate-50 border border-slate-200 rounded-full px-3.5 py-1.5 text-xs text-slate-800 font-mono focus:outline-none focus:border-emerald-500 cursor-pointer">
              <option value="ALL">🏢 Todos os Setores</option>
            </select>
          </div>

          <div class="h-4 w-px bg-slate-200 hidden sm:block"></div>

          <!-- Presets Institucionais -->
          <div class="inline-flex bg-slate-100 border border-slate-200 rounded-full p-1 gap-1">
            <button onclick="setFilter('ALL')" id="flt-ALL" class="filter-btn active rounded-full px-3 py-1 text-xs font-mono font-medium">Todos (<span id="cnt-ALL">--</span>)</button>
            <button onclick="setFilter('CAT_ULTRA_CRITIC')" id="flt-CAT_ULTRA_CRITIC" class="filter-btn rounded-full px-3 py-1 text-xs font-mono font-bold text-amber-800">💎 Máxima Solvência (<span id="cnt-CAT_ULTRA_CRITIC">--</span>)</button>
            <button onclick="setFilter('TIER1')" id="flt-TIER1" class="filter-btn rounded-full px-3 py-1 text-xs font-mono font-bold text-emerald-800">Tier 1 (<span id="cnt-TIER1">--</span>)</button>
            <button onclick="setFilter('ASYMMETRY')" id="flt-ASYMMETRY" class="filter-btn rounded-full px-3 py-1 text-xs font-mono font-bold text-sky-800">Assimetria (<span id="cnt-ASYMMETRY">--</span>)</button>
            <button onclick="setFilter('NTNB')" id="flt-NTNB" class="filter-btn rounded-full px-3 py-1 text-xs font-mono font-bold text-teal-800">Spread NTN-B (<span id="cnt-NTNB">--</span>)</button>
            <button onclick="setFilter('NET_CASH')" id="flt-NET_CASH" class="filter-btn rounded-full px-3 py-1 text-xs font-mono font-bold text-indigo-800">Caixa Líq (<span id="cnt-NET_CASH">--</span>)</button>
          </div>

          <div class="h-4 w-px bg-slate-200 hidden sm:block"></div>

          <!-- Gatekeepers -->
          <div class="flex items-center gap-2 flex-wrap">
            <label class="flex items-center gap-1.5 cursor-pointer glass-pill px-3 py-1 rounded-full text-xs select-none hover:border-slate-300 transition">
              <input type="checkbox" id="chkLiquidity1M" checked onchange="toggleGatekeeper()" class="w-3.5 h-3.5 rounded text-emerald-600 bg-white border-slate-300">
              <span class="text-slate-700">Liq &ge; R$ 1M</span>
              <span class="text-[11px] text-emerald-700 font-mono font-bold" id="cnt-liq-badge">--</span>
            </label>
            <label class="flex items-center gap-1.5 cursor-pointer glass-pill px-3 py-1 rounded-full text-xs select-none hover:border-slate-300 transition">
              <input type="checkbox" id="chkLatestBalance" checked onchange="toggleGatekeeper()" class="w-3.5 h-3.5 rounded text-emerald-600 bg-white border-slate-300">
              <span class="text-slate-700">Balanço 2T26</span>
              <span class="text-[11px] text-emerald-700 font-mono font-bold" id="cnt-bal-badge">--</span>
            </label>
            <label class="flex items-center gap-1.5 cursor-pointer glass-pill px-3 py-1 rounded-full text-xs select-none hover:border-slate-300 transition">
              <input type="checkbox" id="chkFilterDistortions" onchange="toggleGatekeeper()" class="w-3.5 h-3.5 rounded text-purple-600 bg-white border-slate-300">
              <span class="text-slate-700">Só Recorrente</span>
              <span class="text-[11px] text-purple-700 font-mono font-bold" id="cnt-rec-badge">--</span>
            </label>
            <label class="flex items-center gap-1.5 cursor-pointer glass-pill px-3 py-1 rounded-full text-xs select-none hover:border-slate-300 transition" title="Munger Acid Test: Exige conversão EBIT/EBITDA >= 75% ou Bancos ROE >= 15%">
              <input type="checkbox" id="chkAcidTest" onchange="toggleGatekeeper()" class="w-3.5 h-3.5 rounded text-amber-600 bg-white border-slate-300">
              <span class="text-slate-700">Acid Test &ge; 75%</span>
            </label>
            <label class="flex items-center gap-1.5 cursor-pointer glass-pill px-3 py-1 rounded-full text-xs select-none hover:border-slate-300 transition" title="Governança: Exige ações ordinárias (ON - 100% Tag Along Legal)">
              <input type="checkbox" id="chkOnlyON" onchange="toggleGatekeeper()" class="w-3.5 h-3.5 rounded text-indigo-600 bg-white border-slate-300">
              <span class="text-slate-700">Só Ações ON</span>
            </label>
          </div>
        </div>

        <div class="flex items-center gap-3">
          <span class="text-xs font-mono text-slate-700 bg-slate-100 px-3 py-1 rounded-full border border-slate-200" id="tableCountBadge">-- ativos</span>
          <div id="tableQuadrantFilterBadge" class="hidden items-center gap-1"></div>
        </div>
      </div>"""

code = code.replace(old_scanner_toolbar, new_scanner_toolbar)

# Cabeçalho da Tabela
old_table_header = """            <thead class="sticky top-0 bg-[#0A0E1A]/95 backdrop-blur-md z-10 border-b border-white/10 shadow-sm">
              <tr class="text-slate-300 text-xs font-bold uppercase tracking-wider select-none">
                <th onclick="sortTable('ticker')" class="py-3 px-3.5 cursor-pointer hover:text-amber-400" title="Ticker e Nome da Empresa">Ativo ⬍</th>
                <th onclick="sortTable('cotacao')" class="py-3 px-3 cursor-pointer hover:text-amber-400 text-right" title="Cotação Atual">Cotação ⬍</th>
                <th onclick="sortTable('quality_score')" class="py-3 px-3 cursor-pointer hover:text-amber-400 text-center" title="Charlie Munger Quality Score (0 a 100)">Score ⬍</th>
                <th onclick="sortTable('ey_spread')" class="py-3 px-3 cursor-pointer hover:text-amber-400 text-right" title="Prêmio Real sobre NTN-B 6,50%">Spread NTN-B ⬍</th>
                <th onclick="sortTable('pl')" class="py-3 px-3 cursor-pointer hover:text-amber-400 text-right" title="P/L LTM e P/L Run-Rate Anualizado (2T26) para detecção de ciclo">P/L &amp; Run-Rate ⬍</th>
                <th onclick="sortTable('ev_ebitda')" class="py-3 px-3 cursor-pointer hover:text-amber-400 text-right" title="Valor da Firma sobre EBITDA">EV / EBITDA ⬍</th>
                <th onclick="sortTable('roic')" class="py-3 px-3 cursor-pointer hover:text-amber-400 text-right" title="Retorno sobre Capital Empregado (ROIC / ROE para bancos)">ROIC / ROE ⬍</th>
                <th onclick="sortTable('mrg_liq')" class="py-3 px-3 cursor-pointer hover:text-amber-400 text-right" title="Margem Líquida">Margem Líq. ⬍</th>
                <th onclick="sortTable('div_liq_ebitda')" class="py-3 px-3 cursor-pointer hover:text-amber-400 text-right" title="Dívida Líquida / EBITDA (Solvência e Risco de Balanço)">Dív. / EBITDA ⬍</th>
                <th onclick="sortTable('div_yield')" class="py-3 px-3 cursor-pointer hover:text-amber-400 text-right" title="Dividend Yield LTM e Payout (% do Lucro Líquido Pago em Proventos)">DY &amp; Payout ⬍</th>
              </tr>
            </thead>"""

new_table_header = """            <thead class="sticky top-0 bg-slate-100 z-10 border-b border-slate-200 shadow-xs">
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

code = code.replace(old_table_header, new_table_header)

# Tabela Divide
code = code.replace('class="divide-y divide-[#1B2232]/60"', 'class="divide-y divide-slate-100"')

# Linhas da tabela em renderTable()
code = code.replace("const rowBg = isSelected ? 'bg-emerald-500/15 border-l-2 border-emerald-400 font-bold' : (idx % 2 === 0 ? 'bg-white/[0.01]' : 'bg-transparent');",
                    "const rowBg = isSelected ? 'bg-emerald-50 border-l-4 border-emerald-600 font-bold' : (idx % 2 === 0 ? 'bg-white' : 'bg-slate-50/50');")

code = code.replace("tr.className = `cursor-pointer transition duration-150 hover:bg-white/[0.05] hover:border-l-2 hover:border-emerald-400 ${rowBg}`;",
                    "tr.className = `cursor-pointer transition duration-150 hover:bg-slate-100/70 ${rowBg}`;")

# Cores semânticas de texto no tema claro
old_colors_fn = """    function getColorRoe(val) {
      if (val === null || val === undefined) return 'text-slate-500';
      const num = Math.abs(val) < 2.0 ? val * 100 : val;
      if (num >= 15.0) return 'text-emerald-400 font-bold';
      if (num >= 8.0) return 'text-slate-200';
      if (num >= 0.0) return 'text-amber-400';
      return 'text-rose-400 font-bold';
    }

    function getColorPl(val) {
      if (val === null || val === undefined) return 'text-slate-500';
      if (val < 0) return 'text-rose-400 font-bold';
      if (val <= 12.0) return 'text-emerald-400 font-semibold';
      if (val <= 22.0) return 'text-slate-200';
      return 'text-amber-400';
    }

    function getColorDy(val) {
      if (val === null || val === undefined) return 'text-slate-500';
      const num = Math.abs(val) < 2.0 ? val * 100 : val;
      if (num >= 6.0) return 'text-emerald-400 font-bold';
      if (num >= 3.0) return 'text-slate-200';
      if (num > 0) return 'text-slate-400';
      return 'text-slate-500';
    }

    function getColorDebt(val, isFin = false) {
      if (isFin) return 'text-sky-400 font-medium';
      if (val === null || val === undefined) return 'text-slate-400';
      if (val < 0) return 'text-emerald-400 font-semibold';
      if (val <= 1.5) return 'text-emerald-400 font-semibold';
      if (val <= 2.7) return 'text-amber-400';
      return 'text-rose-400 font-bold';
    }

    function getColorMrgLiq(val) {
      if (val === null || val === undefined) return 'text-slate-500';
      const num = Math.abs(val) < 2.0 ? val * 100 : val;
      if (num >= 12.0) return 'text-emerald-400 font-semibold';
      if (num >= 4.0) return 'text-slate-200';
      if (num >= 0) return 'text-amber-400';
      return 'text-rose-400 font-bold';
    }

    function getColorAcidTest(val) {
      if (val === null || val === undefined) return 'text-slate-400';
      const num = Math.abs(val) < 2.0 ? val * 100 : val;
      if (num >= 75.0) return 'text-emerald-400 font-semibold';
      if (num >= 60.0) return 'text-amber-400';
      return 'text-rose-400 font-bold';
    }"""

new_colors_fn = """    function getColorRoe(val) {
      if (val === null || val === undefined) return 'text-slate-400';
      const num = Math.abs(val) < 2.0 ? val * 100 : val;
      if (num >= 15.0) return 'text-emerald-700 font-bold';
      if (num >= 8.0) return 'text-slate-800';
      if (num >= 0.0) return 'text-amber-800 font-medium';
      return 'text-rose-700 font-bold';
    }

    function getColorPl(val) {
      if (val === null || val === undefined) return 'text-slate-400';
      if (val < 0) return 'text-rose-700 font-bold';
      if (val <= 12.0) return 'text-emerald-700 font-semibold';
      if (val <= 22.0) return 'text-slate-800';
      return 'text-amber-800 font-medium';
    }

    function getColorDy(val) {
      if (val === null || val === undefined) return 'text-slate-400';
      const num = Math.abs(val) < 2.0 ? val * 100 : val;
      if (num >= 6.0) return 'text-emerald-700 font-bold';
      if (num >= 3.0) return 'text-slate-800 font-medium';
      if (num > 0) return 'text-slate-600';
      return 'text-slate-400';
    }

    function getColorDebt(val, isFin = false) {
      if (isFin) return 'text-sky-700 font-medium';
      if (val === null || val === undefined) return 'text-slate-400';
      if (val < 0) return 'text-emerald-700 font-semibold';
      if (val <= 1.5) return 'text-emerald-700 font-semibold';
      if (val <= 2.7) return 'text-amber-800 font-medium';
      return 'text-rose-700 font-bold';
    }

    function getColorMrgLiq(val) {
      if (val === null || val === undefined) return 'text-slate-400';
      const num = Math.abs(val) < 2.0 ? val * 100 : val;
      if (num >= 12.0) return 'text-emerald-700 font-semibold';
      if (num >= 4.0) return 'text-slate-800';
      if (num >= 0) return 'text-amber-800 font-medium';
      return 'text-rose-700 font-bold';
    }

    function getColorAcidTest(val) {
      if (val === null || val === undefined) return 'text-slate-400';
      const num = Math.abs(val) < 2.0 ? val * 100 : val;
      if (num >= 75.0) return 'text-emerald-700 font-semibold';
      if (num >= 60.0) return 'text-amber-800 font-medium';
      return 'text-rose-700 font-bold';
    }

    function getColorSpread(val) {
      if (val === null || val === undefined) return 'text-slate-400';
      if (val >= 3.0) return 'text-emerald-700 font-bold';
      if (val >= 0.0) return 'text-teal-700 font-semibold';
      return 'text-rose-700 font-bold';
    }"""

# Converter de double braces se necessário
old_fn_with_braces = old_colors_fn.replace('{', '{{').replace('}', '}}')
new_fn_with_braces = new_colors_fn.replace('{', '{{').replace('}', '}}')
code = code.replace(old_fn_with_braces, new_fn_with_braces)

# Garantir que textos na tabela sejam text-slate-800
code = code.replace('<td class="py-2.5 px-3 text-right text-slate-200">', '<td class="py-2.5 px-3 text-right text-slate-800 font-medium">')
code = code.replace('<td class="py-2.5 px-3 text-right text-slate-300">', '<td class="py-2.5 px-3 text-right text-slate-800 font-medium">')

# 3. MATRIZ: Ajustar controles da barra superior da matriz
old_matrix_toolbar = """        <!-- Controles Interativos -->
        <div class="flex items-center gap-2 text-xs font-mono">
          <!-- Seletor Eixo X -->
          <div class="inline-flex bg-slate-900/80 border border-white/10 rounded-full p-0.5">
            <button type="button" id="btn-x-pl" onclick="switchMatrixX('pl')" class="px-3 py-0.5 rounded-full bg-amber-500/20 text-amber-300 font-bold border border-amber-500/40">P/L</button>
            <button type="button" id="btn-x-ey" onclick="switchMatrixX('ey')" class="px-3 py-0.5 rounded-full text-slate-400 hover:text-white">EY% (NTN-B)</button>
          </div>

          <!-- Seletor 3ª Dimensão: Tamanho da Bolha -->
          <div class="inline-flex items-center gap-1.5 bg-slate-900/80 border border-white/10 rounded-full px-3 py-1">
            <span class="text-[10px] text-slate-400">Tamanho:</span>
            <select id="sel-bubble-metric" onchange="switchBubbleMetric(this.value)" class="bg-transparent text-slate-200 text-[11px] focus:outline-none cursor-pointer">
              <option value="mcap" class="bg-white text-slate-800">Valor de Mercado</option>
              <option value="volume" class="bg-white text-slate-800">Volume Diário</option>
              <option value="fixed" class="bg-white text-slate-800">Fixo</option>
            </select>
          </div>

          <!-- Seletor 3ª Dimensão: Cor da Bolha -->
          <div class="inline-flex items-center gap-1.5 bg-slate-900/80 border border-emerald-500/30 rounded-full px-3 py-1">
            <span class="text-[10px] text-emerald-400 font-bold">Cor:</span>
            <select id="sel-bubble-color" onchange="switchBubbleColor(this.value)" class="bg-transparent text-emerald-300 font-bold text-[11px] focus:outline-none cursor-pointer">
              <option value="asymmetry" selected class="bg-white text-slate-800">🎯 Assimetria Favorável (CFA)</option>
              <option value="momentum" class="bg-white text-slate-800">⚡ Momento 2T26 (Run-Rate)</option>
              <option value="dividend" class="bg-white text-slate-800">💰 Dividend Yield</option>
              <option value="sector" class="bg-white text-slate-800">🏢 Setores B3</option>
              <option value="relative" class="bg-white text-slate-800">📐 Posição vs Curva Fair Value</option>
            </select>
          </div>

          <!-- Zoom & Pan -->
          <div class="flex items-center gap-1">
            <button onclick="zoomMatrix(1.3)" class="w-6 h-6 flex items-center justify-center text-slate-300 hover:text-white bg-slate-900/80 border border-white/10 rounded-full font-bold transition" title="Zoom +">+</button>
            <button onclick="zoomMatrix(0.77)" class="w-6 h-6 flex items-center justify-center text-slate-300 hover:text-white bg-slate-900/80 border border-white/10 rounded-full font-bold transition" title="Zoom -">−</button>
            <button onclick="resetMatrixZoom()" class="px-2.5 h-6 flex items-center gap-1 text-slate-300 hover:text-white bg-slate-900/80 border border-white/10 rounded-full text-[11px] transition" title="Reset Zoom">
              <span>↺</span> <span id="matrixZoomLabel">100%</span>
            </button>
          </div>
          <span id="matrixVisibleCount" class="hidden">0</span>

          <!-- Ação Rápida: Abrir Selecionada no Dossiê -->
          <button onclick="openSelectedInDossier()" class="px-3.5 h-7 flex items-center gap-1 bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-400 hover:to-teal-400 text-black font-bold rounded-full text-[11px] transition shadow-lg shadow-emerald-500/20 cursor-pointer">
            <span>Ver no Dossiê ➜</span>
          </button>
        </div>"""

new_matrix_toolbar = """        <!-- Controles Interativos -->
        <div class="flex items-center gap-2 text-xs font-mono">
          <!-- Seletor Eixo X -->
          <div class="inline-flex bg-slate-100 border border-slate-200 rounded-full p-0.5">
            <button type="button" id="btn-x-pl" onclick="switchMatrixX('pl')" class="px-3 py-0.5 rounded-full bg-emerald-50 text-emerald-800 font-bold border border-emerald-300">P/L</button>
            <button type="button" id="btn-x-ey" onclick="switchMatrixX('ey')" class="px-3 py-0.5 rounded-full text-slate-600 hover:text-slate-900">EY% (NTN-B)</button>
          </div>

          <!-- Seletor 3ª Dimensão: Tamanho da Bolha -->
          <div class="inline-flex items-center gap-1.5 bg-slate-50 border border-slate-200 rounded-full px-3 py-1">
            <span class="text-[10px] text-slate-500 font-semibold">Tamanho:</span>
            <select id="sel-bubble-metric" onchange="switchBubbleMetric(this.value)" class="bg-transparent text-slate-800 text-[11px] font-semibold focus:outline-none cursor-pointer">
              <option value="mcap">Valor de Mercado</option>
              <option value="volume">Volume Diário</option>
              <option value="fixed">Fixo</option>
            </select>
          </div>

          <!-- Seletor 3ª Dimensão: Cor da Bolha -->
          <div class="inline-flex items-center gap-1.5 bg-emerald-50/80 border border-emerald-200 rounded-full px-3 py-1">
            <span class="text-[10px] text-emerald-800 font-bold">Cor:</span>
            <select id="sel-bubble-color" onchange="switchBubbleColor(this.value)" class="bg-transparent text-emerald-800 font-bold text-[11px] focus:outline-none cursor-pointer">
              <option value="asymmetry" selected>🎯 Assimetria Favorável (CFA)</option>
              <option value="momentum">⚡ Momento 2T26 (Run-Rate)</option>
              <option value="dividend">💰 Dividend Yield</option>
              <option value="sector">🏢 Setores B3</option>
              <option value="relative">📐 Posição vs Curva Fair Value</option>
            </select>
          </div>

          <!-- Zoom & Pan -->
          <div class="flex items-center gap-1">
            <button onclick="zoomMatrix(1.3)" class="w-6 h-6 flex items-center justify-center text-slate-700 hover:bg-slate-200 bg-slate-100 border border-slate-200 rounded-full font-bold transition cursor-pointer" title="Zoom +">+</button>
            <button onclick="zoomMatrix(0.77)" class="w-6 h-6 flex items-center justify-center text-slate-700 hover:bg-slate-200 bg-slate-100 border border-slate-200 rounded-full font-bold transition cursor-pointer" title="Zoom -">−</button>
            <button onclick="resetMatrixZoom()" class="px-2.5 h-6 flex items-center gap-1 text-slate-700 hover:bg-slate-200 bg-slate-100 border border-slate-200 rounded-full text-[11px] transition cursor-pointer" title="Reset Zoom">
              <span>↺</span> <span id="matrixZoomLabel">100%</span>
            </button>
          </div>
          <span id="matrixVisibleCount" class="hidden">0</span>

          <!-- Ação Rápida: Abrir Selecionada no Dossiê -->
          <button onclick="openSelectedInDossier()" class="px-3.5 h-7 flex items-center gap-1 bg-emerald-600 hover:bg-emerald-500 text-white font-bold rounded-full text-[11px] transition shadow-xs cursor-pointer">
            <span>Ver no Dossiê ➜</span>
          </button>
        </div>"""

code = code.replace(old_matrix_toolbar, new_matrix_toolbar)

# Sub-Barra da Matriz
code = code.replace('border-b border-white/10 flex flex-wrap items-center justify-between gap-2 bg-[#06080C]/80',
                    'border-b border-slate-200 flex flex-wrap items-center justify-between gap-2 bg-slate-50')

# Rótulos da legenda da matriz
code = code.replace('text-emerald-300 font-semibold">Assimetria Favorável', 'text-emerald-700 font-bold">Assimetria Favorável')
code = code.replace('text-amber-300">Preço Justo / Carrego', 'text-amber-800 font-semibold">Preço Justo / Carrego')
code = code.replace('text-rose-300">Entrada Esticada', 'text-rose-700 font-bold">Entrada Esticada')

# Tooltip da Matriz (Card elegante escuro flutuante sobre fundo branco)
code = code.replace('glass-panel rounded-xl p-3 text-xs text-slate-200 shadow-2xl z-50 font-mono backdrop-blur-xl border border-white/10',
                    'bg-slate-900 rounded-xl p-3.5 text-xs text-white shadow-2xl z-50 font-mono border border-slate-700')

# 4. HOME VIEW: Cores das Listas Top 5 e Seleção de Máxima Solvência
code = code.replace("text-amber-300 font-mono", "text-slate-900 font-bold font-mono")
code = code.replace("text-cyan-400 font-mono", "text-sky-700 font-bold font-mono")
code = code.replace("text-emerald-400 font-mono", "text-emerald-700 font-bold font-mono")
code = code.replace("text-[11px] text-slate-300 font-sans truncate", "text-[11px] text-slate-600 font-sans truncate")
code = code.replace("bg-white/[0.02]", "bg-slate-50")
code = code.replace("border-white/10", "border-slate-200")
code = code.replace("border-white/5", "border-slate-200/60")

# Salvar o arquivo transformado
with open("build_standalone_html.py", "w", encoding="utf-8") as f:
    f.write(code)

print("build_standalone_html.py polido com sucesso!")
