"""
apply_ux_and_educational_overhaul.py
====================================
Implementa a reformulação estrutural de UX, produto e didática do Terminal B3:
1. Hero Search e Portal Central na Home Page.
2. Sistema Universal de Tooltips Didáticos (Balõezinhos ⓘ) com dicionário completo de termos.
3. Hierarquização dos filtros do Scanner B3 (Filtros Essenciais vs Filtros Avançados Colapsáveis).
4. Resumo Executivo em linguagem humana no Dossiê 360°.
5. Atualização de index.html e sincronização com o artefato brain/munger_terminal.html.
"""

import re
import os
import shutil

INDEX_FILE = "index.html"
BRAIN_ARTIFACT = r"C:\Users\dougl\.gemini\antigravity\brain\19bf6b03-9073-46f6-9498-57b18f1f9a41\munger_terminal.html"

with open(INDEX_FILE, "r", encoding="utf-8") as f:
    html = f.read()

# ==============================================================================
# 1. ESTILOS CSS DOS TOOLTIPS E BADGES
# ==============================================================================
style_addition = """    .info-badge {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 14px;
      height: 14px;
      border-radius: 9999px;
      font-size: 10px;
      font-weight: 700;
      color: #64748B;
      background-color: #F1F5F9;
      border: 1px solid #CBD5E1;
      cursor: help;
      transition: all 0.15s ease;
      vertical-align: middle;
      margin-left: 3px;
    }
    .info-badge:hover {
      color: #0F172A;
      background-color: #E2E8F0;
      border-color: #94A3B8;
      transform: scale(1.1);
    }
  </style>"""

html = html.replace("  </style>", style_addition)

# ==============================================================================
# 2. MARKUP DO TOOLTIP GLOBAL NO BODY
# ==============================================================================
tooltip_markup = """<body class="h-screen text-slate-800 bg-[#F8FAFC] flex overflow-hidden font-sans antialiased selection:bg-emerald-100 selection:text-emerald-900">

  <!-- GLOBAL INTERACTIVE EDUCATIONAL TOOLTIP (BALÃOZINHO INSTITUCIONAL) -->
  <div id="globalTooltip" class="fixed hidden z-[999999] max-w-xs sm:max-w-sm bg-slate-900 text-white p-3 rounded-xl shadow-2xl border border-slate-700 pointer-events-none transition-opacity duration-150 text-xs font-sans">
    <div class="font-bold text-amber-300 font-mono text-xs flex items-center gap-1.5 border-b border-slate-700/80 pb-1 mb-1.5" id="gtTitle"></div>
    <div class="text-slate-200 text-[11px] leading-relaxed font-sans" id="gtDesc"></div>
    <div class="text-slate-400 text-[10px] font-mono mt-1.5 pt-1 border-t border-slate-800 flex items-center justify-between" id="gtFoot"></div>
  </div>"""

html = html.replace('<body class="h-screen text-slate-800 bg-[#F8FAFC] flex overflow-hidden font-sans antialiased selection:bg-emerald-100 selection:text-emerald-900">', tooltip_markup)

# ==============================================================================
# 3. HERO SEARCH & DISCOVERY PORTAL NA HOME PAGE
# ==============================================================================
old_home_header = """      <!-- WORKSPACE 0: 🏠 HOME (PANORAMA GERAL EXECUTIVO) -->
      <section id="view-home" class="w-full glass-panel rounded-2xl flex flex-col p-5 sm:p-6 space-y-5">
        <!-- 1. Header Executivo Limpo (Sem poluição de botões duplicados) -->
        <div class="flex flex-wrap items-center justify-between gap-4 p-5 glass-card rounded-2xl flex-shrink-0 bg-white border border-slate-200">
          <div>
            <div class="flex items-center gap-2.5">
              <span class="text-sm font-mono font-bold text-slate-900 uppercase tracking-wider flex items-center gap-2">
                <span><svg class="w-4 h-4 stroke-[1.75] inline-block" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg></span> COCKPIT EXECUTIVO B3 • ANÁLISE FUNDAMENTALISTA
              </span>
              <span class="px-2.5 py-0.5 text-[10px] font-mono bg-emerald-50 text-emerald-800 border border-emerald-200 rounded-full font-bold">
                BASE AUDITADA • 2T26
              </span>
            </div>
            <p class="text-xs text-slate-600 mt-1.5 max-w-4xl leading-relaxed">
              Painel institucional de inteligência de mercado: prêmio de risco sovereign (NTN-B), assimetrias de valuation, sustentabilidade de proventos e solvência de balanços para alocação com margem de segurança.
            </p>
          </div>
          <div class="flex items-center gap-2 font-mono text-xs">
            <span class="text-[11px] text-slate-500">Universo auditado:</span>
            <span class="px-3 py-1 bg-slate-100 border border-slate-200 text-slate-800 font-bold rounded-full">194 Ações B3</span>
          </div>
        </div>"""

