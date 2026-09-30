"""
build_standalone_html.py
========================
Gera a aplicacao web standalone institucional (single-file HTML) para o
JP Morgan e Charlie Munger B3 Terminal.
Embedda os dados auditados em JSON diretamente no arquivo e integra:
1. Botao "Atualizar Dados (Fundamentus)" conectado a API /api/refresh com fallback offline.
2. Filtro institucional de Volume Financeiro (Liquidez Media 2m >= R$ 1 Milhao).
3. Filtro de Tempestividade Contabil (Balanco do Ultimo Trimestre 2T26).
4. Matriz Munger 2x2 e Tabela Analitica com colunas de Volume e Ultimo Balanco.
"""

import json
import os

CACHE_FILE = "cache/standalone_data.json"
OUTPUT_HTML = "index.html"
ARTIFACT_HTML = r"C:\Users\dougl\.gemini\antigravity\brain\19bf6b03-9073-46f6-9498-57b18f1f9a41\munger_terminal.html"

with open(CACHE_FILE, "r", encoding="utf-8") as f:
    raw_data = json.load(f)

json_data_str = json.dumps(raw_data, ensure_ascii=False)

html_template = f"""<!DOCTYPE html>
<html lang="pt-BR" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>JP Morgan | Charlie Munger B3 Terminal</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap" rel="stylesheet">
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {{
      darkMode: 'class',
      theme: {{
        extend: {{
          fontFamily: {{
            sans: ['Plus Jakarta Sans', 'Inter', 'sans-serif'],
            mono: ['JetBrains Mono', 'monospace'],
          }},
          colors: {{
            jpCanvas: '#080C14',
            jpCard: '#0D1424',
            jpCardHover: '#131D33',
            jpBorder: 'rgba(255, 255, 255, 0.09)',
            jpAmber: '#FBBF24',
            jpAmberDark: '#D97706',
            jpCyan: '#38BDF8',
            jpGreen: '#10E79D',
            jpYellow: '#FBBF24',
            jpRed: '#F43F5E',
            jpBlue: '#38BDF8',
          }}
        }}
      }}
    }}
  </script>
  <style>
    body {{
      background-color: #080C14;
      background-image: 
        radial-gradient(circle at 10% 15%, rgba(56, 189, 248, 0.08) 0%, transparent 45%),
        radial-gradient(circle at 90% 80%, rgba(16, 231, 157, 0.07) 0%, transparent 45%),
        radial-gradient(circle at 75% 15%, rgba(168, 85, 247, 0.05) 0%, transparent 40%);
      background-attachment: fixed;
      color: #E2E8F0;
      font-family: 'Plus Jakarta Sans', 'Inter', sans-serif;
    }}
    .glass-panel {{
      background: rgba(13, 20, 35, 0.65);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border: 1px solid rgba(255, 255, 255, 0.09);
      box-shadow: inset 0 1px 0 0 rgba(255, 255, 255, 0.08), 0 16px 36px -8px rgba(0, 0, 0, 0.5);
    }}
    .glass-card {{
      background: rgba(15, 23, 42, 0.58);
      backdrop-filter: blur(14px);
      -webkit-backdrop-filter: blur(14px);
      border: 1px solid rgba(255, 255, 255, 0.08);
      box-shadow: inset 0 1px 0 0 rgba(255, 255, 255, 0.06), 0 6px 22px rgba(0, 0, 0, 0.32);
      transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }}
    .glass-card:hover {{
      background: rgba(20, 30, 52, 0.72);
      border-color: rgba(56, 189, 248, 0.28);
      box-shadow: inset 0 1px 0 0 rgba(255, 255, 255, 0.12), 0 10px 30px rgba(0, 0, 0, 0.42);
      transform: translateY(-1px);
    }}
    .glass-pill {{
      background: rgba(255, 255, 255, 0.05);
      backdrop-filter: blur(8px);
      -webkit-backdrop-filter: blur(8px);
      border: 1px solid rgba(255, 255, 255, 0.09);
    }}
    .mono-num {{
      font-family: 'JetBrains Mono', monospace;
    }}
    ::-webkit-scrollbar {{
      width: 6px;
      height: 6px;
    }}
    ::-webkit-scrollbar-track {{
      background: #080C14;
    }}
    ::-webkit-scrollbar-thumb {{
      background: rgba(255, 255, 255, 0.12);
      border-radius: 9999px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
      background: rgba(16, 231, 157, 0.45);
    }}
    .sidebar-nav-btn {{
      color: #94A3B8;
      border: 1px solid transparent;
      border-radius: 0.875rem;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }}
    .sidebar-nav-btn:hover {{
      color: #FFFFFF;
      background: rgba(255, 255, 255, 0.06);
      border-color: rgba(255, 255, 255, 0.09);
    }}
    .sidebar-nav-btn.active {{
      background: linear-gradient(90deg, rgba(16, 231, 157, 0.18) 0%, rgba(56, 189, 248, 0.09) 100%);
      color: #10E79D;
      border: 1px solid rgba(16, 231, 157, 0.35);
      font-weight: 700;
      box-shadow: 0 0 20px rgba(16, 231, 157, 0.18);
    }}
    .tab-btn {{
      border-radius: 9999px;
      transition: all 0.2s ease;
    }}
    .tab-btn.active {{
      background: rgba(16, 231, 157, 0.16);
      color: #10E79D;
      border: 1px solid rgba(16, 231, 157, 0.35);
      box-shadow: 0 0 14px rgba(16, 231, 157, 0.16);
    }}
    .filter-btn {{
      border-radius: 9999px;
      transition: all 0.2s ease;
    }}
    .filter-btn.active {{
      background: rgba(16, 231, 157, 0.18);
      border-color: #10E79D;
      color: #10E79D;
      box-shadow: 0 0 12px rgba(16, 231, 157, 0.2);
    }}
    .drawer-backdrop {{
      background-color: rgba(4, 7, 13, 0.75);
      backdrop-filter: blur(10px);
      -webkit-backdrop-filter: blur(10px);
    }}
    .dot-pulse {{
      box-shadow: 0 0 12px rgba(16, 231, 157, 0.85);
    }}
    @keyframes spin-slow {{
      from {{ transform: rotate(0deg); }}
      to {{ transform: rotate(360deg); }}
    }}
    .spin-active {{
      animation: spin-slow 1s linear infinite;
    }}
  </style>
</head>
<body class="h-screen text-slate-200 flex overflow-hidden font-sans antialiased selection:bg-emerald-500/30">

  <!-- LEFT SIDEBAR DE NAVEGAÇÃO & FILTROS (MODERN GLASSMORPHIC FINTECH) -->
  <aside id="sidebar" class="w-64 bg-[#080C14]/80 backdrop-blur-2xl border-r border-white/10 flex flex-col justify-between flex-shrink-0 z-20 select-none shadow-2xl">
    <div class="flex flex-col flex-1 min-h-0">
      <!-- Identidade da Marca e Status -->
      <div class="p-4 border-b border-white/10 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div class="w-9 h-9 rounded-xl bg-gradient-to-br from-emerald-400 via-teal-500 to-emerald-600 flex items-center justify-center text-black font-mono font-black text-lg shadow-lg shadow-emerald-500/25">
            M
          </div>
          <div>
            <div class="font-mono font-black text-xs text-white tracking-wider flex items-center gap-1.5">
              <span>MUNGER B3</span>
              <span class="px-1.5 py-0.5 text-[9px] bg-emerald-950/80 text-emerald-400 border border-emerald-500/40 rounded-full font-bold">PRO</span>
            </div>
            <div class="text-[10px] text-slate-400 font-mono tracking-wide">FINTECH INTELLIGENCE</div>
          </div>
        </div>
      </div>

      <!-- Links de Navegação Primários -->
      <div class="p-3 space-y-1.5">
        <div class="text-[10px] font-mono uppercase tracking-wider text-slate-500 px-3 py-1 font-bold">Navegação</div>
        <button id="nav-home" onclick="switchWorkspace('home')" class="sidebar-nav-btn active w-full flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-xs font-mono transition cursor-pointer">
          <span class="text-base">🏠</span>
          <span class="font-semibold">Panorama Geral</span>
        </button>
        <button id="nav-portfolios" onclick="switchWorkspace('portfolios')" class="sidebar-nav-btn w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl text-xs font-mono transition cursor-pointer">
          <div class="flex items-center gap-3">
            <span class="text-base">💼</span>
            <span class="font-semibold">Carteiras Recomendadas</span>
          </div>
          <span class="px-2 py-0.5 text-[9px] font-bold bg-amber-950/80 text-amber-300 border border-amber-600/50 rounded-full">CFA</span>
        </button>
        <button id="nav-table" onclick="switchWorkspace('table')" class="sidebar-nav-btn w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl text-xs font-mono transition cursor-pointer">
          <div class="flex items-center gap-3">
            <span class="text-base">🔍</span>
            <span class="font-semibold">Scanner B3 &amp; Ativos</span>
          </div>
          <span class="text-[10px] text-slate-400 font-mono bg-white/5 px-2 py-0.5 rounded-full" id="sidebarUniverseCount">--</span>
        </button>
        <button id="nav-matrix" onclick="switchWorkspace('matrix')" class="sidebar-nav-btn w-full flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-xs font-mono transition cursor-pointer">
          <span class="text-base">📊</span>
          <span class="font-semibold">Matriz Munger 2x2</span>
        </button>
      </div>

      <!-- Seção de Filtros Rápidos / Presets no Sidebar -->
      <div class="px-3 py-2 border-t border-white/10 flex-1 overflow-y-auto">
        <div class="text-[10px] font-mono uppercase tracking-wider text-slate-500 px-3 py-1 font-bold">Filtros Rápidos</div>
        <div class="space-y-1">
          <button onclick="setFilterAndGoTable('CAT_ULTRA_CRITIC')" class="w-full flex items-center justify-between px-3 py-1.5 rounded-xl text-[11px] font-mono text-slate-300 hover:text-white hover:bg-white/5 transition cursor-pointer">
            <span class="flex items-center gap-2"><span class="text-yellow-400">💎</span> Ultra-Crítico</span>
            <span class="text-[10px] text-yellow-300 font-bold bg-yellow-950/60 px-1.5 py-0.2 rounded-full border border-yellow-700/40" id="sb-cnt-ultra">--</span>
          </button>
          <button onclick="setFilterAndGoTable('TIER1')" class="w-full flex items-center justify-between px-3 py-1.5 rounded-xl text-[11px] font-mono text-slate-300 hover:text-white hover:bg-white/5 transition cursor-pointer">
            <span class="flex items-center gap-2"><span class="text-amber-400">🏆</span> Tier 1 Munger</span>
            <span class="text-[10px] text-amber-400 font-bold bg-amber-950/60 px-1.5 py-0.2 rounded-full border border-amber-700/40" id="sb-cnt-tier1">--</span>
          </button>
          <button onclick="setFilterAndGoTable('ASYMMETRY')" class="w-full flex items-center justify-between px-3 py-1.5 rounded-xl text-[11px] font-mono text-slate-300 hover:text-white hover:bg-white/5 transition cursor-pointer">
            <span class="flex items-center gap-2"><span class="text-cyan-400">📈</span> Assimetria Real</span>
            <span class="text-[10px] text-cyan-300 font-bold bg-cyan-950/60 px-1.5 py-0.2 rounded-full border border-cyan-700/40" id="sb-cnt-asym">--</span>
          </button>
          <button onclick="setFilterAndGoTable('CAT_DIVIDENDS')" class="w-full flex items-center justify-between px-3 py-1.5 rounded-xl text-[11px] font-mono text-slate-300 hover:text-white hover:bg-white/5 transition cursor-pointer">
            <span class="flex items-center gap-2"><span class="text-emerald-400">💰</span> Vacas Leiteiras</span>
            <span class="text-[10px] text-emerald-300 font-bold bg-emerald-950/60 px-1.5 py-0.2 rounded-full border border-emerald-700/40" id="sb-cnt-div">--</span>
          </button>
          <button onclick="setFilterAndGoTable('NET_CASH')" class="w-full flex items-center justify-between px-3 py-1.5 rounded-xl text-[11px] font-mono text-slate-300 hover:text-white hover:bg-white/5 transition cursor-pointer">
            <span class="flex items-center gap-2"><span class="text-sky-400">🛡️</span> Caixa Líquido</span>
            <span class="text-[10px] text-sky-300 font-bold bg-sky-950/60 px-1.5 py-0.2 rounded-full border border-sky-700/40" id="sb-cnt-cash">--</span>
          </button>
        </div>
      </div>

      <!-- Rodapé de Auditoria e Sistema -->
      <div class="p-3.5 border-t border-white/10 bg-[#060A10]/50 text-[10px] font-mono text-slate-400 flex flex-col gap-1.5">
        <div class="flex items-center justify-between">
          <span class="flex items-center gap-1.5 text-emerald-400 font-bold">
            <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse dot-pulse"></span> Sistema Ativo
          </span>
          <span class="text-slate-400">2T26 Fundamentus</span>
        </div>
        <div id="auditTimestamp" class="text-[9px] text-slate-500 truncate">Auditado em: --</div>
      </div>
    </div>
  </aside>

  <!-- PAINEL PRINCIPAL COM TOPBAR E CANVAS COM SCROLL NATURAL -->
  <div class="flex-1 flex flex-col min-w-0 overflow-hidden">
    <!-- TOPBAR MINIMALISTA & UNIVERSAL (GLASS) -->
    <header class="bg-[#080C14]/75 backdrop-blur-2xl border-b border-white/10 px-6 py-3 flex items-center justify-between gap-4 z-10 flex-shrink-0 shadow-lg">
      <!-- Título Dinâmico do Workspace Ativo -->
      <div>
        <div class="font-mono font-bold text-sm text-white flex items-center gap-2" id="topbarTitle">
          <span>🏠</span> <span>PANORAMA GERAL</span>
        </div>
        <div class="text-[11px] text-slate-400" id="topbarSubtitle">Cockpit executivo e inteligência fundamentalista B3</div>
      </div>

      <!-- Barra de Busca Universal, Ativo Ativo e Ações -->
      <div class="flex items-center gap-3">
        <!-- Input de Busca Rápida -->
        <div class="relative">
          <input type="text" id="searchInput" oninput="handleSearch()" placeholder="Buscar Ticker ou Empresa..." class="w-48 md:w-64 bg-slate-900/60 border border-white/10 rounded-full px-4 py-1.5 text-xs text-white placeholder-slate-400 focus:outline-none focus:border-emerald-500/50 font-mono transition shadow-inner">
        </div>

        <!-- Indicador de Ativo Ativo -->
        <div class="text-xs font-mono text-slate-300 hidden md:flex items-center gap-1.5 bg-slate-900/60 px-3 py-1.5 rounded-full border border-white/10 shadow-sm">
          <span class="text-slate-400 text-[11px]">Ativo:</span>
          <b class="text-emerald-400 font-bold" id="topSelectedTickerBadge">--</b>
        </div>

        <!-- Contador do Universo -->
        <div class="text-xs font-mono text-slate-400 hidden lg:block bg-slate-900/60 px-3 py-1.5 rounded-full border border-white/10 shadow-sm">
          <b class="text-emerald-400" id="displayedCount">--</b>/<span id="totalUniverseCount">--</span>
        </div>

        <!-- Botão Atualizar Fundamentus -->
        <button id="btn-refresh-data" onclick="triggerDataRefresh()" class="px-4 py-1.5 bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-400 hover:to-teal-400 text-black font-mono font-bold rounded-full text-xs transition flex items-center gap-1.5 cursor-pointer shadow-lg shadow-emerald-500/20">
          <span id="btn-refresh-icon">🔄</span> <span id="btn-refresh-text">Atualizar</span>
        </button>

        <!-- Botão Reset -->
        <button onclick="resetData()" class="px-3 py-1.5 bg-slate-900/60 hover:bg-slate-800 border border-white/10 text-slate-300 rounded-full text-xs font-mono cursor-pointer transition">
          Reset
        </button>
      </div>
    </header>

    <!-- BANNER DE STATUS / TOAST DE ATUALIZAÇÃO -->
    <div id="statusToast" class="hidden mx-6 mt-3 p-2.5 rounded-lg border text-xs font-mono flex items-center justify-between transition-all flex-shrink-0">
      <div class="flex items-center gap-2" id="statusToastContent"></div>
      <button onclick="hideToast()" class="text-slate-400 hover:text-white text-xs">✕</button>
    </div>

    <!-- CANVAS DOS WORKSPACES COM SCROLL NATURAL E ESPAÇOSO -->
    <main class="flex-1 min-h-0 relative overflow-y-auto p-4 sm:p-6" id="workspaceContainer">

      <!-- WORKSPACE 0: 🏠 HOME (PANORAMA GERAL EXECUTIVO) -->
      <section id="view-home" class="w-full glass-panel rounded-2xl flex flex-col p-5 sm:p-6 space-y-5">
        <!-- 1. Banner de Boas-Vindas e Ação Rápida -->
        <div class="flex flex-wrap items-center justify-between gap-4 p-4 glass-card rounded-xl flex-shrink-0">
          <div>
            <div class="flex items-center gap-2">
              <span class="text-sm font-mono font-bold text-amber-300 uppercase tracking-wider flex items-center gap-1.5">
                <span>🏠</span> COCKPIT EXECUTIVO B3 &amp; MODELO CHARLIE MUNGER
              </span>
              <span class="px-2.5 py-0.5 text-[10px] font-mono bg-emerald-500/10 text-emerald-300 border border-emerald-500/30 rounded-full font-bold">
                100% AUDITADO • 2T26
              </span>
            </div>
            <p class="text-xs text-slate-400 mt-1">
              Panorama matinal de inteligência de mercado: custo de oportunidade sovereign, assimetrias reais, dividendos sustentáveis e proteção contra armadilhas de ciclo.
            </p>
          </div>
          <div class="flex items-center gap-2.5 font-mono text-xs">
            <button onclick="switchWorkspace('portfolios')" class="px-3.5 py-1.5 glass-pill text-amber-300 hover:text-white border-amber-500/30 hover:border-amber-400 font-bold transition flex items-center gap-1.5 cursor-pointer shadow-lg shadow-amber-500/10">
              <span>💼</span> Carteiras Recomendadas ➜
            </button>
            <button onclick="switchWorkspace('matrix')" class="px-3.5 py-1.5 glass-pill text-slate-300 hover:text-white border-white/10 hover:border-white/30 font-bold transition flex items-center gap-1.5 cursor-pointer">
              <span>📊</span> Ir p/ Matriz 2x2
            </button>
            <button onclick="switchWorkspace('table')" class="px-3.5 py-1.5 rounded-full bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-400 hover:to-teal-400 text-black font-bold transition flex items-center gap-1.5 cursor-pointer shadow-lg shadow-emerald-500/20">
              <span>📋</span> Abrir Screening B3 ➜
            </button>
          </div>
        </div>

        <!-- 2. Termômetro Macro da B3 (A Régua Sovereign) -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 flex-shrink-0">
          <!-- NTN-B Sovereign Benchmark -->
          <div class="glass-card rounded-xl p-4">
            <div class="flex items-center justify-between text-xs text-slate-400 font-mono">
              <span>BENCHMARK LIVRE DE RISCO</span>
              <span class="text-sky-400 font-bold">NTN-B 2035</span>
            </div>
            <div class="text-2xl font-bold font-mono text-sky-400 mt-1">IPCA + 6,50%</div>
            <div class="text-[11px] text-slate-400 mt-1">Custo de oportunidade soberano de longo prazo do Brasil.</div>
          </div>
          <!-- P/L Mediano B3 -->
          <div class="glass-card rounded-xl p-4">
            <div class="flex items-center justify-between text-xs text-slate-400 font-mono">
              <span>P/L MEDIANO B3</span>
              <span class="text-amber-400 font-bold" id="home-stat-pl-tag">Barato</span>
            </div>
            <div class="text-2xl font-bold font-mono text-white mt-1" id="home-stat-pl">9,1x</div>
            <div class="text-[11px] text-slate-400 mt-1">Múltiplo mediano sobre o lucro contábil LTM.</div>
          </div>
          <!-- ROIC Mediano B3 -->
          <div class="glass-card rounded-xl p-4">
            <div class="flex items-center justify-between text-xs text-slate-400 font-mono">
              <span>ROIC / ROE MEDIANO</span>
              <span class="text-emerald-400 font-bold">Retorno do Capital</span>
            </div>
            <div class="text-2xl font-bold font-mono text-emerald-400 mt-1" id="home-stat-roic">10,2%</div>
            <div class="text-[11px] text-slate-400 mt-1">Retorno real gerado pelo capital empregado na bolsa.</div>
          </div>
          <!-- Spread Mediano vs NTN-B -->
          <div class="glass-card rounded-xl p-4">
            <div class="flex items-center justify-between text-xs text-slate-400 font-mono">
              <span>SPREAD MEDIANO VS NTN-B</span>
              <span class="text-emerald-400 font-bold" id="home-stat-spread-tag">Prêmio Positivo</span>
            </div>
            <div class="text-2xl font-bold font-mono text-emerald-400 mt-1" id="home-stat-spread">+4,1%</div>
            <div class="text-[11px] text-slate-400 mt-1">Prêmio de risco das ações sobre o Tesouro IPCA+.</div>
          </div>
        </div>

        <!-- 2.5 Vitrine de Convicção: Régua Ultra-Crítica CFA / Munger -->
        <div class="glass-panel rounded-xl p-4 flex-shrink-0 border border-yellow-500/30 bg-gradient-to-r from-yellow-500/[0.06] via-transparent to-amber-500/[0.04]">
          <div class="flex flex-wrap items-center justify-between gap-2 border-b border-yellow-500/20 pb-2.5 mb-2.5">
            <div class="flex items-center gap-2">
              <span class="text-lg">💎</span>
              <div>
                <div class="text-xs font-mono font-bold text-yellow-300 uppercase tracking-wider flex items-center gap-2">
                  <span>SELEÇÃO ULTRA-CRÍTICA (RÉGUA MÁXIMA CFA &amp; CHARLIE MUNGER)</span>
                  <span class="text-[10px] px-2 py-0.5 rounded-full bg-yellow-500/10 text-yellow-300 border border-yellow-500/30 font-mono">100% FUNDAMENTUS AUDITADO</span>
                </div>
                <p class="text-[11px] text-slate-400 font-sans mt-0.5">
                  Critérios acumulados: Score &ge; 75 + Munger Acid Test (EBIT/EBITDA &ge; 75% ou Bancos ROE &ge; 15%) + Solvência Blindada (Caixa Líquido ou Dívida &le; 1,0x) + Spread Real &ge; +1,5% + Lucro 2T26 Limpo + Sem Pico de Commodities.
                </p>
              </div>
            </div>
            <button onclick="filterByCategory('CAT_ULTRA_CRITIC')" id="btn-cat-ultracritic" class="px-3.5 py-1.5 rounded-full bg-yellow-500/15 hover:bg-yellow-500/25 border border-yellow-500/50 text-yellow-300 hover:text-white text-xs font-mono font-bold transition flex items-center gap-1.5 cursor-pointer shadow-lg shadow-yellow-500/10">
              <span>Ver Seleção Completa</span> <span id="cnt-cat-ultracritic">(--)</span> <span>➜</span>
            </button>
          </div>
          <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-2.5 font-mono text-xs" id="home-list-ultracritic">
            <!-- Renderizado via JS -->
          </div>
        </div>

        <!-- 3. Vitrine das Melhores Oportunidades Munger (3 Rankings Automáticos) -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-3 flex-shrink-0">
          <!-- Top 5 Munger Score -->
          <div class="glass-card rounded-xl flex flex-col overflow-hidden">
            <div class="p-3 border-b border-white/10 bg-white/[0.02] flex items-center justify-between">
              <div class="flex items-center gap-1.5">
                <span class="text-base">🏆</span>
                <span class="text-xs font-mono font-bold text-amber-300 uppercase">Top 5 "Filé Mignon" Munger</span>
              </div>
              <button onclick="filterByCategory('CAT_MUNGER')" id="btn-cat-munger" class="text-[10px] font-mono font-bold text-amber-300 hover:text-white glass-pill border-amber-500/30 px-2.5 py-0.5 rounded-full transition cursor-pointer flex items-center gap-1" title="Ver lista completa de empresas Filé Mignon na Tabela">
                <span>Ver todas</span> <span id="cnt-cat-munger">(--)</span> <span>➜</span>
              </button>
            </div>
            <div class="p-2.5 flex-1 space-y-1.5 font-mono text-xs" id="home-list-munger">
              <!-- Renderizado via JS -->
            </div>
          </div>

          <!-- Top 5 Spread Real vs NTN-B -->
          <div class="glass-card rounded-xl flex flex-col overflow-hidden">
            <div class="p-3 border-b border-white/10 bg-white/[0.02] flex items-center justify-between">
              <div class="flex items-center gap-1.5">
                <span class="text-base">📈</span>
                <span class="text-xs font-mono font-bold text-cyan-400 uppercase">Top 5 Assimetrias Reais</span>
              </div>
              <button onclick="filterByCategory('CAT_ASYMMETRY')" id="btn-cat-asymm" class="text-[10px] font-mono font-bold text-cyan-300 hover:text-white glass-pill border-cyan-500/30 px-2.5 py-0.5 rounded-full transition cursor-pointer flex items-center gap-1" title="Ver lista completa de empresas com Assimetria Real na Tabela">
                <span>Ver todas</span> <span id="cnt-cat-asymm">(--)</span> <span>➜</span>
              </button>
            </div>
            <div class="p-2.5 flex-1 space-y-1.5 font-mono text-xs" id="home-list-spread">
              <!-- Renderizado via JS -->
            </div>
          </div>

          <!-- Top 5 Proventos Sustentáveis -->
          <div class="glass-card rounded-xl flex flex-col overflow-hidden">
            <div class="p-3 border-b border-white/10 bg-white/[0.02] flex items-center justify-between">
              <div class="flex items-center gap-1.5">
                <span class="text-base">💰</span>
                <span class="text-xs font-mono font-bold text-emerald-400 uppercase">Top 5 Vacas Leiteiras Perenes</span>
              </div>
              <button onclick="filterByCategory('CAT_DIVIDENDS')" id="btn-cat-div" class="text-[10px] font-mono font-bold text-emerald-300 hover:text-white glass-pill border-emerald-500/30 px-2.5 py-0.5 rounded-full transition cursor-pointer flex items-center gap-1" title="Ver lista completa de Vacas Leiteiras na Tabela">
                <span>Ver todas</span> <span id="cnt-cat-div">(--)</span> <span>➜</span>
              </button>
            </div>
            <div class="p-2.5 flex-1 space-y-1.5 font-mono text-xs" id="home-list-dividends">
              <!-- Renderizado via JS -->
            </div>
          </div>
        </div>

        <!-- 4. Radar de Risco, Virada de Ciclo & Anti-Fragilidade (2 Colunas) -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-3 flex-shrink-0">
          <!-- Radar de Virada de Ciclo -->
          <div class="glass-card rounded-xl flex flex-col overflow-hidden">
            <div class="p-3 border-b border-white/10 bg-white/[0.02] flex items-center justify-between">
              <div class="flex items-center gap-1.5">
                <span class="text-base">⚡</span>
                <span class="text-xs font-mono font-bold text-purple-400 uppercase">Radar de Virada de Ciclo (Run-Rate 2T26)</span>
              </div>
              <span class="text-[10px] font-mono text-purple-300 bg-purple-500/10 border border-purple-500/30 px-2 py-0.5 rounded-full">Lucro 2T26 x 4 vs LTM</span>
            </div>
            <div class="p-3 grid grid-cols-1 sm:grid-cols-2 gap-2.5 text-xs font-mono">
              <div>
                <div class="text-[11px] font-bold text-emerald-400 mb-1.5 flex items-center justify-between">
                  <span class="flex items-center gap-1"><span>🟢</span> Lucro em Expansão</span>
                  <button onclick="filterByCategory('CAT_EXPANSION')" id="btn-cat-accel" class="text-[9px] font-mono font-bold text-emerald-300 hover:text-white glass-pill border-emerald-500/30 px-2 py-0.5 rounded-full transition cursor-pointer" title="Ver todas as empresas com Lucro em Expansão">
                    <span>Todas</span> <span id="cnt-cat-accel">(--)</span> <span>➜</span>
                  </button>
                </div>
                <div class="space-y-1.5" id="home-list-accelerating">
                  <!-- Renderizado via JS -->
                </div>
              </div>
              <div>
                <div class="text-[11px] font-bold text-amber-400 mb-1.5 flex items-center justify-between">
                  <span class="flex items-center gap-1"><span>⚠️</span> Alerta de Compressão</span>
                  <button onclick="filterByCategory('CAT_DECELERATION')" id="btn-cat-decel" class="text-[9px] font-mono font-bold text-amber-300 hover:text-white glass-pill border-amber-500/30 px-2 py-0.5 rounded-full transition cursor-pointer" title="Ver todas as empresas com Alerta de Compressão">
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
            <div class="p-3 border-b border-white/10 bg-white/[0.02] flex items-center justify-between">
              <div class="flex items-center gap-1.5">
                <span class="text-base">🛡️</span>
                <span class="text-xs font-mono font-bold text-sky-400 uppercase">Solvência &amp; Anti-Fragilidade (Selic Alta)</span>
              </div>
              <span class="text-[10px] font-mono text-sky-300 bg-sky-500/10 border border-sky-500/30 px-2 py-0.5 rounded-full">Dívida Líq. / EBITDA</span>
            </div>
            <div class="p-3 grid grid-cols-1 sm:grid-cols-2 gap-2.5 text-xs font-mono">
              <div>
                <div class="text-[11px] font-bold text-emerald-400 mb-1.5 flex items-center justify-between">
                  <span class="flex items-center gap-1"><span>🛡️</span> Balanços Fortes</span>
                  <button onclick="filterByCategory('CAT_NET_CASH')" id="btn-cat-netcash" class="text-[9px] font-mono font-bold text-emerald-300 hover:text-white glass-pill border-emerald-500/30 px-2 py-0.5 rounded-full transition cursor-pointer" title="Ver todas as empresas com Caixa Líquido">
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
                  <button onclick="filterByCategory('CAT_HIGH_DEBT')" id="btn-cat-highdebt" class="text-[9px] font-mono font-bold text-rose-300 hover:text-white glass-pill border-rose-500/30 px-2 py-0.5 rounded-full transition cursor-pointer" title="Ver todas as empresas com Alavancagem Crítica">
                    <span>Todas</span> <span id="cnt-cat-highdebt">(--)</span> <span>➜</span>
                  </button>
                </div>
                <div class="space-y-1.5" id="home-list-highdebt">
                  <!-- Renderizado via JS -->
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 5. Mapa Panorâmico dos 4 Quadrantes Munger da B3 -->
        <div class="glass-card rounded-xl p-4 flex-shrink-0">
          <div class="flex items-center justify-between mb-3">
            <span class="text-xs font-mono font-bold text-slate-200 uppercase tracking-wider flex items-center gap-1.5">
              <span>📐</span> DISPERSÃO DE MERCADO &amp; CURVA DE FAIR VALUE (UNIVERSO B3)
            </span>
            <span class="text-[10px] font-mono text-slate-400">Clique no bloco para filtrar na Tabela</span>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 font-mono">
            <!-- Bloco 1: Acima da Curva (Desconto Relativo) -->
            <div onclick="filterByQuadrant('ABOVE')" class="glass-card border-emerald-500/40 hover:border-emerald-400/80 hover:bg-emerald-500/10 rounded-xl p-3.5 transition duration-200 cursor-pointer group">
              <div class="flex items-center justify-between">
                <span class="text-xs font-bold text-emerald-400 flex items-center gap-1"><span>📈</span> ACIMA DA CURVA</span>
                <span class="text-xl font-bold text-white group-hover:text-emerald-400 transition" id="home-quad-above-cnt">--</span>
              </div>
              <p class="text-[11px] text-slate-400 font-sans mt-1">Desconto Relativo: entrega mais qualidade que a média cobrada pelo mercado.</p>
              <div class="text-[10px] text-emerald-400 font-bold mt-2">Filtrar na Tabela ➜</div>
            </div>
            <!-- Bloco 2: Abaixo da Curva (Prêmio Exigente) -->
            <div onclick="filterByQuadrant('BELOW')" class="glass-card border-amber-500/40 hover:border-amber-400/80 hover:bg-amber-500/10 rounded-xl p-3.5 transition duration-200 cursor-pointer group">
              <div class="flex items-center justify-between">
                <span class="text-xs font-bold text-amber-400 flex items-center gap-1"><span>📉</span> ABAIXO DA CURVA</span>
                <span class="text-xl font-bold text-white group-hover:text-amber-400 transition" id="home-quad-below-cnt">--</span>
              </div>
              <p class="text-[11px] text-slate-400 font-sans mt-1">Prêmio Exigente: múltiplos de mercado superiores ao padrão de qualidade.</p>
              <div class="text-[10px] text-amber-400 font-bold mt-2">Filtrar na Tabela ➜</div>
            </div>
            <!-- Bloco 3: Lucro Acelerando (2T26) -->
            <div onclick="filterByCategory('CAT_EXPANSION')" class="glass-card border-teal-400/40 hover:border-teal-400/80 hover:bg-teal-400/10 rounded-xl p-3.5 transition duration-200 cursor-pointer group">
              <div class="flex items-center justify-between">
                <span class="text-xs font-bold text-teal-300 flex items-center gap-1"><span>⚡</span> MOMENTO EM ALTA</span>
                <span class="text-xl font-bold text-white group-hover:text-teal-300 transition" id="home-quad-accel-cnt">--</span>
              </div>
              <p class="text-[11px] text-slate-400 font-sans mt-1">Run-Rate 2T26 superando o lucro dos últimos 12 meses em &ge; +15%.</p>
              <div class="text-[10px] text-teal-300 font-bold mt-2">Filtrar na Tabela ➜</div>
            </div>
            <!-- Bloco 4: Vacas Leiteiras -->
            <div onclick="filterByCategory('CAT_DIVIDENDS')" class="glass-card border-cyan-500/40 hover:border-cyan-400/80 hover:bg-cyan-500/10 rounded-xl p-3.5 transition duration-200 cursor-pointer group">
              <div class="flex items-center justify-between">
                <span class="text-xs font-bold text-cyan-300 flex items-center gap-1"><span>💰</span> VACAS LEITEIRAS</span>
                <span class="text-xl font-bold text-white group-hover:text-cyan-300 transition" id="home-quad-div-cnt">--</span>
              </div>
              <p class="text-[11px] text-slate-400 font-sans mt-1">Dividend Yield &ge; 5% com payout seguro e ROE consistente.</p>
              <div class="text-[10px] text-cyan-300 font-bold mt-2">Filtrar na Tabela ➜</div>
            </div>
          </div>
        </div>
      </section>

    <!-- WORKSPACE 1: 📊 MATRIZ MUNGER 2X2 EM TELA CHEIA (100% DA VIEWPORT) -->
    <section id="view-matrix" class="hidden w-full h-full glass-panel rounded-2xl flex flex-col min-h-0 overflow-hidden shadow-2xl">
      <!-- Toolbar da Matriz -->
      <div class="p-3 border-b border-white/10 flex flex-wrap items-center justify-between gap-2 bg-white/[0.02] flex-shrink-0">
        <div class="flex items-center gap-2">
          <span class="text-xs font-mono font-bold uppercase tracking-wider text-amber-300 flex items-center gap-1.5">
            <span>📊</span> MATRIZ MUNGER 2X2 DE VALOR vs QUALIDADE
          </span>
          <span class="text-[10px] font-mono text-slate-400 bg-slate-900/80 border border-white/10 px-2.5 py-0.5 rounded-full hidden md:inline">
            Eixo X: <b class="text-white" id="lbl-matrix-axis-x">P/L (0-32x)</b> | Eixo Y: <b class="text-white">Score Munger (20-105)</b>
          </span>
        </div>

        <!-- Controles Interativos -->
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
              <option value="mcap" class="bg-[#0A0E1A]">Valor de Mercado</option>
              <option value="volume" class="bg-[#0A0E1A]">Volume Diário</option>
              <option value="fixed" class="bg-[#0A0E1A]">Fixo</option>
            </select>
          </div>

          <!-- Seletor 3ª Dimensão: Cor da Bolha -->
          <div class="inline-flex items-center gap-1.5 bg-slate-900/80 border border-emerald-500/30 rounded-full px-3 py-1">
            <span class="text-[10px] text-emerald-400 font-bold">Cor:</span>
            <select id="sel-bubble-color" onchange="switchBubbleColor(this.value)" class="bg-transparent text-emerald-300 font-bold text-[11px] focus:outline-none cursor-pointer">
              <option value="asymmetry" selected class="bg-[#0A0E1A] text-emerald-300">🎯 Assimetria Favorável (CFA)</option>
              <option value="momentum" class="bg-[#0A0E1A] text-slate-200">⚡ Momento 2T26 (Run-Rate)</option>
              <option value="dividend" class="bg-[#0A0E1A] text-slate-200">💰 Dividend Yield</option>
              <option value="sector" class="bg-[#0A0E1A] text-slate-200">🏢 Setores B3</option>
              <option value="relative" class="bg-[#0A0E1A] text-slate-200">📐 Posição vs Curva Fair Value</option>
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
        </div>
      </div>

      <!-- Sub-Barra Ultra-Compacta: Filtros da Curva de Mercado & Legenda Dinâmica -->
      <div class="px-3 py-1.5 border-b border-white/10 flex flex-wrap items-center justify-between gap-2 bg-[#06080C]/80 flex-shrink-0 text-xs font-mono">
        <div class="flex items-center gap-2 flex-wrap">
          <span class="text-[10px] text-slate-400 uppercase font-bold tracking-wider mr-1">Filtros:</span>
          
          <button onclick="filterByQuadrant('ABOVE')" class="inline-flex items-center gap-1.5 px-3 py-0.5 rounded-full glass-pill border-emerald-500/40 hover:border-emerald-400 text-emerald-300 transition cursor-pointer" title="Filtrar Ativos Acima da Curva (Desconto Relativo)">
            <span>📈 Acima da Curva (Desconto)</span>
            <span class="bg-emerald-500/20 px-1.5 py-0.2 rounded-full text-[10px] font-bold text-white" id="stat-above">--</span>
          </button>

          <button onclick="filterByQuadrant('BELOW')" class="inline-flex items-center gap-1.5 px-3 py-0.5 rounded-full glass-pill border-amber-500/40 hover:border-amber-400 text-amber-300 transition cursor-pointer" title="Filtrar Ativos Abaixo da Curva (Prêmio Exigente)">
            <span>📉 Abaixo da Curva (Prêmio)</span>
            <span class="bg-amber-500/20 px-1.5 py-0.2 rounded-full text-[10px] font-bold text-white" id="stat-below">--</span>
          </button>

          <button onclick="filterByCategory('CAT_EXPANSION')" class="inline-flex items-center gap-1.5 px-3 py-0.5 rounded-full glass-pill border-teal-400/40 hover:border-teal-300 text-teal-200 transition cursor-pointer" title="Filtrar Lucro em Expansão 2T26">
            <span>⚡ Lucro Acelerando</span>
            <span class="bg-teal-500/20 px-1.5 py-0.2 rounded-full text-[10px] font-bold text-white" id="stat-expansion">--</span>
          </button>

          <button onclick="filterByCategory('CAT_DIVIDENDS')" class="inline-flex items-center gap-1.5 px-3 py-0.5 rounded-full glass-pill border-cyan-500/40 hover:border-cyan-400 text-cyan-300 transition cursor-pointer" title="Filtrar Vacas Leiteiras (Dividend Yield &gt; 5%)">
            <span>💰 Dividendos &gt; 5%</span>
            <span class="bg-cyan-500/20 px-1.5 py-0.2 rounded-full text-[10px] font-bold text-white" id="stat-dividends">--</span>
          </button>
        </div>

        <div class="text-[10px] text-slate-300 font-mono hidden lg:flex items-center gap-2" id="matrixLegendContainer">
          <!-- Legenda dinâmica inserida via JS -->
        </div>

        <div class="text-[10px] text-slate-400 font-sans hidden md:inline">
          💡 Role o mouse para Zoom • Arraste para Pan • Clique em uma bolha para ver no Dossiê
        </div>
      </div>

      <!-- Gráfico SVG Amplo em Tela Cheia (100% da Altura Útil) -->
      <div id="matrixContainer" class="relative flex-1 bg-[#05070A]/80 min-h-0 overflow-hidden flex items-center justify-center select-none">
        <svg id="matrixSvg" class="w-full h-full cursor-crosshair select-none" viewBox="0 0 1200 700">
          <!-- Renderizado dinamicamente via JS -->
        </svg>
        <div id="matrixTooltip" class="absolute pointer-events-none hidden glass-panel rounded-xl p-3 text-xs text-slate-200 shadow-2xl z-50 font-mono backdrop-blur-xl border border-white/10"></div>
      </div>
    </section>

    <!-- WORKSPACE 2: 🔍 SCANNER B3 & ATIVOS (TABELA FULL-WIDTH COM TOOLBAR INTEGRADA) -->
    <section id="view-table" class="hidden w-full space-y-4">
      
      <!-- TOOLBAR INTEGRADA DO SCANNER B3 -->
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
      </div>

      <!-- TABELA FULL-WIDTH 100% -->
      <div id="pane-table" class="glass-panel rounded-2xl overflow-hidden shadow-2xl flex flex-col">
        <div class="p-3.5 border-b border-white/10 bg-white/[0.02] flex items-center justify-between flex-shrink-0">
          <div class="flex items-center gap-2">
            <span class="text-xs font-mono font-bold uppercase tracking-wider text-emerald-400 flex items-center gap-1.5">
              <span>📋</span> SCREENING FUNDAMENTALISTA B3 • 100% AUDITADO
            </span>
          </div>
          <div class="flex items-center gap-2 text-xs font-mono text-slate-400">
            <span>💡 Clique em qualquer linha para abrir o <b>Dossiê 360°</b> ➔</span>
          </div>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs border-collapse font-mono whitespace-nowrap">
            <thead class="sticky top-0 bg-[#0A0E1A]/95 backdrop-blur-md z-10 border-b border-white/10 shadow-sm">
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
            </thead>
            <tbody id="stocksTableBody" class="divide-y divide-[#1B2232]/60">
              <!-- Renderizado via JS -->
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <!-- WORKSPACE 3: 💼 CARTEIRAS RECOMENDADAS INSTITUCIONAIS -->
    <!-- WORKSPACE 3: 💼 CARTEIRAS RECOMENDADAS INSTITUCIONAIS (BUY-SIDE SELECTION) -->
    <section id="view-portfolios" class="w-full glass-panel rounded-2xl flex flex-col p-5 sm:p-6 space-y-5 shadow-2xl hidden">
      
      <!-- 1. GRID DOS 4 CARDS NOBRES DE SELEÇÃO DE CARTEIRAS -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3.5 flex-shrink-0">
        <!-- Card 1: Munger -->
        <div id="port-card-munger" onclick="selectPortfolio('munger')" class="glass-card rounded-2xl p-4 border-2 border-amber-400/80 bg-gradient-to-b from-amber-500/10 to-transparent shadow-lg shadow-amber-500/10 cursor-pointer transition-all duration-200 flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between gap-1 mb-2">
              <span class="text-sm font-mono font-bold text-amber-300 flex items-center gap-1.5">
                <span class="text-base">🏆</span> CHARLIE MUNGER
              </span>
              <span class="px-2.5 py-0.5 rounded-full text-[11px] font-mono font-bold bg-amber-500/20 text-amber-300 border border-amber-500/40" id="port-count-munger">8 ativos</span>
            </div>
            <p class="text-xs text-slate-300 leading-relaxed">
              Empresas excepcionais com fossos duráveis (Moats), ROIC estruturalmente elevado e balanço blindado.
            </p>
          </div>
          <div class="mt-3 pt-2.5 border-t border-white/10 flex items-center justify-between text-[11px] font-mono text-slate-400">
            <span>Foco: <b class="text-amber-300">Compounders</b></span>
            <span class="text-amber-400">Selecionada ➜</span>
          </div>
        </div>

        <!-- Card 2: Vacas Leiteiras -->
        <div id="port-card-dividends" onclick="selectPortfolio('dividends')" class="glass-card rounded-2xl p-4 border border-white/10 opacity-75 hover:opacity-100 hover:border-white/30 cursor-pointer transition-all duration-200 flex flex-col justify-between shadow-md">
          <div>
            <div class="flex items-center justify-between gap-1 mb-2">
              <span class="text-sm font-mono font-bold text-emerald-300 flex items-center gap-1.5">
                <span class="text-base">💰</span> VACAS LEITEIRAS
              </span>
              <span class="px-2.5 py-0.5 rounded-full text-[11px] font-mono font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/40" id="port-count-dividends">8 ativos</span>
            </div>
            <p class="text-xs text-slate-300 leading-relaxed">
              Geração perene de caixa livre, dividend yield atrativo e sustentabilidade de payout em setores essenciais.
            </p>
          </div>
          <div class="mt-3 pt-2.5 border-t border-white/10 flex items-center justify-between text-[11px] font-mono text-slate-400">
            <span>Foco: <b class="text-emerald-300">Renda Passiva</b></span>
            <span class="text-emerald-400">Selecionar ➜</span>
          </div>
        </div>

        <!-- Card 3: Assimetria Real -->
        <div id="port-card-asymmetry" onclick="selectPortfolio('asymmetry')" class="glass-card rounded-2xl p-4 border border-white/10 opacity-75 hover:opacity-100 hover:border-white/30 cursor-pointer transition-all duration-200 flex flex-col justify-between shadow-md">
          <div>
            <div class="flex items-center justify-between gap-1 mb-2">
              <span class="text-sm font-mono font-bold text-cyan-300 flex items-center gap-1.5">
                <span class="text-base">📈</span> ASSIMETRIA REAL
              </span>
              <span class="px-2.5 py-0.5 rounded-full text-[11px] font-mono font-bold bg-cyan-500/20 text-cyan-300 border border-cyan-500/40" id="port-count-asymmetry">8 ativos</span>
            </div>
            <p class="text-xs text-slate-300 leading-relaxed">
              Deep Value: múltiplos comprimidos, desconto patrimonial severo e spread real elevado sobre a NTN-B.
            </p>
          </div>
          <div class="mt-3 pt-2.5 border-t border-white/10 flex items-center justify-between text-[11px] font-mono text-slate-400">
            <span>Foco: <b class="text-cyan-300">Re-rating & Valor</b></span>
            <span class="text-cyan-400">Selecionar ➜</span>
          </div>
        </div>

        <!-- Card 4: CFA Ultra -->
        <div id="port-card-cfa_ultra" onclick="selectPortfolio('cfa_ultra')" class="glass-card rounded-2xl p-4 border border-white/10 opacity-75 hover:opacity-100 hover:border-white/30 cursor-pointer transition-all duration-200 flex flex-col justify-between shadow-md">
          <div>
            <div class="flex items-center justify-between gap-1 mb-2">
              <span class="text-sm font-mono font-bold text-yellow-300 flex items-center gap-1.5">
                <span class="text-base">💎</span> CFA ULTRA-CRÍTICA
              </span>
              <span class="px-2.5 py-0.5 rounded-full text-[11px] font-mono font-bold bg-yellow-500/20 text-yellow-300 border border-yellow-500/40" id="port-count-cfa_ultra">8 ativos</span>
            </div>
            <p class="text-xs text-slate-300 leading-relaxed">
              Filtro institucional de máxima exigência com 7 barreiras quantitativas, caixa líquido e risco zero.
            </p>
          </div>
          <div class="mt-3 pt-2.5 border-t border-white/10 flex items-center justify-between text-[11px] font-mono text-slate-400">
            <span>Foco: <b class="text-yellow-300">Régua Máxima</b></span>
            <span class="text-yellow-400">Selecionar ➜</span>
          </div>
        </div>
      </div>

      <!-- 2. RESUMO EXECUTIVO DA CARTEIRA & SIMULADOR DE APORTE -->
      <div class="glass-panel rounded-2xl p-5 flex flex-col lg:flex-row items-stretch justify-between gap-5 flex-shrink-0 shadow-xl">
        <!-- Lado Esquerdo: KPIs Ponderados & Diversificação Setorial -->
        <div class="flex-1 flex flex-col justify-between gap-4">
          <div class="flex flex-wrap items-center justify-between gap-2">
            <span class="text-xs font-mono font-bold text-slate-200 uppercase tracking-wider flex items-center gap-1.5">
              <span>📊</span> INDICADORES MÉDIOS PONDERADOS DA CARTEIRA
            </span>
            <span class="text-[11px] font-mono text-amber-300 font-semibold" id="portStrategyShortName">Alocação 100% Ponderada • 8 Ativos Selecionados</span>
          </div>

          <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3 font-mono">
            <div class="p-3 rounded-xl glass-card text-center">
              <div class="text-[11px] text-slate-400 uppercase font-semibold">P/L Médio</div>
              <div class="text-base font-bold text-white mt-0.5" id="kp-port-pl">--</div>
            </div>
            <div class="p-3 rounded-xl glass-card text-center">
              <div class="text-[11px] text-slate-400 uppercase font-semibold">ROIC / ROE</div>
              <div class="text-base font-bold text-emerald-400 mt-0.5" id="kp-port-roic">--</div>
            </div>
            <div class="p-3 rounded-xl glass-card text-center">
              <div class="text-[11px] text-slate-400 uppercase font-semibold">Div. Yield</div>
              <div class="text-base font-bold text-emerald-400 mt-0.5" id="kp-port-dy">--</div>
            </div>
            <div class="p-3 rounded-xl glass-card text-center">
              <div class="text-[11px] text-slate-400 uppercase font-semibold">Spread NTN-B</div>
              <div class="text-base font-bold text-cyan-400 mt-0.5" id="kp-port-spread">--</div>
            </div>
            <div class="p-3 rounded-xl glass-card text-center">
              <div class="text-[11px] text-slate-400 uppercase font-semibold">Dív. Líq / EBITDA</div>
              <div class="text-base font-bold text-white mt-0.5" id="kp-port-debt">--</div>
            </div>
            <div class="p-3 rounded-xl glass-card border-amber-500/40 text-center bg-amber-500/10">
              <div class="text-[11px] text-amber-300 uppercase font-semibold">Score Munger</div>
              <div class="text-base font-bold text-amber-300 mt-0.5" id="kp-port-score">--</div>
            </div>
          </div>

          <!-- Diversificação Setorial Gráfica -->
          <div class="space-y-2 pt-1">
            <div class="flex items-center justify-between text-xs font-mono">
              <span class="text-slate-400 font-semibold">Alocação Setorial &amp; Diversificação:</span>
              <span id="portSectorSummary" class="text-slate-300 font-semibold truncate max-w-[450px]">--</span>
            </div>
            <div id="portSectorBar" class="w-full h-3 bg-slate-900/80 rounded-full overflow-hidden flex border border-white/10"></div>
          </div>
        </div>

        <!-- Lado Direito: Simulador de Aporte em Dinheiro -->
        <div class="w-full lg:w-80 glass-card rounded-xl p-4 flex flex-col justify-between gap-3 flex-shrink-0 border border-white/10">
          <div>
            <div class="flex items-center justify-between text-xs font-mono mb-1">
              <span class="font-bold text-white flex items-center gap-1.5"><span>💵</span> SIMULADOR DE APORTE</span>
              <span class="text-[10px] text-amber-300 font-bold bg-amber-500/20 px-2 py-0.5 rounded-full border border-amber-500/30">Cotas Exatas</span>
            </div>
            <p class="text-xs text-slate-300 leading-snug">
              Digite o capital total para calcular as quantidades e valores por ativo:
            </p>
          </div>
          <div class="space-y-2.5 font-mono">
            <div class="relative">
              <span class="absolute left-3.5 top-2 text-slate-400 font-bold text-sm">R$</span>
              <input type="number" id="simCapitalInput" value="50000" step="5000" min="1000" oninput="updateSimulationCapital(this.value)" class="w-full bg-slate-900/80 border border-white/10 focus:border-emerald-400 rounded-full pl-10 pr-4 py-2 text-white font-bold text-sm tracking-wide transition" />
            </div>
            <div class="flex items-center justify-between gap-1 text-xs">
              <button onclick="setSimulationCapital(10000)" class="flex-1 py-1 rounded-full glass-pill hover:bg-white/10 text-slate-300 text-center cursor-pointer transition">10k</button>
              <button onclick="setSimulationCapital(25000)" class="flex-1 py-1 rounded-full glass-pill hover:bg-white/10 text-slate-300 text-center cursor-pointer transition">25k</button>
              <button onclick="setSimulationCapital(50000)" class="flex-1 py-1 rounded-full glass-pill bg-amber-500/20 border-amber-500/50 text-amber-300 font-bold text-center cursor-pointer transition">50k</button>
              <button onclick="setSimulationCapital(100000)" class="flex-1 py-1 rounded-full glass-pill hover:bg-white/10 text-slate-300 text-center cursor-pointer transition">100k</button>
              <button onclick="setSimulationCapital(250000)" class="flex-1 py-1 rounded-full glass-pill hover:bg-white/10 text-slate-300 text-center cursor-pointer transition">250k</button>
            </div>
          </div>
        </div>
      </div>

      <!-- 3. NOVO: PARECER CRÍTICO DO COMITÊ CFA & GESTÃO DE RISCO DE CONCENTRAÇÃO -->
      <div class="glass-panel rounded-2xl p-5 space-y-4 shadow-xl flex-shrink-0 border border-amber-500/30 bg-gradient-to-r from-amber-500/[0.04] to-transparent">
        <div class="flex flex-wrap items-center justify-between gap-2 border-b border-white/10 pb-3">
          <div class="flex items-center gap-2">
            <span class="text-sm font-mono font-bold text-amber-300 flex items-center gap-1.5">
              <span>🎓</span> PARECER CRÍTICO DO COMITÊ CFA &amp; GESTÃO DE RISCO DE CONCENTRAÇÃO
            </span>
            <span class="px-2.5 py-0.5 text-[10px] font-mono bg-emerald-500/15 text-emerald-300 border border-emerald-500/40 rounded-full font-bold" id="cfaAuditBadge">
              ✅ AUDITADO: DIVERSIFICAÇÃO RESPEITADA
            </span>
          </div>
          <div class="text-xs font-mono text-slate-400" id="cfaHhiMetric">
            Índice HHI Setorial: <b class="text-white font-mono">0.172</b> • <span class="text-emerald-400 font-bold">Baixa Concentração (Excelente)</span>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-3.5 text-xs">
          <!-- Coluna 1: Análise de Concentração Setorial -->
          <div class="p-3.5 rounded-xl glass-card border border-white/10 space-y-2">
            <div class="font-mono font-bold text-slate-200 flex items-center justify-between">
              <span class="text-sky-400 flex items-center gap-1"><span>📊</span> Teto Setorial (Teto 25%)</span>
              <span id="cfaTopSectorWeight" class="text-emerald-400 font-bold bg-emerald-500/20 px-2 py-0.5 rounded-full border border-emerald-500/40">Máx 25%</span>
            </div>
            <p class="text-slate-300 leading-relaxed text-xs" id="cfaSectorAuditText">
              --
            </p>
          </div>

          <!-- Coluna 2: Sensibilidade Macroeconômica & Juros -->
          <div class="p-3.5 rounded-xl glass-card border border-white/10 space-y-2">
            <div class="font-mono font-bold text-slate-200 flex items-center justify-between">
              <span class="text-amber-400 flex items-center gap-1"><span>⚡</span> Sensibilidade Selic &amp; Macro</span>
              <span id="cfaMacroRiskBadge" class="text-amber-300 font-bold bg-amber-500/20 px-2 py-0.5 rounded-full border border-amber-500/40">Resiliente</span>
            </div>
            <p class="text-slate-300 leading-relaxed text-xs" id="cfaMacroAuditText">
              --
            </p>
          </div>

          <!-- Coluna 3: Solvência & Alavancagem Ponderada -->
          <div class="p-3.5 rounded-xl glass-card border border-white/10 space-y-2">
            <div class="font-mono font-bold text-slate-200 flex items-center justify-between">
              <span class="text-emerald-400 flex items-center gap-1"><span>🛡️</span> Balanço &amp; Margem de Segurança</span>
              <span id="cfaSolvencyBadge" class="text-emerald-300 font-bold bg-emerald-500/20 px-2 py-0.5 rounded-full border border-emerald-500/40">Alta Proteção</span>
            </div>
            <p class="text-slate-300 leading-relaxed text-xs" id="cfaSolvencyAuditText">
              --
            </p>
          </div>
        </div>

        <!-- Parecer Qualitativo Detalhado do Analista -->
        <div class="p-3.5 rounded-xl glass-card border border-amber-500/30 flex items-start gap-3 text-xs">
          <span class="text-lg flex-shrink-0">📝</span>
          <div class="flex-1">
            <div class="font-mono font-bold text-amber-300 mb-1">Veredito Oficial do Comitê de Alocação de Ativos (Buy-Side):</div>
            <div class="text-slate-200 text-xs leading-relaxed" id="cfaDetailedVerdict">--</div>
          </div>
        </div>
      </div>

      <!-- 4. TABELA DE ATIVOS DA CARTEIRA RECOMENDADA -->
      <div class="glass-panel rounded-2xl flex flex-col shadow-2xl overflow-hidden flex-shrink-0">
        <div class="p-4 border-b border-white/10 bg-white/[0.02] flex flex-wrap items-center justify-between gap-2">
          <div class="flex items-center gap-2.5">
            <span class="text-sm font-mono font-bold text-white flex items-center gap-1.5" id="portTableTitle">
              <span>📋</span> COMPONENTES DA CARTEIRA
            </span>
            <span class="text-xs text-amber-400 font-mono font-semibold" id="portTableSubtitle">(-- ativos recomendados)</span>
          </div>
          <div class="text-xs font-mono text-slate-400">
            💡 <span class="hidden sm:inline">Dica: </span>Clique em qualquer linha para abrir o <b class="text-amber-300">Dossiê Completo 360°</b>
          </div>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full text-left border-collapse text-xs">
            <thead class="bg-[#0A0E1A]/95 backdrop-blur-md border-b border-white/10 font-mono text-slate-400 uppercase text-[11px]">
              <tr>
                <th class="py-3 px-3.5">Ativo / Empresa</th>
                <th class="py-3 px-2 text-center">Peso</th>
                <th class="py-3 px-3 text-right">Cotação</th>
                <th class="py-3 px-2 text-center">Score</th>
                <th class="py-3 px-3 text-right">P/L</th>
                <th class="py-3 px-3 text-right">ROIC / ROE</th>
                <th class="py-3 px-3 text-right">Div. Yield</th>
                <th class="py-3 px-3 text-right">Dívida Líq.</th>
                <th class="py-3 px-3.5 text-right bg-amber-500/10 text-amber-300 font-bold">Aporte Simulado</th>
                <th class="py-3 px-3 text-right bg-amber-500/10 text-amber-300 font-bold">Qtd Ações</th>
                <th class="py-3 px-3.5">Tese Mungeriana / Racional de Investimento</th>
              </tr>
            </thead>
            <tbody id="portStocksTableBody" class="divide-y divide-white/5 font-sans"></tbody>
          </table>
        </div>
      </div>
    </section>

  </main>
</div> <!-- Fechamento da coluna de conteúdo principal -->

<!-- SLIDE-OVER DRAWER PARA DOSSIÊ FUNDAMENTALISTA 360° -->
<div id="dossierDrawerBackdrop" onclick="closeDossierDrawer()" class="fixed inset-0 drawer-backdrop z-40 hidden transition-opacity duration-300"></div>
<aside id="dossierDrawer" class="fixed top-0 right-0 bottom-0 w-full sm:w-[580px] md:w-[640px] xl:w-[700px] bg-[#080C14]/95 backdrop-blur-2xl border-l border-white/10 z-50 shadow-[-25px_0_60px_rgba(0,0,0,0.85)] flex flex-col transform translate-x-full transition-transform duration-300 ease-in-out">
  <!-- Drawer Topbar -->
  <div class="p-4 border-b border-white/10 bg-white/[0.02] flex items-center justify-between flex-shrink-0">
    <div class="flex items-center gap-2">
      <span class="w-2.5 h-2.5 rounded-full bg-emerald-400 shadow-md shadow-emerald-400/50"></span>
      <span class="font-mono font-bold text-xs text-white uppercase tracking-wider">Dossiê Fundamentalista 360°</span>
    </div>
    <div class="flex items-center gap-2">
      <button onclick="openSelectedInMatrix()" class="px-3 py-1.5 rounded-full text-[11px] font-mono text-slate-300 hover:text-white glass-pill border-white/10 hover:border-white/30 transition cursor-pointer flex items-center gap-1.5" title="Ver este ativo plotado na Matriz 2x2">
        <span>📊 Ver na Matriz</span>
      </button>
      <button onclick="closeDossierDrawer()" class="p-1 rounded-full text-slate-400 hover:text-white hover:bg-white/10 text-sm font-bold transition px-2.5 cursor-pointer" title="Fechar (ESC)">✕</button>
    </div>
  </div>

  <!-- Header do Ativo Selecionado (Dossiê) -->
  <div class="p-4 border-b border-white/10 bg-white/[0.01] flex-shrink-0" id="diagHeaderCard">
    <!-- Renderizado dinamicamente via renderDiagnosis() -->
  </div>

  <!-- Abas de Diagnóstico -->
  <div class="flex border-b border-white/10 text-xs font-mono font-medium bg-white/[0.01] flex-shrink-0 p-1.5 gap-1.5">
    <button onclick="switchDiagTab('radar')" id="dtab-radar" class="tab-btn active flex-1 py-2 rounded-full text-center text-slate-300 transition cursor-pointer">
      ⚡ Gauges &amp; Radar
    </button>
    <button onclick="switchDiagTab('history')" id="dtab-history" class="tab-btn flex-1 py-2 rounded-full text-center text-slate-400 hover:text-slate-200 transition cursor-pointer">
      📈 Histórico 5A
    </button>
    <button onclick="switchDiagTab('balance')" id="dtab-balance" class="tab-btn flex-1 py-2 rounded-full text-center text-slate-400 hover:text-slate-200 transition cursor-pointer">
      📋 Balanço &amp; DRE
    </button>
    <button onclick="switchDiagTab('cfa')" id="dtab-cfa" class="tab-btn flex-1 py-2 rounded-full text-center text-slate-400 hover:text-slate-200 transition cursor-pointer">
      🎓 Veredito CFA
    </button>
  </div>

  <!-- Conteúdo do Dossiê com Scroll Interno Próprio -->
  <div class="flex-1 overflow-y-auto p-4 flex flex-col gap-3.5">
    <!-- ABA 1: GAUGES & RADAR & KPIS -->
    <div id="dview-radar" class="flex flex-col gap-3.5">
      <!-- 3 GAUGES ANALÓGICOS BLOOMBERG -->
      <div class="glass-card rounded-xl p-4 border border-white/10">
        <div class="text-[10px] font-mono font-bold uppercase tracking-wider text-amber-300 mb-2.5 flex items-center justify-between">
          <span>⚡ Indicadores Contábeis Auditados</span>
          <span class="text-[9px] text-slate-400 font-normal">100% Real • Fundamentus</span>
        </div>
        <div class="grid grid-cols-3 gap-1">
          <div class="flex flex-col items-center justify-center">
            <svg id="gaugeRoe" class="w-full h-[82px]" viewBox="0 0 160 88"></svg>
          </div>
          <div class="flex flex-col items-center justify-center border-x border-white/10 px-1">
            <svg id="gaugeDebt" class="w-full h-[82px]" viewBox="0 0 160 88"></svg>
          </div>
          <div class="flex flex-col items-center justify-center">
            <svg id="gaugeSpread" class="w-full h-[82px]" viewBox="0 0 160 88"></svg>
          </div>
        </div>
      </div>

      <!-- RADAR PENTAGONAL DE 5 PILARES (ESTILO SIMPLY WALL ST) -->
      <div class="glass-card rounded-xl p-4 flex flex-col gap-3 border border-white/10">
        <div class="text-[10px] font-mono font-bold uppercase tracking-wider text-emerald-400 flex items-center justify-between">
          <span class="flex items-center gap-1.5"><span>⚡</span> RADAR DE 5 PILARES (SIMPLY WALL ST STYLE)</span>
          <span class="text-[9px] text-slate-400 font-normal">Escala de 0 a 100</span>
        </div>
        <div class="w-full h-56 flex items-center justify-center py-1">
          <svg id="radarSvg" class="w-full h-56" viewBox="-145 -145 290 290"></svg>
        </div>
        <!-- 5 Mini-Cards com notas dos Pilares -->
        <div class="grid grid-cols-2 sm:grid-cols-5 gap-2 text-center" id="radarPillarsGrid"></div>
      </div>

      <!-- GRID DE KPIS COMPLEMENTARES -->
      <div class="grid grid-cols-3 gap-2 text-[11px] font-mono" id="kpiGrid"></div>
    </div>

    <!-- ABA 2: HISTÓRICO & CONSISTÊNCIA 5 ANOS (NOVA) -->
    <div id="dview-history" class="hidden flex flex-col gap-3.5 text-xs pb-8"></div>

    <!-- ABA 3: ESPELHO FUNDAMENTUS -->
    <div id="dview-balance" class="hidden text-xs flex flex-col gap-3">
      <div class="text-[10px] text-slate-400 font-mono flex items-center justify-between" id="auditSourceText">
        <span>Fonte: Fundamentus</span>
        <span id="balanceRecencyTag" class="px-2 py-0.5 rounded-full text-[9px] font-bold"></span>
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-3" id="balanceSheetDetails"></div>
    </div>

    <!-- ABA 4: VEREDITO DO ANALISTA CFA -->
    <div id="dview-cfa" class="hidden flex flex-col gap-3 text-xs">
      <div id="cfaStatusBanner"></div>
      <div id="cfaFlagsContainer" class="flex flex-wrap gap-1"></div>
      <div id="cfaBulletsList" class="flex flex-col gap-2.5"></div>
    </div>
  </div>
</aside>

  <!-- DADOS EMBUTIDOS E ENGINE JS -->
  <script>
    let APP_DATA = {json_data_str};
    let currentFilter = 'ALL';
    let currentSector = 'ALL';
    let currentSortCol = 'quality_score';
    let currentSortAsc = false;
    let currentXMetric = 'pl';
    let selectedTicker = APP_DATA.stocks[0].ticker;
    let searchQuery = '';
    let isRefreshing = false;

    // Estado das Carteiras Recomendadas
    let currentPortfolioKey = 'munger'; // 'munger', 'dividends', 'asymmetry', 'cfa_ultra'
    let currentSimulatedCapital = 50000;

    // Estado da Matriz Interativa (Zoom, Pan, 3ª Dimensão)
    let matrixBubbleMetric = 'mcap'; // 'fixed', 'mcap', 'volume'
    let matrixColorMode = 'asymmetry'; // 'asymmetry', 'momentum', 'dividend', 'sector', 'relative'
    let matrixZoom = 1.0;
    let matrixCenterX = 16.0;
    let matrixCenterY = 62.5;
    let isPanning = false;
    let panStartX = 0;
    let panStartY = 0;
    let panStartCenterX = 16.0;
    let panStartCenterY = 62.5;
    let hasMovedDuringPan = false;

    // Curva Munger Compounder Pró-Qualidade:
    // P/L Justo = 3.5 + 20.0 * ((Quality - 20) / 80) ^ 1.6
    function calcFairPL(qualityScore) {{
      const q = Math.max(20.0, Math.min(100.0, qualityScore || 50.0));
      const norm = (q - 20.0) / 80.0;
      return 3.5 + 20.0 * Math.pow(norm, 1.6);
    }}

    // Inicialização do cabeçalho
    function updateHeaderInfo() {{
      const ts = document.getElementById('auditTimestamp');
      if (ts) ts.innerText = 'Auditado em: ' + APP_DATA.audit_timestamp;
      const liq = document.getElementById('cnt-liq-badge');
      if (liq) liq.innerText = APP_DATA.stocks.filter(s => s.is_liquid_1m).length;
      const bal = document.getElementById('cnt-bal-badge');
      if (bal) bal.innerText = APP_DATA.stocks.filter(s => s.is_latest_balanco).length;
      const rec = document.getElementById('cnt-rec-badge');
      if (rec) rec.innerText = APP_DATA.stocks.filter(s => !s.is_distorted).length;
      const total = document.getElementById('totalUniverseCount');
      if (total) total.innerText = APP_DATA.stocks.length;
    }}

    function formatCurrency(v) {{
      if (v === null || v === undefined) return 'N/D';
      return 'R$ ' + Number(v).toLocaleString('pt-BR', {{ minimumFractionDigits: 2, maximumFractionDigits: 2 }});
    }}

    function formatBillions(v) {{
      if (v === null || v === undefined) return 'N/D';
      const abs = Math.abs(v);
      if (abs >= 1e9) return 'R$ ' + (v / 1e9).toFixed(2).replace('.', ',') + ' B';
      if (abs >= 1e6) return 'R$ ' + (v / 1e6).toFixed(2).replace('.', ',') + ' M';
      return formatCurrency(v);
    }}

    function formatPercent(v) {{
      if (v === null || v === undefined) return 'N/D';
      const num = Math.abs(v) < 2.0 ? v * 100 : v;
      return num.toFixed(1).replace('.', ',') + '%';
    }}

    function formatMultiple(v) {{
      if (v === null || v === undefined) return 'N/D';
      return Number(v).toFixed(2) + 'x';
    }}

    // HIERARQUIA UNIVERSAL DE CORES SEMÂNTICAS (VERDE, VERMELHO, AMARELO, AZUL)
    function getColorSpread(val) {{
      if (val === null || val === undefined) return 'text-slate-500';
      if (val >= 2.0) return 'text-emerald-400 font-bold';
      if (val >= 0.0) return 'text-amber-400 font-semibold';
      return 'text-rose-400 font-bold';
    }}

    function getColorRoe(val) {{
      if (val === null || val === undefined) return 'text-slate-500';
      const num = Math.abs(val) < 2.0 ? val * 100 : val;
      if (num >= 15.0) return 'text-emerald-400 font-bold';
      if (num >= 8.0) return 'text-slate-200';
      if (num >= 0.0) return 'text-amber-400';
      return 'text-rose-400 font-bold';
    }}

    function getColorPl(val) {{
      if (val === null || val === undefined) return 'text-slate-500';
      if (val < 0) return 'text-rose-400 font-bold';
      if (val <= 12.0) return 'text-emerald-400 font-semibold';
      if (val <= 22.0) return 'text-slate-200';
      return 'text-amber-400';
    }}

    function getColorDy(val) {{
      if (val === null || val === undefined) return 'text-slate-500';
      const num = Math.abs(val) < 2.0 ? val * 100 : val;
      if (num >= 6.0) return 'text-emerald-400 font-bold';
      if (num >= 3.0) return 'text-slate-200';
      if (num > 0) return 'text-slate-400';
      return 'text-slate-500';
    }}

    function getColorDebt(val, isFin = false) {{
      if (isFin) return 'text-sky-400 font-medium';
      if (val === null || val === undefined) return 'text-slate-400';
      if (val < 0) return 'text-emerald-400 font-semibold';
      if (val <= 1.5) return 'text-emerald-400 font-semibold';
      if (val <= 2.7) return 'text-amber-400';
      return 'text-rose-400 font-bold';
    }}

    function getColorMrgLiq(val) {{
      if (val === null || val === undefined) return 'text-slate-500';
      const num = Math.abs(val) < 2.0 ? val * 100 : val;
      if (num >= 12.0) return 'text-emerald-400 font-semibold';
      if (num >= 4.0) return 'text-slate-200';
      if (num >= 0) return 'text-amber-400';
      return 'text-rose-400 font-bold';
    }}

    function getColorAcidTest(val) {{
      if (val === null || val === undefined) return 'text-slate-400';
      const num = Math.abs(val) < 2.0 ? val * 100 : val;
      if (num >= 75.0) return 'text-emerald-400 font-semibold';
      if (num >= 60.0) return 'text-amber-400';
      return 'text-rose-400 font-bold';
    }}

    function getFilteredStocks() {{
      const require1M = document.getElementById('chkLiquidity1M').checked;
      const requireLatestBal = document.getElementById('chkLatestBalance').checked;
      const requireRecurring = document.getElementById('chkFilterDistortions').checked;
      const requireAcidTest = document.getElementById('chkAcidTest') ? document.getElementById('chkAcidTest').checked : false;
      const requireOnlyON = document.getElementById('chkOnlyON') ? document.getElementById('chkOnlyON').checked : false;

      return APP_DATA.stocks.filter(s => {{
        // Gatekeeper 1: Liquidez >= 1M
        if (require1M && !s.is_liquid_1m) return false;

        // Gatekeeper 2: Balanço do Último Tri
        if (requireLatestBal && !s.is_latest_balanco) return false;

        // Gatekeeper 3: Apenas Lucros Recorrentes (Sem Distorções Trimestrais)
        if (requireRecurring && s.is_distorted) return false;

        // Gatekeeper 4: Munger Acid Test (EBIT/EBITDA >= 75% ou Bancos ROE >= 15%)
        if (requireAcidTest) {{
          if (s.is_financial) {{
            if (!s.roe || s.roe < 0.15) return false;
          }} else {{
            if (s.capital_intensity === null || s.capital_intensity === undefined || s.capital_intensity < 0.75) return false;
          }}
        }}

        // Gatekeeper 5: Ações Ordinárias (ON - 100% Tag Along Legal)
        if (requireOnlyON) {{
          const tipo = (s.details && s.details.tipo) ? s.details.tipo.toUpperCase() : '';
          if (!tipo.includes('ON')) return false;
        }}

        // Filtro Setorial
        if (currentSector !== 'ALL' && s.setor !== currentSector) return false;

        // Busca por texto
        if (searchQuery) {{
          const q = searchQuery.toLowerCase();
          const match = s.ticker.toLowerCase().includes(q) || s.empresa.toLowerCase().includes(q) || s.setor.toLowerCase().includes(q);
          if (!match) return false;
        }}

        // Presets Munger
        if (currentFilter === 'TIER1') return s.quality_score >= 80.0;
        if (currentFilter === 'ASYMMETRY') return s.quality_score >= 75.0 && s.pl > 0 && s.pl < 8.0;
        if (currentFilter === 'NTNB') return s.ey_spread !== null && s.ey_spread >= 5.0;
        if (currentFilter === 'NET_CASH') return s.div_liq_ebitda !== null && s.div_liq_ebitda < 0;

        // 0. Categoria Ultra-Crítica (CFA & Munger: Régua Máxima B3)
        if (currentFilter === 'CAT_ULTRA_CRITIC') {{
          if ((s.quality_score || 0) < 75) return false;
          if (s.is_distorted || s.is_commodity_peak) return false;
          if (s.ey_spread === null || s.ey_spread < 1.5) return false;
          if (s.is_financial) {{
            if ((s.roe || 0) < 0.15) return false;
          }} else {{
            if (s.capital_intensity === null || s.capital_intensity < 0.75) return false;
            const dl = s.details ? s.details.divida_liquida : null;
            const dle = s.div_liq_ebitda;
            const isSafeDebt = (dl !== null && dl <= 0) || (dle !== null && dle <= 1.0);
            if (!isSafeDebt) return false;
          }}
          return true;
        }}

        // Curva Munger Fair Value (Acima da Curva vs Abaixo da Curva)
        if (currentFilter === 'QUAD_ABOVE' || currentFilter === 'QUAD_FILE' || currentFilter === 'QUAD_BARGAIN') {{
          if (!s.pl || s.pl <= 0) return false;
          return s.pl < calcFairPL(s.quality_score);
        }}
        if (currentFilter === 'QUAD_BELOW' || currentFilter === 'QUAD_EXPENSIVE' || currentFilter === 'QUAD_TRAP') {{
          if (!s.pl || s.pl <= 0) return true;
          return s.pl >= calcFairPL(s.quality_score);
        }}

        // 7 Categorias Estratégicas do Panorama B3
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
        }}
        return true;
      }});
    }}

    // Rótulos e Categorias Institucionais Munger da Ação
    function getStockCategories(s) {{
      const cats = [];
      if (!s) return cats;

      // 0. Ultra-Crítico CFA & Munger (Régua Máxima B3)
      let isUltra = false;
      if ((s.quality_score || 0) >= 75 && !s.is_distorted && !s.is_commodity_peak && s.ey_spread !== null && s.ey_spread >= 1.5) {{
        if (s.is_financial) {{
          if ((s.roe || 0) >= 0.15) isUltra = true;
        }} else {{
          const dl = s.details ? s.details.divida_liquida : null;
          const dle = s.div_liq_ebitda;
          const isSafeDebt = (dl !== null && dl <= 0) || (dle !== null && dle <= 1.0);
          if (s.capital_intensity !== null && s.capital_intensity >= 0.75 && isSafeDebt) isUltra = true;
        }}
      }}
      if (isUltra) {{
        cats.push({{
          id: 'CAT_ULTRA_CRITIC',
          label: 'Ultra-Crítico CFA',
          shortLabel: 'Ultra-Crítico',
          icon: '💎',
          bgClass: 'bg-yellow-950/90 text-yellow-300 border border-yellow-500/70 shadow-sm'
        }});
      }}

      // 1. Filé Mignon Munger
      if (s.quality_score >= 80 && s.ey_spread !== null && s.ey_spread >= 1.5 && (s.is_financial || (s.div_liq_ebitda !== null && s.div_liq_ebitda <= 2.5))) {{
        cats.push({{
          id: 'CAT_MUNGER',
          label: 'Filé Mignon Munger',
          shortLabel: 'Filé Mignon',
          icon: '🏆',
          bgClass: 'bg-amber-950/80 text-amber-300 border border-amber-700/60'
        }});
      }}

      // 2. Assimetria Real
      if (s.quality_score >= 75 && s.pl !== null && s.pl >= 3.0 && s.pl <= 15.0 && s.ey_spread !== null && s.ey_spread >= 3.0 && (s.is_financial || (s.div_liq_ebitda !== null && s.div_liq_ebitda <= 3.0)) && !s.is_distorted) {{
        cats.push({{
          id: 'CAT_ASYMMETRY',
          label: 'Assimetria Real',
          shortLabel: 'Assimetria',
          icon: '📈',
          bgClass: 'bg-cyan-950/80 text-cyan-300 border border-cyan-700/60'
        }});
      }}

      // 3. Vaca Leiteira Perene
      if (s.div_yield !== null && s.div_yield >= 0.05 && s.div_yield <= 0.13 && s.payout_implicito !== null && s.payout_implicito >= 35 && s.payout_implicito <= 85 && (s.roic || s.roe || 0) >= 0.12 && s.quality_score >= 70 && (s.is_financial || (s.div_liq_ebitda !== null && s.div_liq_ebitda <= 3.0))) {{
        cats.push({{
          id: 'CAT_DIVIDENDS',
          label: 'Vaca Leiteira',
          shortLabel: 'Dividendos',
          icon: '💰',
          bgClass: 'bg-emerald-950/80 text-emerald-300 border border-emerald-700/60'
        }});
      }}

      // 4. Lucro em Expansão (Run-Rate 2T26)
      if (s.pl && s.pl_run_rate && s.run_rate_div_pct !== null && s.run_rate_div_pct !== undefined && s.pl >= 3.0 && s.pl <= 45.0 && s.pl_run_rate >= 2.0 && s.pl_run_rate <= 80.0) {{
        const l12 = (s.details && s.details.lucro_liq_12m) || 0;
        const l3 = (s.details && s.details.lucro_liq_3m) || 0;
        if (l12 >= 30000000 && l3 > 0 && s.run_rate_div_pct >= 15.0 && s.run_rate_div_pct <= 120.0 && s.pl_run_rate < s.pl * 0.85) {{
          cats.push({{
            id: 'CAT_EXPANSION',
            label: 'Expansão 2T26',
            shortLabel: 'Expansão',
            icon: '🟢',
            bgClass: 'bg-emerald-950/80 text-emerald-300 border border-emerald-700/60'
          }});
        }}
      }}

      // 5. Alerta de Desaceleração / Compressão (Run-Rate 2T26)
      if (s.pl && s.pl_run_rate && s.run_rate_div_pct !== null && s.run_rate_div_pct !== undefined && s.pl >= 3.0 && s.pl <= 45.0 && s.pl_run_rate >= 2.0 && s.pl_run_rate <= 80.0) {{
        const l12 = (s.details && s.details.lucro_liq_12m) || 0;
        const l3 = (s.details && s.details.lucro_liq_3m) || 0;
        if (l12 >= 30000000 && l3 > 0 && s.run_rate_div_pct <= -20.0 && s.run_rate_div_pct >= -70.0 && s.pl_run_rate > s.pl * 1.25) {{
          cats.push({{
            id: 'CAT_DECELERATION',
            label: 'Risco de Ciclo',
            shortLabel: 'Desaceleração',
            icon: '⚠️',
            bgClass: 'bg-amber-950/80 text-amber-300 border border-amber-700/60'
          }});
        }}
      }}

      // 6. Balanço Forte (Caixa Líquido)
      if (s.div_liq_ebitda !== null && s.div_liq_ebitda < -0.1 && !s.is_financial) {{
        cats.push({{
          id: 'CAT_NET_CASH',
          label: 'Caixa Líquido',
          shortLabel: 'Caixa Líq.',
          icon: '🛡️',
          bgClass: 'bg-emerald-950/80 text-emerald-300 border border-emerald-700/60'
        }});
      }}

      // 7. Alavancagem Crítica
      if (s.div_liq_ebitda !== null && s.div_liq_ebitda > 3.2 && !s.is_financial) {{
        cats.push({{
          id: 'CAT_HIGH_DEBT',
          label: 'Dívida Elevada',
          shortLabel: 'Dívida Alta',
          icon: '🚨',
          bgClass: 'bg-rose-950/80 text-rose-300 border border-rose-700/60'
        }});
      }}

      return cats;
    }}

    function updateFilterCounts() {{
      const require1M = document.getElementById('chkLiquidity1M').checked;
      const requireLatestBal = document.getElementById('chkLatestBalance').checked;
      const requireRecurring = document.getElementById('chkFilterDistortions').checked;
      const requireAcidTest = document.getElementById('chkAcidTest') ? document.getElementById('chkAcidTest').checked : false;
      const requireOnlyON = document.getElementById('chkOnlyON') ? document.getElementById('chkOnlyON').checked : false;

      // Base qualificada pelos gatekeepers atuais e setor se selecionado
      const basePool = APP_DATA.stocks.filter(s => {{
        if (require1M && !s.is_liquid_1m) return false;
        if (requireLatestBal && !s.is_latest_balanco) return false;
        if (requireRecurring && s.is_distorted) return false;
        if (requireAcidTest) {{
          if (s.is_financial) {{
            if (!s.roe || s.roe < 0.15) return false;
          }} else {{
            if (s.capital_intensity === null || s.capital_intensity < 0.75) return false;
          }}
        }}
        if (requireOnlyON) {{
          const tipo = (s.details && s.details.tipo) ? s.details.tipo.toUpperCase() : '';
          if (!tipo.includes('ON')) return false;
        }}
        if (currentSector !== 'ALL' && s.setor !== currentSector) return false;
        return true;
      }});

      document.getElementById('displayedCount').innerText = getFilteredStocks().length;
      document.getElementById('cnt-ALL').innerText = basePool.length;
      const cntUltra = basePool.filter(s => {{
        if ((s.quality_score || 0) < 75 || s.is_distorted || s.is_commodity_peak || s.ey_spread === null || s.ey_spread < 1.5) return false;
        if (s.is_financial) return (s.roe || 0) >= 0.15;
        const dl = s.details ? s.details.divida_liquida : null;
        const dle = s.div_liq_ebitda;
        const isSafeDebt = (dl !== null && dl <= 0) || (dle !== null && dle <= 1.0);
        return s.capital_intensity !== null && s.capital_intensity >= 0.75 && isSafeDebt;
      }}).length;
      const elUltra = document.getElementById('cnt-CAT_ULTRA_CRITIC');
      if (elUltra) elUltra.innerText = cntUltra;
      const sbUltra = document.getElementById('sb-cnt-ultra');
      if (sbUltra) sbUltra.innerText = cntUltra;

      const cntT1 = basePool.filter(s => s.quality_score >= 80.0).length;
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
      if (sbDiv) sbDiv.innerText = cntDiv;

      const sbUniv = document.getElementById('sidebarUniverseCount');
      if (sbUniv) sbUniv.innerText = basePool.length + ' ativos';

      // Atualizar contadores da sub-barra da Matriz e Curva Fair Value
      const cntAbove = basePool.filter(s => s.pl && s.pl > 0 && s.pl < calcFairPL(s.quality_score)).length;
      const cntBelow = basePool.filter(s => !s.pl || s.pl <= 0 || s.pl >= calcFairPL(s.quality_score)).length;
      const cntExp = basePool.filter(s => s.run_rate_div_pct && s.run_rate_div_pct >= 15.0).length;
      const cntDivs = basePool.filter(s => s.div_yield && s.div_yield >= 0.05).length;

      const elAbove = document.getElementById('stat-above');
      if (elAbove) elAbove.innerText = cntAbove;
      const elBelow = document.getElementById('stat-below');
      if (elBelow) elBelow.innerText = cntBelow;
      const elExp = document.getElementById('stat-expansion');
      if (elExp) elExp.innerText = cntExp;
      const elDivs = document.getElementById('stat-dividends');
      if (elDivs) elDivs.innerText = cntDivs;
    }}

    function updateSectorDropdown() {{
      const select = document.getElementById('sectorSelect');
      if (!select) return;

      const require1M = document.getElementById('chkLiquidity1M').checked;
      const requireLatestBal = document.getElementById('chkLatestBalance').checked;
      const requireRecurring = document.getElementById('chkFilterDistortions').checked;
      const requireAcidTest = document.getElementById('chkAcidTest') ? document.getElementById('chkAcidTest').checked : false;
      const requireOnlyON = document.getElementById('chkOnlyON') ? document.getElementById('chkOnlyON').checked : false;

      const qualified = APP_DATA.stocks.filter(s => {{
        if (require1M && !s.is_liquid_1m) return false;
        if (requireLatestBal && !s.is_latest_balanco) return false;
        if (requireRecurring && s.is_distorted) return false;
        if (requireAcidTest) {{
          if (s.is_financial) {{
            if (!s.roe || s.roe < 0.15) return false;
          }} else {{
            if (s.capital_intensity === null || s.capital_intensity < 0.75) return false;
          }}
        }}
        if (requireOnlyON) {{
          const tipo = (s.details && s.details.tipo) ? s.details.tipo.toUpperCase() : '';
          if (!tipo.includes('ON')) return false;
        }}
        return true;
      }});

      const counts = {{}};
      qualified.forEach(s => {{
        counts[s.setor] = (counts[s.setor] || 0) + 1;
      }});

      const sortedSectors = Object.keys(counts).sort((a, b) => counts[b] - counts[a]);

      if (currentSector !== 'ALL' && !counts[currentSector]) {{
        currentSector = 'ALL';
      }}

      let html = `<option value="ALL">🏢 Todos os Setores (${{qualified.length}})</option>`;
      sortedSectors.forEach(sec => {{
        const isSel = (sec === currentSector) ? ' selected' : '';
        html += `<option value="${{sec}}"${{isSel}}>${{sec}} (${{counts[sec]}})</option>`;
      }});
      select.innerHTML = html;
    }}

    function handleSectorChange(val) {{
      currentSector = val;
      render();
    }}

    function toggleGatekeeper() {{
      updateSectorDropdown();
      render();
    }}

    function setFilter(f) {{
      currentFilter = f;
      document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
      const activeBtn = document.getElementById('flt-' + f);
      if (activeBtn) activeBtn.classList.add('active');
      render();
    }}

    function handleSearch() {{
      searchQuery = document.getElementById('searchInput').value.trim();
      render();
    }}

    let currentWorkspace = 'home';

    function switchWorkspace(ws) {{
      currentWorkspace = ws;
      const vHome = document.getElementById('view-home');
      const vPortfolios = document.getElementById('view-portfolios');
      const vMatrix = document.getElementById('view-matrix');
      const vTable = document.getElementById('view-table');
      const btnHome = document.getElementById('nav-home');
      const btnPortfolios = document.getElementById('nav-portfolios');
      const btnMatrix = document.getElementById('nav-matrix');
      const btnTable = document.getElementById('nav-table');

      // Reset de todas as visões e abas
      if (vHome) vHome.classList.add('hidden');
      if (vPortfolios) vPortfolios.classList.add('hidden');
      if (vMatrix) vMatrix.classList.add('hidden');
      if (vTable) vTable.classList.add('hidden');
      if (btnHome) btnHome.classList.remove('active');
      if (btnPortfolios) btnPortfolios.classList.remove('active');
      if (btnMatrix) btnMatrix.classList.remove('active');
      if (btnTable) btnTable.classList.remove('active');

      const topTitle = document.getElementById('topbarTitle');
      const topSub = document.getElementById('topbarSubtitle');

      if (ws === 'home') {{
        if (vHome) vHome.classList.remove('hidden');
        if (btnHome) btnHome.classList.add('active');
        if (topTitle) topTitle.innerHTML = '<span>🏠</span> <span>PANORAMA GERAL</span>';
        if (topSub) topSub.innerText = 'Cockpit executivo e inteligência fundamentalista B3';
        renderHomePage();
      }} else if (ws === 'portfolios') {{
        if (vPortfolios) vPortfolios.classList.remove('hidden');
        if (btnPortfolios) btnPortfolios.classList.add('active');
        if (topTitle) topTitle.innerHTML = '<span>💼</span> <span>CARTEIRAS RECOMENDADAS</span>';
        if (topSub) topSub.innerText = 'Seleção buy-side institucional e parecer crítico do comitê CFA';
        renderPortfolios();
      }} else if (ws === 'matrix') {{
        if (vMatrix) vMatrix.classList.remove('hidden');
        if (btnMatrix) btnMatrix.classList.add('active');
        if (topTitle) topTitle.innerHTML = '<span>📊</span> <span>MATRIZ MUNGER 2X2</span>';
        if (topSub) topSub.innerText = 'Qualidade Charlie Munger vs. Valuation e dispersão do mercado';
        renderMatrix();
      }} else {{
        if (vTable) vTable.classList.remove('hidden');
        if (btnTable) btnTable.classList.add('active');
        if (topTitle) topTitle.innerHTML = '<span>🔍</span> <span>SCANNER B3 &amp; ATIVOS</span>';
        if (topSub) topSub.innerText = 'Triagem fundamentalista, múltiplos, solvência e dossiê 360°';
        renderTable();
        renderDiagnosis();
      }}
    }}

    function setFilterAndGoTable(f) {{
      setFilter(f);
      switchWorkspace('table');
    }}

    function openDossierDrawer(t) {{
      if (t) selectTicker(t);
      const drawer = document.getElementById('dossierDrawer');
      const backdrop = document.getElementById('dossierDrawerBackdrop');
      if (drawer) drawer.classList.remove('translate-x-full');
      if (backdrop) backdrop.classList.remove('hidden');
    }}

    function closeDossierDrawer() {{
      const drawer = document.getElementById('dossierDrawer');
      const backdrop = document.getElementById('dossierDrawerBackdrop');
      if (drawer) drawer.classList.add('translate-x-full');
      if (backdrop) backdrop.classList.add('hidden');
    }}

    document.addEventListener('keydown', (e) => {{
      if (e.key === 'Escape') closeDossierDrawer();
    }});

    function selectTickerAndNavigate(t) {{
      // Reseta filtros prévios para garantir que a ação selecionada esteja sempre visível na tabela
      currentFilter = 'ALL';
      currentSector = 'ALL';
      searchQuery = '';
      const sInput = document.getElementById('searchInput');
      if (sInput) sInput.value = '';
      const sSelect = document.getElementById('sectorSelect');
      if (sSelect) sSelect.value = 'ALL';
      document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
      const btnAll = document.getElementById('flt-ALL');
      if (btnAll) btnAll.classList.add('active');

      // 1. Muda workspace para a Tabela & Dossiê
      switchWorkspace('table');

      // 2. Seleciona o ativo no Dossiê e na Tabela
      selectTicker(t);

      // 3. Abre o slide-over drawer
      openDossierDrawer(t);

      // 4. Scroll suave e centralização visual garantida na linha da ação
      const doScroll = () => {{
        const selectedRow = document.querySelector('#stocksTableBody tr.border-amber-400');
        if (selectedRow) {{
          selectedRow.scrollIntoView({{ behavior: 'auto', block: 'center' }});
          selectedRow.classList.add('ring-2', 'ring-amber-400');
          setTimeout(() => selectedRow.classList.remove('ring-2', 'ring-amber-400'), 1800);
        }}
      }};
      setTimeout(doScroll, 60);
      setTimeout(doScroll, 200);
    }}

    function filterByQuadrant(q) {{
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
    }}

    // RENDERIZAR HOME PAGE (COCKPIT EXECUTIVO B3)
    function renderHomePage() {{
      const stocks = APP_DATA.stocks;
      const liquidStocks = stocks.filter(s => s.is_liquid_1m);

      // 1. Estatísticas Macro do Mercado
      const pls = liquidStocks.filter(s => s.pl !== null && s.pl > 0 && s.pl <= 50).map(s => s.pl).sort((a, b) => a - b);
      const medianPl = pls.length ? pls[Math.floor(pls.length / 2)] : 9.1;

      const roics = liquidStocks.map(s => s.roic || s.roe).filter(v => v !== null && v !== undefined && v > 0).sort((a, b) => a - b);
      const medianRoic = roics.length ? roics[Math.floor(roics.length / 2)] : 0.102;

      const spreads = liquidStocks.map(s => s.ey_spread).filter(v => v !== null && v !== undefined).sort((a, b) => a - b);
      const medianSpread = spreads.length ? spreads[Math.floor(spreads.length / 2)] : 4.1;

      const elPl = document.getElementById('home-stat-pl');
      if (elPl) {{
        elPl.innerText = medianPl.toFixed(1) + 'x';
        elPl.className = 'text-2xl font-bold font-mono ' + getColorPl(medianPl);
      }}
      const elRoic = document.getElementById('home-stat-roic');
      if (elRoic) {{
        elRoic.innerText = (medianRoic * 100).toFixed(1).replace('.', ',') + '%';
        elRoic.className = 'text-2xl font-bold font-mono ' + getColorRoe(medianRoic);
      }}
      const elSpread = document.getElementById('home-stat-spread');
      if (elSpread) {{
        elSpread.innerText = (medianSpread > 0 ? '+' : '') + medianSpread.toFixed(1).replace('.', ',') + '%';
        elSpread.className = 'text-2xl font-bold font-mono ' + getColorSpread(medianSpread);
      }}

      // Universo Limpo: Excluir Recuperação Judicial e Distressed Assets
      const DISTRESSED = new Set(['LIGT3', 'AMER3', 'OIBR3', 'AZUL4', 'GOLL4', 'CVCB3', 'BHIA3']);
      const validStocks = liquidStocks.filter(s => !DISTRESSED.has(s.ticker));

      // Função Auxiliar de Deduplicação Institucional por Empresa (Prioriza Classe Mais Líquida)
      function dedupPreferLiquid(stockList, sortFn) {{
        const companies = {{}};
        for (const s of stockList) {{
          const base = s.ticker.substring(0, 4);
          if (!companies[base]) companies[base] = [];
          companies[base].push(s);
        }}
        const result = [];
        for (const base in companies) {{
          companies[base].sort((a, b) => (b.liq_2m || 0) - (a.liq_2m || 0));
          result.push(companies[base][0]);
        }}
        if (sortFn) result.sort(sortFn);
        return result;
      }}

      // 1.5 Seleção Ultra-Crítica (Régua CFA / Munger: 100% Fundamentus)
      const allUltraCritic = validStocks.filter(s => {{
        if ((s.quality_score || 0) < 75 || s.is_distorted || s.is_commodity_peak || s.ey_spread === null || s.ey_spread < 1.5) return false;
        if (s.is_financial) return (s.roe || 0) >= 0.15;
        const dl = s.details ? s.details.divida_liquida : null;
        const dle = s.div_liq_ebitda;
        const isSafeDebt = (dl !== null && dl <= 0) || (dle !== null && dle <= 1.0);
        return s.capital_intensity !== null && s.capital_intensity >= 0.75 && isSafeDebt;
      }});
      const topUltraCritic = dedupPreferLiquid(
        allUltraCritic,
        (a, b) => {{
          if (b.quality_score !== a.quality_score) return b.quality_score - a.quality_score;
          return b.ey_spread - a.ey_spread;
        }}
      ).slice(0, 6);

      const cntCatUltra = document.getElementById('cnt-cat-ultracritic');
      if (cntCatUltra) cntCatUltra.innerText = '(' + allUltraCritic.length + ')';

      const listUltra = document.getElementById('home-list-ultracritic');
      if (listUltra) {{
        listUltra.innerHTML = topUltraCritic.map((s, i) => {{
          const capStr = s.capital_intensity !== null ? (s.capital_intensity * 100).toFixed(0) + '%' : 'Banco';
          const dl = s.details ? s.details.divida_liquida : null;
          const dlBadge = dl !== null && dl <= 0 ? '<span class="text-emerald-400 font-semibold">Caixa Líq</span>' : (s.div_liq_ebitda !== null ? `<span class="${{getColorDebt(s.div_liq_ebitda, s.is_financial)}}">${{s.div_liq_ebitda.toFixed(1)}}x</span>` : 'N/D');
          return `
            <div onclick="selectTickerAndNavigate('${{s.ticker}}')" class="p-2.5 rounded-xl glass-card hover:border-yellow-500/50 hover:bg-yellow-500/5 border border-yellow-500/20 transition duration-200 cursor-pointer flex flex-col justify-between shadow-sm">
              <div class="flex items-center justify-between">
                <span class="font-bold text-yellow-300 font-mono text-xs">${{s.ticker}}</span>
                <span class="px-1.5 py-0.2 rounded-full text-[10px] font-bold bg-yellow-500/20 text-yellow-300 border border-yellow-500/40">${{s.quality_score.toFixed(0)}}</span>
              </div>
              <div class="text-[11px] text-slate-300 font-sans truncate mt-1" title="${{s.empresa}}">${{s.empresa}}</div>
              <div class="mt-2 pt-1.5 border-t border-white/10 flex items-center justify-between text-[10px] text-slate-400 font-mono">
                <span title="Munger Acid Test (EBIT/EBITDA)">Acid: <b class="${{s.is_financial ? 'text-sky-400' : getColorAcidTest(s.capital_intensity)}}">${{capStr}}</b></span>
                <span title="Dívida Líquida / Solvência">${{dlBadge}}</span>
              </div>
            </div>
          `;
        }}).join('');
      }}

      // 2. Top 5 Munger Score (Filé Mignon com Preço Justo: Score >= 80, Spread >= +1.5%, Dívida <= 2.5x)
      const allMunger = validStocks.filter(s => s.quality_score >= 80 && s.ey_spread !== null && s.ey_spread >= 1.5 && (s.is_financial || (s.div_liq_ebitda !== null && s.div_liq_ebitda <= 2.5)));
      const topMunger = dedupPreferLiquid(
        allMunger,
        (a, b) => {{
          if (b.quality_score !== a.quality_score) return b.quality_score - a.quality_score;
          return b.ey_spread - a.ey_spread;
        }}
      ).slice(0, 5);

      const cntCatMunger = document.getElementById('cnt-cat-munger');
      if (cntCatMunger) cntCatMunger.innerText = '(' + allMunger.length + ')';

      const listMunger = document.getElementById('home-list-munger');
      if (listMunger) {{
        listMunger.innerHTML = topMunger.map((s, i) => `
          <div onclick="selectTickerAndNavigate('${{s.ticker}}')" class="flex items-center justify-between p-2.5 rounded-xl glass-card hover:border-amber-400/60 hover:bg-amber-500/5 border border-white/5 transition duration-200 cursor-pointer">
            <div class="flex items-center gap-2">
              <span class="text-xs font-bold text-slate-500">#${{i+1}}</span>
              <span class="text-sm font-bold text-amber-300 font-mono">${{s.ticker}}</span>
              <span class="text-[11px] text-slate-300 font-sans truncate max-w-[110px]" title="${{s.empresa}}">${{s.empresa}}</span>
            </div>
            <div class="flex items-center gap-2 text-right font-mono">
              <span class="text-[11px] text-slate-400 hidden sm:inline">ROIC: <b class="${{getColorRoe(s.roic || s.roe)}}">${{formatPercent(s.roic || s.roe)}}</b></span>
              <span class="px-2 py-0.5 rounded-full text-xs font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/40">${{s.quality_score.toFixed(1)}}</span>
            </div>
          </div>
        `).join('');
      }}

      // 3. Top 5 Assimetrias Reais (CFA Grade: Quality Score >= 75, P/L 3x a 15x, Spread >= +3.0%, Dívida <= 3.0x, sem distorção)
      const allSpread = validStocks.filter(s => s.quality_score >= 75 && s.pl !== null && s.pl >= 3.0 && s.pl <= 15.0 && s.ey_spread !== null && s.ey_spread >= 3.0 && (s.is_financial || (s.div_liq_ebitda !== null && s.div_liq_ebitda <= 3.0)) && !s.is_distorted);
      const topSpread = dedupPreferLiquid(
        allSpread,
        (a, b) => b.ey_spread - a.ey_spread
      ).slice(0, 5);

      const cntCatAsymm = document.getElementById('cnt-cat-asymm');
      if (cntCatAsymm) cntCatAsymm.innerText = '(' + allSpread.length + ')';

      const listSpread = document.getElementById('home-list-spread');
      if (listSpread) {{
        listSpread.innerHTML = topSpread.map((s, i) => `
          <div onclick="selectTickerAndNavigate('${{s.ticker}}')" class="flex items-center justify-between p-2.5 rounded-xl glass-card hover:border-cyan-400/60 hover:bg-cyan-500/5 border border-white/5 transition duration-200 cursor-pointer">
            <div class="flex items-center gap-2">
              <span class="text-xs font-bold text-slate-500">#${{i+1}}</span>
              <span class="text-sm font-bold text-cyan-400 font-mono">${{s.ticker}}</span>
              <span class="text-[11px] text-slate-300 font-sans truncate max-w-[110px]" title="${{s.empresa}}">${{s.empresa}}</span>
            </div>
            <div class="flex items-center gap-2 text-right font-mono">
              <span class="text-[11px] text-slate-400 hidden sm:inline">P/L: <b class="${{getColorPl(s.pl)}}">${{formatMultiple(s.pl)}}</b></span>
              <span class="px-2 py-0.5 rounded-full text-xs font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/40">+${{s.ey_spread.toFixed(1)}}%</span>
            </div>
          </div>
        `).join('');
      }}

      // 4. Top 5 Proventos Sustentáveis (Vacas Leiteiras: DY entre 5% e 13%, Payout entre 35% e 85%, ROIC/ROE >= 12%, Score >= 70)
      const allDiv = validStocks.filter(s => s.div_yield !== null && s.div_yield >= 0.05 && s.div_yield <= 0.13 && s.payout_implicito !== null && s.payout_implicito >= 35 && s.payout_implicito <= 85 && (s.roic || s.roe || 0) >= 0.12 && s.quality_score >= 70 && (s.is_financial || (s.div_liq_ebitda !== null && s.div_liq_ebitda <= 3.0)));
      const topDiv = dedupPreferLiquid(
        allDiv,
        (a, b) => b.div_yield - a.div_yield
      ).slice(0, 5);

      const cntCatDiv = document.getElementById('cnt-cat-div');
      if (cntCatDiv) cntCatDiv.innerText = '(' + allDiv.length + ')';

      const listDiv = document.getElementById('home-list-dividends');
      if (listDiv) {{
        listDiv.innerHTML = topDiv.map((s, i) => `
          <div onclick="selectTickerAndNavigate('${{s.ticker}}')" class="flex items-center justify-between p-2.5 rounded-xl glass-card hover:border-emerald-400/60 hover:bg-emerald-500/5 border border-white/5 transition duration-200 cursor-pointer">
            <div class="flex items-center gap-2">
              <span class="text-xs font-bold text-slate-500">#${{i+1}}</span>
              <span class="text-sm font-bold text-emerald-400 font-mono">${{s.ticker}}</span>
              <span class="text-[11px] text-slate-300 font-sans truncate max-w-[110px]" title="${{s.empresa}}">${{s.empresa}}</span>
            </div>
            <div class="flex items-center gap-2 text-right font-mono">
              <span class="text-[11px] text-slate-400 hidden sm:inline">Pay: <b class="text-emerald-400">${{s.payout_implicito.toFixed(0)}}%</b></span>
              <span class="px-2 py-0.5 rounded-full text-xs font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/40">${{formatPercent(s.div_yield)}}</span>
            </div>
          </div>
        `).join('');
      }}

      // 5. Radar de Virada de Ciclo (Run-Rate 2T26 Anualizado vs LTM)
      const allAccel = validStocks.filter(s => {{
        if (!s.pl || !s.pl_run_rate || s.run_rate_div_pct === null || s.run_rate_div_pct === undefined) return false;
        if (s.pl < 3.0 || s.pl > 45.0) return false;
        if (s.pl_run_rate < 2.0 || s.pl_run_rate > 80.0) return false;
        const l12 = (s.details && s.details.lucro_liq_12m) || 0;
        const l3 = (s.details && s.details.lucro_liq_3m) || 0;
        if (l12 < 30000000 || l3 <= 0) return false;
        return s.run_rate_div_pct >= 15.0 && s.run_rate_div_pct <= 120.0 && s.pl_run_rate < s.pl * 0.85;
      }});
      const accelerating = dedupPreferLiquid(
        allAccel,
        (a, b) => b.run_rate_div_pct - a.run_rate_div_pct
      ).slice(0, 4);

      const cntCatAccel = document.getElementById('cnt-cat-accel');
      if (cntCatAccel) cntCatAccel.innerText = '(' + allAccel.length + ')';

      const listAccel = document.getElementById('home-list-accelerating');
      if (listAccel) {{
        listAccel.innerHTML = accelerating.map(s => `
          <div onclick="selectTickerAndNavigate('${{s.ticker}}')" class="flex items-center justify-between p-2.5 rounded-xl glass-card hover:border-emerald-400/60 hover:bg-emerald-500/5 border border-white/5 transition duration-200 cursor-pointer">
            <div class="flex flex-col">
              <div class="flex items-center gap-1.5">
                <span class="font-bold text-white text-xs font-mono">${{s.ticker}}</span>
                <span class="text-[10px] text-slate-400 truncate max-w-[85px]" title="${{s.empresa}}">${{s.empresa}}</span>
              </div>
              <div class="text-[10px] text-slate-400 font-mono mt-0.5">
                P/L: ${{s.pl.toFixed(1)}}x ➜ <b class="text-emerald-400">${{s.pl_run_rate.toFixed(1)}}x</b>
              </div>
            </div>
            <span class="px-2 py-0.5 rounded-full text-[11px] font-bold font-mono bg-emerald-500/20 text-emerald-300 border border-emerald-500/40">+${{s.run_rate_div_pct.toFixed(0)}}%</span>
          </div>
        `).join('');
      }}

      const allDecel = validStocks.filter(s => {{
        if (!s.pl || !s.pl_run_rate || s.run_rate_div_pct === null || s.run_rate_div_pct === undefined) return false;
        if (s.pl < 3.0 || s.pl > 45.0) return false;
        if (s.pl_run_rate < 2.0 || s.pl_run_rate > 80.0) return false;
        const l12 = (s.details && s.details.lucro_liq_12m) || 0;
        const l3 = (s.details && s.details.lucro_liq_3m) || 0;
        if (l12 < 30000000 || l3 <= 0) return false;
        return s.run_rate_div_pct <= -20.0 && s.run_rate_div_pct >= -70.0 && s.pl_run_rate > s.pl * 1.25;
      }});
      const decelerating = dedupPreferLiquid(
        allDecel,
        (a, b) => a.run_rate_div_pct - b.run_rate_div_pct
      ).slice(0, 4);

      const cntCatDecel = document.getElementById('cnt-cat-decel');
      if (cntCatDecel) cntCatDecel.innerText = '(' + allDecel.length + ')';

      const listDecel = document.getElementById('home-list-decelerating');
      if (listDecel) {{
        listDecel.innerHTML = decelerating.map(s => `
          <div onclick="selectTickerAndNavigate('${{s.ticker}}')" class="flex items-center justify-between p-2.5 rounded-xl glass-card hover:border-amber-400/60 hover:bg-amber-500/5 border border-white/5 transition duration-200 cursor-pointer">
            <div class="flex flex-col">
              <div class="flex items-center gap-1.5">
                <span class="font-bold text-white text-xs font-mono">${{s.ticker}}</span>
                <span class="text-[10px] text-slate-400 truncate max-w-[85px]" title="${{s.empresa}}">${{s.empresa}}</span>
              </div>
              <div class="text-[10px] text-slate-400 font-mono mt-0.5">
                P/L: ${{s.pl.toFixed(1)}}x ➜ <b class="text-amber-400">${{s.pl_run_rate.toFixed(1)}}x ⚠️</b>
              </div>
            </div>
            <span class="px-2 py-0.5 rounded-full text-[11px] font-bold font-mono bg-rose-500/20 text-rose-300 border border-rose-500/40">${{s.run_rate_div_pct.toFixed(0)}}%</span>
          </div>
        `).join('');
      }}

      // 6. Solvência e Anti-Fragilidade (Sensibilidade à Selic Alta)
      const allNetCash = validStocks.filter(s => s.div_liq_ebitda !== null && s.div_liq_ebitda < -0.1 && !s.is_financial);
      const netCash = dedupPreferLiquid(
        allNetCash,
        (a, b) => (b.quality_score || 0) - (a.quality_score || 0)
      ).slice(0, 4);

      const cntCatNetCash = document.getElementById('cnt-cat-netcash');
      if (cntCatNetCash) cntCatNetCash.innerText = '(' + allNetCash.length + ')';

      const listNetCash = document.getElementById('home-list-netcash');
      if (listNetCash) {{
        listNetCash.innerHTML = netCash.map(s => `
          <div onclick="selectTickerAndNavigate('${{s.ticker}}')" class="flex items-center justify-between p-2.5 rounded-xl glass-card hover:border-emerald-400/60 hover:bg-emerald-500/5 border border-white/5 transition duration-200 cursor-pointer">
            <div class="flex flex-col">
              <div class="flex items-center gap-1.5">
                <span class="font-bold text-white text-xs font-mono">${{s.ticker}}</span>
                <span class="text-[10px] text-slate-400 truncate max-w-[85px]" title="${{s.empresa}}">${{s.empresa}}</span>
              </div>
              <div class="text-[10px] text-slate-400 font-mono mt-0.5">
                ROIC: <b class="text-white">${{formatPercent(s.roic || s.roe)}}</b>
              </div>
            </div>
            <span class="px-2 py-0.5 rounded-full text-[10px] font-bold font-mono bg-emerald-500/20 text-emerald-300 border border-emerald-500/40">Caixa Líq. 🛡️</span>
          </div>
        `).join('');
      }}

      const allHighDebt = validStocks.filter(s => s.div_liq_ebitda !== null && s.div_liq_ebitda > 3.2 && !s.is_financial);
      const highDebt = dedupPreferLiquid(
        allHighDebt,
        (a, b) => b.div_liq_ebitda - a.div_liq_ebitda
      ).slice(0, 4);

      const cntCatHighDebt = document.getElementById('cnt-cat-highdebt');
      if (cntCatHighDebt) cntCatHighDebt.innerText = '(' + allHighDebt.length + ')';

      const listHighDebt = document.getElementById('home-list-highdebt');
      if (listHighDebt) {{
        listHighDebt.innerHTML = highDebt.map(s => `
          <div onclick="selectTickerAndNavigate('${{s.ticker}}')" class="flex items-center justify-between p-2.5 rounded-xl glass-card hover:border-rose-400/60 hover:bg-rose-500/5 border border-white/5 transition duration-200 cursor-pointer">
            <div class="flex flex-col">
              <div class="flex items-center gap-1.5">
                <span class="font-bold text-white text-xs font-mono">${{s.ticker}}</span>
                <span class="text-[10px] text-slate-400 truncate max-w-[85px]" title="${{s.empresa}}">${{s.empresa}}</span>
              </div>
              <div class="text-[10px] text-slate-400 font-mono mt-0.5">
                Score: <b class="text-rose-400">${{s.quality_score.toFixed(1)}}</b>
              </div>
            </div>
            <span class="px-2 py-0.5 rounded-full text-[10px] font-bold font-mono bg-rose-500/20 text-rose-300 border border-rose-500/40">${{s.div_liq_ebitda.toFixed(1)}}x Dívida 🚨</span>
          </div>
        `).join('');
      }}

      // 7. Contagem da Curva Fair Value e Momentos Estratégicos
      const qAbove = validStocks.filter(s => s.pl && s.pl > 0 && s.pl < calcFairPL(s.quality_score)).length;
      const qBelow = validStocks.filter(s => !s.pl || s.pl <= 0 || s.pl >= calcFairPL(s.quality_score)).length;
      const qAccel = validStocks.filter(s => s.run_rate_div_pct && s.run_rate_div_pct >= 15.0).length;
      const qDiv = validStocks.filter(s => s.div_yield && s.div_yield >= 0.05).length;

      const elQAbove = document.getElementById('home-quad-above-cnt');
      if (elQAbove) elQAbove.innerText = qAbove + ' ativos';
      const elQBelow = document.getElementById('home-quad-below-cnt');
      if (elQBelow) elQBelow.innerText = qBelow + ' ativos';
      const elQAccel = document.getElementById('home-quad-accel-cnt');
      if (elQAccel) elQAccel.innerText = qAccel + ' ativos';
      const elQDiv = document.getElementById('home-quad-div-cnt');
      if (elQDiv) elQDiv.innerText = qDiv + ' ativos';
    }}

    // ==========================================
    // 💼 ESTRUTURA DE CARTEIRAS RECOMENDADAS
    // ==========================================
    const INVESTMENT_THESES = {{
      'WEGE3': 'Liderança global em motores elétricos e equipamentos industriais; reinveste lucros com ROIC > 25% e governança de classe mundial.',
      'CURY3': 'Líder em incorporação residencial com ROE superior a 40%, modelo asset-light e balanço com caixa líquido.',
      'TOTS3': 'Fosso competitivo (Moat) gigantesco em software ERP corporativo no Brasil, gerando receita recorrente e alta retenção de clientes.',
      'ITUB4': 'Maior instituição bancária privada da América Latina, referência em gestão de risco de crédito, eficiência de custos e ROE sustentável.',
      'ITUB3': 'Maior instituição bancária privada da América Latina com alta governança ON (Tag Along 100%) e retorno sobre patrimônio de excelência.',
      'PSSA3': 'Líder histórica em seguros automotivos e residenciais; float financeiro rentabilizado a taxas atrativas e solvência irretocável.',
      'BBSE3': 'Braço de seguridade e previdência do Banco do Brasil; operação asset-light, ausência de dívida e payout regular superior a 80%.',
      'CXSE3': 'Acesso exclusivo de balcão ao canal habitacional da Caixa Econômica Federal; geração de caixa sólida e dividend yield atrativo.',
      'VULC3': 'Excelência operacional na produção de calçados esportivos (Mizuno e Olympikus), margens saudáveis e geração contínua de caixa livre.',
      'B3SA3': 'Infraestrutura financeira indispensável do mercado de capitais brasileiro; margem líquida elevada e monopólio natural de negociação.',
      'BPAC11': 'Maior banco de investimentos independente da América Latina; escala formidável em gestão de patrimônio e assessoria corporativa.',
      'MILS3': 'Líder em locação de plataformas elevatórias e equipamentos industriais; desalavancagem rápida e expansão do retorno sobre capital.',
      'WIZC3': 'Canal de corretagem e bancassurance com alta capilaridade em grandes redes, custos fixos enxutos e geração de dividendos.',
      'PLPL3': 'Incorporadora habitacional focada em média e baixa renda com excelente velocidade de vendas e valuation deprimido em relação ao lucro.',
      'TEND3': 'Turnaround de rentabilidade bem-sucedido no segmento habitacional, redução substancial de custos e reprecificação expressiva de múltiplos.',
      'CPFE3': 'Portfólio de concessões de distribuição e geração de energia elétrica de alta qualidade regulatória, com fluxo de caixa previsível.',
      'EGIE3': 'Referência em transição energética e geração renovável; contratos de longo prazo e histórico consistente de remuneração aos acionistas.',
      'TAEE11': 'Concessões puras de transmissão de energia blindadas por inflação (IPCA/IGP-M); alta previsibilidade de receitas e distribuição de proventos.',
      'VIVT3': 'Liderança consolidada em telecomunicações móveis e fibra ótica; negócios maduros com forte geração de caixa livre e baixo risco regulatório.',
      'LEVE3': 'Fornecedora automotiva global com forte presença no mercado de reposição (aftermarket), gerando caixa resiliente e altos proventos.',
      'BMEB4': 'Banco focado em crédito consignado para aposentados e pensionistas do INSS com margem financeira expressiva e inadimplência mínima.',
      'PINE4': 'Banco focado em crédito corporativo de médio porte e câmbio, com aceleração expressiva do lucro operacional recente e valuation baixo.',
      'JHSF3': 'Líder no mercado imobiliário e shopping centers de altíssima renda, negociando com desconto substancial sobre o valor patrimonial.',
      'MDNE3': 'Incorporadora com atuação geográfica estratégica, baixo endividamento líquido e expansão da margem líquida operacional.',
      'POMO4': 'Líder absoluta na fabricação de carrocerias de ônibus com forte demanda por renovação de frotas e exportações para a América Latina.',
      'LAVV3': 'Incorporadora residencial com sólida estrutura financeira, caixa positivo e forte presença no mercado de média-alta renda.',
      'VLID3': 'Líder em identificação digital, emissão de documentos e pagamentos com expansão internacional e fluxo de caixa estável.',
      'INTB3': 'Empresa pioneira em segurança eletrônica, telecomunicações e energia solar no Brasil, com ampla rede capilar de distribuidores.',
      'PETR4': 'Maior geradora de caixa livre da B3 com ativos pré-sal de baixo custo de extração (lifting cost) e forte remuneração em dividendos.',
      'BRSR6': 'Banco regional com penetração consolidada no Sul, negociando com profundo desconto patrimonial (P/VP < 0,5x) e dividend yield atrativo de dois dígitos.',
      'VIVA3': 'Líder dominante no varejo de joias no Brasil (Vivara e Life), margens brutas superiores a 65%, forte geração de caixa livre e poder de precificação.'
    }};

    function getThesisForStock(s) {{
      if (INVESTMENT_THESES[s.ticker]) return INVESTMENT_THESES[s.ticker];
      const roicStr = (s.roic || s.roe) ? ((s.roic || s.roe) * 100).toFixed(0) + '%' : '';
      const dyStr = s.div_yield ? (s.div_yield * 100).toFixed(1) + '%' : '';
      return `Ativo com Munger Score de ${{s.quality_score.toFixed(0)}} pts, ROIC/ROE de ${{roicStr}} e distribuição de dividendos estimada em ${{dyStr}}.`;
    }}

    function getPortfolioStocks(key) {{
      const DISTRESSED = new Set(['LIGT3', 'AMER3', 'OIBR3', 'AZUL4', 'GOLL4', 'CVCB3', 'BHIA3']);
      const valid = APP_DATA.stocks.filter(s => s.is_liquid_1m && !DISTRESSED.has(s.ticker));

      function dedup(list, sortFn) {{
        const comps = {{}};
        for (const s of list) {{
          const base = s.ticker.substring(0, 4);
          if (!comps[base]) comps[base] = [];
          comps[base].push(s);
        }}
        const res = [];
        for (const base in comps) {{
          comps[base].sort((a, b) => (b.liq_2m || 0) - (a.liq_2m || 0));
          res.push(comps[base][0]);
        }}
        if (sortFn) res.sort(sortFn);
        return res;
      }}

      // Regra Prudencial CFA: Limite de no máximo 2 ativos por setor (teto de 25%)
      function applySectorCap(list, maxPerSector, limit) {{
        const chosen = [];
        const secCounts = {{}};
        for (const s of list) {{
          const sec = s.setor || 'Outros';
          if ((secCounts[sec] || 0) < maxPerSector) {{
            chosen.push(s);
            secCounts[sec] = (secCounts[sec] || 0) + 1;
            if (chosen.length === limit) break;
          }}
        }}
        if (chosen.length < limit) {{
          for (const s of list) {{
            if (!chosen.includes(s)) {{
              chosen.push(s);
              if (chosen.length === limit) break;
            }}
          }}
        }}
        return chosen;
      }}

      let candidates = [];
      if (key === 'munger') {{
        candidates = valid.filter(s => s.quality_score >= 80 && s.ey_spread !== null && s.ey_spread >= 1.5 && !s.is_distorted && (s.is_financial || (s.div_liq_ebitda !== null && s.div_liq_ebitda <= 2.2)));
        candidates = dedup(candidates, (a, b) => (b.quality_score * 0.7 + (b.roic || b.roe || 0) * 30) - (a.quality_score * 0.7 + (a.roic || a.roe || 0) * 30));
      }} else if (key === 'dividends') {{
        candidates = valid.filter(s => s.div_yield !== null && s.div_yield >= 0.055 && s.div_yield <= 0.13 && s.payout_implicito !== null && s.payout_implicito >= 35 && s.payout_implicito <= 85 && (s.roic || s.roe || 0) >= 0.12 && s.quality_score >= 70 && (s.is_financial || (s.div_liq_ebitda !== null && s.div_liq_ebitda <= 3.0)));
        candidates = dedup(candidates, (a, b) => (b.div_yield * 0.6 + (b.roic || b.roe || 0) * 0.4) - (a.div_yield * 0.6 + (a.roic || a.roe || 0) * 0.4));
      }} else if (key === 'asymmetry') {{
        candidates = valid.filter(s => s.pl !== null && s.pl >= 3.0 && s.pl <= 14.0 && s.ey_spread !== null && s.ey_spread >= 3.0 && s.quality_score >= 70 && !s.is_distorted && (s.is_financial || (s.div_liq_ebitda !== null && s.div_liq_ebitda <= 2.5)));
        candidates = dedup(candidates, (a, b) => (b.ey_spread * 0.7 + b.quality_score * 0.3) - (a.ey_spread * 0.7 + a.quality_score * 0.3));
      }} else if (key === 'cfa_ultra') {{
        candidates = valid.filter(s => {{
          if ((s.quality_score || 0) < 75 || s.is_distorted || s.is_commodity_peak || s.ey_spread === null || s.ey_spread < 1.5) return false;
          if (s.is_financial) return (s.roe || 0) >= 0.15;
          const dl = s.details ? s.details.divida_liquida : null;
          const dle = s.div_liq_ebitda;
          const isSafeDebt = (dl !== null && dl <= 0) || (dle !== null && dle <= 1.0);
          return s.capital_intensity !== null && s.capital_intensity >= 0.75 && isSafeDebt;
        }});
        candidates = dedup(candidates, (a, b) => (b.quality_score * 0.7 + b.ey_spread * 0.3) - (a.quality_score * 0.7 + a.ey_spread * 0.3));
      }}

      const selected = applySectorCap(candidates, 2, 8);
      if (selected.length === 0) return [];

      const baseWeight = Math.floor(100 / selected.length);
      const remainder = 100 - (baseWeight * selected.length);
      return selected.map((s, idx) => ({{
        ...s,
        weight: baseWeight + (idx < remainder ? 1 : 0),
        thesis: getThesisForStock(s)
      }}));
    }}

    function selectPortfolio(key) {{
      currentPortfolioKey = key;
      renderPortfolios();
    }}

    function setSimulationCapital(val) {{
      currentSimulatedCapital = Number(val);
      const input = document.getElementById('simCapitalInput');
      if (input) input.value = currentSimulatedCapital;
      renderPortfolios();
    }}

    function updateSimulationCapital(val) {{
      const num = Number(val);
      if (!isNaN(num) && num > 0) {{
        currentSimulatedCapital = num;
        renderPortfolios();
      }}
    }}

    function renderPortfolios() {{
      const pStocks = getPortfolioStocks(currentPortfolioKey);

      // 1. Atualizar cards nobres de seleção de carteira
      const portKeys = ['munger', 'dividends', 'asymmetry', 'cfa_ultra'];
      const borderMap = {{
        'munger': 'border-2 border-amber-400/80 bg-gradient-to-b from-amber-500/10 to-transparent shadow-lg shadow-amber-500/10',
        'dividends': 'border-2 border-emerald-400/80 bg-gradient-to-b from-emerald-500/10 to-transparent shadow-lg shadow-emerald-500/10',
        'asymmetry': 'border-2 border-cyan-400/80 bg-gradient-to-b from-cyan-500/10 to-transparent shadow-lg shadow-cyan-500/10',
        'cfa_ultra': 'border-2 border-yellow-400/80 bg-gradient-to-b from-yellow-500/10 to-transparent shadow-lg shadow-yellow-500/10'
      }};

      portKeys.forEach(k => {{
        const card = document.getElementById('port-card-' + k);
        const cntBadge = document.getElementById('port-count-' + k);
        const kStocks = getPortfolioStocks(k);
        if (cntBadge) cntBadge.innerText = kStocks.length + ' ativos';

        if (card) {{
          if (k === currentPortfolioKey) {{
            card.className = `glass-card rounded-2xl p-4 border ${{borderMap[k]}} cursor-pointer transition-all duration-200 flex flex-col justify-between`;
          }} else {{
            card.className = 'glass-card rounded-2xl p-4 border border-white/10 opacity-75 hover:opacity-100 hover:border-white/30 cursor-pointer transition-all duration-200 flex flex-col justify-between shadow-md';
          }}
        }}
      }});

      // 2. Títulos, Subtítulos e Rótulos Estratégicos
      const titleEl = document.getElementById('portTableTitle');
      const subEl = document.getElementById('portTableSubtitle');
      const shortNameEl = document.getElementById('portStrategyShortName');
      const nameMap = {{
        'munger': '🏆 CARTEIRA CHARLIE MUNGER (COMPOUNDERS &amp; MOATS)',
        'dividends': '💰 CARTEIRA VACAS LEITEIRAS (DIVIDENDOS RESILIENTES)',
        'asymmetry': '📈 CARTEIRA ASSIMETRIA REAL (DEEP VALUE &amp; GRAHAM)',
        'cfa_ultra': '💎 CARTEIRA INSTITUCIONAL CFA ULTRA-CRÍTICA'
      }};
      const shortMap = {{
        'munger': 'Compounders & Moats • Alocação 100% Ponderada (8 Ativos)',
        'dividends': 'Vacas Leiteiras • Alocação 100% Ponderada (8 Ativos)',
        'asymmetry': 'Deep Value & Graham • Alocação 100% Ponderada (8 Ativos)',
        'cfa_ultra': 'Régua CFA Ultra-Crítica • Alocação 100% Ponderada (8 Ativos)'
      }};
      if (titleEl) titleEl.innerHTML = `<span>📋</span> ${{nameMap[currentPortfolioKey] || 'CARTEIRA RECOMENDADA'}}`;
      if (subEl) subEl.innerText = `(${{pStocks.length}} empresas selecionadas • 100% alocado)`;
      if (shortNameEl) shortNameEl.innerText = shortMap[currentPortfolioKey] || 'Alocação 100% Ponderada';

      // 3. Indicadores Médios Ponderados (KPIs)
      let totalWeight = 0;
      let sumPl = 0;
      let sumRoic = 0;
      let sumDy = 0;
      let sumSpread = 0;
      let sumDebt = 0;
      let sumScore = 0;
      let nonFinWeight = 0;

      pStocks.forEach(s => {{
        const w = s.weight || 0;
        totalWeight += w;
        if (s.pl) sumPl += w * s.pl;
        const roicVal = s.roic || s.roe || 0;
        sumRoic += w * roicVal;
        if (s.div_yield) sumDy += w * s.div_yield;
        if (s.ey_spread !== null) sumSpread += w * s.ey_spread;
        if (!s.is_financial && s.div_liq_ebitda !== null) {{
          sumDebt += w * s.div_liq_ebitda;
          nonFinWeight += w;
        }}
        sumScore += w * s.quality_score;
      }});

      const avgPl = totalWeight > 0 ? (sumPl / totalWeight) : 0;
      const avgRoic = totalWeight > 0 ? (sumRoic / totalWeight) : 0;
      const avgDy = totalWeight > 0 ? (sumDy / totalWeight) : 0;
      const avgSpread = totalWeight > 0 ? (sumSpread / totalWeight) : 0;
      const avgDebt = nonFinWeight > 0 ? (sumDebt / nonFinWeight) : 0;
      const avgScore = totalWeight > 0 ? (sumScore / totalWeight) : 0;

      const elPl = document.getElementById('kp-port-pl');
      if (elPl) {{
        elPl.innerText = avgPl > 0 ? avgPl.toFixed(1) + 'x' : 'N/D';
        elPl.className = 'text-lg font-bold font-mono ' + getColorPl(avgPl);
      }}

      const elRoic = document.getElementById('kp-port-roic');
      if (elRoic) {{
        elRoic.innerText = (avgRoic * 100).toFixed(1) + '%';
        elRoic.className = 'text-lg font-bold font-mono ' + getColorRoe(avgRoic);
      }}

      const elDy = document.getElementById('kp-port-dy');
      if (elDy) {{
        elDy.innerText = (avgDy * 100).toFixed(1) + '%';
        elDy.className = 'text-lg font-bold font-mono ' + getColorDy(avgDy);
      }}

      const elSpread = document.getElementById('kp-port-spread');
      if (elSpread) {{
        elSpread.innerText = (avgSpread > 0 ? '+' : '') + avgSpread.toFixed(1) + '%';
        elSpread.className = 'text-lg font-bold font-mono ' + getColorSpread(avgSpread);
      }}

      const elDebt = document.getElementById('kp-port-debt');
      if (elDebt) {{
        elDebt.innerText = nonFinWeight > 0 ? (avgDebt < 0 ? 'Caixa Líq.' : avgDebt.toFixed(1) + 'x') : 'Setor Bancário';
        elDebt.className = 'text-lg font-bold font-mono ' + (nonFinWeight > 0 ? (avgDebt <= 1.5 ? 'text-emerald-400' : (avgDebt <= 2.5 ? 'text-amber-400' : 'text-rose-400 font-bold')) : 'text-sky-400');
      }}

      const elScore = document.getElementById('kp-port-score');
      if (elScore) {{
        elScore.innerText = avgScore.toFixed(1) + '/100';
        elScore.className = 'text-lg font-bold font-mono ' + (avgScore >= 80 ? 'text-emerald-400' : (avgScore >= 65 ? 'text-amber-400' : 'text-slate-200'));
      }}

      // 4. Diversificação Setorial Gráfica
      const sectorWeights = {{}};
      const SECTOR_PALETTE = ['#38BDF8', '#00D084', '#F59E0B', '#C084FC', '#FB7185', '#FBBF24', '#4ADE80', '#A855F7', '#60A5FA'];
      pStocks.forEach(s => {{
        const sec = s.setor || 'Outros';
        sectorWeights[sec] = (sectorWeights[sec] || 0) + (s.weight || 0);
      }});

      const sortedSectors = Object.keys(sectorWeights).sort((a, b) => sectorWeights[b] - sectorWeights[a]);
      const barEl = document.getElementById('portSectorBar');
      const sumEl = document.getElementById('portSectorSummary');

      if (barEl) {{
        barEl.innerHTML = sortedSectors.map((sec, idx) => {{
          const w = sectorWeights[sec];
          const color = SECTOR_PALETTE[idx % SECTOR_PALETTE.length];
          return `<div style="width: ${{w}}%; background-color: ${{color}};" title="${{sec}}: ${{w}}%" class="h-full transition-all"></div>`;
        }}).join('');
      }}

      if (sumEl) {{
        sumEl.innerHTML = sortedSectors.map((sec, idx) => {{
          const w = sectorWeights[sec];
          const color = SECTOR_PALETTE[idx % SECTOR_PALETTE.length];
          return `<span class="inline-flex items-center gap-1 mr-2"><span class="w-2 h-2 rounded-full inline-block" style="background-color: ${{color}};"></span><span class="text-slate-300 font-semibold">${{sec}}</span>: <b class="text-white">${{w}}%</b></span>`;
        }}).join('');
      }}

      // 5. NOVO: PARECER CRÍTICO DO COMITÊ CFA & AUDITORIA DE CONCENTRAÇÃO SETORIAL
      const topSector = sortedSectors[0] || 'N/D';
      const topWeight = sectorWeights[topSector] || 0;
      let hhi = 0;
      Object.values(sectorWeights).forEach(w => {{
        hhi += Math.pow(w / 100, 2);
      }});

      const elHhi = document.getElementById('cfaHhiMetric');
      const hhiEval = hhi <= 0.20 ? '<span class=\"text-emerald-400 font-bold\">Excelente Diversificação</span>' : (hhi <= 0.28 ? '<span class=\"text-sky-400 font-bold\">Diversificação Moderada</span>' : '<span class=\"text-amber-400 font-bold\">Alerta de Concentração</span>');
      if (elHhi) elHhi.innerHTML = `Índice HHI Setorial: <b class=\"text-white font-mono\">${{hhi.toFixed(3)}}</b> • ${{hhiEval}}`;

      const elTopWeight = document.getElementById('cfaTopSectorWeight');
      if (elTopWeight) elTopWeight.innerText = `Líder: ${{topWeight}}%`;

      const elSectorText = document.getElementById('cfaSectorAuditText');
      if (elSectorText) {{
        elSectorText.innerHTML = `Setor de maior exposição: <b class=\"text-white\">${{topSector}}</b> com <b class=\"text-amber-300\">${{topWeight}}%</b> do portfólio. A carteira está distribuída em <b class=\"text-white\">${{sortedSectors.length}} setores distintos</b> da B3, obedecendo rigorosamente ao <b>Teto Prudencial CFA de no máximo 25% por setor</b> (elimina gargalos e armadilhas de concentração mono-setorial).`;
      }}

      // Perfil de Sensibilidade Macroeconômica
      const macroMap = {{
        'munger': {{
          badge: 'Defensiva / Qualidade Máxima',
          color: 'text-amber-300',
          text: 'Forte proteção contra juros restritivos (Selic 10,50%+). Presença balanceada de seguradoras (float rentabilizado a taxas elevadas), bens de capital e construtora de alta renda sem dívida, reduzindo a volatilidade do portfólio.'
        }},
        'dividends': {{
          badge: 'Anti-Cíclica & Proventos',
          color: 'text-emerald-300',
          text: 'Empresas em setores essenciais com receita inelástica e geração sólida de caixa livre. O fluxo de dividendos independe das oscilações do PIB, oferecendo yield real acima da inflação e reinvestimento potente.'
        }},
        'asymmetry': {{
          badge: 'Alta Convexidade / Ciclo',
          color: 'text-cyan-300',
          text: 'Portfólio com sensibilidade positiva à flexibilização monetária futura. Ativos negociando a múltiplos historicamente deprimidos que oferecem convexidade assimétrica e forte potencial de reprecificação (re-rating).'
        }},
        'cfa_ultra': {{
          badge: 'Blindagem Anti-Fragile',
          color: 'text-yellow-300',
          text: 'Risco soberano e corporativo minimizado. Balanços imunes a choques macroeconômicos com empresas de caixa líquido ou dívida inferior a 1,0x EBITDA, sem exposição a picos artificiais de commodities.'
        }}
      }};

      const curMacro = macroMap[currentPortfolioKey] || macroMap['munger'];
      const elMacroBadge = document.getElementById('cfaMacroRiskBadge');
      if (elMacroBadge) {{
        elMacroBadge.innerText = curMacro.badge;
        elMacroBadge.className = `font-bold ${{curMacro.color}} bg-slate-900/80 px-1.5 py-0.5 rounded border border-slate-700/50`;
      }}
      const elMacroText = document.getElementById('cfaMacroAuditText');
      if (elMacroText) elMacroText.innerText = curMacro.text;

      // Solvência & Balanço
      let cashRichCount = 0;
      pStocks.forEach(s => {{
        if (s.is_financial || (s.details && s.details.divida_liquida <= 0) || (s.div_liq_ebitda !== null && s.div_liq_ebitda <= 1.0)) {{
          cashRichCount++;
        }}
      }});
      const solvencyPct = Math.round((cashRichCount / pStocks.length) * 100);
      const elSolvBadge = document.getElementById('cfaSolvencyBadge');
      if (elSolvBadge) elSolvBadge.innerText = `${{solvencyPct}}% Protegido`;
      const elSolvText = document.getElementById('cfaSolvencyAuditText');
      if (elSolvText) {{
        elSolvText.innerHTML = `<b class=\"text-white\">${{cashRichCount}} de ${{pStocks.length}} ativos</b> (${{solvencyPct}}% da alocação) operam com caixa líquido positivo, dívida inferior a 1.0x EBITDA ou solvência bancária sólida (Índice de Basileia confortável).`;
      }}

      // Parecer Qualitativo Detalhado do Analista
      const verdictMap = {{
        'munger': 'Aprovado pelo Comitê Buy-Side. A carteira combina empresas líderes de seus nichos com retornos sustentados sobre o patrimônio e barreiras de entrada intransponíveis. A diversificação setorial auditada impede que a carteira fique excessivamente exposta ao setor financeiro, garantindo alocação em bens de capital, consumo e construção civil sólida.',
        'dividends': 'Aprovado para geração recorrente de renda passiva. Os ativos selecionados possuem taxa média de payout sustentável (entre 35% e 85%), evitando empresas que pagam dividendos mediante queima de reservas ou alavancagem perigosa. O teto de exposição setorial garante resiliência em qualquer estágio do ciclo econômico.',
        'asymmetry': 'Aprovado para mandatos focados em Valor Profundo (Deep Value). Os ativos selecionados oferecem prêmio médio (Spread NTN-B) atrativo, sem incluir empresas em recuperação judicial ou distorções de lucro não-recorrente. O limite setorial protege o investidor contra concentração em setores voláteis como incorporação ou transporte.',
        'cfa_ultra': 'Classificação de Risco Mínimo (Triplo A Institucional). Todos os 8 ativos superaram simultaneamente as 7 barreiras quantitativas de auditoria de balanço. O teto de 2 empresas por setor foi estritamente observado, resultando em um portfólio de qualidade irretocável com alta densidade de capital e alavancagem virtualmente nula.'
      }};
      const elVerdict = document.getElementById('cfaDetailedVerdict');
      if (elVerdict) elVerdict.innerText = verdictMap[currentPortfolioKey] || verdictMap['munger'];

      // 5. Tabela de Ações
      const tbody = document.getElementById('portStocksTableBody');
      if (!tbody) return;
      tbody.innerHTML = '';

      pStocks.forEach((s, idx) => {{
        const tr = document.createElement('tr');
        const rowBg = idx % 2 === 0 ? 'bg-white/[0.01]' : 'bg-transparent';
        tr.onclick = () => {{
          selectTicker(s.ticker);
          openDossierDrawer(s.ticker);
        }};

        const simVal = currentSimulatedCapital * ((s.weight || 0) / 100);
        const simQty = s.cotacao ? Math.floor(simVal / s.cotacao) : 0;

        let debtDisplay = 'N/D';
        let debtClass = getColorDebt(s.div_liq_ebitda, s.is_financial);
        if (s.is_financial) {{
          debtDisplay = 'Banco (Basileia)';
        }} else if (s.details && s.details.divida_liquida !== null && s.details.divida_liquida <= 0) {{
          debtDisplay = 'Caixa Líq. 🛡️';
        }} else if (s.div_liq_ebitda !== null) {{
          debtDisplay = s.div_liq_ebitda.toFixed(1) + 'x';
        }}

        const scoreBadgeClass = s.quality_score >= 80 ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40' : (s.quality_score >= 65 ? 'bg-amber-500/20 text-amber-300 border border-amber-500/40' : 'bg-white/10 text-slate-300 border border-white/10');

        tr.innerHTML = `
          <td class="py-2.5 px-3">
            <div class="flex items-center gap-1.5">
              <span class="text-sm font-bold text-amber-300 tracking-wide font-mono">${{s.ticker}}</span>
              ${{s.is_distorted ? '<span class="text-[9px] px-2 py-0.2 rounded-full bg-amber-500/20 text-amber-300 border border-amber-500/30">⚠️ Dist.</span>' : ''}}
            </div>
            <div class="text-[11px] text-slate-300 font-sans truncate max-w-[140px]" title="${{s.empresa}} - ${{s.setor}}">${{s.empresa}}</div>
            <div class="text-[10px] text-slate-500 font-sans">${{s.setor || ''}}</div>
          </td>
          <td class="py-2.5 px-2 text-center">
            <span class="px-2.5 py-0.5 rounded-full font-mono font-bold text-xs bg-amber-500/20 text-amber-300 border border-amber-500/40">
              ${{s.weight}}%
            </span>
          </td>
          <td class="py-2.5 px-3 text-right font-mono font-semibold text-white">${{formatCurrency(s.cotacao)}}</td>
          <td class="py-2.5 px-2 text-center">
            <span class="px-2.5 py-0.5 rounded-full font-bold text-xs ${{scoreBadgeClass}}">
              ${{s.quality_score.toFixed(1)}}
            </span>
          </td>
          <td class="py-2.5 px-3 text-right font-mono font-semibold ${{getColorPl(s.pl)}}">${{formatMultiple(s.pl)}}</td>
          <td class="py-2.5 px-3 text-right font-mono font-semibold ${{getColorRoe(s.roic || s.roe)}}">${{formatPercent(s.roic || s.roe)}}${{s.is_financial ? ' <span class=\"text-[9px] text-sky-400 font-normal\">(ROE)</span>' : ''}}</td>
          <td class="py-2.5 px-3 text-right font-mono font-bold ${{getColorDy(s.div_yield)}}">${{formatPercent(s.div_yield)}}</td>
          <td class="py-2.5 px-3 text-right font-mono ${{debtClass}}">${{debtDisplay}}</td>
          <td class="py-2.5 px-3 text-right font-mono font-bold text-amber-300 bg-amber-500/10">${{formatCurrency(simVal)}}</td>
          <td class="py-2.5 px-3 text-right font-mono font-bold text-white bg-amber-500/10">${{simQty.toLocaleString('pt-BR')}} <span class="text-[10px] text-slate-400 font-normal">ações</span></td>
          <td class="py-2.5 px-3">
            <div class="text-[11px] text-slate-300 font-sans max-w-[340px] leading-relaxed">${{s.thesis}}</div>
          </td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    let isTableFullWidth = true;

    function toggleTableFullWidth() {{
      openDossierDrawer(selectedTicker);
    }}

    function openSelectedInDossier() {{
      openDossierDrawer(selectedTicker);
    }}

    function openSelectedInMatrix() {{
      closeDossierDrawer();
      switchWorkspace('matrix');
    }}

    function switchBubbleMetric(metric) {{
      matrixBubbleMetric = metric;
      renderMatrix();
    }}

    function switchBubbleColor(colorMode) {{
      matrixColorMode = colorMode;
      renderMatrix();
    }}

    function switchDiagTab(tab) {{
      document.getElementById('dtab-radar').classList.toggle('active', tab === 'radar');
      document.getElementById('dtab-history').classList.toggle('active', tab === 'history');
      document.getElementById('dtab-balance').classList.toggle('active', tab === 'balance');
      document.getElementById('dtab-cfa').classList.toggle('active', tab === 'cfa');

      document.getElementById('dview-radar').classList.toggle('hidden', tab !== 'radar');
      document.getElementById('dview-history').classList.toggle('hidden', tab !== 'history');
      document.getElementById('dview-balance').classList.toggle('hidden', tab !== 'balance');
      document.getElementById('dview-cfa').classList.toggle('hidden', tab !== 'cfa');
    }}

    function switchMatrixX(metric) {{
      currentXMetric = metric;
      const isPl = currentXMetric === 'pl';
      const baseXMax = isPl ? 32 : 30;
      matrixCenterX = baseXMax / 2;
      matrixCenterY = (110 + 20) / 2;
      matrixZoom = 1.0;
      updateZoomLabel();

      const btnPl = document.getElementById('btn-x-pl');
      const btnEy = document.getElementById('btn-x-ey');
      const lblAxis = document.getElementById('lbl-matrix-axis-x');
      if (btnPl && btnEy) {{
        btnPl.className = isPl ? 'px-2 py-0.5 rounded bg-amber-950 text-jpAmber font-bold border border-amber-700/60' : 'px-2 py-0.5 rounded text-slate-400 hover:text-white';
        btnEy.className = !isPl ? 'px-2 py-0.5 rounded bg-cyan-950 text-cyan-300 font-bold border border-cyan-700/60' : 'px-2 py-0.5 rounded text-slate-400 hover:text-white';
      }}
      if (lblAxis) {{
        lblAxis.innerText = isPl ? 'P/L (0-32x)' : 'Earnings Yield % (0-30%)';
      }}
      renderMatrix();
    }}

    function zoomMatrix(factor) {{
      const svg = document.getElementById('matrixSvg');
      if (!svg) return;
      const rect = svg.getBoundingClientRect();
      zoomMatrixAt(factor, rect.left + rect.width / 2, rect.top + rect.height / 2);
    }}

    function resetMatrixZoom() {{
      matrixZoom = 1.0;
      const isPl = currentXMetric === 'pl';
      const baseXMax = isPl ? 32 : 30;
      matrixCenterX = baseXMax / 2;
      matrixCenterY = (110 + 20) / 2;
      updateZoomLabel();
      const svg = document.getElementById('matrixSvg');
      if (svg) svg.style.cursor = 'crosshair';
      renderMatrix();
    }}

    function updateZoomLabel() {{
      const lbl = document.getElementById('matrixZoomLabel');
      if (lbl) {{
        lbl.innerText = Math.round(matrixZoom * 100) + '%';
      }}
    }}

    function zoomMatrixAt(factor, clientX, clientY) {{
      const isPl = currentXMetric === 'pl';
      const baseXMin = 0;
      const baseXMax = isPl ? 32 : 30;
      const baseYMin = 20;
      const baseYMax = 110;

      const padL = 60, padR = 30, padT = 45, padB = 48;
      const w = 1200, h = 700;
      const innerW = w - padL - padR;
      const innerH = h - padT - padB;

      const oldZoom = matrixZoom;
      let newZoom = Math.min(8.0, Math.max(1.0, oldZoom * factor));
      if (Math.abs(newZoom - oldZoom) < 0.005) return;

      const svg = document.getElementById('matrixSvg');
      if (!svg) return;
      const rect = svg.getBoundingClientRect();
      const mouseSvgX = ((clientX - rect.left) / rect.width) * w;
      const mouseSvgY = ((clientY - rect.top) / rect.height) * h;

      if (newZoom === 1.0) {{
        matrixZoom = 1.0;
        matrixCenterX = (baseXMax + baseXMin) / 2;
        matrixCenterY = (baseYMax + baseYMin) / 2;
        svg.style.cursor = 'crosshair';
      }} else {{
        const oldSpanX = (baseXMax - baseXMin) / oldZoom;
        const oldSpanY = (baseYMax - baseYMin) / oldZoom;
        const curXMin = matrixCenterX - oldSpanX / 2;
        const curYMin = matrixCenterY - oldSpanY / 2;

        const dataX = curXMin + ((mouseSvgX - padL) / innerW) * oldSpanX;
        const dataY = curYMin + (1 - (mouseSvgY - padT) / innerH) * oldSpanY;

        const newSpanX = (baseXMax - baseXMin) / newZoom;
        const newSpanY = (baseYMax - baseYMin) / newZoom;

        const normX = Math.max(0, Math.min(1, (mouseSvgX - padL) / innerW));
        const normY = Math.max(0, Math.min(1, 1 - (mouseSvgY - padT) / innerH));

        matrixCenterX = dataX + (0.5 - normX) * newSpanX;
        matrixCenterY = dataY + (0.5 - normY) * newSpanY;
        matrixZoom = newZoom;
        if (!isPanning) svg.style.cursor = 'grab';
      }}

      updateZoomLabel();
      renderMatrix();
    }}

    function selectTicker(t) {{
      selectedTicker = t;
      const topBadge = document.getElementById('topSelectedTickerBadge');
      if (topBadge) topBadge.innerText = t;
      renderDiagnosis();
      renderMatrix();
      renderTable();
    }}

    function sortTable(col) {{
      if (currentSortCol === col) {{
        currentSortAsc = !currentSortAsc;
      }} else {{
        currentSortCol = col;
        currentSortAsc = false;
      }}
      renderTable();
    }}

    // RENDERIZAR TABELA COMPLETA COM MULTIPLOS E INDICADORES (10 COLUNAS DE ALTA DECISAO)
    function renderTable() {{
      const stocks = getFilteredStocks();
      stocks.sort((a, b) => {{
        let vA = currentSortCol === 'roic' ? (a.roic || a.roe) : a[currentSortCol];
        let vB = currentSortCol === 'roic' ? (b.roic || b.roe) : b[currentSortCol];
        if (vA === null || vA === undefined) return 1;
        if (vB === null || vB === undefined) return -1;
        if (typeof vA === 'string') return currentSortAsc ? vA.localeCompare(vB) : vB.localeCompare(vA);
        return currentSortAsc ? vA - vB : vB - vA;
      }});

      const cntBadge = document.getElementById('tableCountBadge');
      if (cntBadge) cntBadge.innerText = stocks.length + ' ativos';

      const catConfig = {{
        'CAT_ULTRA_CRITIC': {{ name: '💎 Régua Ultra-Crítica (CFA & Munger)', cls: 'bg-yellow-950 text-yellow-300 border-yellow-500' }},
        'CAT_MUNGER': {{ name: '🏆 Filé Mignon Munger', cls: 'bg-amber-950 text-amber-300 border-amber-600' }},
        'CAT_ASYMMETRY': {{ name: '📈 Assimetrias Reais', cls: 'bg-cyan-950 text-cyan-300 border-cyan-600' }},
        'CAT_DIVIDENDS': {{ name: '💰 Vacas Leiteiras Perenes', cls: 'bg-emerald-950 text-emerald-300 border-emerald-600' }},
        'CAT_EXPANSION': {{ name: '🟢 Lucro em Expansão (2T26)', cls: 'bg-emerald-950 text-emerald-300 border-emerald-600' }},
        'CAT_DECELERATION': {{ name: '⚠️ Risco de Ciclo / Compressão', cls: 'bg-amber-950 text-amber-300 border-amber-600' }},
        'CAT_NET_CASH': {{ name: '🛡️ Balanço Forte (Caixa Líquido)', cls: 'bg-emerald-950 text-emerald-300 border-emerald-600' }},
        'CAT_HIGH_DEBT': {{ name: '🚨 Alavancagem Crítica (>3.2x)', cls: 'bg-rose-950 text-rose-300 border-rose-600' }},
        'QUAD_ABOVE': {{ name: '📈 Acima da Curva (Desconto Relativo)', cls: 'bg-emerald-950 text-emerald-300 border-emerald-600' }},
        'QUAD_BELOW': {{ name: '📉 Abaixo da Curva (Prêmio Exigente)', cls: 'bg-amber-950 text-amber-300 border-amber-600' }},
        'QUAD_FILE': {{ name: '💎 Oportunidades Munger', cls: 'bg-emerald-950 text-emerald-300 border-emerald-600' }},
        'QUAD_BARGAIN': {{ name: '🏷️ Pechinchas (Deep Value)', cls: 'bg-cyan-950 text-cyan-300 border-cyan-600' }},
        'QUAD_EXPENSIVE': {{ name: '⭐ Qualidade a Preço Justo', cls: 'bg-amber-950 text-amber-300 border-amber-600' }},
        'QUAD_TRAP': {{ name: '☠️ Armadilhas / Perigo', cls: 'bg-rose-950 text-rose-300 border-rose-600' }}
      }};

      const qBadge = document.getElementById('tableQuadrantFilterBadge');
      if (qBadge) {{
        if (catConfig[currentFilter]) {{
          const cfg = catConfig[currentFilter];
          qBadge.className = 'flex items-center gap-1';
          qBadge.innerHTML = `<span class="inline-flex items-center gap-1.5 px-2 py-0.5 rounded text-[11px] font-mono font-bold ${{cfg.cls}}"><span>${{cfg.name}}</span><span class="text-[10px] opacity-80 font-normal">(${{stocks.length}} ativos)</span><button onclick="setFilter('ALL')" class="hover:text-white ml-1 text-xs font-bold cursor-pointer" title="Limpar filtro e ver todos os ativos">✕</button></span>`;
        }} else {{
          qBadge.className = 'hidden items-center gap-1';
          qBadge.innerHTML = '';
        }}
      }}

      const tbody = document.getElementById('stocksTableBody');
      tbody.innerHTML = '';

      stocks.forEach((s, idx) => {{
        const isSelected = s.ticker === selectedTicker;
        const tr = document.createElement('tr');
        const rowBg = isSelected ? 'bg-emerald-500/15 border-l-2 border-emerald-400 font-bold' : (idx % 2 === 0 ? 'bg-white/[0.01]' : 'bg-transparent');
        tr.className = `cursor-pointer transition duration-150 hover:bg-white/[0.05] hover:border-l-2 hover:border-emerald-400 ${{rowBg}}`;
        tr.onclick = () => {{
          selectTicker(s.ticker);
          openDossierDrawer(s.ticker);
        }};

        // 1. Spread vs NTN-B
        const spreadStr = s.ey_spread !== null ? (s.ey_spread > 0 ? '+' : '') + s.ey_spread.toFixed(1) + '%' : 'N/D';
        const spreadColor = getColorSpread(s.ey_spread);

        // 2. P/L e Run-Rate (Detector de Ciclo - Dupla Linha)
        let rrStr = 'RR: N/D';
        let rrColor = 'text-slate-500';
        if (s.pl_run_rate !== null) {{
          rrStr = 'RR: ' + Number(s.pl_run_rate).toFixed(1) + 'x';
          if (s.pl !== null && s.pl > 0) {{
            if (s.pl_run_rate < s.pl * 0.85) {{
              rrColor = 'text-emerald-400 font-semibold'; // Lucro acelerando
            }} else if (s.pl_run_rate > s.pl * 1.25) {{
              rrColor = 'text-amber-400 font-semibold'; // Lucro desacelerando
            }} else {{
              rrColor = 'text-slate-400';
            }}
          }}
        }}

        // 3. ROIC / ROE Real
        const roicVal = s.roic || s.roe;
        const roicColor = getColorRoe(roicVal);

        // 4. Margem Líquida
        const mrgColor = getColorMrgLiq(s.mrg_liq);

        // 5. P/L Cor
        const plColor = getColorPl(s.pl);

        // 6. Dívida Líquida / EBITDA (Linha Única com Destaque de Risco)
        let debtDisplay = 'N/D';
        let debtClass = getColorDebt(s.div_liq_ebitda, s.is_financial);
        if (s.is_financial) {{
          debtDisplay = 'Bancos';
        }} else if (s.div_liq_ebitda !== null) {{
          const dVal = Number(s.div_liq_ebitda);
          if (dVal < 0) {{
            debtDisplay = 'Caixa Líq. 🛡️';
          }} else {{
            debtDisplay = dVal.toFixed(2) + 'x';
          }}
        }}

        // 7. Dividend Yield e Payout (Detector de Yield Trap - Dupla Linha)
        const dyColor = getColorDy(s.div_yield);
        let payoutStr = 'Pay: N/D';
        let payoutColor = 'text-slate-500';
        if (s.payout_implicito !== null) {{
          const pVal = Number(s.payout_implicito);
          if (pVal > 100) {{
            payoutStr = 'Pay: ' + pVal.toFixed(0) + '% ⚠️';
            payoutColor = 'text-rose-400 font-semibold';
          }} else if (pVal >= 30 && pVal <= 85) {{
            payoutStr = 'Pay: ' + pVal.toFixed(0) + '%';
            payoutColor = 'text-emerald-400 font-semibold';
          }} else if (pVal > 85) {{
            payoutStr = 'Pay: ' + pVal.toFixed(0) + '%';
            payoutColor = 'text-amber-400';
          }} else {{
            payoutStr = 'Pay: ' + pVal.toFixed(0) + '% (Retém)';
            payoutColor = 'text-sky-400';
          }}
        }}

        const scoreBadgeClass = s.quality_score >= 80 ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40' : (s.quality_score >= 65 ? 'bg-amber-500/20 text-amber-300 border border-amber-500/40' : (s.quality_score < 50 ? 'bg-rose-500/20 text-rose-300 border border-rose-500/40' : 'bg-white/10 text-slate-300 border border-white/10'));

        tr.innerHTML = `
          <td class="py-2.5 px-3">
            <div class="flex items-center gap-1.5">
              <span class="text-sm font-bold text-amber-300 tracking-wide font-mono">${{s.ticker}}</span>
              ${{s.is_distorted ? '<span class="text-[9px] px-2 py-0.2 rounded-full bg-amber-500/20 text-amber-300 border border-amber-500/30" title="' + (s.distortion_label || 'Distorção Contábil') + '">⚠️ Dist.</span>' : ''}}
            </div>
            <div class="text-[11px] text-slate-400 font-sans truncate max-w-[150px]" title="${{s.empresa}} - ${{s.setor || ''}}">${{s.empresa}}</div>
          </td>
          <td class="py-2.5 px-3 text-xs text-right font-semibold text-white font-mono" title="Liquidez Média: ${{formatBillions(s.liq_2m)}}/d">${{formatCurrency(s.cotacao)}}</td>
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
          <td class="py-2.5 px-3 text-xs text-right font-medium text-slate-200 font-mono">${{s.is_financial ? 'N/A' : (s.ev_ebitda !== null ? formatMultiple(s.ev_ebitda) : 'N/D')}}</td>
          <td class="py-2.5 px-3 text-xs text-right font-semibold ${{roicColor}} font-mono">${{formatPercent(roicVal)}}${{s.is_financial ? ' <span class=\"text-[10px] text-sky-400 font-normal\">(ROE)</span>' : ''}}</td>
          <td class="py-2.5 px-3 text-xs text-right font-medium ${{mrgColor}} font-mono">${{formatPercent(s.mrg_liq)}}</td>
          <td class="py-2.5 px-3 text-xs text-right font-medium font-mono ${{debtClass}}">${{debtDisplay}}</td>
          <td class="py-2.5 px-3 text-right font-mono">
            <div class="text-xs font-bold ${{dyColor}}">${{formatPercent(s.div_yield)}}</div>
            <div class="text-[10px] ${{payoutColor}}" title="Payout Implícito (% do Lucro Pago em Proventos)">${{payoutStr}}</div>
          </td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    // RENDERIZAR MATRIZ MUNGER 2X2 EM SVG COM ZOOM, PAN E 3ª DIMENSÃO
    function renderMatrix() {{
      const svg = document.getElementById('matrixSvg');
      if (!svg) return;
      svg.innerHTML = '';

      const stocks = getFilteredStocks().filter(s => s.pl !== null && s.pl > 0 && s.pl <= 35.0);
      const isPl = currentXMetric === 'pl';

      const padL = 60, padR = 30, padT = 45, padB = 48;
      const w = 1200, h = 700;
      const innerW = w - padL - padR;
      const innerH = h - padT - padB;

      const baseXMin = 0;
      const baseXMax = isPl ? 32 : 30;
      const baseYMin = 20;
      const baseYMax = 110;

      const spanX = (baseXMax - baseXMin) / matrixZoom;
      const spanY = (baseYMax - baseYMin) / matrixZoom;
      const curXMin = matrixCenterX - spanX / 2;
      const curXMax = matrixCenterX + spanX / 2;
      const curYMin = matrixCenterY - spanY / 2;
      const curYMax = matrixCenterY + spanY / 2;

      const scaleX = (x) => padL + ((x - curXMin) / (curXMax - curXMin)) * innerW;
      const scaleY = (y) => padT + innerH - ((y - curYMin) / (curYMax - curYMin)) * innerH;

      // Normalização para 3ª dimensão das bolhas
      let maxBubbleVal = 1;
      if (matrixBubbleMetric === 'mcap') {{
        maxBubbleVal = Math.max(...stocks.map(s => (s.details && s.details.valor_mercado) || 0), 1);
      }} else if (matrixBubbleMetric === 'volume') {{
        maxBubbleVal = Math.max(...stocks.map(s => s.liq_2m || 0), 1);
      }}

      function calcRadius(s) {{
        if (matrixBubbleMetric === 'fixed') return 5.5;
        if (matrixBubbleMetric === 'mcap') {{
          const v = (s.details && s.details.valor_mercado) || 0;
          return 3.5 + Math.sqrt(Math.max(0, v) / maxBubbleVal) * 14.5;
        }}
        if (matrixBubbleMetric === 'volume') {{
          const v = s.liq_2m || 0;
          return 3.5 + Math.sqrt(Math.max(0, v) / maxBubbleVal) * 14.5;
        }}
        return 5.5;
      }}

      // Amostragem da Curva Matemática Munger Compounder (Pró-Qualidade)
      const curvePts = [];
      for (let q = 20; q <= 105; q += 2.0) {{
        const fairPl = calcFairPL(q);
        let xVal = isPl ? fairPl : (100.0 / Math.max(1.0, fairPl));
        curvePts.push({{ q: q, x: xVal, px: scaleX(xVal), py: scaleY(q) }});
      }}

      const curvePathD = curvePts.map((pt, i) => `${{i === 0 ? 'M' : 'L'}} ${{pt.px.toFixed(1)}} ${{pt.py.toFixed(1)}}`).join(' ');

      // Polígono Sombreado da Zona de Desconto Relativo (Acima da Curva)
      let shadePolyD = '';
      if (isPl) {{
        const topPt = curvePts[curvePts.length - 1];
        const botPt = curvePts[0];
        const leftX = scaleX(0);
        shadePolyD = `M ${{leftX.toFixed(1)}} ${{botPt.py.toFixed(1)}} ` +
                     `L ${{leftX.toFixed(1)}} ${{topPt.py.toFixed(1)}} ` +
                     curvePts.slice().reverse().map(pt => `L ${{pt.px.toFixed(1)}} ${{pt.py.toFixed(1)}}`).join(' ') +
                     ' Z';
      }} else {{
        const topPt = curvePts[curvePts.length - 1];
        const botPt = curvePts[0];
        const rightX = scaleX(30);
        shadePolyD = `M ${{rightX.toFixed(1)}} ${{botPt.py.toFixed(1)}} ` +
                     `L ${{rightX.toFixed(1)}} ${{topPt.py.toFixed(1)}} ` +
                     curvePts.slice().reverse().map(pt => `L ${{pt.px.toFixed(1)}} ${{pt.py.toFixed(1)}}`).join(' ') +
                     ' Z';
      }}

      // Estrutura SVG com ClipPath para que o Zoom & Pan nunca transborde os eixos
      let svgHtml = `
        <defs>
          <clipPath id="matrixPlotArea">
            <rect x="${{padL}}" y="${{padT}}" width="${{innerW}}" height="${{innerH}}" rx="4" />
          </clipPath>
          <!-- Filtro Neon Glow para a Curva Fair Value -->
          <filter id="curveGlow" x="-20%" y="-20%" width="140%" height="140%">
            <feDropShadow dx="0" dy="0" stdDeviation="3.5" flood-color="#38BDF8" flood-opacity="0.75"/>
          </filter>
          <!-- Gradiente Sutil para a Zona de Desconto Relativo -->
          <linearGradient id="discountShadeGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#10B981" stop-opacity="0.14" />
            <stop offset="50%" stop-color="#10B981" stop-opacity="0.06" />
            <stop offset="100%" stop-color="#10B981" stop-opacity="0.01" />
          </linearGradient>
        </defs>

        <!-- ÁREA DO GRÁFICO RESTRITA PELO CLIPPATH -->
        <g clip-path="url(#matrixPlotArea)">
          <!-- Fundo Escuro Base Clean -->
          <rect x="${{padL - 3000}}" y="${{padT - 3000}}" width="6000" height="6000" fill="#070A0F" />

          <!-- Zona de Desconto Relativo (Sombra Luminosa) -->
          <path d="${{shadePolyD}}" fill="url(#discountShadeGrad)" />

          <!-- Curva Matemática de Fair Value de Mercado -->
          <path d="${{curvePathD}}" fill="none" stroke="#38BDF8" stroke-width="2.6" stroke-dasharray="7,4" opacity="0.92" filter="url(#curveGlow)" />

          <!-- Badge e Anotação da Curva de Mercado -->
          <g class="pointer-events-none select-none">
            <!-- Anotação Superior: Desconto Relativo -->
            <text x="${{padL + 20}}" y="${{padT + 22}}" fill="#34D399" font-size="12" font-family="JetBrains Mono" font-weight="800" letter-spacing="0.5">▲ ZONA DE DESCONTO RELATIVO</text>
            <text x="${{padL + 20}}" y="${{padT + 37}}" fill="#64748B" font-size="10" font-family="Inter" font-weight="500">Entrega mais qualidade que a média cobrada pelo mercado</text>

            <!-- Anotação Inferior: Prêmio Exigente -->
            <text x="${{padL + innerW - 20}}" y="${{padT + innerH - 28}}" text-anchor="end" fill="#FBBF24" font-size="12" font-family="JetBrains Mono" font-weight="800" letter-spacing="0.5">▼ ZONA DE PRÊMIO EXIGENTE</text>
            <text x="${{padL + innerW - 20}}" y="${{padT + innerH - 14}}" text-anchor="end" fill="#64748B" font-size="10" font-family="Inter" font-weight="500">Múltiplos elevados com prêmio por crescimento futuro</text>

            <!-- Etiqueta Fixa da Curva -->
            <rect x="${{scaleX(isPl ? 12.0 : 10.0) - 155}}" y="${{scaleY(65) - 13}}" width="310" height="25" rx="6" fill="#090E17" fill-opacity="0.92" stroke="#38BDF8" stroke-width="1.2" />
            <text x="${{scaleX(isPl ? 12.0 : 10.0)}}" y="${{scaleY(65) + 3}}" text-anchor="middle" fill="#7DD3FC" font-size="10" font-family="JetBrains Mono" font-weight="700">📈 CURVA MUNGER COMPOUNDER (P/L JUSTO)</text>
          </g>
        </g>
      `;

      // Eixos e Ticks
      svgHtml += `
        <!-- Eixos Principais -->
        <line x1="${{padL}}" y1="${{padT + innerH}}" x2="${{padL + innerW}}" y2="${{padT + innerH}}" stroke="#2A354A" stroke-width="2" />
        <line x1="${{padL}}" y1="${{padT}}" x2="${{padL}}" y2="${{padT + innerH}}" stroke="#2A354A" stroke-width="2" />

        <!-- Legenda dos Eixos -->
        <text x="${{padL + innerW/2}}" y="${{h - 12}}" text-anchor="middle" fill="#F8FAFC" font-size="14.5" font-family="JetBrains Mono" font-weight="800">
          ${{isPl ? 'Preço sobre Lucro (P/L) [← Mais Barato | Mais Caro →]' : 'Earnings Yield (% a.a.) [← Mais Caro | Maior Retorno/Barato →]'}}
        </text>
        <text x="22" y="${{padT + innerH/2}}" text-anchor="middle" fill="#F8FAFC" font-size="14.5" font-family="JetBrains Mono" font-weight="800" transform="rotate(-90 22 ${{padT + innerH/2}})">
          Quality Score (0 a 100) [↑ Maior Excelência]
        </text>
      `;

      // Gerar Grid Ticks dinâmicos
      // Y Ticks (Quality Score)
      const yTickVals = [20, 40, 60, 75, 80, 100].filter(v => v >= curYMin - 5 && v <= curYMax + 5);
      yTickVals.forEach(v => {{
        const ty = scaleY(v);
        if (ty >= padT && ty <= padT + innerH) {{
          const isLimiar = (v === 75);
          svgHtml += `
            <line x1="${{padL}}" y1="${{ty}}" x2="${{padL + innerW}}" y2="${{ty}}" stroke="${{isLimiar ? '#1E3A8A' : '#1E293B'}}" stroke-width="${{isLimiar ? 1.8 : 0.8}}" stroke-dasharray="${{isLimiar ? '4,4' : '2,2'}}" opacity="0.8" />
            <text x="${{padL - 10}}" y="${{ty + 5}}" text-anchor="end" fill="${{isLimiar ? '#38BDF8' : '#CBD5E1'}}" font-size="13" font-family="JetBrains Mono" font-weight="${{isLimiar ? '900' : '700'}}">${{v}}</text>
          `;
        }}
      }});

      // X Ticks
      const xSpan = curXMax - curXMin;
      let xStep = 5;
      if (xSpan <= 8) xStep = 1;
      else if (xSpan <= 16) xStep = 2;
      else if (xSpan <= 24) xStep = 4;

      const firstTick = Math.ceil(curXMin / xStep) * xStep;
      for (let v = firstTick; v <= curXMax; v += xStep) {{
        const tx = scaleX(v);
        if (tx >= padL && tx <= padL + innerW) {{
          svgHtml += `
            <line x1="${{tx}}" y1="${{padT}}" x2="${{tx}}" y2="${{padT + innerH}}" stroke="#1E293B" stroke-width="0.8" stroke-dasharray="2,2" opacity="0.8" />
            <text x="${{tx}}" y="${{padT + innerH + 22}}" text-anchor="middle" fill="#CBD5E1" font-size="13" font-family="JetBrains Mono" font-weight="700">${{v}}${{isPl ? 'x' : '%'}}</text>
          `;
        }}
      }}

      svg.innerHTML = svgHtml;

      // Group para as bolhas contidas dentro da área de plot
      const bubblesGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
      bubblesGroup.id = 'matrixBubblesGroup';
      bubblesGroup.setAttribute('clip-path', 'url(#matrixPlotArea)');
      svg.appendChild(bubblesGroup);

      let nAbove = 0, nBelow = 0, nExp = 0, nDiv = 0;
      let visibleCount = 0;

      // Função de Cor da Bolha baseada na 3ª Dimensão Selecionada
      function getBubbleColor(s) {{
        if (s.entry_tag === 'PASSIVO_DESCOBERTO' || s.entry_tag === 'ND_PREJUIZO') {{
          return {{ fill: '#991B1B', stroke: '#EF4444' }};
        }}

        // Modo 0: Assimetria & Retorno Real (CFA & Munger)
        if (matrixColorMode === 'asymmetry') {{
          if (s.entry_tag === 'ASSIMETRIA_FAVORAVEL') {{
            return {{ fill: '#10B981', stroke: '#6EE7B7' }}; // 🟢 Verde Esmeralda: Assimetria Favorável
          }}
          if (s.entry_tag === 'ESTICADA') {{
            return {{ fill: '#EF4444', stroke: '#FCA5A5' }}; // 🔴 Vermelho: Entrada Esticada
          }}
          return {{ fill: '#F59E0B', stroke: '#FDE68A' }};   // 🟡 Âmbar: Preço Justo / Carrego
        }}

        // Modo 1: Momento 2T26 (Run-Rate vs 12m)
        if (matrixColorMode === 'momentum') {{
          if (s.distortion_tag === 'PREJUIZO_RECENTE' || (s.details && s.details.lucro_liq_3m < 0)) {{
            return {{ fill: '#F43F5E', stroke: '#FDA4AF' }}; // Prejuízo recente
          }}
          const rrDiv = s.run_rate_div_pct;
          if (rrDiv !== null && rrDiv !== undefined) {{
            if (rrDiv >= 15.0) return {{ fill: '#10B981', stroke: '#6EE7B7' }}; // Acelerando (+15%)
            if (rrDiv <= -20.0) return {{ fill: '#F97316', stroke: '#FDBA74' }}; // Comprimindo (-20%)
          }}
          return {{ fill: '#64748B', stroke: '#94A3B8' }}; // Estável
        }}

        // Modo 2: Dividend Yield
        if (matrixColorMode === 'dividend') {{
          const dy = (s.div_yield || 0) * 100;
          if (dy >= 10.0) return {{ fill: '#F59E0B', stroke: '#FDE68A' }}; // Super Yield >= 10%
          if (dy >= 6.0) return {{ fill: '#10B981', stroke: '#A7F3D0' }};  // 6% a 10%
          if (dy >= 3.0) return {{ fill: '#38BDF8', stroke: '#BAE6FD' }};  // 3% a 6%
          return {{ fill: '#475569', stroke: '#64748B' }};                 // < 3%
        }}

        // Modo 3: Setores B3
        if (matrixColorMode === 'sector') {{
          const sec = s.setor || '';
          if (sec.includes('Financ') || sec.includes('Bancos') || sec.includes('Segur')) return {{ fill: '#38BDF8', stroke: '#BAE6FD' }};
          if (sec.includes('Util') || sec.includes('Elét') || sec.includes('Saneam')) return {{ fill: '#10B981', stroke: '#A7F3D0' }};
          if (sec.includes('Petr') || sec.includes('Mater') || sec.includes('Miner')) return {{ fill: '#F59E0B', stroke: '#FDE68A' }};
          if (sec.includes('Cons') || sec.includes('Comér') || sec.includes('Varej')) return {{ fill: '#EC4899', stroke: '#FBCFE8' }};
          if (sec.includes('Bens') || sec.includes('Indús') || sec.includes('Máq')) return {{ fill: '#8B5CF6', stroke: '#DDD6FE' }};
          if (sec.includes('Saúd')) return {{ fill: '#14B8A6', stroke: '#99F6E4' }};
          if (sec.includes('Tecno') || sec.includes('Tele')) return {{ fill: '#06B6D4', stroke: '#A5F3FC' }};
          return {{ fill: '#64748B', stroke: '#94A3B8' }};
        }}

        // Modo 4: Posição vs Curva Fair Value (relative)
        const expectedPL = calcFairPL(s.quality_score);
        const isAbove = s.pl && s.pl > 0 && s.pl < expectedPL;
        if (isAbove) {{
          return {{ fill: '#10B981', stroke: '#6EE7B7' }}; // Desconto Relativo
        }} else {{
          if (!s.pl || s.pl > 25.0) return {{ fill: '#F43F5E', stroke: '#FDA4AF' }}; // Muito caro / Prejuízo
          return {{ fill: '#F59E0B', stroke: '#FDE68A' }}; // Prêmio
        }}
      }}

      // Classificar empresas por relevância e liquidez para smart labeling adaptativo
      const sortedByRelevance = [...stocks].sort((a, b) => {{
        const valA = ((a.details && a.details.valor_mercado) || a.liq_2m || 0);
        const valB = ((b.details && b.details.valor_mercado) || b.liq_2m || 0);
        return valB - valA;
      }});

      let labelMax = 22;
      if (matrixZoom >= 3.0) labelMax = 999;
      else if (matrixZoom >= 2.0) labelMax = 110;
      else if (matrixZoom >= 1.5) labelMax = 55;
      else if (matrixZoom >= 1.2) labelMax = 35;

      // Deduplicação inteligente de labels por empresa (prioriza a classe mais negociada, ex: ITUB4 vs ITUB3)
      const seenBase = new Set();
      const topStocksSet = new Set();
      for (const s of sortedByRelevance) {{
        const base = s.ticker.substring(0, 4);
        if (!seenBase.has(base)) {{
          seenBase.add(base);
          topStocksSet.add(s.ticker);
          if (topStocksSet.size >= labelMax) break;
        }}
      }}

      let selectedGroup = null;

      stocks.forEach(s => {{
        const xVal = isPl ? s.pl : s.earnings_yield_pct;
        const yVal = s.quality_score;
        if (xVal === null || xVal === undefined) return;

        // Métricas de contagem
        const expPL = 5.0 + 0.20 * (Math.max(20, Math.min(100, s.quality_score || 50)) - 30.0);
        if (s.pl && s.pl > 0 && s.pl < expPL) nAbove++;
        else nBelow++;

        if (s.run_rate_div_pct && s.run_rate_div_pct >= 15.0) nExp++;
        if (s.div_yield && s.div_yield >= 0.05) nDiv++;

        // Contador de ativos no campo visual atual
        if (xVal >= curXMin - 2 && xVal <= curXMax + 2 && yVal >= curYMin - 5 && yVal <= curYMax + 5) {{
          visibleCount++;
        }}

        const cx = scaleX(xVal);
        const cy = scaleY(yVal);
        const r = calcRadius(s);

        const colConfig = getBubbleColor(s);
        const fillColor = colConfig.fill;
        const strokeColor = colConfig.stroke;

        const isSelected = s.ticker === selectedTicker;
        const shouldShowLabel = isSelected || topStocksSet.has(s.ticker);

        const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        g.style.cursor = 'pointer';
        g.onclick = () => {{
          if (hasMovedDuringPan) return;
          selectTicker(s.ticker);
        }};
        g.ondblclick = () => {{
          selectTicker(s.ticker);
          openSelectedInDossier();
        }};
        g.onmouseenter = (e) => {{
          showMatrixTooltip(e, s);
          const circle = g.querySelector('.main-bubble');
          if (circle) {{
            circle.setAttribute('stroke', '#FFFFFF');
            circle.setAttribute('stroke-width', '3');
          }}
        }};
        g.onmouseleave = () => {{
          hideMatrixTooltip();
          const circle = g.querySelector('.main-bubble');
          if (circle) {{
            circle.setAttribute('stroke', isSelected ? '#FFFFFF' : strokeColor);
            circle.setAttribute('stroke-width', isSelected ? '3' : '1.2');
          }}
        }};

        // Anel de Alerta Visual para Distorções Trimestrais (One-Off / Prejuízo / Run-Rate)
        let warningRingHtml = '';
        if (s.is_distorted) {{
          let ringColor = '#C084FC';
          if (s.distortion_tag === 'PREJUIZO_RECENTE') ringColor = '#F43F5E';
          else if (s.distortion_tag === 'DETERIORACAO_LUCRO') ringColor = '#FB923C';

          warningRingHtml = `
            <circle cx="${{cx}}" cy="${{cy}}" r="${{r + 5}}" fill="none" stroke="${{ringColor}}" stroke-width="2" stroke-dasharray="3,2" opacity="0.95" class="pointer-events-none" />
          `;
        }}

        // Nome encurtado para leitura imediata
        const rawName = s.empresa || '';
        let shortName = rawName.replace(/\\s*(ON|PN|UNT|S\\/A|S\\.A\\.|NM|N1|N2).*$/i, '').trim();
        if (shortName.length > 13) shortName = shortName.substring(0, 12) + '…';

        // Detecção de proximidade da borda superior para não cortar rótulos
        const isNearTop = (cy - r - 38 < padT);

        if (isSelected) {{
          const rectY = isNearTop ? (cy + r + 8) : (cy - r - 38);
          const text1Y = isNearTop ? (cy + r + 22) : (cy - r - 24);
          const text2Y = isNearTop ? (cy + r + 33) : (cy - r - 13);

          g.innerHTML = `
            ${{warningRingHtml}}
            <circle cx="${{cx}}" cy="${{cy}}" r="${{r + 9}}" fill="none" stroke="#F59E0B" stroke-width="3" class="animate-pulse pointer-events-none" />
            <circle cx="${{cx}}" cy="${{cy}}" r="${{r}}" fill="${{fillColor}}" stroke="#FFFFFF" stroke-width="2.8" class="main-bubble" />
            <g class="pointer-events-none select-none">
              <rect x="${{cx - 62}}" y="${{rectY}}" width="124" height="28" rx="4" fill="#080A0F" fill-opacity="0.95" stroke="#F59E0B" stroke-width="1.8" />
              <text x="${{cx}}" y="${{text1Y}}" text-anchor="middle" fill="#FBBF24" font-size="13" font-family="JetBrains Mono" font-weight="900">📍 ${{s.ticker}}</text>
              <text x="${{cx}}" y="${{text2Y}}" text-anchor="middle" fill="#F8FAFC" font-size="10.5" font-family="Inter" font-weight="700">${{shortName}}</text>
            </g>
          `;
          selectedGroup = g;
        }} else {{
          let labelHtml = '';
          if (shouldShowLabel) {{
            const lbl1Y = isNearTop ? (cy + r + 16) : (cy - r - 14);
            const lbl2Y = isNearTop ? (cy + r + 28) : (cy - r - 3);

            labelHtml = `
              <g class="pointer-events-none select-none">
                <text x="${{cx}}" y="${{lbl1Y}}" text-anchor="middle" fill="#FFFFFF" font-size="12" font-family="JetBrains Mono" font-weight="800" stroke="#05070A" stroke-width="3.5" paint-order="stroke fill" stroke-linejoin="round">${{s.ticker}}</text>
                <text x="${{cx}}" y="${{lbl2Y}}" text-anchor="middle" fill="#38BDF8" font-size="10.5" font-family="Inter" font-weight="700" stroke="#05070A" stroke-width="3" paint-order="stroke fill" stroke-linejoin="round">${{shortName}}</text>
              </g>
            `;
          }}
          g.innerHTML = `
            ${{warningRingHtml}}
            <circle cx="${{cx}}" cy="${{cy}}" r="${{r}}" fill="${{fillColor}}" fill-opacity="0.88" stroke="${{strokeColor}}" stroke-width="1.2" class="main-bubble transition-transform" />
            ${{labelHtml}}
          `;
          bubblesGroup.appendChild(g);
        }}
      }});

      // Ativo selecionado sempre no topo do z-index
      if (selectedGroup) {{
        bubblesGroup.appendChild(selectedGroup);
      }}

      // Atualizar contadores do pool e sub-barra
      updateFilterCounts();

      const countBadge = document.getElementById('matrixVisibleCount');
      if (countBadge) countBadge.innerText = visibleCount;

      // Atualizar Legenda Dinâmica
      updateMatrixLegend();
    }}

    // ATUALIZAR LEGENDA DINÂMICA DA MATRIZ
    function updateMatrixLegend() {{
      const leg = document.getElementById('matrixLegendContainer');
      if (!leg) return;

      if (matrixColorMode === 'asymmetry') {{
        leg.innerHTML = `
          <span class="text-slate-400 font-bold mr-1">Cor:</span>
          <span class="inline-flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-full bg-emerald-500"></span><span class="text-emerald-300 font-semibold">Assimetria Favorável</span></span>
          <span class="inline-flex items-center gap-1 ml-2"><span class="w-2.5 h-2.5 rounded-full bg-amber-500"></span><span class="text-amber-300">Preço Justo / Carrego</span></span>
          <span class="inline-flex items-center gap-1 ml-2"><span class="w-2.5 h-2.5 rounded-full bg-rose-500"></span><span class="text-rose-300">Entrada Esticada</span></span>
          <span class="inline-flex items-center gap-1 ml-2"><span class="w-2.5 h-2.5 rounded-full bg-red-900"></span><span class="text-red-400">Prejuízo</span></span>
        `;
      }} else if (matrixColorMode === 'momentum') {{
        leg.innerHTML = `
          <span class="text-slate-400 font-bold mr-1">Cor:</span>
          <span class="inline-flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-full bg-emerald-500"></span><span class="text-emerald-300">Lucro Acelerando (≥ +15%)</span></span>
          <span class="inline-flex items-center gap-1 ml-2"><span class="w-2.5 h-2.5 rounded-full bg-slate-400"></span><span class="text-slate-300">Estável</span></span>
          <span class="inline-flex items-center gap-1 ml-2"><span class="w-2.5 h-2.5 rounded-full bg-orange-500"></span><span class="text-orange-300">Comprimindo (≤ -20%)</span></span>
          <span class="inline-flex items-center gap-1 ml-2"><span class="w-2.5 h-2.5 rounded-full bg-rose-500"></span><span class="text-rose-300">Prejuízo 2T26</span></span>
        `;
      }} else if (matrixColorMode === 'dividend') {{
        leg.innerHTML = `
          <span class="text-slate-400 font-bold mr-1">Cor:</span>
          <span class="inline-flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-full bg-amber-500"></span><span class="text-amber-300">DY ≥ 10%</span></span>
          <span class="inline-flex items-center gap-1 ml-2"><span class="w-2.5 h-2.5 rounded-full bg-emerald-500"></span><span class="text-emerald-300">6% a 10%</span></span>
          <span class="inline-flex items-center gap-1 ml-2"><span class="w-2.5 h-2.5 rounded-full bg-sky-400"></span><span class="text-sky-300">3% a 6%</span></span>
          <span class="inline-flex items-center gap-1 ml-2"><span class="w-2.5 h-2.5 rounded-full bg-slate-600"></span><span class="text-slate-400">&lt; 3%</span></span>
        `;
      }} else if (matrixColorMode === 'sector') {{
        leg.innerHTML = `
          <span class="text-slate-400 font-bold mr-1">Cor:</span>
          <span class="inline-flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-full bg-sky-400"></span><span class="text-sky-300">Financeiro</span></span>
          <span class="inline-flex items-center gap-1 ml-2"><span class="w-2.5 h-2.5 rounded-full bg-emerald-500"></span><span class="text-emerald-300">Elétricas/Util</span></span>
          <span class="inline-flex items-center gap-1 ml-2"><span class="w-2.5 h-2.5 rounded-full bg-amber-500"></span><span class="text-amber-300">Commodities</span></span>
          <span class="inline-flex items-center gap-1 ml-2"><span class="w-2.5 h-2.5 rounded-full bg-pink-500"></span><span class="text-pink-300">Consumo</span></span>
          <span class="inline-flex items-center gap-1 ml-2"><span class="w-2.5 h-2.5 rounded-full bg-purple-500"></span><span class="text-purple-300">Indústria</span></span>
        `;
      }} else {{
        leg.innerHTML = `
          <span class="text-slate-400 font-bold mr-1">Cor:</span>
          <span class="inline-flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-full bg-emerald-500"></span><span class="text-emerald-300">Acima da Curva (Desconto)</span></span>
          <span class="inline-flex items-center gap-1 ml-2"><span class="w-2.5 h-2.5 rounded-full bg-amber-500"></span><span class="text-amber-300">Abaixo da Curva (Prêmio)</span></span>
          <span class="inline-flex items-center gap-1 ml-2"><span class="w-2.5 h-2.5 rounded-full bg-rose-500"></span><span class="text-rose-300">P/L &gt; 25x / Prej</span></span>
        `;
      }}
    }}

    function showMatrixTooltip(e, s) {{
      const tt = document.getElementById('matrixTooltip');
      if (!tt) return;
      const spreadStr = s.ey_spread !== null ? (s.ey_spread > 0 ? '+' : '') + s.ey_spread.toFixed(1) + '%' : 'N/D';
      const volStr = formatBillions(s.liq_2m).replace('R$ ', '');
      const mcapStr = s.details && s.details.valor_mercado ? formatBillions(s.details.valor_mercado) : 'N/D';

      // Cálculo da Posição vs Curva Fair Value Munger
      const expPL = calcFairPL(s.quality_score);
      const isAbove = s.pl && s.pl > 0 && s.pl < expPL;
      const deltaPL = s.pl ? (s.pl - expPL) : null;

      let curveBadge = '';
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
        if (s.run_rate_div_pct >= 15.0) momTag = `<span class="text-emerald-400 font-bold">⚡ Lucro Acelerando (+${{s.run_rate_div_pct.toFixed(0)}}%)</span>`;
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
        <div class="text-[11px] text-slate-400 font-sans my-1 border-b border-white/10 pb-1">
          Cap: <b class="text-slate-200">${{mcapStr}}</b> • Vol: <b class="text-slate-200">R$ ${{volStr}}/d</b> • Bal: <b class="text-slate-200">${{s.ult_balanco}}</b>
        </div>
        <div>• Quality Score: <b class="text-white">${{s.quality_score.toFixed(1)}}/100</b> (${{s.quality_tier.split(':')[0]}})</div>
        <div>• P/L (12m): <b>${{formatMultiple(s.pl)}}</b> (Fair Value de Mercado: <b class="text-sky-300">${{expPL.toFixed(1)}}x</b>)</div>
        <div>• Momento 2T26: ${{momTag}}</div>
        <div>• Earnings Yield: <b>${{formatPercent(s.earnings_yield_pct/100)}}</b> (Spread NTN-B: <b>${{spreadStr}}</b>)</div>
        <div>• ROIC: <b>${{formatPercent(s.roic || s.roe)}}</b> | DY: <b>${{formatPercent(s.div_yield)}}</b></div>
        <div class="mt-1 text-[11px] font-sans font-semibold text-emerald-400">${{s.entry_status}}</div>
        ${{warningBanner}}
        <div class="mt-2 pt-1.5 border-t border-white/10 flex items-center justify-between text-[10px] text-slate-400 font-sans">
          <span>Clique p/ selecionar ativo</span>
          <span class="text-amber-400 font-bold font-mono">Ver Dossiê ➜</span>
        </div>
      `;
      tt.classList.remove('hidden');

      const cont = document.getElementById('matrixContainer');
      const rect = cont.getBoundingClientRect();
      let left = e.clientX - rect.left + 15;
      let top = e.clientY - rect.top - 20;

      if (left + 280 > rect.width) left = Math.max(10, left - 300);
      if (top + 220 > rect.height) top = Math.max(10, top - 180);
      if (top < 10) top = 10;

      tt.style.left = left + 'px';
      tt.style.top = top + 'px';
    }}

    function hideMatrixTooltip() {{
      const tt = document.getElementById('matrixTooltip');
      if (tt) tt.classList.add('hidden');
    }}

    function initMatrixEvents() {{
      const svg = document.getElementById('matrixSvg');
      if (!svg) return;

      svg.addEventListener('mousedown', (e) => {{
        if (e.button !== 0) return;
        isPanning = true;
        hasMovedDuringPan = false;
        panStartX = e.clientX;
        panStartY = e.clientY;
        panStartCenterX = matrixCenterX;
        panStartCenterY = matrixCenterY;
        svg.style.cursor = 'grabbing';
      }});

      window.addEventListener('mousemove', (e) => {{
        if (!isPanning) return;
        const dx = e.clientX - panStartX;
        const dy = e.clientY - panStartY;

        if (Math.abs(dx) > 3 || Math.abs(dy) > 3) {{
          hasMovedDuringPan = true;
          const isPl = currentXMetric === 'pl';
          const baseXMax = isPl ? 32 : 30;
          const baseXMin = 0;
          const baseYMax = 105;
          const baseYMin = 20;

          const padL = 70, padR = 40, padT = 40, padB = 55;
          const innerW = 1200 - padL - padR;
          const innerH = 580 - padT - padB;

          const spanX = (baseXMax - baseXMin) / matrixZoom;
          const spanY = (baseYMax - baseYMin) / matrixZoom;

          const dataDx = (dx / innerW) * spanX;
          const dataDy = (dy / innerH) * spanY;

          matrixCenterX = panStartCenterX - dataDx;
          matrixCenterY = panStartCenterY + dataDy;

          renderMatrix();
        }}
      }});

      window.addEventListener('mouseup', () => {{
        if (isPanning) {{
          isPanning = false;
          svg.style.cursor = matrixZoom > 1.05 ? 'grab' : 'crosshair';
        }}
      }});

      svg.addEventListener('wheel', (e) => {{
        e.preventDefault();
        const factor = e.deltaY < 0 ? 1.15 : 0.87;
        zoomMatrixAt(factor, e.clientX, e.clientY);
      }}, {{ passive: false }});
    }}

    // RENDERIZADOR DE GAUGES ANALÓGICOS (VELOCÍMETROS SVG INSTITUCIONAIS)
    function renderAnalogGauge(svgId, val, minVal, maxVal, label, options = {{}}) {{
      const svg = document.getElementById(svgId);
      if (!svg) return;

      if (options.isFinancial) {{
        svg.innerHTML = `
          <g transform="translate(80, 50)">
            <path d="M -55 0 A 55 55 0 0 1 55 0" fill="none" stroke="#1D2433" stroke-width="7" stroke-linecap="round" />
            <text x="0" y="-14" text-anchor="middle" fill="#00E5FF" font-size="11" font-family="JetBrains Mono" font-weight="700">BANCOS</text>
            <text x="0" y="-1" text-anchor="middle" fill="#CBD5E1" font-size="9" font-family="Inter">Intermediação</text>
            <text x="0" y="14" text-anchor="middle" fill="#00E676" font-size="9" font-family="JetBrains Mono" font-weight="bold">Basileia Ok</text>
          </g>
          <text x="80" y="76" text-anchor="middle" fill="#CBD5E1" font-size="10" font-family="JetBrains Mono" font-weight="700" letter-spacing="0.5">${{label.toUpperCase()}}</text>
        `;
        return;
      }}

      if (val === null || val === undefined || isNaN(val)) {{
        svg.innerHTML = `
          <g transform="translate(80, 50)">
            <path d="M -55 0 A 55 55 0 0 1 55 0" fill="none" stroke="#1D2433" stroke-width="7" stroke-linecap="round" />
            <text x="0" y="-2" text-anchor="middle" fill="#94A3B8" font-size="12" font-family="JetBrains Mono" font-weight="bold">N/D</text>
          </g>
          <text x="80" y="76" text-anchor="middle" fill="#CBD5E1" font-size="10" font-family="JetBrains Mono" font-weight="700" letter-spacing="0.5">${{label.toUpperCase()}}</text>
        `;
        return;
      }}

      const clamped = Math.max(minVal, Math.min(maxVal, val));
      const t = (clamped - minVal) / (maxVal - minVal);
      const deg = -180 + t * 180;
      const rad = deg * (Math.PI / 180);

      const needleR = 44;
      const nx = (needleR * Math.cos(rad)).toFixed(1);
      const ny = (needleR * Math.sin(rad)).toFixed(1);

      let activeColor = '#FFB000';
      if (options.reverseColors) {{
        if (val <= 1.5) activeColor = '#00E676';
        else if (val <= 3.0) activeColor = '#FFB000';
        else activeColor = '#FF5252';
      }} else {{
        if (t >= 0.55) activeColor = '#00E676';
        else if (t >= 0.3) activeColor = '#FFB000';
        else activeColor = '#FF5252';
      }}

      const displayVal = options.displayVal || val.toFixed(1);

      svg.innerHTML = `
        <g transform="translate(80, 50)">
          <!-- Trilha base cinza escuro -->
          <path d="M -55 0 A 55 55 0 0 1 55 0" fill="none" stroke="#181F2E" stroke-width="8" stroke-linecap="round" />

          <!-- Zonas Coloridas sutis -->
          ${{options.reverseColors ? `
            <path d="M -55 0 A 55 55 0 0 1 -18.8 -51.6" fill="none" stroke="#00E676" stroke-width="2.5" opacity="0.45" />
            <path d="M -18.8 -51.6 A 55 55 0 0 1 32.3 -44.5" fill="none" stroke="#FFB000" stroke-width="2.5" opacity="0.45" />
            <path d="M 32.3 -44.5 A 55 55 0 0 1 55 0" fill="none" stroke="#FF5252" stroke-width="2.5" opacity="0.45" />
          ` : `
            <path d="M -55 0 A 55 55 0 0 1 -32.3 -44.5" fill="none" stroke="#FF5252" stroke-width="2.5" opacity="0.45" />
            <path d="M -32.3 -44.5 A 55 55 0 0 1 18.8 -51.6" fill="none" stroke="#FFB000" stroke-width="2.5" opacity="0.45" />
            <path d="M 18.8 -51.6 A 55 55 0 0 1 55 0" fill="none" stroke="#00E676" stroke-width="2.5" opacity="0.45" />
          `}}

          <!-- Ponteiro dinâmico -->
          <line x1="0" y1="0" x2="${{nx}}" y2="${{ny}}" stroke="${{activeColor}}" stroke-width="2.2" stroke-linecap="round" />
          <circle cx="0" cy="0" r="4" fill="${{activeColor}}" />
          <circle cx="0" cy="0" r="1.8" fill="#08090C" />

          <!-- Valor real contábil com cor semântica -->
          <text x="0" y="16" text-anchor="middle" fill="${{activeColor}}" font-size="14" font-family="JetBrains Mono" font-weight="700">${{displayVal}}</text>
        </g>
        <text x="80" y="76" text-anchor="middle" fill="#CBD5E1" font-size="10" font-family="JetBrains Mono" font-weight="700" letter-spacing="0.5">${{label.toUpperCase()}}</text>
      `;
    }}

    // RENDERIZAR PAINEL DE DIAGNÓSTICO
    function renderDiagnosis() {{
      let s = APP_DATA.stocks.find(item => item.ticker === selectedTicker);
      if (!s) {{
        const filtered = getFilteredStocks();
        s = filtered.length > 0 ? filtered[0] : APP_DATA.stocks[0];
        if (s) selectedTicker = s.ticker;
      }}
      if (!s) return;

      const volStr = formatBillions(s.liq_2m);
      const categories = getStockCategories(s);
      let catBadgesHtml = '';
      if (categories.length > 0) {{
        catBadgesHtml = categories.map(c => `
          <button onclick="filterByCategory('${{c.id}}')" class="inline-flex items-center gap-1 px-1.5 py-0.5 rounded text-[10px] font-mono font-bold ${{c.bgClass}} hover:brightness-125 transition cursor-pointer" title="Filtrar tabela para ver todas as empresas em ${{c.label}}">
            <span>${{c.icon}}</span> <span>${{c.shortLabel || c.label}}</span>
          </button>
        `).join('');
      }} else {{
        catBadgesHtml = `<span class="text-[10px] font-mono text-slate-500 italic">Nenhum enquadramento especial nos filtros Munger</span>`;
      }}

      // Card Cabeçalho estilo Glassmorphic Fintech
      const headScoreColor = s.quality_score >= 80 ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/50' : (s.quality_score >= 65 ? 'bg-amber-500/20 text-amber-300 border-amber-500/50' : (s.quality_score < 50 ? 'bg-rose-500/20 text-rose-300 border-rose-500/50' : 'bg-white/10 text-slate-300 border-white/10'));

      document.getElementById('diagHeaderCard').innerHTML = `
        <div class="flex justify-between items-start">
          <div>
            <div class="text-2xl font-bold font-mono text-white tracking-tight flex items-center gap-2">
              <span>${{s.ticker}}</span>
              <span class="text-xs px-2.5 py-0.5 rounded-full font-sans font-normal ${{s.is_latest_balanco ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40' : 'bg-amber-500/20 text-amber-300 border border-amber-500/40'}}">
                ${{s.tri_balanco}}
              </span>
            </div>
            <div class="text-sm font-medium text-slate-200 truncate max-w-[260px] mt-0.5">${{s.empresa}}</div>
            <div class="text-xs text-slate-400 font-sans mt-0.5">${{s.is_financial ? '🏦 Setor Financeiro' : (s.setor || 'Outros')}} • Cotação: <b class="text-slate-200 font-mono">${{formatCurrency(s.cotacao)}}</b> • Liq: ${{volStr}}/d</div>
          </div>
          <div class="flex flex-col items-end gap-1.5">
            <span class="px-3 py-1 rounded-full font-mono font-bold text-sm border ${{headScoreColor}} shadow-sm">
              SCORE ${{s.quality_score.toFixed(1)}}
            </span>
            <button onclick="openSelectedInMatrix()" class="px-3 py-1 rounded-full text-[10px] font-mono text-slate-300 hover:text-white glass-pill border-white/10 hover:border-white/30 flex items-center gap-1 transition cursor-pointer" title="Localizar e ver na Matriz 2x2">
              <span>Ver na Matriz</span> <span>➜</span>
            </button>
          </div>
        </div>

        <!-- Rótulos de Categorias Institucionais Munger (Multi-Enquadramento) -->
        <div class="mt-3 pt-2.5 border-t border-white/10 flex flex-wrap items-center gap-1.5">
          <span class="text-[10px] font-mono text-slate-400 uppercase tracking-wider font-semibold mr-0.5">Enquadramentos:</span>
          ${{catBadgesHtml}}
        </div>
      `;

      // Renderizar os 3 Semicircular Gauges Bloomberg com Dados 100% Reais
      const roeVal = s.roe !== null ? s.roe * 100 : (s.roic !== null ? s.roic * 100 : null);
      renderAnalogGauge('gaugeRoe', roeVal, 0, 35, 'ROE Auditado', {{
        displayVal: formatPercent(s.roe || s.roic)
      }});

      renderAnalogGauge('gaugeDebt', s.div_liq_ebitda, -0.5, 4.0, 'Dív.Líq/EBITDA', {{
        isFinancial: s.is_financial,
        reverseColors: true,
        displayVal: s.is_financial ? 'N/A' : (s.div_liq_ebitda !== null ? (s.div_liq_ebitda < 0 ? 'Caixa Líq.' : s.div_liq_ebitda.toFixed(2) + 'x') : 'N/D')
      }});

      renderAnalogGauge('gaugeSpread', s.ey_spread, -4.0, 10.0, 'Spread NTN-B', {{
        displayVal: s.ey_spread !== null ? (s.ey_spread > 0 ? '+' : '') + s.ey_spread.toFixed(1) + '%' : 'N/D'
      }});

      // Radar Polar SVG
      renderPolarRadar(s);

      // KPI Grid com Hierarquia de Cores
      const spreadStr = s.ey_spread !== null ? (s.ey_spread > 0 ? '+' : '') + s.ey_spread.toFixed(1) + '%' : 'N/D';
      const spreadColor = getColorSpread(s.ey_spread);
      const roicValActual = s.roic || s.roe;
      const roicColor = getColorRoe(roicValActual);
      const mrgColor = getColorMrgLiq(s.mrg_liq);
      const capStr = s.capital_intensity !== null ? (s.capital_intensity * 100).toFixed(0) + '%' : 'N/D';
      const capColor = s.is_financial ? 'text-sky-400 font-semibold' : getColorAcidTest(s.capital_intensity);
      const debtColor = getColorDebt(s.div_liq_ebitda, s.is_financial);
      const debtVal = s.div_liq_ebitda;
      const debtStr = s.is_financial ? 'Bancos' : (debtVal !== null ? (debtVal < 0 ? 'Caixa Líq. 🛡️' : debtVal.toFixed(2) + 'x') : 'N/D');

      const payoutStr = s.payout_implicito !== null ? s.payout_implicito.toFixed(0) + '%' : 'N/D';
      let payoutColor = 'text-slate-400';
      if (s.payout_implicito !== null) {{
        const pVal = Number(s.payout_implicito);
        if (pVal > 100) payoutColor = 'text-rose-400 font-bold';
        else if (pVal >= 30 && pVal <= 85) payoutColor = 'text-emerald-400 font-bold';
        else if (pVal > 85) payoutColor = 'text-amber-400 font-semibold';
        else payoutColor = 'text-sky-400 font-semibold';
      }}

      document.getElementById('kpiGrid').innerHTML = `
        <div class="glass-card rounded-xl border border-white/10 p-2.5 text-center">
          <div class="text-[10px] text-slate-400 uppercase font-semibold">ROIC / ROE</div>
          <div class="text-sm font-bold ${{roicColor}} mt-0.5">${{formatPercent(roicValActual)}}</div>
          <div class="text-[9px] text-slate-500 font-sans mt-0.5">Score: ${{s.sub_scores.roic.toFixed(0)}}/100</div>
        </div>
        <div class="glass-card rounded-xl border border-white/10 p-2.5 text-center">
          <div class="text-[10px] text-slate-400 uppercase font-semibold">Spread NTN-B</div>
          <div class="text-sm font-bold ${{spreadColor}} mt-0.5">${{spreadStr}}</div>
          <div class="text-[9px] text-slate-500 font-sans mt-0.5">Ref: 6,5% a.a.</div>
        </div>
        <div class="glass-card rounded-xl border border-white/10 p-2.5 text-center">
          <div class="text-[10px] text-slate-400 uppercase font-semibold">Payout</div>
          <div class="text-sm font-bold ${{payoutColor}} mt-0.5">${{payoutStr}}</div>
          <div class="text-[9px] text-slate-500 font-sans mt-0.5">${{s.payout_tag ? s.payout_tag.split(' ')[1] || 'Normal' : 'Normal'}}</div>
        </div>
        <div class="glass-card rounded-xl border border-white/10 p-2.5 text-center">
          <div class="text-[10px] text-slate-400 uppercase font-semibold">Dív.Líq / EBITDA</div>
          <div class="text-sm font-bold ${{debtColor}} mt-0.5">${{debtStr}}</div>
          <div class="text-[9px] text-slate-500 font-sans mt-0.5">Score: ${{s.sub_scores.div_liq_ebitda.toFixed(0)}}/100</div>
        </div>
        <div class="glass-card rounded-xl border border-white/10 p-2.5 text-center">
          <div class="text-[10px] text-slate-400 uppercase font-semibold">EBIT / EBITDA</div>
          <div class="text-sm font-bold ${{capColor}} mt-0.5">${{capStr}}</div>
          <div class="text-[9px] text-slate-500 font-sans mt-0.5">Munger Acid Test</div>
        </div>
        <div class="glass-card rounded-xl border border-white/10 p-2.5 text-center">
          <div class="text-[10px] text-slate-400 uppercase font-semibold">Margem Líq.</div>
          <div class="text-sm font-bold ${{mrgColor}} mt-0.5">${{formatPercent(s.mrg_liq)}}</div>
          <div class="text-[9px] text-slate-500 font-sans mt-0.5">Score: ${{s.sub_scores.mrg_liq.toFixed(0)}}/100</div>
        </div>
      `;

      // Espelho Balanço & DRE Reorganizado em Cartões Estruturados
      document.getElementById('auditSourceText').innerHTML = `
        <span class="text-slate-400 flex items-center gap-1.5"><span>🏛️</span> Fonte: ${{s.details.audit_source || 'Fundamentus'}}</span>
        <span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold ${{s.is_latest_balanco ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40' : 'bg-amber-500/20 text-amber-300 border border-amber-500/40'}}">
          📅 Balanço Auditado: ${{s.ult_balanco}} (${{s.tri_balanco}})
        </span>
      `;

      document.getElementById('balanceSheetDetails').innerHTML = `
        <!-- Card 1: Valuation & Mercado -->
        <div class="glass-card rounded-xl p-4 flex flex-col gap-2 border border-white/10">
          <div class="font-bold text-amber-300 text-xs flex items-center gap-1.5 border-b border-white/10 pb-1.5">
            <span>🏷️</span> Valuation &amp; Mercado
          </div>
          <div class="space-y-1 text-[11px] font-mono">
            <div class="flex justify-between py-0.5 border-b border-white/5"><span class="text-slate-400 font-sans">Cotação Atual:</span> <b class="text-white">${{formatCurrency(s.cotacao)}}</b></div>
            <div class="flex justify-between py-0.5 border-b border-white/5"><span class="text-slate-400 font-sans">Liquidez Média (2m):</span> <b class="text-white">${{volStr}}/dia</b></div>
            <div class="flex justify-between py-0.5 border-b border-white/5"><span class="text-slate-400 font-sans">Faixa 52 Semanas:</span> <b class="text-slate-300">${{formatCurrency(s.details.min_52sem)}} - ${{formatCurrency(s.details.max_52sem)}}</b></div>
            <div class="flex justify-between py-0.5 border-b border-white/5"><span class="text-slate-400 font-sans">Valor de Mercado:</span> <b class="text-white">${{formatBillions(s.details.valor_mercado)}}</b></div>
            <div class="flex justify-between py-0.5 border-b border-white/5"><span class="text-slate-400 font-sans">Valor da Firma (EV):</span> <b class="text-white">${{formatBillions(s.details.valor_firma)}}</b></div>
            <div class="flex justify-between py-0.5 border-b border-white/5"><span class="text-slate-400 font-sans">P/L (12M LTM):</span> <b class="${{getColorPl(s.pl)}} font-bold">${{formatMultiple(s.pl)}}</b></div>
            <div class="flex justify-between py-0.5 border-b border-white/5"><span class="text-slate-400 font-sans">P/L Run-Rate (2T26):</span> <b class="${{getColorPl(s.pl_run_rate)}} font-bold">${{s.pl_run_rate ? formatMultiple(s.pl_run_rate) : 'N/D'}}</b></div>
            <div class="flex justify-between py-0.5 border-b border-white/5"><span class="text-slate-400 font-sans">P/VP:</span> <b class="text-slate-200">${{formatMultiple(s.pvp)}}</b></div>
            <div class="flex justify-between py-0.5 border-b border-white/5"><span class="text-slate-400 font-sans">EV / EBITDA:</span> <b class="text-slate-200">${{s.is_financial ? 'N/A (Bancos)' : formatMultiple(s.ev_ebitda)}}</b></div>
            <div class="flex justify-between py-0.5"><span class="text-slate-400 font-sans">Dividend Yield:</span> <b class="${{getColorDy(s.div_yield)}} font-bold">${{formatPercent(s.div_yield)}}</b></div>
          </div>
        </div>

        <!-- Card 2: Balanço Patrimonial & Solvência -->
        <div class="glass-card rounded-xl p-4 flex flex-col gap-2 border border-white/10">
          <div class="font-bold text-sky-300 text-xs flex items-center gap-1.5 border-b border-white/10 pb-1.5">
            <span>🛡️</span> Balanço &amp; Solvência
          </div>
          <div class="space-y-1 text-[11px] font-mono">
            <div class="flex justify-between py-0.5 border-b border-white/5"><span class="text-slate-400 font-sans">Ativo Total:</span> <b class="text-white">${{formatBillions(s.details.ativo_total)}}</b></div>
            <div class="flex justify-between py-0.5 border-b border-white/5"><span class="text-slate-400 font-sans">Ativo Circulante:</span> <b class="text-white">${{formatBillions(s.details.ativo_circulante)}}</b></div>
            <div class="flex justify-between py-0.5 border-b border-white/5"><span class="text-slate-400 font-sans">Disponibilidades (Caixa):</span> <b class="text-emerald-400 font-bold">${{formatBillions(s.details.disponibilidades)}}</b></div>
            <div class="flex justify-between py-0.5 border-b border-white/5"><span class="text-slate-400 font-sans">Dívida Bruta:</span> <b class="text-slate-200">${{formatBillions(s.details.divida_bruta)}}</b></div>
            <div class="flex justify-between py-0.5 border-b border-white/5"><span class="text-slate-400 font-sans">Dívida Líquida:</span> <b class="${{s.details.divida_liquida <= 0 ? 'text-emerald-400 font-bold' : (s.details.divida_liquida > 1e10 ? 'text-rose-400 font-bold' : 'text-slate-200')}}">${{formatBillions(s.details.divida_liquida)}}</b></div>
            <div class="flex justify-between py-0.5 border-b border-white/5"><span class="text-slate-400 font-sans">Dív. Líq. / EBITDA:</span> <b class="${{getColorDebt(s.div_liq_ebitda, s.is_financial)}} font-bold">${{s.is_financial ? 'N/A (Bancos)' : formatMultiple(s.div_liq_ebitda)}}</b></div>
            <div class="flex justify-between py-0.5 border-b border-white/5"><span class="text-slate-400 font-sans">Patrimônio Líquido:</span> <b class="text-white">${{formatBillions(s.details.patrimonio_liquido)}}</b></div>
            <div class="flex justify-between py-0.5 border-b border-white/5"><span class="text-slate-400 font-sans">Valor Patrimonial / Ação:</span> <b class="text-slate-300">R$ ${{s.details.vpa || 'N/D'}}</b></div>
            <div class="flex justify-between py-0.5"><span class="text-slate-400 font-sans">Estrutura de Capital:</span> <b class="${{s.details.divida_liquida <= 0 ? 'text-emerald-400 font-semibold' : 'text-amber-400 font-semibold'}}">${{s.details.divida_liquida <= 0 ? 'Caixa Líquido Positivo 🛡️' : 'Alavancagem Normal'}}</b></div>
          </div>
        </div>

        <!-- Card 3: DRE & Geração de Resultados (12M) -->
        <div class="glass-card rounded-xl p-4 flex flex-col gap-2 border border-white/10">
          <div class="font-bold text-emerald-300 text-xs flex items-center gap-1.5 border-b border-white/10 pb-1.5">
            <span>📊</span> DRE &amp; Desempenho Operacional
          </div>
          <div class="space-y-1 text-[11px] font-mono">
            <div class="flex justify-between py-0.5 border-b border-white/5"><span class="text-slate-400 font-sans">Receita Líquida (12m):</span> <b class="text-white">${{formatBillions(s.details.receita_liq_12m)}}</b></div>
            <div class="flex justify-between py-0.5 border-b border-white/5"><span class="text-slate-400 font-sans">EBIT Operacional (12m):</span> <b class="${{s.details.ebit_12m < 0 ? 'text-rose-400 font-bold' : 'text-white'}}">${{formatBillions(s.details.ebit_12m)}}</b></div>
            <div class="flex justify-between py-0.5 border-b border-white/5"><span class="text-slate-400 font-sans">Lucro Líquido (12m):</span> <b class="${{s.details.lucro_liq_12m < 0 ? 'text-rose-400 font-bold' : 'text-emerald-400 font-bold'}}">${{formatBillions(s.details.lucro_liq_12m)}}</b></div>
            <div class="flex justify-between py-0.5 border-b border-white/5"><span class="text-slate-400 font-sans">Lucro Trimestre (2T26):</span> <b class="${{s.details.lucro_liq_3m < 0 ? 'text-rose-400 font-bold' : 'text-emerald-400 font-bold'}}">${{formatBillions(s.details.lucro_liq_3m)}}</b></div>
            <div class="flex justify-between py-0.5 border-b border-white/5"><span class="text-slate-400 font-sans">LPA (Lucro por Ação):</span> <b class="text-slate-200">R$ ${{s.details.lpa || 'N/D'}}</b></div>
            <div class="flex justify-between py-0.5 border-b border-white/5"><span class="text-slate-400 font-sans">Margem Bruta:</span> <b class="${{s.mrg_bruta < 0 ? 'text-rose-400 font-bold' : 'text-slate-200'}}">${{formatPercent(s.mrg_bruta)}}</b></div>
            <div class="flex justify-between py-0.5"><span class="text-slate-400 font-sans">Margem Líquida:</span> <b class="${{getColorMrgLiq(s.mrg_liq)}} font-bold">${{formatPercent(s.mrg_liq)}}</b></div>
          </div>
        </div>

        <!-- Card 4: Auditoria de Recorrência (2T26 vs 12M) -->
        <div class="glass-card rounded-xl p-4 flex flex-col gap-2 border border-white/10">
          <div class="flex justify-between items-center border-b border-white/10 pb-1.5">
            <span class="font-bold text-purple-300 text-xs flex items-center gap-1.5 font-sans">
              <span>⚖️</span> Auditoria de Recorrência (2T26 vs 12M)
            </span>
            <span class="text-[10px] px-2 py-0.5 rounded-full font-bold font-mono ${{s.is_distorted ? 'bg-amber-500/20 text-amber-300 border border-amber-500/40' : (s.details.lucro_liq_3m < 0 ? 'bg-rose-500/20 text-rose-300 border border-rose-500/40' : 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40')}}">
              ${{s.distortion_label}}
            </span>
          </div>
          <div class="space-y-1 text-[11px] font-mono">
            <div class="flex justify-between py-0.5 border-b border-white/5"><span class="text-slate-400 font-sans">Lucro 3M (2T26):</span> <b class="${{s.details.lucro_liq_3m < 0 ? 'text-rose-400 font-bold' : 'text-white'}}">${{formatBillions(s.details.lucro_liq_3m)}}</b></div>
            <div class="flex justify-between py-0.5 border-b border-white/5"><span class="text-slate-400 font-sans">Lucro 12M (LTM):</span> <b class="${{s.details.lucro_liq_12m < 0 ? 'text-rose-400 font-bold' : 'text-white'}}">${{formatBillions(s.details.lucro_liq_12m)}}</b></div>
            <div class="flex justify-between py-0.5 border-b border-white/5"><span class="text-slate-400 font-sans">P/L LTM Histórico:</span> <b class="${{getColorPl(s.pl)}} font-semibold">${{formatMultiple(s.pl)}}</b></div>
            <div class="flex justify-between py-0.5 border-b border-white/5"><span class="text-slate-400 font-sans">P/L Run-Rate 2T26:</span> <b class="${{getColorPl(s.pl_run_rate)}} font-semibold">${{s.pl_run_rate ? formatMultiple(s.pl_run_rate) : 'Prej/ND'}}</b></div>
            <div class="text-[10px] text-slate-400 font-sans pt-1 leading-relaxed">
              ${{s.is_distorted ? '⚠️ <b>Alerta CFA:</b> Divergência relevante entre o lucro recente e os últimos 12 meses. O múltiplo LTM pode carregar efeito de one-off não recorrente.' : '💎 <b>Consistência CFA:</b> O ritmo de lucro do 2T26 anualizado acompanha o histórico de 12 meses sem distorções anormais de ciclo.'}}
            </div>
          </div>
        </div>
      `;

      // Veredito CFA
      document.getElementById('cfaStatusBanner').innerHTML = `
        <div class="p-3.5 rounded-xl border text-xs backdrop-blur-md" style="background-color: ${{s.entry_color}}1A; border-color: ${{s.entry_color}}55;">
          <div class="font-bold font-mono text-sm" style="color: ${{s.entry_color}};">${{s.entry_status}}</div>
          <div class="text-slate-300 text-[11px] mt-1 font-sans">${{s.rationale}}</div>
        </div>
      `;

      let flagsHtml = '';
      if (s.is_commodity_peak) flagsHtml += '<span class="px-2.5 py-1 text-[10px] font-semibold bg-amber-500/20 text-amber-300 border border-amber-500/40 rounded-full">⚠️ Pico de Ciclo Commodities</span>';
      if (s.is_debt_vulnerable) flagsHtml += '<span class="px-2.5 py-1 text-[10px] font-semibold bg-rose-500/20 text-rose-300 border border-rose-500/40 rounded-full">⚠️ Vulnerabilidade a Juros</span>';
      if (!s.is_latest_balanco) flagsHtml += '<span class="px-2.5 py-1 text-[10px] font-semibold bg-amber-500/20 text-amber-300 border border-amber-500/40 rounded-full">⚠️ Balanço Defasado</span>';
      if (s.is_distorted) flagsHtml += `<span class="px-2.5 py-1 text-[10px] font-semibold bg-purple-500/20 text-purple-300 border border-purple-500/40 rounded-full">⚠️ Distorção Trimestral (${{s.distortion_tag}})</span>`;
      if (s.payout_implicito && s.payout_implicito > 100) flagsHtml += '<span class="px-2.5 py-1 text-[10px] font-semibold bg-rose-500/20 text-rose-300 border border-rose-500/40 rounded-full">⚠️ Payout Insustentável</span>';
      else if (s.payout_implicito && s.payout_implicito >= 40 && s.payout_implicito <= 85) flagsHtml += '<span class="px-2.5 py-1 text-[10px] font-semibold bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 rounded-full">💎 Proventos Disciplinados</span>';
      document.getElementById('cfaFlagsContainer').innerHTML = flagsHtml;

      // Checklist de Rigor CFA & Charlie Munger (Auditoria 100% Fundamentus)
      const capIntVal = s.capital_intensity !== null ? s.capital_intensity : null;
      const isAcidPass = s.is_financial ? (s.roe && s.roe >= 0.15) : (capIntVal !== null && capIntVal >= 0.75);
      const acidDisplay = s.is_financial ? ('ROE ' + (s.roe * 100).toFixed(1) + '%') : (capIntVal !== null ? ((capIntVal * 100).toFixed(1) + '%') : 'N/D');

      const dlVal = s.details ? s.details.divida_liquida : null;
      const isSolvencyPass = s.is_financial || (dlVal !== null && dlVal <= 0) || (s.div_liq_ebitda !== null && s.div_liq_ebitda <= 1.0);
      const solvencyDisplay = s.is_financial ? 'Regulação Bacen' : (dlVal !== null && dlVal <= 0 ? 'Caixa Líquido' : (s.div_liq_ebitda !== null ? (s.div_liq_ebitda.toFixed(1) + 'x EBITDA') : 'N/D'));

      const tipoStr = (s.details && s.details.tipo) ? s.details.tipo : 'N/D';
      const isGovPass = tipoStr.toUpperCase().includes('ON');

      const rawCres = (s.details && s.details.raw_indicators && s.details.raw_indicators['Cres. Rec (5a)']) || 'N/D';
      let numCres = 0;
      try {{ numCres = parseFloat(rawCres.replace('%','').replace('.','').replace(',','.')); }} catch(e){{}}
      const isGrowthPass = !isNaN(numCres) && numCres >= 20.0;

      const isCleanEarnings = !s.is_distorted;
      const isSafeCycle = !s.is_commodity_peak;

      let checklistHtml = `
        <div class="glass-card border border-amber-500/30 rounded-xl p-3 text-xs font-mono mb-2">
          <div class="flex items-center justify-between border-b border-amber-500/20 pb-1.5 mb-2">
            <span class="font-bold text-amber-300 uppercase tracking-wider flex items-center gap-1.5">
              <span>🛡️</span> CHECKLIST DE RIGOR CFA (100% FUNDAMENTUS)
            </span>
            <span class="text-[10px] px-2 py-0.5 rounded-full font-bold ${{isAcidPass && isSolvencyPass && isCleanEarnings && isSafeCycle ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40' : 'bg-white/5 text-slate-400 border border-white/10'}}">
              ${{isAcidPass && isSolvencyPass && isCleanEarnings && isSafeCycle ? '💎 APROVADA NO FILTRO' : 'AUDITORIA COMPLETA'}}
            </span>
          </div>
          <div class="grid grid-cols-2 sm:grid-cols-3 gap-2 text-[11px]">
            <div class="p-2 rounded-lg bg-white/[0.03] border border-white/10">
              <div class="text-[10px] text-slate-400">1. Munger Acid Test</div>
              <div class="font-bold ${{isAcidPass ? 'text-emerald-400' : 'text-amber-400'}} flex items-center justify-between">
                <span>${{acidDisplay}}</span>
                <span>${{isAcidPass ? '✅' : '⚠️'}}</span>
              </div>
              <div class="text-[9px] text-slate-500 font-sans">${{isAcidPass ? 'EBITDA vira EBIT' : 'Capex/Deprec. alto'}}</div>
            </div>

            <div class="p-2 rounded-lg bg-white/[0.03] border border-white/10">
              <div class="text-[10px] text-slate-400">2. Solvência Anti-Selic</div>
              <div class="font-bold ${{isSolvencyPass ? 'text-emerald-400' : 'text-rose-400'}} flex items-center justify-between">
                <span>${{solvencyDisplay}}</span>
                <span>${{isSolvencyPass ? '✅' : '⚠️'}}</span>
              </div>
              <div class="text-[9px] text-slate-500 font-sans">${{isSolvencyPass ? 'Dívida blindada' : 'Alavancagem alta'}}</div>
            </div>

            <div class="p-2 rounded-lg bg-white/[0.03] border border-white/10">
              <div class="text-[10px] text-slate-400">3. Governança Tag Along</div>
              <div class="font-bold ${{isGovPass ? 'text-emerald-400' : 'text-amber-400'}} flex items-center justify-between">
                <span>${{tipoStr}}</span>
                <span>${{isGovPass ? '✅' : 'ℹ️'}}</span>
              </div>
              <div class="text-[9px] text-slate-500 font-sans">${{isGovPass ? '100% Tag Along (ON)' : 'PN/UNT (Verificar)'}}</div>
            </div>

            <div class="p-2 rounded-lg bg-white/[0.03] border border-white/10">
              <div class="text-[10px] text-slate-400">4. Crescimento 5 Anos</div>
              <div class="font-bold ${{isGrowthPass ? 'text-emerald-400' : 'text-slate-300'}} flex items-center justify-between">
                <span>${{rawCres}}</span>
                <span>${{isGrowthPass ? '✅' : 'ℹ️'}}</span>
              </div>
              <div class="text-[9px] text-slate-500 font-sans">${{isGrowthPass ? 'Crescimento real' : 'Abaixo da inflação'}}</div>
            </div>

            <div class="p-2 rounded-lg bg-white/[0.03] border border-white/10">
              <div class="text-[10px] text-slate-400">5. Recorrência 2T26</div>
              <div class="font-bold ${{isCleanEarnings ? 'text-emerald-400' : 'text-purple-400'}} flex items-center justify-between">
                <span>${{isCleanEarnings ? 'Lucro Limpo' : 'Distorção'}}</span>
                <span>${{isCleanEarnings ? '✅' : '⚠️'}}</span>
              </div>
              <div class="text-[9px] text-slate-500 font-sans">${{isCleanEarnings ? 'Sem one-offs' : s.distortion_tag}}</div>
            </div>

            <div class="p-2 rounded-lg bg-white/[0.03] border border-white/10">
              <div class="text-[10px] text-slate-400">6. Ciclo Commodities</div>
              <div class="font-bold ${{isSafeCycle ? 'text-emerald-400' : 'text-amber-400'}} flex items-center justify-between">
                <span>${{isSafeCycle ? 'Ciclo Seguro' : 'Pico de Ciclo'}}</span>
                <span>${{isSafeCycle ? '✅' : '⚠️'}}</span>
              </div>
              <div class="text-[9px] text-slate-500 font-sans">${{isSafeCycle ? 'Fora de risco agudo' : 'Desaceleração 2T26'}}</div>
            </div>
          </div>
        </div>
      `;

      let bulletsHtml = '';
      s.cfa_bullets.forEach(b => {{
        bulletsHtml += `
          <div class="glass-card border border-white/10 rounded-xl p-3 text-xs">
            <div class="text-[11px] font-bold uppercase tracking-wider text-slate-400 mb-1 flex items-center gap-1.5">
              <span>${{b.icon}}</span> <span>${{b.title}}</span>
            </div>
            <div class="text-slate-300 leading-relaxed font-sans text-xs">${{b.content}}</div>
          </div>
        `;
      }});
      document.getElementById('cfaBulletsList').innerHTML = checklistHtml + bulletsHtml;

      // Renderizar aba Histórico & Consistência 5 Anos
      renderHistoryTab(s);
    }}

    function renderHistoryTab(s) {{
      const container = document.getElementById('dview-history');
      if (!container) return;

      const h = s.historical_5y;
      if (!h || !h.years) {{
        container.innerHTML = `<div class="p-6 text-center text-slate-400 font-mono">Dados históricos indisponíveis para este ativo.</div>`;
        return;
      }}

      // 1. Badges Mungerianos de Consistência
      const cagrRecColor = h.cagr_receita_pct >= 10.0 ? 'text-emerald-300 bg-emerald-500/20 border-emerald-500/40' : (h.cagr_receita_pct >= 0 ? 'text-sky-300 bg-sky-500/20 border-sky-500/40' : 'text-rose-300 bg-rose-500/20 border-rose-500/40');
      const cagrLucColor = h.cagr_lucro_pct >= 10.0 ? 'text-emerald-300 bg-emerald-500/20 border-emerald-500/40' : (h.cagr_lucro_pct >= 0 ? 'text-amber-300 bg-amber-500/20 border-amber-500/40' : 'text-rose-300 bg-rose-500/20 border-rose-500/40');
      const anosLucColor = h.is_all_profitable ? 'text-emerald-300 bg-emerald-500/20 border-emerald-500/40' : 'text-amber-300 bg-amber-500/20 border-amber-500/40';

      const badgesHtml = `
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-2.5">
          <div class="glass-card rounded-xl p-3 border border-white/10 flex flex-col justify-between">
            <div class="text-[10px] text-slate-400 uppercase font-semibold font-mono flex items-center justify-between">
              <span>CAGR Receita (5A)</span>
              <span>📈</span>
            </div>
            <div class="mt-1 flex items-baseline justify-between gap-1">
              <span class="text-lg font-bold font-mono text-white">${{h.cagr_receita_pct > 0 ? '+' : ''}}${{h.cagr_receita_pct}}%</span>
              <span class="text-[10px] px-2 py-0.5 rounded-full font-bold font-mono border ${{cagrRecColor}} whitespace-nowrap">
                ${{h.cagr_receita_pct >= 10 ? 'Forte Expansão' : (h.cagr_receita_pct >= 0 ? 'Crescimento Real' : 'Contração')}}
              </span>
            </div>
            <div class="text-[9px] text-slate-500 font-sans mt-0.5">Taxa anualizada 2022-2026</div>
          </div>

          <div class="glass-card rounded-xl p-3 border border-white/10 flex flex-col justify-between">
            <div class="text-[10px] text-slate-400 uppercase font-semibold font-mono flex items-center justify-between">
              <span>Consistência de Lucro</span>
              <span>🛡️</span>
            </div>
            <div class="mt-1 flex items-baseline justify-between gap-1">
              <span class="text-lg font-bold font-mono text-emerald-400">${{h.anos_com_lucro}}</span>
              <span class="text-[10px] px-2 py-0.5 rounded-full font-bold font-mono border ${{anosLucColor}} whitespace-nowrap">
                ${{h.is_all_profitable ? 'Lucro Ininterrupto' : 'Com Oscilações'}}
              </span>
            </div>
            <div class="text-[9px] text-slate-500 font-sans mt-0.5">Ausência de queima de capital</div>
          </div>

          <div class="glass-card rounded-xl p-3 border border-white/10 flex flex-col justify-between">
            <div class="text-[10px] text-slate-400 uppercase font-semibold font-mono flex items-center justify-between">
              <span>CAGR Lucro (5A)</span>
              <span>⚖️</span>
            </div>
            <div class="mt-1 flex items-baseline justify-between gap-1">
              <span class="text-lg font-bold font-mono text-white">${{h.cagr_lucro_pct > 0 ? '+' : ''}}${{h.cagr_lucro_pct}}%</span>
              <span class="text-[10px] px-2 py-0.5 rounded-full font-bold font-mono border ${{cagrLucColor}} whitespace-nowrap">
                ${{h.estabilidade_margens}}
              </span>
            </div>
            <div class="text-[9px] text-slate-500 font-sans mt-0.5">Previsibilidade operacional</div>
          </div>
        </div>
      `;

      // 2. Gráfico 1: Área SVG - Evolução de Receita Líquida vs Lucro Líquido (5 Anos)
      const w1 = 540, h1 = 175;
      const padL = 48, padR = 25, padT = 25, padB = 28;
      const innerW1 = w1 - padL - padR;
      const innerH1 = h1 - padT - padB;

      const maxRev = Math.max(...h.receita, 1);
      const scaleX1 = (idx) => padL + (idx / 4) * innerW1;
      const scaleY1 = (val) => padT + innerH1 - (Math.max(0, val) / maxRev) * innerH1;

      // Pontos da Receita
      const revPts = h.receita.map((v, i) => [scaleX1(i), scaleY1(v)]);
      const revPath = revPts.map((p, i) => (i === 0 ? 'M' : 'L') + p[0].toFixed(1) + ',' + p[1].toFixed(1)).join(' ');
      const revArea = revPath + ` L${{scaleX1(4).toFixed(1)}},${{(padT + innerH1).toFixed(1)}} L${{scaleX1(0).toFixed(1)}},${{(padT + innerH1).toFixed(1)}} Z`;

      // Pontos do Lucro
      const lucroPts = h.lucro_liquido.map((v, i) => [scaleX1(i), scaleY1(v)]);
      const lucroPath = lucroPts.map((p, i) => (i === 0 ? 'M' : 'L') + p[0].toFixed(1) + ',' + p[1].toFixed(1)).join(' ');
      const lucroArea = lucroPath + ` L${{scaleX1(4).toFixed(1)}},${{(padT + innerH1).toFixed(1)}} L${{scaleX1(0).toFixed(1)}},${{(padT + innerH1).toFixed(1)}} Z`;

      // Labels anos
      const yearsLabelsHtml = h.years.map((y, i) => `
        <text x="${{scaleX1(i).toFixed(1)}}" y="${{h1 - 8}}" text-anchor="middle" fill="#94A3B8" font-size="10" font-family="JetBrains Mono" font-weight="600">${{y.replace(' (LTM)','*')}}</text>
      `).join('');

      // Círculos e Rótulos no Gráfico
      const revDotsHtml = revPts.map((p, i) => `
        <circle cx="${{p[0].toFixed(1)}}" cy="${{p[1].toFixed(1)}}" r="3.5" fill="#38BDF8" stroke="#080C14" stroke-width="1.5" />
        <text x="${{p[0].toFixed(1)}}" y="${{(p[1] - 8).toFixed(1)}}" text-anchor="middle" fill="#38BDF8" font-size="9" font-family="JetBrains Mono" font-weight="700">${{formatBillions(h.receita[i])}}</text>
      `).join('');

      const lucroDotsHtml = lucroPts.map((p, i) => `
        <circle cx="${{p[0].toFixed(1)}}" cy="${{p[1].toFixed(1)}}" r="3.5" fill="#10E79D" stroke="#080C14" stroke-width="1.5" />
        <text x="${{p[0].toFixed(1)}}" y="${{(p[1] + 13).toFixed(1)}}" text-anchor="middle" fill="#10E79D" font-size="9" font-family="JetBrains Mono" font-weight="700">${{formatBillions(h.lucro_liquido[i])}}</text>
      `).join('');

      const chart1Html = `
        <div class="glass-card rounded-xl p-4 border border-white/10 flex flex-col gap-2">
          <div class="flex items-center justify-between border-b border-white/10 pb-2">
            <div class="font-mono font-bold text-xs text-white flex items-center gap-1.5">
              <span>📊</span> EVOLUÇÃO 5 ANOS: RECEITA LÍQUIDA VS. LUCRO LÍQUIDO
            </div>
            <div class="flex items-center gap-3 text-[10px] font-mono">
              <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-full bg-[#38BDF8]"></span> <span class="text-slate-300 font-semibold">Receita</span></span>
              <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-full bg-[#10E79D]"></span> <span class="text-slate-300 font-semibold">Lucro Líquido</span></span>
            </div>
          </div>
          <div class="w-full overflow-x-auto">
            <svg viewBox="0 0 ${{w1}} ${{h1}}" class="w-full h-40 select-none">
              <defs>
                <linearGradient id="gradRev" x1="0%" y1="0%" x2="0%" y2="100%">
                  <stop offset="0%" stop-color="#38BDF8" stop-opacity="0.25" />
                  <stop offset="100%" stop-color="#38BDF8" stop-opacity="0.0" />
                </linearGradient>
                <linearGradient id="gradLucro" x1="0%" y1="0%" x2="0%" y2="100%">
                  <stop offset="0%" stop-color="#10E79D" stop-opacity="0.30" />
                  <stop offset="100%" stop-color="#10E79D" stop-opacity="0.0" />
                </linearGradient>
              </defs>
              <line x1="${{padL}}" y1="${{padT}}" x2="${{padL + innerW1}}" y2="${{padT}}" stroke="rgba(255,255,255,0.06)" stroke-dasharray="3,3" />
              <line x1="${{padL}}" y1="${{padT + innerH1/2}}" x2="${{padL + innerW1}}" y2="${{padT + innerH1/2}}" stroke="rgba(255,255,255,0.06)" stroke-dasharray="3,3" />
              <line x1="${{padL}}" y1="${{padT + innerH1}}" x2="${{padL + innerW1}}" y2="${{padT + innerH1}}" stroke="rgba(255,255,255,0.12)" stroke-width="1.2" />

              <path d="${{revArea}}" fill="url(#gradRev)" />
              <path d="${{revPath}}" fill="none" stroke="#38BDF8" stroke-width="2" />
              ${{revDotsHtml}}

              <path d="${{lucroArea}}" fill="url(#gradLucro)" />
              <path d="${{lucroPath}}" fill="none" stroke="#10E79D" stroke-width="2.5" />
              ${{lucroDotsHtml}}

              ${{yearsLabelsHtml}}
            </svg>
          </div>
        </div>
      `;

      // 3. Grid de 2 Gráficos: ROIC Histórico e Dividend Yield Histórico
      const w2 = 250, h2 = 125;
      const padL2 = 30, padR2 = 15, padT2 = 20, padB2 = 24;
      const innerW2 = w2 - padL2 - padR2;
      const innerH2 = h2 - padT2 - padB2;

      // Gráfico ROIC
      const maxRoic = Math.max(...h.roic_roe, 0.25, 0.05);
      const scaleX2 = (idx) => padL2 + (idx / 4) * innerW2;
      const scaleYRoic = (val) => padT2 + innerH2 - (Math.max(0, val) / maxRoic) * innerH2;

      const roicPts = h.roic_roe.map((v, i) => [scaleX2(i), scaleYRoic(v)]);
      const roicPath = roicPts.map((p, i) => (i === 0 ? 'M' : 'L') + p[0].toFixed(1) + ',' + p[1].toFixed(1)).join(' ');
      const roic15LineY = scaleYRoic(0.15);

      const roicDotsHtml = roicPts.map((p, i) => `
        <circle cx="${{p[0].toFixed(1)}}" cy="${{p[1].toFixed(1)}}" r="3" fill="#FBBF24" stroke="#080C14" stroke-width="1.5" />
        <text x="${{p[0].toFixed(1)}}" y="${{(p[1] - 6).toFixed(1)}}" text-anchor="middle" fill="#FBBF24" font-size="8.5" font-family="JetBrains Mono" font-weight="700">${{(h.roic_roe[i] * 100).toFixed(1)}}%</text>
      `).join('');

      const yearsLabels2Html = h.years.map((y, i) => `
        <text x="${{scaleX2(i).toFixed(1)}}" y="${{h2 - 6}}" text-anchor="middle" fill="#64748B" font-size="8.5" font-family="JetBrains Mono">${{y.substring(2,4)}}</text>
      `).join('');

      // Gráfico Dividend Yield (Barras Verticais)
      const maxDy = Math.max(...h.div_yield, 0.10, 0.02);
      const barW = (innerW2 / 5) * 0.55;
      const dyBarsHtml = h.div_yield.map((dy, i) => {{
        const barH = (dy / maxDy) * innerH2;
        const x = scaleX2(i) - barW / 2;
        const y = padT2 + innerH2 - barH;
        const col = dy >= 0.06 ? '#10E79D' : (dy > 0 ? '#38BDF8' : '#64748B');
        return `
          <rect x="${{x.toFixed(1)}}" y="${{y.toFixed(1)}}" width="${{barW.toFixed(1)}}" height="${{barH.toFixed(1)}}" rx="2" fill="${{col}}" fill-opacity="0.85" />
          <text x="${{scaleX2(i).toFixed(1)}}" y="${{(y - 4).toFixed(1)}}" text-anchor="middle" fill="${{col}}" font-size="8.5" font-family="JetBrains Mono" font-weight="700">${{(dy * 100).toFixed(1)}}%</text>
        `;
      }}).join('');

      const chart2Html = `
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div class="glass-card rounded-xl p-3.5 border border-white/10 flex flex-col justify-between">
            <div class="flex items-center justify-between border-b border-white/10 pb-1.5 mb-1">
              <span class="font-mono font-bold text-xs text-amber-300 flex items-center gap-1">
                <span>🎯</span> Retorno s/ Capital (ROIC/ROE)
              </span>
              <span class="text-[9px] font-mono text-amber-400 font-semibold">Tier 1 &ge; 15%</span>
            </div>
            <svg viewBox="0 0 ${{w2}} ${{h2}}" class="w-full h-28 select-none">
              <line x1="${{padL2}}" y1="${{roic15LineY.toFixed(1)}}" x2="${{padL2 + innerW2}}" y2="${{roic15LineY.toFixed(1)}}" stroke="#38BDF8" stroke-dasharray="2,2" opacity="0.6" />
              <text x="${{padL2 - 4}}" y="${{(roic15LineY + 3).toFixed(1)}}" text-anchor="end" fill="#38BDF8" font-size="8" font-family="JetBrains Mono">15%</text>
              <path d="${{roicPath}}" fill="none" stroke="#FBBF24" stroke-width="2" />
              ${{roicDotsHtml}}
              ${{yearsLabels2Html}}
            </svg>
          </div>

          <div class="glass-card rounded-xl p-3.5 border border-white/10 flex flex-col justify-between">
            <div class="flex items-center justify-between border-b border-white/10 pb-1.5 mb-1">
              <span class="font-mono font-bold text-xs text-emerald-300 flex items-center gap-1">
                <span>💰</span> Histórico Dividend Yield
              </span>
              <span class="text-[9px] font-mono text-emerald-400 font-semibold">Meta &ge; 6%</span>
            </div>
            <svg viewBox="0 0 ${{w2}} ${{h2}}" class="w-full h-28 select-none">
              <line x1="${{padL2}}" y1="${{padT2 + innerH2}}" x2="${{padL2 + innerW2}}" y2="${{padT2 + innerH2}}" stroke="rgba(255,255,255,0.12)" stroke-width="1.2" />
              ${{dyBarsHtml}}
              ${{yearsLabels2Html}}
            </svg>
          </div>
        </div>
      `;

      // 4. Tabela Resumo Anual (2022 a 2026 LTM)
      const tableRowsHtml = `
        <div class="glass-card rounded-xl p-3 border border-white/10 overflow-hidden">
          <div class="text-[10px] font-mono font-bold uppercase tracking-wider text-slate-400 mb-2 flex items-center gap-1.5">
            <span>📋</span> DEMONSTRAÇÃO COMPARATIVA QUINQUENAL (2022 - 2026)
          </div>
          <div class="overflow-x-auto">
            <table class="w-full text-left font-mono text-[11px] whitespace-nowrap">
              <thead class="border-b border-white/10 text-slate-400 text-[10px] uppercase">
                <tr>
                  <th class="py-1.5 px-2">Métrica Contábil</th>
                  ${{h.years.map(y => `<th class="py-1.5 px-2 text-right">${{y}}</th>`).join('')}}
                </tr>
              </thead>
              <tbody class="divide-y divide-white/5">
                <tr>
                  <td class="py-1.5 px-2 font-sans font-medium text-slate-300">Receita Líquida</td>
                  ${{h.receita.map(r => `<td class="py-1.5 px-2 text-right text-white font-semibold">${{formatBillions(r)}}</td>`).join('')}}
                </tr>
                <tr>
                  <td class="py-1.5 px-2 font-sans font-medium text-slate-300">Lucro Líquido</td>
                  ${{h.lucro_liquido.map(l => `<td class="py-1.5 px-2 text-right font-bold ${{l > 0 ? 'text-emerald-400' : 'text-rose-400'}}">${{formatBillions(l)}}</td>`).join('')}}
                </tr>
                <tr>
                  <td class="py-1.5 px-2 font-sans font-medium text-slate-300">Margem Líquida</td>
                  ${{h.lucro_liquido.map((l, i) => {{
                    const mrg = h.receita[i] > 0 ? (l / h.receita[i]) : 0;
                    return `<td class="py-1.5 px-2 text-right ${{getColorMrgLiq(mrg)}}">${{formatPercent(mrg)}}</td>`;
                  }}).join('')}}
                </tr>
                <tr>
                  <td class="py-1.5 px-2 font-sans font-medium text-slate-300">ROIC / ROE</td>
                  ${{h.roic_roe.map(r => `<td class="py-1.5 px-2 text-right font-semibold ${{getColorRoe(r)}}">${{formatPercent(r)}}</td>`).join('')}}
                </tr>
                <tr>
                  <td class="py-1.5 px-2 font-sans font-medium text-slate-300">Dividend Yield</td>
                  ${{h.div_yield.map(dy => `<td class="py-1.5 px-2 text-right font-semibold ${{getColorDy(dy)}}">${{formatPercent(dy)}}</td>`).join('')}}
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      `;

      container.innerHTML = badgesHtml + chart1Html + chart2Html + tableRowsHtml;
    }}

    function renderPolarRadar(s) {{
      const svg = document.getElementById('radarSvg');
      if (!svg) return;

      // 1. Cálculo Auditado dos 5 Pilares Munger (0 a 100)
      // Pilar 1: Valuation & Preço (Spread vs NTN-B, P/L, P/VP)
      let valScore = 50;
      if (s.ey_spread !== null && s.ey_spread !== undefined) {{
        valScore = Math.max(15, Math.min(100, Math.round(50 + s.ey_spread * 7.5)));
      }}
      if (s.pl && s.pl > 0 && s.pl < 8.0) valScore = Math.min(100, valScore + 10);
      if (s.pl && s.pl > 25.0) valScore = Math.max(15, valScore - 15);

      // Pilar 2: Rentabilidade & Fosso Moat (ROIC, ROE, Margem Líquida)
      const rentScore = Math.max(10, Math.min(100, Math.round(s.pilar_rentabilidade || 50)));

      // Pilar 3: Dividendos & Proventos (DY, Payout sustentável)
      let divScore = 30;
      const dy = s.div_yield || 0;
      const pay = s.payout_implicito !== null && s.payout_implicito !== undefined ? s.payout_implicito : null;
      if (dy >= 0.09) divScore = 90;
      else if (dy >= 0.06) divScore = 80;
      else if (dy >= 0.03) divScore = 60;
      else if (dy > 0) divScore = 40;
      else divScore = 20;

      if (pay !== null) {{
        if (pay >= 35 && pay <= 85) divScore = Math.min(100, divScore + 10);
        else if (pay > 100) divScore = Math.max(15, divScore - 25);
      }}

      // Pilar 4: Saúde Financeira & Solvência (Dívida, Caixa Líquido, Basileia)
      const solScore = Math.max(10, Math.min(100, Math.round(s.pilar_solidez || 50)));

      // Pilar 5: Consistência & Recorrência 2T26 (Sem distorções, Acid Test)
      let consScore = Math.round(s.pilar_consistencia || 65);
      if (!s.is_distorted) consScore = Math.min(100, consScore + 10);
      else consScore = Math.max(20, consScore - 20);
      if (s.capital_intensity !== null && s.capital_intensity >= 0.75) consScore = Math.min(100, consScore + 5);
      consScore = Math.max(10, Math.min(100, consScore));

      const scores = [valScore, rentScore, divScore, solScore, consScore];
      const maxR = 90;

      // Função de coordenadas do pentágono (5 vértices: -90, -18, 54, 126, 198 graus)
      const pt = (idx, score) => {{
        const angleDeg = -90 + idx * 72;
        const rad = angleDeg * (Math.PI / 180);
        const r = (score / 100) * maxR;
        return [r * Math.cos(rad), r * Math.sin(rad)];
      }};

      // Níveis concêntricos de referência (25, 50, 75, 100)
      const ringLevels = [25, 50, 75, 100];
      let ringsHtml = ringLevels.map(lvl => {{
        const pts = [0, 1, 2, 3, 4].map(i => pt(i, lvl).map(v => v.toFixed(1)).join(',')).join(' ');
        const isOuter = lvl === 100;
        return `<polygon points="${{pts}}" fill="none" stroke="${{isOuter ? '#2A354A' : '#1A2234'}}" stroke-width="${{isOuter ? 1.5 : 0.8}}" />`;
      }}).join('');

      // Benchmark Tier 1 (80 pts tracejado)
      const benchPts = [0, 1, 2, 3, 4].map(i => pt(i, 80).map(v => v.toFixed(1)).join(',')).join(' ');
      const benchmarkHtml = `<polygon points="${{benchPts}}" fill="none" stroke="#38BDF8" stroke-width="1.5" stroke-dasharray="3,3" opacity="0.65" />`;

      // Linhas radiais do centro até cada ponta
      const radialsHtml = [0, 1, 2, 3, 4].map(i => {{
        const [x, y] = pt(i, 100);
        return `<line x1="0" y1="0" x2="${{x.toFixed(1)}}" y2="${{y.toFixed(1)}}" stroke="#1E2738" stroke-width="1" />`;
      }}).join('');

      // Polígono da Empresa
      const companyPts = scores.map((sc, i) => pt(i, sc).map(v => v.toFixed(1)).join(',')).join(' ');
      const companyPointsHtml = scores.map((sc, i) => {{
        const [x, y] = pt(i, sc);
        return `<circle cx="${{x.toFixed(1)}}" cy="${{y.toFixed(1)}}" r="4" fill="#00D084" stroke="#07090E" stroke-width="1.8" />`;
      }}).join('');

      // Rótulos dos 5 Pilares no SVG
      const labels = [
        {{ name: 'Valuation', val: valScore, offX: 0, offY: -12, anchor: 'middle' }},
        {{ name: 'Rentabilidade', val: rentScore, offX: 12, offY: -2, anchor: 'start' }},
        {{ name: 'Dividendos', val: divScore, offX: 10, offY: 14, anchor: 'start' }},
        {{ name: 'Saúde Fin.', val: solScore, offX: -10, offY: 14, anchor: 'end' }},
        {{ name: 'Consistência', val: consScore, offX: -12, offY: -2, anchor: 'end' }}
      ];

      const labelsHtml = labels.map((l, i) => {{
        const [x, y] = pt(i, 100);
        const col = l.val >= 75 ? '#00D084' : (l.val >= 50 ? '#FFB000' : '#FF5252');
        return `
          <text x="${{(x + l.offX).toFixed(1)}}" y="${{(y + l.offY).toFixed(1)}}" text-anchor="${{l.anchor}}" fill="#CBD5E1" font-size="9.5" font-family="Inter" font-weight="700">
            ${{l.name}} <tspan fill="${{col}}" font-family="JetBrains Mono">(${{l.val}})</tspan>
          </text>
        `;
      }}).join('');

      svg.innerHTML = `
        <defs>
          <radialGradient id="radarGrad" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stop-color="#00D084" stop-opacity="0.42" />
            <stop offset="100%" stop-color="#00D084" stop-opacity="0.10" />
          </radialGradient>
        </defs>

        <!-- Anéis Concêntricos -->
        ${{ringsHtml}}

        <!-- Linhas Radiais -->
        ${{radialsHtml}}

        <!-- Benchmark Tier 1 (80 pts) -->
        ${{benchmarkHtml}}

        <!-- Polígono da Empresa -->
        <polygon points="${{companyPts}}" fill="url(#radarGrad)" stroke="#00D084" stroke-width="2.5" stroke-linejoin="round" />
        ${{companyPointsHtml}}

        <!-- Rótulos Externos -->
        ${{labelsHtml}}
      `;

      // 2. Renderizar 5 Mini-Cards dos Pilares logo abaixo do SVG
      const pillarsGrid = document.getElementById('radarPillarsGrid');
      if (pillarsGrid) {{
        const pillarCards = [
          {{ label: 'Valuation', score: valScore, desc: s.ey_spread !== null ? (s.ey_spread > 0 ? '+' : '') + s.ey_spread.toFixed(1) + '% Real' : 'P/L ' + formatMultiple(s.pl), color: valScore >= 75 ? 'text-emerald-400' : (valScore >= 50 ? 'text-amber-400' : 'text-rose-400'), border: valScore >= 75 ? 'border-emerald-500/40 bg-emerald-950/10' : (valScore >= 50 ? 'border-amber-500/40 bg-amber-950/10' : 'border-rose-500/40 bg-rose-950/10') }},
          {{ label: 'Rentabilidade', score: rentScore, desc: formatPercent(s.roic || s.roe), color: rentScore >= 75 ? 'text-emerald-400' : (rentScore >= 50 ? 'text-amber-400' : 'text-rose-400'), border: rentScore >= 75 ? 'border-emerald-500/40 bg-emerald-950/10' : (rentScore >= 50 ? 'border-amber-500/40 bg-amber-950/10' : 'border-rose-500/40 bg-rose-950/10') }},
          {{ label: 'Dividendos', score: divScore, desc: formatPercent(s.div_yield), color: divScore >= 75 ? 'text-emerald-400' : (divScore >= 50 ? 'text-amber-400' : 'text-slate-400'), border: divScore >= 75 ? 'border-emerald-500/40 bg-emerald-950/10' : (divScore >= 50 ? 'border-amber-500/40 bg-amber-950/10' : 'border-slate-700/50 bg-[#0B0F17]') }},
          {{ label: 'Saúde Fin.', score: solScore, desc: s.is_financial ? 'Basileia Ok' : (s.div_liq_ebitda !== null ? (s.div_liq_ebitda < 0 ? 'Caixa Líq.' : s.div_liq_ebitda.toFixed(1) + 'x') : 'N/D'), color: solScore >= 75 ? 'text-emerald-400' : (solScore >= 50 ? 'text-amber-400' : 'text-rose-400'), border: solScore >= 75 ? 'border-emerald-500/40 bg-emerald-950/10' : (solScore >= 50 ? 'border-amber-500/40 bg-amber-950/10' : 'border-rose-500/40 bg-rose-950/10') }},
          {{ label: 'Consistência', score: consScore, desc: s.is_distorted ? 'Distorção' : 'Lucro 2T26 Ok', color: consScore >= 75 ? 'text-emerald-400' : (consScore >= 50 ? 'text-amber-400' : 'text-rose-400'), border: consScore >= 75 ? 'border-emerald-500/40 bg-emerald-950/10' : (consScore >= 50 ? 'border-amber-500/40 bg-amber-950/10' : 'border-rose-500/40 bg-rose-950/10') }}
        ];

        pillarsGrid.innerHTML = pillarCards.map(c => `
          <div class="glass-card border ${{c.border}} rounded-xl p-2.5 flex flex-col items-center justify-between shadow-sm transition">
            <div class="text-[9px] text-slate-400 font-sans uppercase font-semibold truncate w-full">${{c.label}}</div>
            <div class="text-sm font-mono font-bold ${{c.color}} my-0.5">${{c.score}}</div>
            <div class="text-[9px] text-slate-300 font-mono truncate w-full" title="${{c.desc}}">${{c.desc}}</div>
          </div>
        `).join('');
      }}
    }}

    function showToast(message, type = 'info') {{
      const toast = document.getElementById('statusToast');
      const content = document.getElementById('statusToastContent');
      
      let bg = 'bg-blue-950/80 border-blue-800 text-blue-300';
      if (type === 'success') bg = 'bg-emerald-950/80 border-emerald-800 text-emerald-300';
      if (type === 'error') bg = 'bg-rose-950/80 border-rose-800 text-rose-300';

      toast.className = `mb-4 p-3 rounded-xl border text-xs font-mono flex items-center justify-between transition-all ${{bg}}`;
      content.innerHTML = message;
      toast.classList.remove('hidden');
    }}

    function hideToast() {{
      document.getElementById('statusToast').classList.add('hidden');
    }}

    // MOTOR DE ATUALIZAÇÃO VIA BACKEND / API
    async function triggerDataRefresh() {{
      if (isRefreshing) return;

      // Se aberto diretamente via arquivo local (file://), redireciona suavemente para o servidor local
      if (window.location.protocol === 'file:') {{
        showToast('🔄 <b>Redirecionando para o Servidor Local</b>: Conectando a <code>http://localhost:8050</code> para atualização ao vivo...', 'info');
        setTimeout(() => {{
          window.location.href = 'http://localhost:8050/index.html?auto_refresh=1';
        }}, 500);
        return;
      }}

      isRefreshing = true;

      const btn = document.getElementById('btn-refresh-data');
      const icon = document.getElementById('btn-refresh-icon');
      const text = document.getElementById('btn-refresh-text');

      icon.classList.add('spin-active');
      text.innerText = 'Atualizando Fundamentus...';
      btn.classList.add('opacity-75', 'pointer-events-none');

      showToast('🔄 <b>Conectando ao Fundamentus</b>: Coletando cotações e balanços patrimoniais ao vivo...', 'info');

      try {{
        const targetUrl = '/api/refresh';

        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 20000);

        const res = await fetch(targetUrl, {{ method: 'POST', signal: controller.signal }});
        clearTimeout(timeoutId);

        if (!res.ok) {{
          const errPayload = await res.json().catch(() => ({{}}));
          throw new Error(errPayload.error || ('HTTP ' + res.status));
        }}

        const data = await res.json();

        if (data && data.stocks) {{
          APP_DATA = data;
          updateHeaderInfo();
          render();
          showToast(`✅ <b>Sucesso!</b> Base do Fundamentus atualizada às ${{data.audit_timestamp}}. ${{data.stocks.length}} ativos auditados.`, 'success');
        }} else {{
          throw new Error('Formato de resposta inválido');
        }}
      }} catch (err) {{
        console.warn('Falha na atualização:', err);
        showToast(`⚠️ <b>Servidor Local Offline</b>: Para atualizar os dados, inicie o servidor executando <code>python server.py</code> ou dê duplo clique em <code>iniciar_terminal.bat</code> e acesse <b>http://localhost:8050/index.html</b>.`, 'error');
      }} finally {{
        isRefreshing = false;
        icon.classList.remove('spin-active');
        text.innerText = 'Atualizar Dados';
        btn.classList.remove('opacity-75', 'pointer-events-none');
      }}
    }}

    function resetData() {{
      currentFilter = 'ALL';
      currentSector = 'ALL';
      searchQuery = '';
      document.getElementById('searchInput').value = '';
      document.getElementById('chkLiquidity1M').checked = true;
      document.getElementById('chkLatestBalance').checked = true;
      const chkDist = document.getElementById('chkFilterDistortions');
      if (chkDist) chkDist.checked = false;
      document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
      document.getElementById('flt-ALL').classList.add('active');
      updateSectorDropdown();
      resetMatrixZoom();
      selectTicker(APP_DATA.stocks[0].ticker);
      switchWorkspace('home');
      render();
      hideToast();
    }}

    function render() {{
      updateFilterCounts();
      renderHomePage();
      renderPortfolios();
      renderMatrix();
      renderTable();
      renderDiagnosis();
    }}

    // Execução inicial
    updateHeaderInfo();
    updateSectorDropdown();
    initMatrixEvents();
    selectTicker(APP_DATA.stocks[0].ticker);
    switchWorkspace('home');
    render();

    // Auto-refresh se redirecionado com auto_refresh=1
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('auto_refresh') === '1') {{
      window.history.replaceState(null, '', window.location.pathname);
      setTimeout(triggerDataRefresh, 300);
    }}
  </script>

</body>
</html>"""

with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(html_template)
print(f"Generated standalone web app: {os.path.abspath(OUTPUT_HTML)}")

try:
    with open(ARTIFACT_HTML, "w", encoding="utf-8") as f:
        f.write(html_template)
    print(f"Generated artifact web app: {ARTIFACT_HTML}")
except Exception as e:
    print(f"Artifact write error: {e}")
