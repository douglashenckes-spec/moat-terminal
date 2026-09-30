"""
apply_categories_hub.py
========================
Transforma as Carteiras Recomendadas e os Filtros Rápidos no
Hub de Categorias Quantitativas B3 & Filtros Baseados em Etiquetas,
em estrita conformidade com a Resolução CVM nº 20/2021:
1. Elimina aportes simulados em dinheiro, cotas e pesos de compra.
2. Padroniza getStockCategories(s) com a taxonomia de 6 dimensões e limite de 5 etiquetas por ativo.
3. Transforma #view-portfolios em um Hub completo de exploração quantitativa.
4. Sincroniza contadores do sidebar e filtros rápidos com as categorias.
"""

import re

with open("build_standalone_html.py", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Atualizar botão do Sidebar (Navegação Primária)
old_sidebar_btn = """        <button id="nav-portfolios" onclick="switchWorkspace('portfolios')" class="sidebar-nav-btn w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl text-xs font-mono transition cursor-pointer">
          <div class="flex items-center gap-3">
            <span class="w-4 h-4 flex items-center justify-center text-slate-700"><svg class="w-4 h-4 stroke-[1.75] inline-block" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M20 7h-4V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v3H4a2 2 0 00-2 2v11a2 2 0 002 2h16a2 2 0 002-2V9a2 2 0 00-2-2zM10 4h4v3h-4V4zM4 9h16v3.5a1.5 1.5 0 01-1.5 1.5h-13A1.5 1.5 0 014 12.5V9z"/></svg></span>
            <span class="font-semibold">Carteiras Recomendadas</span>
          </div>
          <span class="px-2 py-0.5 text-[9px] font-bold bg-amber-50 text-amber-800 border border-amber-200 rounded-full">CFA</span>
        </button>"""

new_sidebar_btn = """        <button id="nav-portfolios" onclick="switchWorkspace('portfolios')" class="sidebar-nav-btn w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl text-xs font-mono transition cursor-pointer">
          <div class="flex items-center gap-3">
            <span class="w-4 h-4 flex items-center justify-center text-slate-700"><svg class="w-4 h-4 stroke-[1.75] inline-block" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/></svg></span>
            <span class="font-semibold">Categorias &amp; Filtros</span>
          </div>
          <span class="px-2 py-0.5 text-[9px] font-bold bg-indigo-50 text-indigo-800 border border-indigo-200 rounded-full">QUANT</span>
        </button>"""

if old_sidebar_btn in code:
    code = code.replace(old_sidebar_btn, new_sidebar_btn)
    print("[OK] Sidebar nav button atualizado com sucesso!")
else:
    print("! Aviso: old_sidebar_btn nao encontrado exatamente. Procurando por padrao...")

# 2. Atualizar Filtros Rápidos no Sidebar
old_sidebar_presets = """      <!-- Seção de Filtros Rápidos / Presets no Sidebar -->
      <div class="px-3 py-2 border-t border-slate-200 flex-1 overflow-y-auto">
        <div class="text-[10px] font-mono uppercase tracking-wider text-slate-500 px-3 py-1 font-bold">Filtros Rápidos</div>
        <div class="space-y-1">
          <button onclick="setFilterAndGoTable('CAT_ULTRA_CRITIC')" class="w-full flex items-center justify-between px-3 py-1.5 rounded-xl text-[11px] font-mono text-slate-600 hover:text-slate-900 hover:bg-slate-100 transition cursor-pointer">
            <span class="flex items-center gap-2 font-medium"><span class="text-amber-700"><svg class="w-4 h-4 stroke-[1.75] inline-block text-amber-700" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M6 3h12l4 6-10 12L2 9l4-6z"/></svg></span> Máxima Solvência</span>
            <span class="text-[10px] text-amber-800 font-bold bg-amber-50 text-amber-800 border border-amber-200 px-1.5 py-0.2 rounded-full border border-yellow-700/40" id="sb-cnt-ultra">--</span>
          </button>
          <button onclick="setFilterAndGoTable('TIER1')" class="w-full flex items-center justify-between px-3 py-1.5 rounded-xl text-[11px] font-mono text-slate-600 hover:text-slate-900 hover:bg-slate-100 transition cursor-pointer">
            <span class="flex items-center gap-2 font-medium"><span class="text-amber-700"><svg class="w-4 h-4 stroke-[1.75] inline-block text-amber-700" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M8 21h8m-4-4v4m-6-13a4 4 0 008 0V4H6v4zm0 0H4a2 2 0 00-2 2v1a3 3 0 003 3h1m8-6h2a2 2 0 012 2v1a3 3 0 01-3 3h-1"/></svg></span> Líderes Setoriais (T1)</span>
            <span class="text-[10px] text-amber-800 font-bold bg-emerald-50 text-emerald-800 border border-emerald-200 px-1.5 py-0.2 rounded-full border border-amber-700/40" id="sb-cnt-tier1">--</span>
          </button>
          <button onclick="setFilterAndGoTable('ASYMMETRY')" class="w-full flex items-center justify-between px-3 py-1.5 rounded-xl text-[11px] font-mono text-slate-600 hover:text-slate-900 hover:bg-slate-100 transition cursor-pointer">
            <span class="flex items-center gap-2 font-medium"><span class="text-sky-700"><svg class="w-4 h-4 stroke-[1.75] inline-block text-sky-700" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/></svg></span> Assimetria de Valuation</span>
            <span class="text-[10px] text-cyan-300 font-bold bg-sky-50 text-sky-800 border border-sky-200 px-1.5 py-0.2 rounded-full border border-cyan-700/40" id="sb-cnt-asym">--</span>
          </button>
          <button onclick="setFilterAndGoTable('CAT_DIVIDENDS')" class="w-full flex items-center justify-between px-3 py-1.5 rounded-xl text-[11px] font-mono text-slate-600 hover:text-slate-900 hover:bg-slate-100 transition cursor-pointer">
            <span class="flex items-center gap-2 font-medium"><span class="text-emerald-700"><svg class="w-4 h-4 stroke-[1.75] inline-block text-emerald-700" fill="none" stroke="currentColor" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path stroke-linecap="round" stroke-linejoin="round" d="M12 7v10m-3-7.5a2.5 2.5 0 015 0c0 2-3 2-3 4h3"/></svg></span> Dividendos Consistentes</span>
            <span class="text-[10px] text-emerald-300 font-bold bg-teal-50 text-teal-800 border border-teal-200 px-1.5 py-0.2 rounded-full border border-emerald-700/40" id="sb-cnt-div">--</span>
          </button>
          <button onclick="setFilterAndGoTable('NET_CASH')" class="w-full flex items-center justify-between px-3 py-1.5 rounded-xl text-[11px] font-mono text-slate-600 hover:text-slate-900 hover:bg-slate-100 transition cursor-pointer">
            <span class="flex items-center gap-2 font-medium"><span class="text-indigo-700"><svg class="w-4 h-4 stroke-[1.75] inline-block text-indigo-700" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg></span> Balanço Desalavancado</span>
            <span class="text-[10px] text-sky-300 font-bold bg-indigo-50 text-indigo-800 border border-indigo-200 px-1.5 py-0.2 rounded-full border border-sky-700/40" id="sb-cnt-cash">--</span>
          </button>
        </div>
      </div>"""

new_sidebar_presets = """      <!-- Seção de Filtros Rápidos / Presets no Sidebar -->
      <div class="px-3 py-2 border-t border-slate-200 flex-1 overflow-y-auto">
        <div class="text-[10px] font-mono uppercase tracking-wider text-slate-500 px-3 py-1 font-bold">Categorias Rápidas</div>
        <div class="space-y-1">
          <button onclick="setFilterAndGoTable('CAT_TIER1')" class="w-full flex items-center justify-between px-3 py-1.5 rounded-xl text-[11px] font-mono text-slate-600 hover:text-slate-900 hover:bg-slate-100 transition cursor-pointer">
            <span class="flex items-center gap-2 font-medium"><span class="text-amber-700"><svg class="w-4 h-4 stroke-[1.75] inline-block text-amber-700" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M8 21h8m-4-4v4m-6-13a4 4 0 008 0V4H6v4zm0 0H4a2 2 0 00-2 2v1a3 3 0 003 3h1m8-6h2a2 2 0 012 2v1a3 3 0 01-3 3h-1"/></svg></span> Padrão Tier 1</span>
            <span class="text-[10px] text-emerald-800 font-bold bg-emerald-50 text-emerald-800 border border-emerald-200 px-1.5 py-0.2 rounded-full" id="sb-cnt-tier1">--</span>
          </button>
          <button onclick="setFilterAndGoTable('CAT_NET_CASH')" class="w-full flex items-center justify-between px-3 py-1.5 rounded-xl text-[11px] font-mono text-slate-600 hover:text-slate-900 hover:bg-slate-100 transition cursor-pointer">
            <span class="flex items-center gap-2 font-medium"><span class="text-emerald-700"><svg class="w-4 h-4 stroke-[1.75] inline-block text-emerald-700" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg></span> Caixa Líquido</span>
            <span class="text-[10px] text-emerald-800 font-bold bg-emerald-50 text-emerald-800 border border-emerald-200 px-1.5 py-0.2 rounded-full" id="sb-cnt-cash">--</span>
          </button>
          <button onclick="setFilterAndGoTable('CAT_EXPANSION')" class="w-full flex items-center justify-between px-3 py-1.5 rounded-xl text-[11px] font-mono text-slate-600 hover:text-slate-900 hover:bg-slate-100 transition cursor-pointer">
            <span class="flex items-center gap-2 font-medium"><span class="text-emerald-600"><svg class="w-4 h-4 stroke-[1.75] inline-block text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/></svg></span> Lucro em Expansão</span>
            <span class="text-[10px] text-emerald-800 font-bold bg-emerald-50 text-emerald-800 border border-emerald-200 px-1.5 py-0.2 rounded-full" id="sb-cnt-exp">--</span>
          </button>
          <button onclick="setFilterAndGoTable('CAT_DIVIDENDS')" class="w-full flex items-center justify-between px-3 py-1.5 rounded-xl text-[11px] font-mono text-slate-600 hover:text-slate-900 hover:bg-slate-100 transition cursor-pointer">
            <span class="flex items-center gap-2 font-medium"><span class="text-emerald-700"><svg class="w-4 h-4 stroke-[1.75] inline-block text-emerald-700" fill="none" stroke="currentColor" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path stroke-linecap="round" stroke-linejoin="round" d="M12 7v10m-3-7.5a2.5 2.5 0 015 0c0 2-3 2-3 4h3"/></svg></span> Dividendos Consistentes</span>
            <span class="text-[10px] text-teal-800 font-bold bg-teal-50 text-teal-800 border border-teal-200 px-1.5 py-0.2 rounded-full" id="sb-cnt-div">--</span>
          </button>
          <button onclick="setFilterAndGoTable('CAT_GRAHAM')" class="w-full flex items-center justify-between px-3 py-1.5 rounded-xl text-[11px] font-mono text-slate-600 hover:text-slate-900 hover:bg-slate-100 transition cursor-pointer">
            <span class="flex items-center gap-2 font-medium"><span class="text-sky-700"><svg class="w-4 h-4 stroke-[1.75] inline-block text-sky-700" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z"/></svg></span> Desconto Graham</span>
            <span class="text-[10px] text-sky-800 font-bold bg-sky-50 text-sky-800 border border-sky-200 px-1.5 py-0.2 rounded-full" id="sb-cnt-graham">--</span>
          </button>
          <button onclick="setFilterAndGoTable('CAT_SPREAD_NTNB')" class="w-full flex items-center justify-between px-3 py-1.5 rounded-xl text-[11px] font-mono text-slate-600 hover:text-slate-900 hover:bg-slate-100 transition cursor-pointer">
            <span class="flex items-center gap-2 font-medium"><span class="text-indigo-700"><svg class="w-4 h-4 stroke-[1.75] inline-block text-indigo-700" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/></svg></span> Prêmio Real NTN-B</span>
            <span class="text-[10px] text-indigo-800 font-bold bg-indigo-50 text-indigo-800 border border-indigo-200 px-1.5 py-0.2 rounded-full" id="sb-cnt-spread">--</span>
          </button>
        </div>
      </div>"""

if old_sidebar_presets in code:
    code = code.replace(old_sidebar_presets, new_sidebar_presets)
    print("[OK] Sidebar presets atualizados com sucesso!")
else:
    print("! Aviso: old_sidebar_presets nao encontrado.")

# 3. Substituir seção completa de #view-portfolios
pattern_view_portfolios = re.compile(
    r'(<!-- WORKSPACE 3:.*?-->\s*<section id="view-portfolios".*?</section>)',
    re.DOTALL
)

new_view_portfolios = """<!-- WORKSPACE 3: 🏷️ HUB DE CATEGORIAS & FILTROS QUANTITATIVOS B3 -->
    <section id="view-portfolios" class="w-full glass-panel rounded-2xl flex flex-col p-5 sm:p-6 space-y-6 shadow-2xl hidden">
      
      <!-- Topo: Título & Descrição Institucional -->
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-slate-200">
        <div>
          <div class="font-mono font-bold text-base text-slate-900 flex items-center gap-2">
            <span class="text-indigo-600"><svg class="w-5 h-5 stroke-[2]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/></svg></span>
            <span>HUB DE CATEGORIAS &amp; FILTROS QUANTITATIVOS</span>
          </div>
          <div class="text-xs text-slate-500 font-sans mt-0.5">
            Classificação matemática e enquadramento objetivo de balanço baseado em dados auditados da CVM / Fundamentus (Até 5 etiquetas por ativo).
          </div>
        </div>
        <div class="flex items-center gap-2">
          <span class="px-2.5 py-1 text-xs font-mono font-semibold bg-indigo-50 text-indigo-800 border border-indigo-200 rounded-full flex items-center gap-1.5">
            <span class="w-2 h-2 rounded-full bg-indigo-600"></span> 100% Quantitativo &amp; Auditado
          </span>
        </div>
      </div>

      <!-- Grid dos Cards de Categorias Quantitativas -->
      <div>
        <div class="text-[11px] font-mono uppercase tracking-wider text-slate-500 font-bold mb-3 flex items-center justify-between">
          <span>Categorias Principais (Clique para explorar os ativos enquadrados):</span>
          <span class="text-slate-400 font-normal">Máx. 5 etiquetas/empresa</span>
        </div>
        <div id="categoryCardsGrid" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3.5 flex-shrink-0">
          <!-- Renderizado dinamicamente via JS -->
        </div>
      </div>

      <!-- Resumo Estatístico da Categoria Selecionada & Racional Metodológico -->
      <div class="glass-panel rounded-2xl p-5 flex flex-col lg:flex-row items-stretch justify-between gap-5 flex-shrink-0 shadow-sm border border-slate-200">
        <!-- KPIs da Categoria -->
        <div class="flex-1 flex flex-col justify-between gap-3">
          <div class="flex flex-wrap items-center justify-between gap-2 border-b border-slate-100 pb-2">
            <span class="text-xs font-mono font-bold text-slate-900 uppercase tracking-wider flex items-center gap-1.5" id="catActiveTitle">
              <span>📊</span> MÉDIAS PONDERADAS DA CATEGORIA
            </span>
            <span class="text-xs font-mono text-indigo-700 font-semibold bg-indigo-50 px-2.5 py-0.5 rounded-full border border-indigo-200" id="catActiveCount">-- ativos</span>
          </div>

          <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3 font-mono">
            <div class="p-3 rounded-xl glass-card text-center">
              <div class="text-[11px] text-slate-500 uppercase font-semibold">Total Ativos</div>
              <div class="text-base font-bold text-slate-900 mt-0.5" id="kp-cat-total">--</div>
            </div>
            <div class="p-3 rounded-xl glass-card text-center">
              <div class="text-[11px] text-slate-500 uppercase font-semibold">P/L Médio</div>
              <div class="text-base font-bold text-slate-900 mt-0.5" id="kp-cat-pl">--</div>
            </div>
            <div class="p-3 rounded-xl glass-card text-center">
              <div class="text-[11px] text-slate-500 uppercase font-semibold">ROIC / ROE Médio</div>
              <div class="text-base font-bold text-emerald-800 mt-0.5" id="kp-cat-roic">--</div>
            </div>
            <div class="p-3 rounded-xl glass-card text-center">
              <div class="text-[11px] text-slate-500 uppercase font-semibold">Div. Yield Médio</div>
              <div class="text-base font-bold text-emerald-800 mt-0.5" id="kp-cat-dy">--</div>
            </div>
            <div class="p-3 rounded-xl glass-card text-center">
              <div class="text-[11px] text-slate-500 uppercase font-semibold">Spread NTN-B Médio</div>
              <div class="text-base font-bold text-sky-800 mt-0.5" id="kp-cat-spread">--</div>
            </div>
            <div class="p-3 rounded-xl glass-card text-center border-indigo-200 bg-indigo-50/50">
              <div class="text-[11px] text-indigo-900 uppercase font-semibold">Score Médio</div>
              <div class="text-base font-bold text-indigo-900 mt-0.5" id="kp-cat-score">--</div>
            </div>
          </div>
        </div>

        <!-- Racional Metodológico da Categoria -->
        <div class="w-full lg:w-96 glass-card rounded-xl p-4 flex flex-col justify-between gap-2.5 flex-shrink-0 border border-slate-200 bg-slate-50/60">
          <div>
            <div class="text-xs font-mono font-bold text-slate-900 flex items-center gap-1.5 mb-1">
              <span>📐</span> RACIONAL METODOLÓGICO
            </div>
            <p class="text-xs text-slate-600 leading-relaxed font-sans" id="catActiveRationale">
              Critério quantitativo auditado.
            </p>
          </div>
          <div class="pt-2 border-t border-slate-200 flex items-center justify-between text-[11px] font-mono text-slate-500">
            <span>Fonte de dados: <b class="text-slate-800">CVM / Fundamentus</b></span>
            <button onclick="setFilterAndGoTable(currentPortfolioKey)" class="text-indigo-600 hover:text-indigo-800 font-bold cursor-pointer transition">
              Ver no Scanner ➜
            </button>
          </div>
        </div>
      </div>

      <!-- Tabela de Ativos da Categoria Selecionada -->
      <div class="glass-panel rounded-2xl flex flex-col shadow-sm overflow-hidden flex-shrink-0 border border-slate-200">
        <div class="p-4 border-b border-slate-200 bg-slate-50 flex flex-wrap items-center justify-between gap-2">
          <div class="flex items-center gap-2.5">
            <span class="text-sm font-mono font-bold text-slate-900 flex items-center gap-1.5" id="catTableTitle">
              <span>📋</span> ATIVOS ENQUADRADOS NA CATEGORIA
            </span>
            <span class="text-xs text-indigo-800 font-mono font-semibold" id="catTableSubtitle">(-- ativos)</span>
          </div>
          <div class="text-xs font-mono text-slate-500">
            💡 Clique em qualquer linha para abrir o <b class="text-slate-800">Dossiê 360°</b> ou na etiqueta para filtrar
          </div>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full text-left border-collapse text-xs">
            <thead class="bg-slate-100 border-b border-slate-200 font-mono text-slate-700 uppercase text-[11px] font-bold">
              <tr>
                <th class="py-3 px-3.5">Ativo / Empresa</th>
                <th class="py-3 px-3 text-right">Cotação</th>
                <th class="py-3 px-2 text-center">Score</th>
                <th class="py-3 px-3 text-right">P/L</th>
                <th class="py-3 px-3 text-right">ROIC / ROE</th>
                <th class="py-3 px-3 text-right">Div. Yield</th>
                <th class="py-3 px-3 text-right">Dívida Líq.</th>
                <th class="py-3 px-3.5 text-slate-700 font-bold">Enquadramentos Atribuídos (Até 5)</th>
                <th class="py-3 px-3 text-center">Ações</th>
              </tr>
            </thead>
            <tbody id="portStocksTableBody" class="divide-y divide-slate-100 font-sans"></tbody>
          </table>
        </div>
      </div>

      <!-- Rodapé Regulatório Legal CVM -->
      <div class="p-4 rounded-xl border border-slate-200 bg-slate-50 text-slate-600 text-xs leading-relaxed space-y-1">
        <div class="font-mono font-bold text-slate-800 flex items-center gap-1.5 text-[11px]">
          <span>⚖️</span> AVISO DE CONFORMIDADE REGULATÓRIA (RESOLUÇÃO CVM Nº 20/2021)
        </div>
        <p class="text-[11px] text-slate-500">
          As categorias, filtros quantitativos e notas fundamentalistas exibidos nesta plataforma decorrem de cálculos matemáticos objetivos e algoritmos públicos aplicados a dados contábeis auditados disponibilizados pela CVM e Fundamentus. 
          Este conteúdo tem caráter <b>exclusivamente educacional, de pesquisa e análise quantitativa independente</b>. 
          Não constitui oferta de compra ou venda de ativos, consultoria, recomendação de investimento ou relatório de análise na acepção da Resolução CVM nº 20/2021. 
          Decisões de investimento devem ser tomadas individualmente com base em juízo próprio de risco e adequação.
        </p>
      </div>

    </section>"""

if pattern_view_portfolios.search(code):
    code = pattern_view_portfolios.sub(new_view_portfolios, code, count=1)
    print("[OK] Secao #view-portfolios substituida com sucesso pelo Hub de Categorias Quantitativas!")
else:
    print("! Erro ao localizar secao #view-portfolios com regex!")

# 4. Atualizar getFilteredStocks: Enquadramentos / Categorias Institucionais
old_flt_cats = """        // 7 Categorias Estratégicas do Panorama B3
        if (currentFilter === 'CAT_MUNGER') {{
          return s.quality_score >= 80 && s.ey_spread !== null && s.ey_spread >= 1.5 && (s.is_financial || (s.div_liq_ebitda !== null && s.div_liq_ebitda <= 2.5));
        }}
        if (currentFilter === 'CAT_ASYMMETRY') {{
          return s.quality_score >= 75 && s.pl !== null && s.pl >= 3.0 && s.pl <= 15.0 && s.ey_spread !== null && s.ey_spread >= 3.0 && (s.is_financial || (s.div_liq_ebitda !== null && s.div_liq_ebitda <= 3.0)) && !s.is_distorted;
        }}
        if (currentFilter === 'CAT_DIVIDENDS') {{
          return s.div_yield !== null && s.div_yield >= 0.05 && s.div_yield <= 0.13 && s.payout_implicito !== null && s.payout_implicito >= 35 && s.payout_implicito <= 85 && (s.roic || s.roe || 0) >= 0.12 && s.quality_score >= 70 && (s.is_financial || (s.div_liq_ebitda !== null && s.div_liq_ebitda <= 3.0));
        }}
        if (currentFilter === 'CAT_EXPANSION') {{
          if (!s.pl || !s.pl_run_rate || s.run_rate_div_pct === null || s.run_rate_div_pct === undefined) return false;
          if (s.pl < 3.0 || s.pl > 45.0 || s.pl_run_rate < 2.0 || s.pl_run_rate > 80.0) return false;
          const l12 = (s.details && s.details.lucro_liq_12m) || 0;
          const l3 = (s.details && s.details.lucro_liq_3m) || 0;
          return l12 >= 30000000 && l3 > 0 && s.run_rate_div_pct >= 15.0 && s.run_rate_div_pct <= 120.0 && s.pl_run_rate < s.pl * 0.85;
        }}
        if (currentFilter === 'CAT_DECELERATION') {{
          if (!s.pl || !s.pl_run_rate || s.run_rate_div_pct === null || s.run_rate_div_pct === undefined) return false;
          if (s.pl < 3.0 || s.pl > 45.0 || s.pl_run_rate < 2.0 || s.pl_run_rate > 80.0) return false;
          const l12 = (s.details && s.details.lucro_liq_12m) || 0;
          const l3 = (s.details && s.details.lucro_liq_3m) || 0;
          return l12 >= 30000000 && l3 > 0 && s.run_rate_div_pct <= -20.0 && s.run_rate_div_pct >= -70.0 && s.pl_run_rate > s.pl * 1.25;
        }}
        if (currentFilter === 'CAT_NET_CASH') {{
          return s.div_liq_ebitda !== null && s.div_liq_ebitda < -0.1 && !s.is_financial;
        }}
        if (currentFilter === 'CAT_HIGH_DEBT') {{
          return s.div_liq_ebitda !== null && s.div_liq_ebitda > 3.2 && !s.is_financial;
        }}"""

new_flt_cats = """        // Enquadramentos / Categorias Institucionais Padronizadas
        if (currentFilter.startsWith('CAT_')) {{
          const cats = getStockCategories(s);
          return cats.some(c => c.id === currentFilter);
        }}"""

if old_flt_cats in code:
    code = code.replace(old_flt_cats, new_flt_cats)
    print("[OK] getFilteredStocks atualizado para filtro dinamico de categorias!")
else:
    print("! Aviso: old_flt_cats nao encontrado.")

# 5. Atualizar getStockCategories(s) com a taxonomia de 6 dimensões e limite de 5 etiquetas
pattern_get_categories = re.compile(
    r'(    // Rótulos e Categorias Institucionais Munger da Ação\s*function getStockCategories\(s\) \{.*?\n    \})',
    re.DOTALL
)

new_get_categories = """    // Rótulos e Categorias Institucionais Munger da Ação (Até 5 por ativo)
    function getStockCategories(s) {{
      const cats = [];
      if (!s) return cats;

      // 1. DIMENSÃO SOLVÊNCIA & BALANÇO (Prioridade)
      if (s.is_financial) {{
        cats.push({{
          id: 'CAT_FINANCIAL',
          label: 'Intermediação Financeira (Bancos)',
          shortLabel: 'Bancos',
          icon: '🏛️',
          bgClass: 'bg-indigo-50 text-indigo-950 border border-indigo-200 font-semibold'
        }});
      }} else {{
        const dl = (s.details && s.details.divida_liquida !== null) ? s.details.divida_liquida : null;
        const dle = s.div_liq_ebitda;
        if ((dl !== null && dl <= 0) || (dle !== null && dle < 0)) {{
          cats.push({{
            id: 'CAT_NET_CASH',
            label: 'Caixa Líquido Positivo',
            shortLabel: 'Caixa Líq.',
            icon: '🛡️',
            bgClass: 'bg-emerald-50 text-emerald-950 border border-emerald-300 font-semibold'
          }});
        }} else if (dle !== null && dle > 2.5) {{
          cats.push({{
            id: 'CAT_HIGH_DEBT',
            label: 'Dívida Elevada',
            shortLabel: 'Dívida Alta',
            icon: '🚨',
            bgClass: 'bg-rose-50 text-rose-950 border border-rose-300 font-semibold'
          }});
        }} else if (dle !== null && dle <= 1.8) {{
          cats.push({{
            id: 'CAT_BALANCED_DEBT',
            label: 'Dívida Equilibrada',
            shortLabel: 'Dívida Ok',
            icon: '⚖️',
            bgClass: 'bg-slate-100 text-slate-800 border border-slate-300 font-semibold'
          }});
        }}
      }}

      // 2. DIMENSÃO MOMENTO DOS RESULTADOS & RECORRÊNCIA
      if (s.pl && s.pl_run_rate && s.run_rate_div_pct !== null && s.run_rate_div_pct !== undefined) {{
        if (s.run_rate_div_pct >= 15.0 && s.pl_run_rate < s.pl * 0.88) {{
          cats.push({{
            id: 'CAT_EXPANSION',
            label: 'Lucro em Expansão (2T26)',
            shortLabel: 'Expansão',
            icon: '🟢',
            bgClass: 'bg-emerald-50 text-emerald-950 border border-emerald-300 font-semibold'
          }});
        }} else if (s.run_rate_div_pct <= -20.0 && s.pl_run_rate > s.pl * 1.25) {{
          cats.push({{
            id: 'CAT_DECELERATION',
            label: 'Desaceleração Recente',
            shortLabel: 'Desaceleração',
            icon: '⚠️',
            bgClass: 'bg-amber-50 text-amber-950 border border-amber-300 font-semibold'
          }});
        }}
      }}

      if (!s.is_distorted && s.historical_5y && s.historical_5y.is_all_profitable) {{
        cats.push({{
          id: 'CAT_CLEAN_EARNINGS',
          label: 'Lucro Limpo & Recorrente',
          shortLabel: 'Lucro Limpo',
          icon: '💎',
          bgClass: 'bg-teal-50 text-teal-950 border border-teal-300 font-semibold'
        }});
      }}

      // 3. DIMENSÃO QUALIDADE & EFICIÊNCIA DE CAPITAL
      const roicOrRoe = s.roic || s.roe || 0;
      if (s.quality_score >= 80 && roicOrRoe >= 0.15) {{
        cats.push({{
          id: 'CAT_TIER1',
          label: 'Padrão Institucional (Tier 1)',
          shortLabel: 'Tier 1',
          icon: '🏆',
          bgClass: 'bg-emerald-50 text-emerald-950 border border-emerald-300 font-semibold'
        }});
      }} else if (!s.is_financial && s.roic >= 0.18) {{
        cats.push({{
          id: 'CAT_HIGH_ROIC',
          label: 'Super ROIC (≥ 18%)',
          shortLabel: 'Super ROIC',
          icon: '🏰',
          bgClass: 'bg-emerald-50 text-emerald-950 border border-emerald-300 font-semibold'
        }});
      }}

      // 4. DIMENSÃO DIVIDENDOS & PROVENTOS
      if (s.div_yield !== null && s.div_yield >= 0.05 && s.payout_implicito !== null && s.payout_implicito >= 30 && s.payout_implicito <= 88) {{
        cats.push({{
          id: 'CAT_DIVIDENDS',
          label: 'Dividendos Consistentes',
          shortLabel: 'Dividendos',
          icon: '💰',
          bgClass: 'bg-emerald-50 text-emerald-950 border border-emerald-300 font-semibold'
        }});
      }} else if (s.payout_implicito !== null && s.payout_implicito > 105) {{
        cats.push({{
          id: 'CAT_PAYOUT_RISK',
          label: 'Payout Excessivo (> 100%)',
          shortLabel: 'Payout Alto',
          icon: '⚠️',
          bgClass: 'bg-rose-50 text-rose-950 border border-rose-300 font-semibold'
        }});
      }}

      // 5. DIMENSÃO VALUATION & MARGEM DE SEGURANÇA
      const lpa = (s.details && s.details.lpa) ? Number(s.details.lpa) : null;
      const vpa = (s.details && s.details.vpa) ? Number(s.details.vpa) : null;
      const cot = Number(s.cotacao);
      if (lpa && vpa && lpa > 0 && vpa > 0 && cot > 0) {{
        const graham = Math.sqrt(22.5 * lpa * vpa);
        if (graham > cot * 1.15) {{
          cats.push({{
            id: 'CAT_GRAHAM',
            label: 'Desconto Graham',
            shortLabel: 'Graham',
            icon: '📐',
            bgClass: 'bg-sky-50 text-sky-950 border border-sky-300 font-semibold'
          }});
        }}
      }}
      if (s.div_yield && s.div_yield >= 0.06 && cot > 0) {{
        const bazin = (cot * s.div_yield) / 0.06;
        if (bazin > cot * 1.15) {{
          cats.push({{
            id: 'CAT_BAZIN',
            label: 'Preço Teto Décio Bazin',
            shortLabel: 'Teto Bazin',
            icon: '🎯',
            bgClass: 'bg-sky-50 text-sky-950 border border-sky-300 font-semibold'
          }});
        }}
      }}
      if (s.ey_spread !== null && s.ey_spread >= 2.0 && (!s.pl || s.pl <= 15.0)) {{
        cats.push({{
          id: 'CAT_SPREAD_NTNB',
          label: 'Prêmio Real sobre NTN-B',
          shortLabel: 'Prêmio Real',
          icon: '📈',
          bgClass: 'bg-sky-50 text-sky-950 border border-sky-300 font-semibold'
        }});
      }}

      // 6. RISCOS DE CICLO & CONTÁBEIS
      if (s.is_commodity_peak) {{
        cats.push({{
          id: 'CAT_COMMODITY_PEAK',
          label: 'Risco de Ciclo Commodities',
          shortLabel: 'Pico Ciclo',
          icon: '⚠️',
          bgClass: 'bg-amber-50 text-amber-950 border border-amber-300 font-semibold'
        }});
      }}
      if (s.is_distorted) {{
        cats.push({{
          id: 'CAT_DISTORTION',
          label: 'Distorção Contábil / One-Off',
          shortLabel: 'One-off',
          icon: '🔍',
          bgClass: 'bg-purple-50 text-purple-950 border border-purple-300 font-semibold'
        }});
      }}

      // Retorna no máximo 5 etiquetas por empresa para não poluir
      return cats.slice(0, 5);
    }}"""

if pattern_get_categories.search(code):
    code = pattern_get_categories.sub(new_get_categories, code, count=1)
    print("[OK] getStockCategories atualizado com sucesso!")
else:
    print("! Erro ao localizar getStockCategories com regex!")

# 6. Atualizar updateFilterCounts para sincronizar com getStockCategories
old_counts = """      const cntT1 = basePool.filter(s => s.quality_score >= 80.0).length;
      document.getElementById('cnt-TIER1').innerText = cntT1;
      const sbT1 = document.getElementById('sb-cnt-tier1');
      if (sbT1) sbT1.innerText = cntT1;

      const cntAsym = basePool.filter(s => s.quality_score >= 75.0 && s.pl > 0 && s.pl < 8.0).length;
      document.getElementById('cnt-ASYMMETRY').innerText = cntAsym;
      const sbAsym = document.getElementById('sb-cnt-asym');
      if (sbAsym) sbAsym.innerText = cntAsym;

      document.getElementById('cnt-NTNB').innerText = basePool.filter(s => s.ey_spread !== null && s.ey_spread >= 5.0).length;

      const cntCash = basePool.filter(s => s.div_liq_ebitda !== null && s.div_liq_ebitda < 0).length;
      document.getElementById('cnt-NET_CASH').innerText = cntCash;
      const sbCash = document.getElementById('sb-cnt-cash');
      if (sbCash) sbCash.innerText = cntCash;

      const cntDiv = basePool.filter(s => s.div_yield !== null && s.div_yield >= 0.05).length;
      const sbDiv = document.getElementById('sb-cnt-div');
      if (sbDiv) sbDiv.innerText = cntDiv;"""

new_counts = """      const cntT1 = basePool.filter(s => getStockCategories(s).some(c => c.id === 'CAT_TIER1')).length;
      const elT1 = document.getElementById('cnt-TIER1');
      if (elT1) elT1.innerText = cntT1;
      const sbT1 = document.getElementById('sb-cnt-tier1');
      if (sbT1) sbT1.innerText = cntT1;

      const cntCash = basePool.filter(s => getStockCategories(s).some(c => c.id === 'CAT_NET_CASH')).length;
      const elCash = document.getElementById('cnt-NET_CASH');
      if (elCash) elCash.innerText = cntCash;
      const sbCash = document.getElementById('sb-cnt-cash');
      if (sbCash) sbCash.innerText = cntCash;

      const cntExp = basePool.filter(s => getStockCategories(s).some(c => c.id === 'CAT_EXPANSION')).length;
      const sbExp = document.getElementById('sb-cnt-exp');
      if (sbExp) sbExp.innerText = cntExp;

      const cntDiv = basePool.filter(s => getStockCategories(s).some(c => c.id === 'CAT_DIVIDENDS')).length;
      const elDiv = document.getElementById('cnt-CAT_DIVIDENDS') || document.getElementById('cnt-DIVIDENDS');
      if (elDiv) elDiv.innerText = cntDiv;
      const sbDiv = document.getElementById('sb-cnt-div');
      if (sbDiv) sbDiv.innerText = cntDiv;

      const cntGraham = basePool.filter(s => getStockCategories(s).some(c => c.id === 'CAT_GRAHAM')).length;
      const sbGraham = document.getElementById('sb-cnt-graham');
      if (sbGraham) sbGraham.innerText = cntGraham;

      const cntSpread = basePool.filter(s => getStockCategories(s).some(c => c.id === 'CAT_SPREAD_NTNB')).length;
      const sbSpread = document.getElementById('sb-cnt-spread');
      if (sbSpread) sbSpread.innerText = cntSpread;"""

if old_counts in code:
    code = code.replace(old_counts, new_counts)
    print("[OK] updateFilterCounts atualizado com contadores sincronizados!")
else:
    print("! Aviso: old_counts nao encontrado exatamente.")

# 7. Atualizar topbar em switchWorkspace('portfolios')
old_ws_port = """      }} else if (ws === 'portfolios') {{
        if (vPortfolios) vPortfolios.classList.remove('hidden');
        if (btnPortfolios) btnPortfolios.classList.add('active');
        if (topTitle) topTitle.innerHTML = '<span class="text-slate-700">' + APP_ICONS.briefcase + '</span> <span>CARTEIRAS RECOMENDADAS</span>';
        if (topSub) topSub.innerText = 'Seleção buy-side institucional e parecer crítico do comitê CFA';
        renderPortfolios();"""

new_ws_port = """      }} else if (ws === 'portfolios') {{
        if (vPortfolios) vPortfolios.classList.remove('hidden');
        if (btnPortfolios) btnPortfolios.classList.add('active');
        if (topTitle) topTitle.innerHTML = '<span class="text-indigo-600"><svg class="w-4 h-4 stroke-[2] inline-block" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/></svg></span> <span>HUB DE CATEGORIAS QUANTITATIVAS</span>';
        if (topSub) topSub.innerText = 'Segmentação matemática, enquadramento de balanço e rastreador de fatores B3';
        renderPortfolios();"""

if old_ws_port in code:
    code = code.replace(old_ws_port, new_ws_port)
    print("[OK] switchWorkspace topbar atualizado!")
else:
    print("! Aviso: old_ws_port nao encontrado.")

# 8. Atualizar estado inicial de currentPortfolioKey
code = code.replace("let currentPortfolioKey = 'munger';", "let currentPortfolioKey = 'CAT_TIER1';")

# 9. Substituir lógica de renderPortfolios, selectPortfolio e getPortfolioStocks
pattern_portfolio_logic = re.compile(
    r'(    function getPortfolioStocks\(key\) \{.*?\n    let isTableFullWidth = true;)',
    re.DOTALL
)

new_portfolio_logic = """    // DEFINIÇÕES METODOLÓGICAS DAS CATEGORIAS QUANTITATIVAS
    const CATEGORY_DEFINITIONS = [
      {{
        id: 'CAT_TIER1',
        name: 'Padrão Institucional (Tier 1)',
        shortName: 'Tier 1',
        icon: '🏆',
        color: 'emerald',
        badgeClass: 'bg-emerald-50 text-emerald-950 border border-emerald-300',
        description: 'Empresas excepcionais com Score Fundamentalista ≥ 80 pts e ROIC/ROE ≥ 15%. Líderes de mercado com vantagens competitivas estruturais duráveis.',
        rationale: 'Filtro quantitativo que conjuga retorno sustentável sobre o capital próprio/investido acima da taxa livre de risco com solidez de balanço e qualidade contábil no percentil 80+ da B3.'
      }},
      {{
        id: 'CAT_NET_CASH',
        name: 'Caixa Líquido Positivo',
        shortName: 'Caixa Líquido',
        icon: '🛡️',
        color: 'emerald',
        badgeClass: 'bg-emerald-50 text-emerald-950 border border-emerald-300',
        description: 'Empresas não-financeiras cuja disponibilidade financeira imediata supera o montante integral da dívida bruta bancária (Dívida Líquida ≤ 0).',
        rationale: 'Critério estritamente contábil de solvência máxima: risco de liquidez e solvência virtualmente nulo no curto e médio prazo, imunes ao ciclo restritivo da taxa Selic.'
      }},
      {{
        id: 'CAT_EXPANSION',
        name: 'Lucro em Expansão (2T26)',
        shortName: 'Expansão 2T26',
        icon: '🟢',
        color: 'emerald',
        badgeClass: 'bg-emerald-50 text-emerald-950 border border-emerald-300',
        description: 'Empresas cujo lucro líquido anualizado do 2T26 (Run-Rate) supera em mais de 15% a média dos últimos 12 meses acumulados.',
        rationale: 'Rastreador de aceleração operacional recente: identifica momento contábil positivo, expansão de margens e alavancagem operacional antes da reprecificação total pelo consenso.'
      }},
      {{
        id: 'CAT_DIVIDENDS',
        name: 'Dividendos Consistentes',
        shortName: 'Dividendos',
        icon: '💰',
        color: 'emerald',
        badgeClass: 'bg-emerald-50 text-emerald-950 border border-emerald-300',
        description: 'Dividend Yield ≥ 5,0% com Payout Disciplinado (entre 30% e 88%), sem comprometer o fluxo de caixa operacional.',
        rationale: 'Filtro de proventos sustentáveis: rejeita empresas que pagam dividendos artificiais através de endividamento (payout > 100%) ou que apresentam yields frágeis não-recorrentes.'
      }},
      {{
        id: 'CAT_GRAHAM',
        name: 'Desconto Benjamin Graham',
        shortName: 'Desconto Graham',
        icon: '📐',
        color: 'sky',
        badgeClass: 'bg-sky-50 text-sky-950 border border-sky-300',
        description: 'Cotação com desconto superior a 15% em relação ao Preço Justo calculado pela fórmula clássica de Graham: √(22,5 × LPA × VPA).',
        rationale: 'Modelo clássico de Value Investing: exige que a ação negocie abaixo do valor intrínseco resultante da combinação harmônica entre lucro por ação e valor patrimonial auditado.'
      }},
      {{
        id: 'CAT_BAZIN',
        name: 'Preço Teto Décio Bazin',
        shortName: 'Teto Bazin',
        icon: '🎯',
        color: 'sky',
        badgeClass: 'bg-sky-50 text-sky-950 border border-sky-300',
        description: 'Cotação de mercado abaixo do Preço Teto Bazin (Proventos / 0,06) com margem de segurança de pelo menos 15%.',
        rationale: 'Metodologia tradicional brasileira de seleção por fluxo de dividendos com taxa de retorno mínima requerida de 6,0% a.a. em proventos.'
      }},
      {{
        id: 'CAT_SPREAD_NTNB',
        name: 'Prêmio Real sobre NTN-B',
        shortName: 'Prêmio Real',
        icon: '📈',
        color: 'sky',
        badgeClass: 'bg-sky-50 text-sky-950 border border-sky-300',
        description: 'Earning Yield real (1 / P/L) superando o rendimento do Tesouro IPCA+ (NTN-B 2035) em mais de 2,0 pontos percentuais.',
        rationale: 'Régua de custo de oportunidade de Charlie Munger: o rendimento operacional dos lucros da empresa supera com folga a taxa real do título soberano livre de risco.'
      }},
      {{
        id: 'CAT_BALANCED_DEBT',
        name: 'Dívida Equilibrada',
        shortName: 'Dívida Ok',
        icon: '⚖️',
        color: 'slate',
        badgeClass: 'bg-slate-100 text-slate-800 border border-slate-300',
        description: 'Empresas com relação Dívida Líquida / EBITDA ≤ 1,8x, com estrutura de capital conservadora e passivos controlados.',
        rationale: 'Garante que os ativos possuam passivo financeiro plenamente amortizável em menos de 2 anos de geração operacional de EBITDA.'
      }},
      {{
        id: 'CAT_CLEAN_EARNINGS',
        name: 'Lucro Limpo & Recorrente',
        shortName: 'Lucro Limpo',
        icon: '💎',
        color: 'teal',
        badgeClass: 'bg-teal-50 text-teal-950 border border-teal-300',
        description: 'Histórico auditado de 5 anos consecutivos sem qualquer trimestre de prejuízo líquido e sem distorções contábeis não-recorrentes.',
        rationale: 'Filtro de resiliência e perenidade: empresas que atravessam oscilações do PIB e ciclos de juros preservando ininterruptamente o capital dos acionistas.'
      }},
      {{
        id: 'CAT_HIGH_ROIC',
        name: 'Super ROIC (≥ 18%)',
        shortName: 'Super ROIC',
        icon: '🏰',
        color: 'emerald',
        badgeClass: 'bg-emerald-50 text-emerald-950 border border-emerald-300',
        description: 'Retorno sobre o Capital Investido ≥ 18%, sinalizando fossos econômicos profundos e capacidade de reinvestimento.',
        rationale: 'Medida direta de eficiência de alocação de capital e barreira de entrada intransponível contra concorrentes.'
      }},
      {{
        id: 'CAT_DECELERATION',
        name: 'Alerta de Desaceleração',
        shortName: 'Desaceleração',
        icon: '⚠️',
        color: 'amber',
        badgeClass: 'bg-amber-50 text-amber-950 border border-amber-300',
        description: 'Empresas cujo lucro trimestral recente anualizado está 20% ou mais abaixo do lucro acumulado nos últimos 12 meses.',
        rationale: 'Sinalizador preventivo de arrefecimento operacional ou pressão em margens que pode demandar cautela adicional.'
      }},
      {{
        id: 'CAT_HIGH_DEBT',
        name: 'Alavancagem Crítica (> 2.5x)',
        shortName: 'Dívida Alta',
        icon: '🚨',
        color: 'rose',
        badgeClass: 'bg-rose-50 text-rose-950 border border-rose-300',
        description: 'Empresas não-financeiras com Dívida Líquida / EBITDA superior a 2,5x em ambiente de taxas de juros elevadas.',
        rationale: 'Marcador de risco de solvência: despesas financeiras absorvem fatia relevante do resultado operacional, comprimindo o lucro líquido.'
      }}
    ];

    function selectPortfolio(key) {{
      currentPortfolioKey = key;
      renderPortfolios();
    }}

    function getPortfolioStocks(key) {{
      const DISTRESSED = new Set(['LIGT3', 'AMER3', 'OIBR3', 'AZUL4', 'GOLL4', 'CVCB3', 'BHIA3']);
      const valid = APP_DATA.stocks.filter(s => s.is_liquid_1m && !DISTRESSED.has(s.ticker));

      // Filtra ativos que possuem esta categoria atribuída nas até 5 etiquetas
      return valid.filter(s => {{
        const cats = getStockCategories(s);
        return cats.some(c => c.id === key);
      }}).sort((a, b) => (b.quality_score || 0) - (a.quality_score || 0));
    }}

    function renderPortfolios() {{
      const pStocks = getPortfolioStocks(currentPortfolioKey);
      const activeDef = CATEGORY_DEFINITIONS.find(c => c.id === currentPortfolioKey) || CATEGORY_DEFINITIONS[0];

      // 1. Renderizar os cards de seleção de categoria
      const grid = document.getElementById('categoryCardsGrid');
      if (grid) {{
        grid.innerHTML = CATEGORY_DEFINITIONS.map(cat => {{
          const count = getPortfolioStocks(cat.id).length;
          const isActive = cat.id === currentPortfolioKey;
          const activeClass = isActive 
            ? 'border-2 border-indigo-500 bg-indigo-50/40 shadow-md shadow-indigo-100' 
            : 'border border-slate-200 hover:border-slate-300 hover:bg-slate-50/60 shadow-xs';
          
          return `
            <div onclick="selectPortfolio('${{cat.id}}')" class="glass-card rounded-2xl p-4 ${{activeClass}} cursor-pointer transition-all duration-200 flex flex-col justify-between">
              <div>
                <div class="flex items-center justify-between gap-1 mb-2">
                  <span class="text-xs font-mono font-bold text-slate-900 flex items-center gap-1.5">
                    <span class="text-base">${{cat.icon}}</span> <span>${{cat.shortName}}</span>
                  </span>
                  <span class="px-2 py-0.5 rounded-full text-[10px] font-mono font-bold ${{isActive ? 'bg-indigo-600 text-white' : 'bg-slate-100 text-slate-700 border border-slate-200'}}">
                    ${{count}} ativos
                  </span>
                </div>
                <p class="text-xs text-slate-600 leading-relaxed font-sans line-clamp-2">
                  ${{cat.description}}
                </p>
              </div>
              <div class="mt-3 pt-2 border-t border-slate-100 flex items-center justify-between text-[11px] font-mono">
                <span class="text-slate-400">Classificação</span>
                <span class="${{isActive ? 'text-indigo-600 font-bold' : 'text-slate-400'}}">${{isActive ? 'Ativa ●' : 'Ver ativos ➜'}}</span>
              </div>
            </div>
          `;
        }}).join('');
      }}

      // 2. Atualizar títulos e dados da categoria ativa
      const activeTitleEl = document.getElementById('catActiveTitle');
      const activeCountEl = document.getElementById('catActiveCount');
      const activeRationaleEl = document.getElementById('catActiveRationale');
      const tableTitleEl = document.getElementById('catTableTitle');
      const tableSubtitleEl = document.getElementById('catTableSubtitle');

      if (activeTitleEl) activeTitleEl.innerHTML = `<span>${{activeDef.icon}}</span> ${{activeDef.name.toUpperCase()}}`;
      if (activeCountEl) activeCountEl.innerText = `${{pStocks.length}} ativos qualificados`;
      if (activeRationaleEl) activeRationaleEl.innerText = activeDef.rationale;
      if (tableTitleEl) tableTitleEl.innerHTML = `<span>${{activeDef.icon}}</span> ATIVOS EM: ${{activeDef.name.toUpperCase()}}`;
      if (tableSubtitleEl) tableSubtitleEl.innerText = `(${{pStocks.length}} ativos enquadrados na B3)`;

      // 3. Médias Ponderadas / Indicadores Estatísticos
      let sumPl = 0, countPl = 0;
      let sumRoic = 0, countRoic = 0;
      let sumDy = 0, countDy = 0;
      let sumSpread = 0, countSpread = 0;
      let sumScore = 0;

      pStocks.forEach(s => {{
        sumScore += s.quality_score || 0;
        if (s.pl && s.pl > 0 && s.pl < 60) {{
          sumPl += s.pl;
          countPl++;
        }}
        const roicVal = s.roic || s.roe || 0;
        if (roicVal > 0) {{
          sumRoic += roicVal;
          countRoic++;
        }}
        if (s.div_yield && s.div_yield > 0) {{
          sumDy += s.div_yield;
          countDy++;
        }}
        if (s.ey_spread !== null && s.ey_spread !== undefined) {{
          sumSpread += s.ey_spread;
          countSpread++;
        }}
      }});

      const avgPl = countPl > 0 ? (sumPl / countPl) : 0;
      const avgRoic = countRoic > 0 ? (sumRoic / countRoic) : 0;
      const avgDy = countDy > 0 ? (sumDy / countDy) : 0;
      const avgSpread = countSpread > 0 ? (sumSpread / countSpread) : 0;
      const avgScore = pStocks.length > 0 ? (sumScore / pStocks.length) : 0;

      const elTotal = document.getElementById('kp-cat-total');
      if (elTotal) elTotal.innerText = pStocks.length + ' ativos';

      const elPl = document.getElementById('kp-cat-pl');
      if (elPl) {{
        elPl.innerText = avgPl > 0 ? avgPl.toFixed(1) + 'x' : 'N/D';
        elPl.className = 'text-base font-bold font-mono ' + getColorPl(avgPl);
      }}

      const elRoic = document.getElementById('kp-cat-roic');
      if (elRoic) {{
        elRoic.innerText = avgRoic > 0 ? (avgRoic * 100).toFixed(1) + '%' : 'N/D';
        elRoic.className = 'text-base font-bold font-mono ' + getColorRoe(avgRoic);
      }}

      const elDy = document.getElementById('kp-cat-dy');
      if (elDy) {{
        elDy.innerText = avgDy > 0 ? (avgDy * 100).toFixed(1) + '%' : 'N/D';
        elDy.className = 'text-base font-bold font-mono ' + getColorDy(avgDy);
      }}

      const elSpread = document.getElementById('kp-cat-spread');
      if (elSpread) {{
        elSpread.innerText = countSpread > 0 ? (avgSpread > 0 ? '+' : '') + avgSpread.toFixed(1) + '%' : 'N/D';
        elSpread.className = 'text-base font-bold font-mono ' + getColorSpread(avgSpread);
      }}

      const elScore = document.getElementById('kp-cat-score');
      if (elScore) {{
        elScore.innerText = avgScore > 0 ? avgScore.toFixed(1) + ' pts' : 'N/D';
        elScore.className = 'text-base font-bold font-mono ' + (avgScore >= 80 ? 'text-emerald-700' : (avgScore >= 65 ? 'text-indigo-800' : 'text-slate-800'));
      }}

      // 4. Renderizar Tabela de Ativos da Categoria
      const tbody = document.getElementById('portStocksTableBody');
      if (!tbody) return;
      tbody.innerHTML = '';

      if (pStocks.length === 0) {{
        tbody.innerHTML = `
          <tr>
            <td colspan="9" class="py-8 text-center text-slate-500 font-mono text-xs">
              Nenhuma empresa atende simultaneamente aos critérios desta categoria com liquidez diária ≥ R$ 1 Milhão.
            </td>
          </tr>
        `;
        return;
      }}

      pStocks.forEach((s, idx) => {{
        const tr = document.createElement('tr');
        const rowBg = idx % 2 === 0 ? 'bg-white' : 'bg-slate-50/40';
        tr.className = `${{rowBg}} hover:bg-indigo-50/30 transition cursor-pointer`;
        tr.onclick = (e) => {{
          if (e.target.closest('button')) return;
          selectTicker(s.ticker);
          openDossierDrawer(s.ticker);
        }};

        let debtDisplay = 'N/D';
        let debtClass = getColorDebt(s.div_liq_ebitda, s.is_financial);
        if (s.is_financial) {{
          debtDisplay = 'Banco (Basileia)';
        }} else if (s.details && s.details.divida_liquida !== null && s.details.divida_liquida <= 0) {{
          debtDisplay = 'Caixa Líq. 🛡️';
        }} else if (s.div_liq_ebitda !== null) {{
          debtDisplay = s.div_liq_ebitda.toFixed(1) + 'x';
        }}

        const scoreBadgeClass = s.quality_score >= 80 ? 'bg-emerald-50 text-emerald-900 border border-emerald-300 font-bold' : (s.quality_score >= 65 ? 'bg-slate-100 text-slate-800 border border-slate-300 font-bold' : 'bg-slate-50 text-slate-700 border border-slate-200');

        // Todas as categorias atribuídas à ação (máximo 5)
        const categories = getStockCategories(s);
        const tagsHtml = categories.map(c => `
          <button onclick="event.stopPropagation(); selectPortfolio('${{c.id}}')" class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-mono font-bold ${{c.bgClass}} hover:brightness-110 transition cursor-pointer" title="Ver todos os ativos de ${{c.label}}">
            <span>${{c.icon}}</span> <span>${{c.shortLabel || c.label}}</span>
          </button>
        `).join('');

        tr.innerHTML = `
          <td class="py-2.5 px-3">
            <div class="flex items-center gap-2.5">
              ${{getStockLogoHtml(s.ticker, s.empresa, 'w-7 h-7')}}
              <div class="flex flex-col min-w-0">
                <div class="flex items-center gap-1.5">
                  <span class="text-sm font-bold text-slate-900 tracking-wide font-mono">${{s.ticker}}</span>
                  <span class="text-[9px] px-1.5 py-0.2 rounded-full font-mono font-bold ${{s.is_latest_balanco ? 'bg-emerald-50 text-emerald-800 border border-emerald-200' : 'bg-slate-100 text-slate-600 border border-slate-200'}}">${{s.tri_balanco}}</span>
                </div>
                <div class="text-[11px] text-slate-600 font-sans truncate max-w-[150px]" title="${{s.empresa}} - ${{s.setor}}">${{s.empresa}}</div>
                <div class="text-[10px] text-slate-400 font-sans">${{s.setor || ''}}</div>
              </div>
            </div>
          </td>
          <td class="py-2.5 px-3 text-right font-mono font-bold text-slate-900">${{formatCurrency(s.cotacao)}}</td>
          <td class="py-2.5 px-2 text-center">
            <span class="px-2.5 py-0.5 rounded-full font-bold text-xs ${{scoreBadgeClass}}">
              ${{s.quality_score.toFixed(1)}}
            </span>
          </td>
          <td class="py-2.5 px-3 text-right font-mono font-semibold ${{getColorPl(s.pl)}}">${{formatMultiple(s.pl)}}</td>
          <td class="py-2.5 px-3 text-right font-mono font-semibold ${{getColorRoe(s.roic || s.roe)}}">${{formatPercent(s.roic || s.roe)}}${{s.is_financial ? ' <span class=\"text-[9px] text-indigo-800 font-normal\">(ROE)</span>' : ''}}</td>
          <td class="py-2.5 px-3 text-right font-mono font-bold ${{getColorDy(s.div_yield)}}">${{formatPercent(s.div_yield)}}</td>
          <td class="py-2.5 px-3 text-right font-mono ${{debtClass}}">${{debtDisplay}}</td>
          <td class="py-2.5 px-3.5">
            <div class="flex flex-wrap items-center gap-1.5 max-w-[320px]">
              ${{tagsHtml}}
            </div>
          </td>
          <td class="py-2.5 px-3 text-center">
            <div class="flex items-center justify-center gap-1.5">
              <button onclick="event.stopPropagation(); selectTicker('${{s.ticker}}'); openDossierDrawer('${{s.ticker}}');" class="px-2 py-1 rounded-md text-[10px] font-mono font-bold bg-slate-100 hover:bg-slate-200 text-slate-700 transition cursor-pointer" title="Abrir Dossiê 360°">
                Dossiê 360°
              </button>
              <button onclick="event.stopPropagation(); openDedicatedCompanyPage('${{s.ticker}}');" class="p-1 rounded-md text-emerald-700 hover:bg-emerald-50 transition cursor-pointer" title="Página Completa da Empresa">
                <svg class="w-3.5 h-3.5 stroke-[2]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/></svg>
              </button>
            </div>
          </td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    let isTableFullWidth = true;"""

if pattern_portfolio_logic.search(code):
    code = pattern_portfolio_logic.sub(new_portfolio_logic, code, count=1)
    print("[OK] Logica completa do Hub de Categorias Quantitativas implementada com sucesso!")
else:
    print("! Erro ao localizar logica de portfolios com regex!")

with open("build_standalone_html.py", "w", encoding="utf-8") as f:
    f.write(code)

print("\nbuild_standalone_html.py gravado com sucesso.")