new_home_hero = """      <!-- WORKSPACE 0: 🏠 HOME (PANORAMA GERAL EXECUTIVO) -->
      <section id="view-home" class="w-full glass-panel rounded-2xl flex flex-col p-5 sm:p-6 space-y-5">
        
        <!-- 0. HERO SEARCH & PORTAL DE ENTRADA INTUITIVO -->
        <div class="bg-gradient-to-br from-white via-slate-50 to-emerald-50/20 border border-slate-200/90 rounded-2xl p-6 sm:p-8 text-center shadow-xs flex flex-col items-center justify-center relative overflow-hidden">
          <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-50 text-emerald-800 border border-emerald-200 text-xs font-mono font-bold mb-2.5">
            <span>✦</span> INTELIGÊNCIA FUNDAMENTALISTA B3 • 2T26 AUDITADO
          </div>
          <h1 class="text-xl sm:text-2xl font-black text-slate-900 tracking-tight max-w-2xl">
            Qualidade, Solidez e Preço Justo de Qualquer Ação da B3
          </h1>
          <p class="text-xs sm:text-sm text-slate-500 max-w-xl mt-1 font-sans">
            Consulte o dossiê 360°, múltiplos sem distorções, veredito CFA e preços tetos de Graham e Bazin em segundos.
          </p>

          <!-- Barra de Busca Proeminente Central -->
          <div class="w-full max-w-xl mt-4 relative">
            <div class="relative flex items-center">
              <span class="absolute left-4 text-slate-400">
                <svg class="w-5 h-5 stroke-[2]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-4.35-4.35"/></svg>
              </span>
              <input type="text" id="heroSearchInput" oninput="handleHeroSearch(this.value)" placeholder="Digite o ticker ou empresa (ex: ITSA4, WEGE3, BBAS3, VALE3)..." class="w-full pl-12 pr-28 py-3.5 bg-white border-2 border-slate-300 hover:border-slate-400 focus:border-emerald-600 focus:outline-none rounded-2xl text-sm font-mono text-slate-900 placeholder-slate-400 shadow-sm transition">
              <button onclick="executeHeroSearch()" class="absolute right-2 px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl text-xs font-mono font-bold shadow-xs transition cursor-pointer">
                Analisar
              </button>
            </div>
            <!-- Sugestões Dropdown do Hero Search -->
            <div id="heroSearchResults" class="hidden absolute left-0 right-0 mt-2 bg-white border border-slate-200 rounded-xl shadow-2xl z-50 overflow-hidden text-left font-mono text-xs max-h-72 overflow-y-auto divide-y divide-slate-100"></div>
          </div>

          <!-- Chips de Ações Mais Pesquisadas -->
          <div class="flex flex-wrap items-center justify-center gap-2 mt-4 text-xs font-mono">
            <span class="text-slate-400 text-[11px] font-sans font-medium">Mais pesquisadas:</span>
            <button onclick="selectTickerAndNavigate('ITSA4')" class="px-2.5 py-1 rounded-lg bg-white hover:bg-slate-100 border border-slate-200 text-slate-800 font-bold hover:border-emerald-500 transition cursor-pointer shadow-2xs">ITSA4</button>
            <button onclick="selectTickerAndNavigate('WEGE3')" class="px-2.5 py-1 rounded-lg bg-white hover:bg-slate-100 border border-slate-200 text-slate-800 font-bold hover:border-emerald-500 transition cursor-pointer shadow-2xs">WEGE3</button>
            <button onclick="selectTickerAndNavigate('VALE3')" class="px-2.5 py-1 rounded-lg bg-white hover:bg-slate-100 border border-slate-200 text-slate-800 font-bold hover:border-emerald-500 transition cursor-pointer shadow-2xs">VALE3</button>
            <button onclick="selectTickerAndNavigate('BBAS3')" class="px-2.5 py-1 rounded-lg bg-white hover:bg-slate-100 border border-slate-200 text-slate-800 font-bold hover:border-emerald-500 transition cursor-pointer shadow-2xs">BBAS3</button>
            <button onclick="selectTickerAndNavigate('PETR4')" class="px-2.5 py-1 rounded-lg bg-white hover:bg-slate-100 border border-slate-200 text-slate-800 font-bold hover:border-emerald-500 transition cursor-pointer shadow-2xs">PETR4</button>
            <button onclick="selectTickerAndNavigate('EGIE3')" class="px-2.5 py-1 rounded-lg bg-white hover:bg-slate-100 border border-slate-200 text-slate-800 font-bold hover:border-emerald-500 transition cursor-pointer shadow-2xs">EGIE3</button>
            <button onclick="selectTickerAndNavigate('RENT3')" class="px-2.5 py-1 rounded-lg bg-white hover:bg-slate-100 border border-slate-200 text-slate-800 font-bold hover:border-emerald-500 transition cursor-pointer shadow-2xs">RENT3</button>
          </div>

          <!-- 4 Portais Diretos de Triagem Rápida -->
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 w-full max-w-4xl mt-5 pt-4 border-t border-slate-200/80">
            <button onclick="setFilterAndGoTable('CAT_TIER1')" class="p-3 bg-white hover:bg-emerald-50/50 border border-slate-200 hover:border-emerald-300 rounded-xl text-left transition cursor-pointer group shadow-2xs">
              <div class="text-base group-hover:scale-110 transition-transform inline-block">🏆</div>
              <div class="font-bold text-xs text-slate-900 mt-1 font-mono">Super Empresas</div>
              <div class="text-[10px] text-slate-500 font-sans mt-0.5">Padrão Tier 1 de Munger</div>
            </button>
            <button onclick="setFilterAndGoTable('CAT_DIVIDENDS')" class="p-3 bg-white hover:bg-emerald-50/50 border border-slate-200 hover:border-emerald-300 rounded-xl text-left transition cursor-pointer group shadow-2xs">
              <div class="text-base group-hover:scale-110 transition-transform inline-block">💰</div>
              <div class="font-bold text-xs text-slate-900 mt-1 font-mono">Dividendos Reais</div>
              <div class="text-[10px] text-slate-500 font-sans mt-0.5">Payout saudável &amp; yield</div>
            </button>
            <button onclick="setFilterAndGoTable('CAT_NET_CASH')" class="p-3 bg-white hover:bg-emerald-50/50 border border-slate-200 hover:border-emerald-300 rounded-xl text-left transition cursor-pointer group shadow-2xs">
              <div class="text-base group-hover:scale-110 transition-transform inline-block">🛡️</div>
              <div class="font-bold text-xs text-slate-900 mt-1 font-mono">Balanço Blindado</div>
              <div class="text-[10px] text-slate-500 font-sans mt-0.5">Caixa líquido / sem dívida</div>
            </button>
            <button onclick="switchWorkspace('matrix')" class="p-3 bg-white hover:bg-indigo-50/50 border border-slate-200 hover:border-indigo-300 rounded-xl text-left transition cursor-pointer group shadow-2xs">
              <div class="text-base group-hover:scale-110 transition-transform inline-block">📈</div>
              <div class="font-bold text-xs text-slate-900 mt-1 font-mono">Matriz Estratégica</div>
              <div class="text-[10px] text-slate-500 font-sans mt-0.5">Curva Fair Value vs Preço</div>
            </button>
          </div>
        </div>"""

if old_home_header in html:
    html = html.replace(old_home_header, new_home_hero)
    print("[OK] Home Hero Search & Discovery adicionado com sucesso!")
else:
    print("! Aviso: old_home_header nao encontrado com precisao.")

# ==============================================================================
# 4. HIERARQUIZAÇÃO DOS FILTROS DO SCANNER B3
# ==============================================================================
old_scanner_toolbar = """      <!-- TOOLBAR INTEGRADA DO SCANNER B3 -->
      <div id="global-filters-toolbar" class="glass-panel rounded-2xl p-4 flex flex-wrap items-center justify-between gap-3 shadow-xl">
        <div class="flex flex-wrap items-center gap-3">
          <!-- Setor Dropdown -->
          <div class="flex items-center gap-2">
            <span class="text-xs font-mono text-slate-400 font-semibold uppercase">Setor:</span>
            <select id="sectorSelect" onchange="handleSectorChange(this.value)" class="bg-slate-50 border border-slate-200 rounded-full px-3.5 py-1.5 text-xs text-slate-900 font-mono focus:outline-none focus:border-emerald-500 cursor-pointer">
              <option value="ALL" class="bg-white text-slate-800">Todos os Setores (Geral)</option>
            </select>
          </div>

          <div class="h-4 w-px bg-white/10 hidden sm:block"></div>

          <!-- Presets de Categorias e Fatores B3 -->
          <div class="inline-flex bg-slate-100 border border-slate-200 rounded-full p-0.5 gap-1">
            <button onclick="setFilter('ALL')" id="flt-ALL" class="filter-btn active rounded-full px-2.5 py-0.5 text-xs font-mono font-medium hover:text-slate-900">Todos (<span id="cnt-ALL">--</span>)</button>
            <button onclick="setFilter('CAT_TIER1')" id="flt-CAT_TIER1" class="filter-btn rounded-full px-2.5 py-0.5 text-xs font-mono font-bold hover:text-slate-900 text-amber-800">🏆 Tier 1 (<span id="cnt-TIER1">--</span>)</button>
            <button onclick="setFilter('CAT_NET_CASH')" id="flt-CAT_NET_CASH" class="filter-btn rounded-full px-2.5 py-0.5 text-xs font-mono font-bold hover:text-slate-900 text-emerald-800">🛡️ Caixa Líq (<span id="cnt-NET_CASH">--</span>)</button>
            <button onclick="setFilter('CAT_EXPANSION')" id="flt-CAT_EXPANSION" class="filter-btn rounded-full px-2.5 py-0.5 text-xs font-mono font-bold hover:text-slate-900 text-emerald-800">🟢 Expansão (<span id="sb-cnt-exp">--</span>)</button>
            <button onclick="setFilter('CAT_DIVIDENDS')" id="flt-CAT_DIVIDENDS" class="filter-btn rounded-full px-2.5 py-0.5 text-xs font-mono font-bold hover:text-slate-900 text-teal-800">💰 Dividendos (<span id="sb-cnt-div">--</span>)</button>
            <button onclick="setFilter('CAT_GRAHAM')" id="flt-CAT_GRAHAM" class="filter-btn rounded-full px-2.5 py-0.5 text-xs font-mono font-bold hover:text-slate-900 text-sky-800">📐 Graham (<span id="sb-cnt-graham">--</span>)</button>
            <button onclick="setFilter('CAT_SPREAD_NTNB')" id="flt-CAT_SPREAD_NTNB" class="filter-btn rounded-full px-2.5 py-0.5 text-xs font-mono font-bold hover:text-slate-900 text-indigo-800">📈 Spread NTN-B (<span id="sb-cnt-spread">--</span>)</button>
          </div>

          <div class="h-4 w-px bg-white/10 hidden sm:block"></div>

          <!-- Gatekeepers -->
          <div class="flex items-center gap-2 flex-wrap">
            <label class="flex items-center gap-1.5 cursor-pointer glass-pill px-3 py-1 rounded-full text-xs select-none hover:border-white/20 transition">
              <input type="checkbox" id="chkLiquidity1M" checked onchange="toggleGatekeeper()" class="w-3.5 h-3.5 rounded text-emerald-600 bg-white border-slate-300">
              <span class="text-slate-700 font-medium">Liq &ge; R$ 1M</span>
              <span class="text-[11px] text-emerald-700 font-bold font-mono font-bold" id="cnt-liq-badge">--</span>
            </label>
            <label class="flex items-center gap-1.5 cursor-pointer glass-pill px-3 py-1 rounded-full text-xs select-none hover:border-white/20 transition">
              <input type="checkbox" id="chkLatestBalance" checked onchange="toggleGatekeeper()" class="w-3.5 h-3.5 rounded text-emerald-600 bg-white border-slate-300">
              <span class="text-slate-700 font-medium">Balanço 2T26</span>
              <span class="text-[11px] text-emerald-700 font-bold font-mono font-bold" id="cnt-bal-badge">--</span>
            </label>
            <label class="flex items-center gap-1.5 cursor-pointer glass-pill px-3 py-1 rounded-full text-xs select-none hover:border-white/20 transition">
              <input type="checkbox" id="chkFilterDistortions" onchange="toggleGatekeeper()" class="w-3.5 h-3.5 rounded text-purple-600 bg-white border-slate-300">
              <span class="text-slate-700 font-medium">Só Recorrente</span>
              <span class="text-[11px] text-purple-400 font-mono font-bold" id="cnt-rec-badge">--</span>
            </label>
            <label class="flex items-center gap-1.5 cursor-pointer glass-pill px-3 py-1 rounded-full text-xs select-none hover:border-white/20 transition" title="Munger Acid Test: Exige conversão EBIT/EBITDA >= 75% ou Bancos ROE >= 15%">
              <input type="checkbox" id="chkAcidTest" onchange="toggleGatekeeper()" class="w-3.5 h-3.5 rounded text-amber-600 bg-white border-slate-300">
              <span class="text-slate-700 font-medium">Acid Test &ge; 75%</span>
            </label>
            <label class="flex items-center gap-1.5 cursor-pointer glass-pill px-3 py-1 rounded-full text-xs select-none hover:border-white/20 transition" title="Governança: Exige ações ordinárias (ON - 100% Tag Along Legal)">
              <input type="checkbox" id="chkOnlyON" onchange="toggleGatekeeper()" class="w-3.5 h-3.5 rounded text-indigo-600 bg-white border-slate-300">
              <span class="text-slate-700 font-medium">Só Ações ON</span>
            </label>
          </div>
        </div>

        <div class="flex items-center gap-3">
          <span class="text-xs font-mono text-slate-700 bg-slate-100 px-3 py-1 rounded-full border border-slate-200 font-bold" id="tableCountBadge">-- ativos</span>
          <div id="tableQuadrantFilterBadge" class="hidden items-center gap-1"></div>
        </div>
      </div>"""

new_scanner_toolbar = """      <!-- TOOLBAR HIERARQUIZADA DO SCANNER B3 -->
      <div id="global-filters-toolbar" class="glass-panel rounded-2xl p-4 flex flex-col gap-3 shadow-sm bg-white border border-slate-200">
        <!-- Linha 1: Filtros Essenciais de 1 Clique + Busca + Botão Avançado -->
        <div class="flex flex-wrap items-center justify-between gap-3">
          <div class="flex flex-wrap items-center gap-2">
            <!-- Pílulas Rápidas Essenciais -->
            <button onclick="setFilter('ALL')" id="flt-ALL" class="filter-btn active rounded-full px-3.5 py-1 text-xs font-mono font-medium hover:text-slate-900 cursor-pointer">
              Todos (<span id="cnt-ALL">--</span>)
            </button>
            <button onclick="setFilter('CAT_TIER1')" id="flt-CAT_TIER1" class="filter-btn rounded-full px-3 py-1 text-xs font-mono font-bold hover:text-slate-900 text-emerald-800 bg-emerald-50/70 border border-emerald-200 cursor-pointer flex items-center gap-1">
              <span>🏆 Super Empresas (Tier 1)</span>
              <span class="bg-emerald-100 text-emerald-950 px-1.5 py-0.2 rounded-full text-[10px]" id="cnt-TIER1">--</span>
            </button>
            <button onclick="setFilter('CAT_DIVIDENDS')" id="flt-CAT_DIVIDENDS" class="filter-btn rounded-full px-3 py-1 text-xs font-mono font-bold hover:text-slate-900 text-teal-800 bg-teal-50/70 border border-teal-200 cursor-pointer flex items-center gap-1">
              <span>💰 Dividendos Reais</span>
              <span class="bg-teal-100 text-teal-950 px-1.5 py-0.2 rounded-full text-[10px]" id="cnt-div-essential">--</span>
            </button>
            <button onclick="setFilter('CAT_NET_CASH')" id="flt-CAT_NET_CASH" class="filter-btn rounded-full px-3 py-1 text-xs font-mono font-bold hover:text-slate-900 text-emerald-800 bg-emerald-50/70 border border-emerald-200 cursor-pointer flex items-center gap-1">
              <span>🛡️ Caixa Líquido</span>
              <span class="bg-emerald-100 text-emerald-950 px-1.5 py-0.2 rounded-full text-[10px]" id="cnt-NET_CASH">--</span>
            </button>
            <button onclick="setFilter('CAT_SPREAD_NTNB')" id="flt-CAT_SPREAD_NTNB" class="filter-btn rounded-full px-3 py-1 text-xs font-mono font-bold hover:text-slate-900 text-indigo-800 bg-indigo-50/70 border border-indigo-200 cursor-pointer flex items-center gap-1">
              <span>📈 Prêmio vs NTN-B</span>
              <span class="bg-indigo-100 text-indigo-950 px-1.5 py-0.2 rounded-full text-[10px]" id="cnt-spread-essential">--</span>
            </button>
          </div>

          <!-- Direita: Campo de Filtro da Tabela + Toggle Avançado -->
          <div class="flex items-center gap-2.5">
            <input type="text" id="tableSearchInput" oninput="handleTableFilter()" placeholder="Filtrar tabela..." class="w-36 sm:w-44 bg-slate-50 border border-slate-200 rounded-full px-3 py-1 text-xs font-mono text-slate-800 placeholder-slate-400 focus:outline-none focus:border-emerald-500">
            <button onclick="toggleAdvancedFilters()" id="btnToggleAdvanced" class="px-3 py-1 bg-slate-100 hover:bg-slate-200 text-slate-700 border border-slate-200 rounded-full text-xs font-mono font-semibold flex items-center gap-1.5 transition cursor-pointer">
              <span>⚙️ Filtros Avançados</span>
              <span id="advFilterActiveBadge" class="hidden w-2 h-2 rounded-full bg-emerald-500"></span>
            </button>
            <span class="text-xs font-mono text-slate-700 bg-slate-100 px-2.5 py-1 rounded-full border border-slate-200 font-bold" id="tableCountBadge">-- ativos</span>
          </div>
        </div>

        <!-- Linha 2: Gaveta Recolhível de Filtros Avançados / Quantitativos -->
        <div id="advancedFiltersDrawer" class="hidden pt-3 border-t border-slate-100 flex flex-wrap items-center justify-between gap-3 text-xs font-mono bg-slate-50/70 p-3 rounded-xl border border-slate-200/80">
          <div class="flex flex-wrap items-center gap-3">
            <!-- Setor Dropdown -->
            <div class="flex items-center gap-1.5">
              <span class="text-slate-500 font-medium">Setor:</span>
              <select id="sectorSelect" onchange="handleSectorChange(this.value)" class="bg-white border border-slate-200 rounded-lg px-2.5 py-1 text-xs text-slate-800 font-mono focus:outline-none focus:border-emerald-500 cursor-pointer">
                <option value="ALL">Todos os Setores (Geral)</option>
              </select>
            </div>

            <div class="h-4 w-px bg-slate-200 hidden sm:block"></div>

            <!-- Mais Categorias Técnicas -->
            <div class="flex items-center gap-1.5">
              <button onclick="setFilter('CAT_EXPANSION')" id="flt-CAT_EXPANSION" class="filter-btn rounded-lg px-2.5 py-1 text-xs font-mono text-slate-700 hover:text-slate-900 border border-slate-200 bg-white cursor-pointer" title="Lucro do 2T26 anualizado superando os 12 meses">
                🟢 Lucro em Expansão
              </button>
              <button onclick="setFilter('CAT_GRAHAM')" id="flt-CAT_GRAHAM" class="filter-btn rounded-lg px-2.5 py-1 text-xs font-mono text-slate-700 hover:text-slate-900 border border-slate-200 bg-white cursor-pointer" title="Preço atual com desconto sobre a fórmula de Benjamin Graham">
                📐 Desconto Graham
              </button>
            </div>

            <div class="h-4 w-px bg-slate-200 hidden sm:block"></div>

            <!-- Gatekeepers com Tooltips Explicativos -->
            <div class="flex items-center gap-2 flex-wrap">
              <label class="flex items-center gap-1.5 cursor-pointer bg-white px-2.5 py-1 rounded-lg border border-slate-200 text-xs select-none hover:border-slate-300">
                <input type="checkbox" id="chkLiquidity1M" checked onchange="toggleGatekeeper()" class="w-3.5 h-3.5 rounded text-emerald-600 bg-white border-slate-300">
                <span class="text-slate-700">Liq &ge; R$ 1M/dia</span>
                <span class="info-badge" data-tooltip="liq">ⓘ</span>
              </label>
              <label class="flex items-center gap-1.5 cursor-pointer bg-white px-2.5 py-1 rounded-lg border border-slate-200 text-xs select-none hover:border-slate-300">
                <input type="checkbox" id="chkLatestBalance" checked onchange="toggleGatekeeper()" class="w-3.5 h-3.5 rounded text-emerald-600 bg-white border-slate-300">
                <span class="text-slate-700">Balanço 2T26</span>
                <span class="info-badge" data-tooltip="recency">ⓘ</span>
              </label>
              <label class="flex items-center gap-1.5 cursor-pointer bg-white px-2.5 py-1 rounded-lg border border-slate-200 text-xs select-none hover:border-slate-300">
                <input type="checkbox" id="chkFilterDistortions" onchange="toggleGatekeeper()" class="w-3.5 h-3.5 rounded text-purple-600 bg-white border-slate-300">
                <span class="text-slate-700">Só Recorrente (Sem One-Off)</span>
                <span class="info-badge" data-tooltip="distortion">ⓘ</span>
              </label>
              <label class="flex items-center gap-1.5 cursor-pointer bg-white px-2.5 py-1 rounded-lg border border-slate-200 text-xs select-none hover:border-slate-300">
                <input type="checkbox" id="chkAcidTest" onchange="toggleGatekeeper()" class="w-3.5 h-3.5 rounded text-amber-600 bg-white border-slate-300">
                <span class="text-slate-700">Munger Acid Test &ge; 75%</span>
                <span class="info-badge" data-tooltip="acid_test">ⓘ</span>
              </label>
              <label class="flex items-center gap-1.5 cursor-pointer bg-white px-2.5 py-1 rounded-lg border border-slate-200 text-xs select-none hover:border-slate-300">
                <input type="checkbox" id="chkOnlyON" onchange="toggleGatekeeper()" class="w-3.5 h-3.5 rounded text-indigo-600 bg-white border-slate-300">
                <span class="text-slate-700">Só Ações ON (Tag Along 100%)</span>
              </label>
            </div>
          </div>
          <div class="text-[11px] text-slate-500 font-sans">
            Filtros técnicos de governança e rigor contábil CVM.
          </div>
        </div>
      </div>"""

if old_scanner_toolbar in html:
    html = html.replace(old_scanner_toolbar, new_scanner_toolbar)
    print("[OK] Toolbar do Scanner B3 hierarquizada com sucesso!")
else:
    print("! Aviso: old_scanner_toolbar nao encontrado exatamente.")

# ==============================================================================
# 5. TOOLTIPS NOS CABEÇALHOS DA TABELA DO SCANNER
# ==============================================================================
old_table_headers = """              <tr class="text-slate-600 text-[11px] font-bold uppercase tracking-wider select-none">
                <th onclick="sortTable('ticker')" class="py-2 px-2.5 cursor-pointer hover:text-emerald-700" title="Ticker e Nome da Empresa">Ativo ⬍</th>
                <th onclick="sortTable('cotacao')" class="py-2 px-2 cursor-pointer hover:text-emerald-700 text-right" title="Cotação Atual">Cotação ⬍</th>
                <th onclick="sortTable('quality_score')" class="py-2 px-1.5 cursor-pointer hover:text-emerald-700 text-center" title="Score de Qualidade Fundamentalista (0 a 100)">Score ⬍</th>
                <th onclick="sortTable('ey_spread')" class="py-2 px-2 cursor-pointer hover:text-emerald-700 text-right" title="Prêmio Real sobre NTN-B 6,50%">Spread NTN-B ⬍</th>
                <th onclick="sortTable('pl')" class="py-2 px-2 cursor-pointer hover:text-emerald-700 text-right" title="P/L LTM e P/L Run-Rate Anualizado (2T26)">P/L &amp; Run-Rate ⬍</th>
                <th onclick="sortTable('ev_ebitda')" class="py-2 px-2 cursor-pointer hover:text-emerald-700 text-right" title="Valor da Firma sobre EBITDA (Múltiplo da Firma)">EV / EBITDA ⬍</th>
                <th onclick="sortTable('roic')" class="py-2 px-2 cursor-pointer hover:text-emerald-700 text-right" title="Retorno sobre Capital Investido (Eficiência Operacional NOPAT/CI)">ROIC ⬍</th>
                <th onclick="sortTable('roe')" class="py-2 px-2 cursor-pointer hover:text-emerald-700 text-right" title="Retorno sobre o Patrimônio Líquido (Retorno do Acionista Lucro/PL)">ROE ⬍</th>
                <th onclick="sortTable('mrg_liq')" class="py-2 px-2 cursor-pointer hover:text-emerald-700 text-right" title="Margem Líquida">Margem Líq. ⬍</th>
                <th onclick="sortTable('div_liq_ebitda')" class="py-2 px-2 cursor-pointer hover:text-emerald-700 text-right" title="Dívida Líquida / EBITDA">Dív. / EBITDA ⬍</th>
                <th onclick="sortTable('div_yield')" class="py-2 px-2.5 cursor-pointer hover:text-emerald-700 text-right" title="Dividend Yield e Payout">DY &amp; Payout ⬍</th>
              </tr>"""

new_table_headers = """              <tr class="text-slate-600 text-[11px] font-bold uppercase tracking-wider select-none">
                <th onclick="sortTable('ticker')" class="py-2 px-2.5 cursor-pointer hover:text-emerald-700">Ativo ⬍</th>
                <th onclick="sortTable('cotacao')" class="py-2 px-2 cursor-pointer hover:text-emerald-700 text-right">Cotação ⬍</th>
                <th onclick="sortTable('quality_score')" class="py-2 px-1.5 cursor-pointer hover:text-emerald-700 text-center">Score ⬍ <span class="info-badge" data-tooltip="quality_score">ⓘ</span></th>
                <th onclick="sortTable('ey_spread')" class="py-2 px-2 cursor-pointer hover:text-emerald-700 text-right">Spread NTN-B ⬍ <span class="info-badge" data-tooltip="ey_spread">ⓘ</span></th>
                <th onclick="sortTable('pl')" class="py-2 px-2 cursor-pointer hover:text-emerald-700 text-right">P/L &amp; Run-Rate ⬍ <span class="info-badge" data-tooltip="pl_run_rate">ⓘ</span></th>
                <th onclick="sortTable('ev_ebitda')" class="py-2 px-2 cursor-pointer hover:text-emerald-700 text-right">EV / EBITDA ⬍ <span class="info-badge" data-tooltip="ev_ebitda">ⓘ</span></th>
                <th onclick="sortTable('roic')" class="py-2 px-2 cursor-pointer hover:text-emerald-700 text-right">ROIC ⬍ <span class="info-badge" data-tooltip="roic">ⓘ</span></th>
                <th onclick="sortTable('roe')" class="py-2 px-2 cursor-pointer hover:text-emerald-700 text-right">ROE ⬍ <span class="info-badge" data-tooltip="roe">ⓘ</span></th>
                <th onclick="sortTable('mrg_liq')" class="py-2 px-2 cursor-pointer hover:text-emerald-700 text-right">Margem Líq. ⬍ <span class="info-badge" data-tooltip="mrg_liq">ⓘ</span></th>
                <th onclick="sortTable('div_liq_ebitda')" class="py-2 px-2 cursor-pointer hover:text-emerald-700 text-right">Dív. / EBITDA ⬍ <span class="info-badge" data-tooltip="debt">ⓘ</span></th>
                <th onclick="sortTable('div_yield')" class="py-2 px-2.5 cursor-pointer hover:text-emerald-700 text-right">DY &amp; Payout ⬍ <span class="info-badge" data-tooltip="payout">ⓘ</span></th>
              </tr>"""

if old_table_headers in html:
    html = html.replace(old_table_headers, new_table_headers)
    print("[OK] Cabeçalhos da tabela enriquecidos com balõezinhos informativos!")
else:
    print("! Aviso: old_table_headers nao encontrado com precisao.")

# ==============================================================================
# 6. DICIONÁRIO DE TOOLTIPS E FUNÇÕES DE HERO SEARCH / TOGGLE NO JAVASCRIPT
# ==============================================================================
js_additions = """
    // =========================================================================
    // DICIONÁRIO INSTITUCIONAL DE BALÕEZINHOS DIDÁTICOS (TOOLTIPS)
    // =========================================================================
    const METRIC_TOOLTIPS = {
      quality_score: {
        title: '🏆 Score de Qualidade Munger (0 a 100)',
        desc: 'Mede a excelência do negócio unindo 3 pilares de Charlie Munger: rentabilidade real com memória histórica (60% LTM + 40% média 5 anos), solidez de balanço anti-crise e consistência de lucros sem prejuízos.',
        foot: 'Tier 1 (≥ 80) = Classe Mundial • Tier 2 (≥ 65) = Saudável'
      },
      ey_spread: {
        title: '📈 Spread vs NTN-B Soberana (6,50% a.a.)',
        desc: 'Compara o rendimento em lucros da ação (Earnings Yield = Lucro/Preço) com o juro real do Tesouro IPCA+ longo. Mostra se a empresa paga prêmio suficiente para justificar o risco da bolsa frente à renda fixa.',
        foot: 'Spread > 0% = Ação compensa o risco soberano do Brasil'
      },
      pl_run_rate: {
        title: '⏱️ P/L (12M) vs P/L Run-Rate (2T26)',
        desc: 'O P/L 12M reflete os últimos 4 trimestres. O P/L Run-Rate anualiza o resultado mais recente (4x 2T26). Se o Run-Rate for menor (verde), os lucros estão acelerando; se for maior (laranja), o lucro recente caiu.',
        foot: 'Permite identificar viradas operacionais antes do mercado'
      },
      ev_ebitda: {
        title: '🏢 EV / EBITDA (Múltiplo da Firma)',
        desc: 'Avalia o custo para comprar todas as ações e pagar todas as dívidas da empresa em relação ao caixa operacional gerado. Inaplicável a bancos, pois depósitos e empréstimos não são dívida corporativa.',
        foot: 'Abaixo de 6.0x = Múltiplo atrativo para indústrias e serviços'
      },
      roic: {
        title: '🏭 ROIC (Retorno s/ Capital Investido)',
        desc: 'Mede o lucro gerado estritamente pelas operações fabris e comerciais sobre o dinheiro empatado no negócio. É a métrica favorita de Charlie Munger para avaliar o fosso competitivo (Moat). Bancos mostram N/A.',
        foot: 'Acima de 15% ao ano = Excelência operacional e barreira de entrada'
      },
      roe: {
        title: '🏛️ ROE (Retorno s/ Patrimônio Líquido)',
        desc: 'Mede quanto lucro a empresa entrega para cada R$ 100 colocados pelos acionistas. É a métrica soberana para instituições financeiras e holdings (como Itaúsa, Itaú e Banco do Brasil).',
        foot: 'Acima de 15% ao ano = Retorno de capital de classe mundial'
      },
      mrg_liq: {
        title: '💧 Margem Líquida (% de Conversão)',
        desc: 'Fatia da receita que sobra como lucro líquido após pagar fornecedores, funcionários, juros da dívida e impostos. Mede o poder de precificação da empresa frente aos competidores.',
        foot: 'Acima de 15% = Forte poder de precificação e margem defensiva'
      },
      debt: {
        title: '🛡️ Dívida Líquida / EBITDA (Solvência)',
        desc: 'Quantos anos de caixa operacional a empresa levaria para quitar toda a sua dívida. Valores negativos indicam Caixa Líquido (mais dinheiro em conta do que dívidas). Para bancos, a higidez segue o Índice de Basileia.',
        foot: '< 1.5x = Muito seguro • > 3.0x = Alerta em juros altos'
      },
      payout: {
        title: '💰 Dividend Yield & Payout Implícito',
        desc: 'Dividend Yield é a taxa de proventos pagos em 12 meses. O Payout Implícito indica quanto do lucro foi distribuído. Faixa saudável: 40% a 85%. Payout > 100% alerta que a empresa queima caixa para pagar proventos.',
        foot: 'DY ≥ 6% = Renda passiva real acima da inflação'
      },
      acid_test: {
        title: '⚗️ Munger Acid Test (EBIT / EBITDA)',
        desc: 'Mede quanto do EBITDA realmente vira lucro antes dos impostos após descontar a depreciação e manutenção de maquinário. Empresas com baixa conversão (< 60%) sofrem com Capex pesado.',
        foot: '≥ 75% = Alta conversão de caixa e baixo arrasto de maquinário'
      },
      liq: {
        title: '💧 Liquidez Média Diária (2 Meses)',
        desc: 'Volume financeiro médio negociado por dia na B3. O filtro de R$ 1 milhão/dia garante que você possa comprar e vender suas ações sem sofrer com deságio de falta de liquidez.',
        foot: 'R$ 1M+/dia = Filtro institucional padrão B3'
      },
      recency: {
        title: '📅 Tempestividade do Balanço (2T26)',
        desc: 'Filtra exclusivamente empresas que já divulgaram as demonstrações contábeis do trimestre mais recente (2T26), evitando dados desatualizados do ano passado.',
        foot: '100% alinhado com o calendário de balanços da CVM'
      },
      distortion: {
        title: '⚠️ Filtro de Distorções Contábeis (One-Offs)',
        desc: 'Elimina empresas cujo lucro foi inflado artificialmente por vendas de ativos, créditos fiscais extraordinários ou ganhos não-recorrentes que não vão se repetir.',
        foot: 'Exige lucro limpo e repetível no longo prazo'
      }
    };

    function initGlobalTooltips() {
      const tooltip = document.getElementById('globalTooltip');
      const titleEl = document.getElementById('gtTitle');
      const descEl = document.getElementById('gtDesc');
      const footEl = document.getElementById('gtFoot');
      if (!tooltip) return;

      document.body.addEventListener('mouseenter', (e) => {
        const target = e.target.closest('[data-tooltip]');
        if (!target) return;
        const key = target.getAttribute('data-tooltip');
        const item = METRIC_TOOLTIPS[key];
        if (!item) return;

        titleEl.textContent = item.title;
        descEl.textContent = item.desc;
        footEl.textContent = item.foot || '';

        tooltip.classList.remove('hidden');
        positionTooltip(e, target, tooltip);
      }, true);

      document.body.addEventListener('mousemove', (e) => {
        const target = e.target.closest('[data-tooltip]');
        if (!target) return;
        positionTooltip(e, target, tooltip);
      }, true);

      document.body.addEventListener('mouseleave', (e) => {
        const target = e.target.closest('[data-tooltip]');
        if (!target) return;
        tooltip.classList.add('hidden');
      }, true);
    }

    function positionTooltip(e, target, tooltip) {
      const rect = target.getBoundingClientRect();
      const tipRect = tooltip.getBoundingClientRect();
      const padding = 12;

      let top = rect.bottom + 8;
      let left = rect.left + (rect.width / 2) - (tipRect.width / 2);

      // Evita sair da tela pela direita ou esquerda
      if (left + tipRect.width > window.innerWidth - padding) {
        left = window.innerWidth - tipRect.width - padding;
      }
      if (left < padding) left = padding;

      // Se passar do fundo da tela, joga para cima do elemento
      if (top + tipRect.height > window.innerHeight - padding) {
        top = rect.top - tipRect.height - 8;
      }

      tooltip.style.top = `${top}px`;
      tooltip.style.left = `${left}px`;
    }

    // =========================================================================
    // HERO SEARCH & DESCOBERTA RÁPIDA NA HOME
    // =========================================================================
    function handleHeroSearch(q) {
      const resBox = document.getElementById('heroSearchResults');
      if (!resBox) return;
      q = (q || '').trim().toUpperCase();
      if (!q) {
        resBox.classList.add('hidden');
        resBox.innerHTML = '';
        return;
      }

      const matches = APP_DATA.stocks.filter(s =>
        s.ticker.includes(q) || s.empresa.toUpperCase().includes(q)
      ).slice(0, 8);

      if (matches.length === 0) {
        resBox.innerHTML = `
          <div class="p-3 text-slate-500 font-sans text-center">
            Nenhuma ação encontrada para "<b>${q}</b>"
          </div>
        `;
        resBox.classList.remove('hidden');
        return;
      }

      resBox.innerHTML = matches.map(s => `
        <div onclick="selectTickerAndNavigate('${s.ticker}')" class="p-2.5 px-3 hover:bg-emerald-50/70 cursor-pointer flex items-center justify-between transition">
          <div class="flex items-center gap-2">
            ${getStockLogoHtml(s.ticker, s.empresa, 'w-6 h-6')}
            <div>
              <div class="flex items-center gap-1.5 font-bold text-slate-900 font-mono text-xs">
                <span>${s.ticker}</span>
                <span class="px-1.5 py-0.2 rounded-full text-[9px] font-bold ${s.quality_score >= 80 ? 'bg-emerald-100 text-emerald-900 border border-emerald-300' : 'bg-slate-100 text-slate-800 border border-slate-300'}">
                  Score ${s.quality_score.toFixed(0)}
                </span>
                ${s.is_financial ? '<span class="text-[9px] text-indigo-800 bg-indigo-50 border border-indigo-200 px-1 rounded">Bancos</span>' : ''}
              </div>
              <div class="text-[10px] text-slate-500 font-sans truncate max-w-[240px]">${s.empresa} • ${s.setor}</div>
            </div>
          </div>
          <div class="text-right font-mono">
            <div class="text-xs font-bold text-slate-900">${formatCurrency(s.cotacao)}</div>
            <div class="text-[10px] ${getColorSpread(s.ey_spread)}">Spread ${s.ey_spread > 0 ? '+' : ''}${s.ey_spread.toFixed(1)}%</div>
          </div>
        </div>
      `).join('');
      resBox.classList.remove('hidden');
    }

    function executeHeroSearch() {
      const inp = document.getElementById('heroSearchInput');
      if (!inp) return;
      const q = inp.value.trim().toUpperCase();
      if (!q) return;
      const match = APP_DATA.stocks.find(s => s.ticker === q) ||
                    APP_DATA.stocks.find(s => s.ticker.includes(q) || s.empresa.toUpperCase().includes(q));
      if (match) {
        selectTickerAndNavigate(match.ticker);
      } else {
        switchWorkspace('table');
        const tInp = document.getElementById('tableSearchInput');
        if (tInp) {
          tInp.value = q;
          handleTableFilter();
        }
      }
    }

    // Toggle da Gaveta de Filtros Avançados
    function toggleAdvancedFilters() {
      const drawer = document.getElementById('advancedFiltersDrawer');
      const badge = document.getElementById('advFilterActiveBadge');
      if (!drawer) return;
      drawer.classList.toggle('hidden');
    }

    // Gerador de Resumo Executivo em Linguagem Humana para o Dossiê
    function generateHumanExecutiveSummary(s) {
      if (!s) return '';
      const isFin = s.is_financial;
      const roePct = s.roe ? (s.roe * 100).toFixed(1) + '%' : 'N/D';
      const roicPct = s.roic ? (s.roic * 100).toFixed(1) + '%' : null;
      const dyPct = s.div_yield ? (s.div_yield * 100).toFixed(1) + '%' : '0.0%';
      const tierShort = s.quality_score >= 80 ? 'Tier 1 (Classe Mundial)' : (s.quality_score >= 65 ? 'Tier 2 (Sólida)' : 'Tier 3 / Atenção');

      if (isFin) {
        return `<b>${s.empresa} (${s.ticker})</b> é uma instituição financeira/holding regulada pelas métricas do Banco Central, avaliada no <b>${tierShort}</b> com nota <b>${s.quality_score.toFixed(1)}/100</b>. Entrega um retorno patrimonial (ROE) robusto de <b>${roePct}</b> ao ano e distribui dividendos regulares de <b>${dyPct}</b> a.a. Seu valuation atual oferece <b>${s.entry_status}</b> frente à renda fixa pública.`;
      }

      const debtStatus = (s.div_liq_ebitda !== null && s.div_liq_ebitda < 0) ? 'opera com caixa líquido positivo (sem endividamento líquido)' : (s.div_liq_ebitda ? `alavancagem controlada de ${s.div_liq_ebitda.toFixed(1)}x EBITDA` : 'estrutura de capital auditada');
      const returnDesc = roicPct ? `retorno operacional (ROIC) de <b>${roicPct}</b> e retorno patrimonial (ROE) de <b>${roePct}</b>` : `ROE de <b>${roePct}</b>`;

      return `<b>${s.empresa} (${s.ticker})</b> atua no setor de <b>${s.setor || 'Atividade Geral'}</b>, classificada no <b>${tierShort}</b> com Score de <b>${s.quality_score.toFixed(1)}/100</b>. Apresenta ${returnDesc}, ${debtStatus} e remuneração em proventos de <b>${dyPct}</b> a.a., posicionando-se em <b>${s.entry_status}</b>.`;
    }
"""

html = html.replace("    // Execução inicial", js_additions + "\n    // Execução inicial")
html = html.replace("    render();\n", "    render();\n    initGlobalTooltips();\n")

# Injetar o resumo executivo no header do Dossiê Drawer
old_dossier_header = """      document.getElementById('diagHeaderCard').innerHTML = `
        <div class="flex justify-between items-start">
          <div class="flex items-center gap-3">
            ${getStockLogoHtml(s.ticker, s.empresa, 'w-12 h-12')}
            <div>
              <div class="text-2xl font-bold font-mono text-slate-900 tracking-tight flex items-center gap-2">
                <span>${s.ticker}</span>
                <span class="text-xs px-2 py-0.5 rounded-full font-sans font-semibold ${s.is_latest_balanco ? 'bg-emerald-100 text-emerald-900 border border-emerald-300' : 'bg-slate-100 text-slate-800 border border-slate-300'}">
                  ${s.tri_balanco} (${s.is_latest_balanco ? 'Vigente' : 'Desfasado'})
                </span>
                ${s.is_distorted ? '<span class="text-xs px-2 py-0.5 rounded-full bg-amber-100 text-amber-900 border border-amber-300 font-semibold">' + s.distortion_label + '</span>' : ''}
              </div>
              <div class="text-sm font-bold text-slate-900 truncate max-w-[260px] mt-0.5">${s.empresa}</div>
              <div class="text-xs text-slate-600 font-sans mt-0.5 font-medium">${s.is_financial ? 'Setor Financeiro' : (s.setor || 'Geral')} • Cotação: <b class="text-slate-900 font-mono font-bold">${formatCurrency(s.cotacao)}</b> • Liq: ${volStr}/d</div>
            </div>
          </div>
          <div class="text-right">
            <div class="px-3 py-1 rounded-xl text-sm font-black font-mono tracking-tight shadow-sm ${s.quality_score >= 80 ? 'bg-emerald-100 text-emerald-950 border border-emerald-300' : (s.quality_score >= 65 ? 'bg-amber-100 text-amber-950 border border-amber-300' : 'bg-rose-100 text-rose-950 border border-rose-300')}">
              SCORE ${s.quality_score.toFixed(1)}
            </div>
            <div class="text-[11px] font-mono font-medium text-slate-600 mt-1">P/L Justo: <b class="text-slate-900 font-bold">${(calcFairPL(s.quality_score)).toFixed(2)}x</b></div>
          </div>
        </div>
        <div class="mt-2.5 pt-2 border-t border-slate-200 flex flex-wrap items-center gap-1.5 text-[11px] font-mono">
          <span class="text-slate-600 font-sans font-bold text-[10px] uppercase tracking-wider mr-1">Enquadramentos:</span>
          ${renderCategoriesBadges(categories)}
        </div>
      `;"""

new_dossier_header = """      document.getElementById('diagHeaderCard').innerHTML = `
        <div class="flex justify-between items-start">
          <div class="flex items-center gap-3">
            ${getStockLogoHtml(s.ticker, s.empresa, 'w-12 h-12')}
            <div>
              <div class="text-2xl font-bold font-mono text-slate-900 tracking-tight flex items-center gap-2">
                <span>${s.ticker}</span>
                <span class="text-xs px-2 py-0.5 rounded-full font-sans font-semibold ${s.is_latest_balanco ? 'bg-emerald-100 text-emerald-900 border border-emerald-300' : 'bg-slate-100 text-slate-800 border border-slate-300'}">
                  ${s.tri_balanco} (${s.is_latest_balanco ? 'Vigente' : 'Desfasado'})
                </span>
                ${s.is_distorted ? '<span class="text-xs px-2 py-0.5 rounded-full bg-amber-100 text-amber-900 border border-amber-300 font-semibold">' + s.distortion_label + '</span>' : ''}
              </div>
              <div class="text-sm font-bold text-slate-900 truncate max-w-[260px] mt-0.5">${s.empresa}</div>
              <div class="text-xs text-slate-600 font-sans mt-0.5 font-medium">${s.is_financial ? 'Setor Financeiro' : (s.setor || 'Geral')} • Cotação: <b class="text-slate-900 font-mono font-bold">${formatCurrency(s.cotacao)}</b> • Liq: ${volStr}/d</div>
            </div>
          </div>
          <div class="text-right">
            <div class="px-3 py-1 rounded-xl text-sm font-black font-mono tracking-tight shadow-sm ${s.quality_score >= 80 ? 'bg-emerald-100 text-emerald-950 border border-emerald-300' : (s.quality_score >= 65 ? 'bg-amber-100 text-amber-950 border border-amber-300' : 'bg-rose-100 text-rose-950 border border-rose-300')}">
              SCORE ${s.quality_score.toFixed(1)}
            </div>
            <div class="text-[11px] font-mono font-medium text-slate-600 mt-1">P/L Justo: <b class="text-slate-900 font-bold">${(calcFairPL(s.quality_score)).toFixed(2)}x</b></div>
          </div>
        </div>

        <!-- Box de Resumo Executivo em Linguagem Natural -->
        <div class="mt-3 p-3 bg-slate-50 border border-slate-200 rounded-xl text-xs font-sans text-slate-700 leading-relaxed flex items-start gap-2.5">
          <span class="text-base mt-0.5">💡</span>
          <div>
            <span class="font-bold text-slate-900 font-mono text-[10px] block uppercase tracking-wider mb-0.5">Diagnóstico para o Investidor</span>
            <span>${generateHumanExecutiveSummary(s)}</span>
          </div>
        </div>

        <div class="mt-2.5 pt-2 border-t border-slate-200 flex flex-wrap items-center gap-1.5 text-[11px] font-mono">
          <span class="text-slate-600 font-sans font-bold text-[10px] uppercase tracking-wider mr-1">Enquadramentos:</span>
          ${renderCategoriesBadges(categories)}
        </div>
      `;"""

if old_dossier_header in html:
    html = html.replace(old_dossier_header, new_dossier_header)
    print("[OK] Resumo Executivo em linguagem humana injetado no Dossiê!")
else:
    print("! Aviso: old_dossier_header nao encontrado com precisao.")

with open(INDEX_FILE, "w", encoding="utf-8") as f:
    f.write(html)

print(f"[OK] {INDEX_FILE} atualizado com sucesso!")
shutil.copy2(INDEX_FILE, BRAIN_ARTIFACT)
print(f"[OK] Artefato {BRAIN_ARTIFACT} sincronizado!")
