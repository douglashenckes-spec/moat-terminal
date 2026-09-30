"""
apply_white_theme.py
====================
Aplica a transformacao completa do Munger Terminal para o EQUITY TERMINAL B3:
1. Tema Branco Institucional (Light / Clean Fintech mode - estilo Stripe/Bloomberg/Linear).
2. Formalizacao de nomenclatura (removendo termos informais como 'Vacas Leiteiras', 'Ultra-Critico', etc.).
3. Rearranjo e desafogamento dos cards da Home (Panorama Geral) para leitura agradavel e sem sobrecarga.
4. Preservacao integral de todas as funcoes interativas, dados contabeis e calculos matematicos.
"""

import os
import re

SOURCE_FILE = "backup_munger_original/build_standalone_html.py"
OUTPUT_BUILDER = "build_standalone_html.py"

with open(SOURCE_FILE, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Substituir Head, Tailwind Config e CSS de Escuro para Branco Institucional
old_head_marker = """<html lang="pt-BR" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>JP Morgan | Charlie Munger B3 Terminal</title>"""

new_head = """<html lang="pt-BR" class="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>EQUITY TERMINAL B3 | Inteligência Fundamentalista</title>"""

code = code.replace(old_head_marker, new_head)

# 2. Configuração de Cores Tailwind
old_colors = """          colors: {
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
          }"""

new_colors = """          colors: {
            jpCanvas: '#F8FAFC',
            jpCard: '#FFFFFF',
            jpCardHover: '#F1F5F9',
            jpBorder: '#E2E8F0',
            jpAmber: '#D97706',
            jpAmberDark: '#B45309',
            jpCyan: '#0284C7',
            jpGreen: '#059669',
            jpYellow: '#D97706',
            jpRed: '#E11D48',
            jpBlue: '#2563EB',
          }"""

code = code.replace(old_colors, new_colors)

# 3. Bloco de Estilos CSS
old_style_block = """  <style>
    body {
      background-color: #080C14;
      background-image: 
        radial-gradient(circle at 10% 15%, rgba(56, 189, 248, 0.08) 0%, transparent 45%),
        radial-gradient(circle at 90% 80%, rgba(16, 231, 157, 0.07) 0%, transparent 45%),
        radial-gradient(circle at 75% 15%, rgba(168, 85, 247, 0.05) 0%, transparent 40%);
      background-attachment: fixed;
      color: #E2E8F0;
      font-family: 'Plus Jakarta Sans', 'Inter', sans-serif;
    }
    .glass-panel {
      background: rgba(13, 20, 35, 0.65);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border: 1px solid rgba(255, 255, 255, 0.09);
      box-shadow: inset 0 1px 0 0 rgba(255, 255, 255, 0.08), 0 16px 36px -8px rgba(0, 0, 0, 0.5);
    }
    .glass-card {
      background: rgba(15, 23, 42, 0.58);
      backdrop-filter: blur(14px);
      -webkit-backdrop-filter: blur(14px);
      border: 1px solid rgba(255, 255, 255, 0.08);
      box-shadow: inset 0 1px 0 0 rgba(255, 255, 255, 0.06), 0 6px 22px rgba(0, 0, 0, 0.32);
      transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .glass-card:hover {
      background: rgba(20, 30, 52, 0.72);
      border-color: rgba(56, 189, 248, 0.28);
      box-shadow: inset 0 1px 0 0 rgba(255, 255, 255, 0.12), 0 10px 30px rgba(0, 0, 0, 0.42);
      transform: translateY(-1px);
    }
    .glass-pill {
      background: rgba(255, 255, 255, 0.05);
      backdrop-filter: blur(8px);
      -webkit-backdrop-filter: blur(8px);
      border: 1px solid rgba(255, 255, 255, 0.09);
    }
    .mono-num {
      font-family: 'JetBrains Mono', monospace;
    }
    ::-webkit-scrollbar {
      width: 6px;
      height: 6px;
    }
    ::-webkit-scrollbar-track {
      background: #080C14;
    }
    ::-webkit-scrollbar-thumb {
      background: rgba(255, 255, 255, 0.12);
      border-radius: 9999px;
    }
    ::-webkit-scrollbar-thumb:hover {
      background: rgba(16, 231, 157, 0.45);
    }
    .sidebar-nav-btn {
      color: #94A3B8;
      border: 1px solid transparent;
      border-radius: 0.875rem;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .sidebar-nav-btn:hover {
      color: #FFFFFF;
      background: rgba(255, 255, 255, 0.06);
      border-color: rgba(255, 255, 255, 0.09);
    }
    .sidebar-nav-btn.active {
      background: linear-gradient(90deg, rgba(16, 231, 157, 0.18) 0%, rgba(56, 189, 248, 0.09) 100%);
      color: #10E79D;
      border: 1px solid rgba(16, 231, 157, 0.35);
      font-weight: 700;
      box-shadow: 0 0 20px rgba(16, 231, 157, 0.18);
    }
    .tab-btn {
      border-radius: 9999px;
      transition: all 0.2s ease;
    }
    .tab-btn.active {
      background: rgba(16, 231, 157, 0.16);
      color: #10E79D;
      border: 1px solid rgba(16, 231, 157, 0.35);
      box-shadow: 0 0 14px rgba(16, 231, 157, 0.16);
    }
    .filter-btn {
      border-radius: 9999px;
      transition: all 0.2s ease;
    }
    .filter-btn.active {
      background: rgba(16, 231, 157, 0.18);
      border-color: #10E79D;
      color: #10E79D;
      box-shadow: 0 0 12px rgba(16, 231, 157, 0.2);
    }
    .drawer-backdrop {
      background-color: rgba(4, 7, 13, 0.75);
      backdrop-filter: blur(10px);
      -webkit-backdrop-filter: blur(10px);
    }
    .dot-pulse {
      box-shadow: 0 0 12px rgba(16, 231, 157, 0.85);
    }"""

new_style_block = """  <style>
    body {
      background-color: #F8FAFC;
      background-image: 
        radial-gradient(circle at 10% 15%, rgba(14, 165, 233, 0.06) 0%, transparent 45%),
        radial-gradient(circle at 90% 80%, rgba(16, 185, 129, 0.05) 0%, transparent 45%);
      background-attachment: fixed;
      color: #0F172A;
      font-family: 'Plus Jakarta Sans', 'Inter', sans-serif;
    }
    .glass-panel {
      background: #FFFFFF;
      border: 1px solid #E2E8F0;
      box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.05);
    }
    .glass-card {
      background: #FFFFFF;
      border: 1px solid #E2E8F0;
      box-shadow: 0 1px 3px 0 rgba(15, 23, 42, 0.04);
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .glass-card:hover {
      background: #FFFFFF;
      border-color: #CBD5E1;
      box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.08);
      transform: translateY(-1px);
    }
    .glass-pill {
      background: #F1F5F9;
      border: 1px solid #E2E8F0;
      color: #334155;
    }
    .glass-pill:hover {
      background: #E2E8F0;
      color: #0F172A;
    }
    .mono-num {
      font-family: 'JetBrains Mono', monospace;
    }
    ::-webkit-scrollbar {
      width: 6px;
      height: 6px;
    }
    ::-webkit-scrollbar-track {
      background: #F8FAFC;
    }
    ::-webkit-scrollbar-thumb {
      background: #CBD5E1;
      border-radius: 9999px;
    }
    ::-webkit-scrollbar-thumb:hover {
      background: #94A3B8;
    }
    .sidebar-nav-btn {
      color: #475569;
      border: 1px solid transparent;
      border-radius: 0.875rem;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .sidebar-nav-btn:hover {
      color: #0F172A;
      background: #F1F5F9;
      border-color: #E2E8F0;
    }
    .sidebar-nav-btn.active {
      background: #ECFDF5;
      color: #065F46;
      border: 1px solid #A7F3D0;
      font-weight: 700;
      box-shadow: 0 2px 8px rgba(16, 185, 129, 0.12);
    }
    .tab-btn {
      border-radius: 9999px;
      transition: all 0.2s ease;
    }
    .tab-btn.active {
      background: #ECFDF5;
      color: #065F46;
      border: 1px solid #A7F3D0;
      font-weight: 700;
    }
    .filter-btn {
      border-radius: 9999px;
      transition: all 0.2s ease;
      color: #475569;
    }
    .filter-btn.active {
      background: #ECFDF5;
      border-color: #10B981;
      color: #065F46;
      box-shadow: 0 1px 4px rgba(16, 185, 129, 0.15);
      font-weight: 700;
    }
    .drawer-backdrop {
      background-color: rgba(15, 23, 42, 0.45);
      backdrop-filter: blur(4px);
      -webkit-backdrop-filter: blur(4px);
    }
    .dot-pulse {
      box-shadow: 0 0 10px rgba(5, 150, 105, 0.6);
    }"""

code = code.replace(old_style_block, new_style_block)

# 4. Body tag
code = code.replace(
    '<body class="h-screen text-slate-200 flex overflow-hidden font-sans antialiased selection:bg-emerald-500/30">',
    '<body class="h-screen text-slate-800 bg-[#F8FAFC] flex overflow-hidden font-sans antialiased selection:bg-emerald-100 selection:text-emerald-900">'
)

# 5. Sidebar Layout & Brand
old_sidebar_header = """  <!-- LEFT SIDEBAR DE NAVEGAÇÃO & FILTROS (MODERN GLASSMORPHIC FINTECH) -->
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
      </div>"""

new_sidebar_header = """  <!-- LEFT SIDEBAR DE NAVEGAÇÃO & FILTROS (CLEAN FINTECH LIGHT) -->
  <aside id="sidebar" class="w-64 bg-white border-r border-slate-200 flex flex-col justify-between flex-shrink-0 z-20 select-none shadow-sm">
    <div class="flex flex-col flex-1 min-h-0">
      <!-- Identidade Institucional -->
      <div class="p-4 border-b border-slate-200 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div class="w-9 h-9 rounded-xl bg-gradient-to-br from-emerald-600 via-teal-600 to-emerald-700 flex items-center justify-center text-white font-mono font-black text-xs shadow-sm shadow-emerald-600/20">
            B3
          </div>
          <div>
            <div class="font-mono font-black text-xs text-slate-900 tracking-wider flex items-center gap-1.5">
              <span>EQUITY TERMINAL</span>
              <span class="px-1.5 py-0.5 text-[9px] bg-emerald-50 text-emerald-700 border border-emerald-200 rounded-full font-bold">PRO</span>
            </div>
            <div class="text-[10px] text-slate-500 font-mono tracking-wide">INTELLIGENCE SUITE</div>
          </div>
        </div>
      </div>"""

code = code.replace(old_sidebar_header, new_sidebar_header)

# Sidebar links e filtros formais
code = code.replace('<span class="px-2 py-0.5 text-[9px] font-bold bg-amber-950/80 text-amber-300 border border-amber-600/50 rounded-full">CFA</span>',
                    '<span class="px-2 py-0.5 text-[9px] font-bold bg-amber-50 text-amber-800 border border-amber-200 rounded-full">CFA</span>')

code = code.replace('<span class="text-[10px] text-slate-400 font-mono bg-white/5 px-2 py-0.5 rounded-full" id="sidebarUniverseCount">--',
                    '<span class="text-[10px] text-slate-600 font-mono bg-slate-100 px-2 py-0.5 rounded-full font-bold" id="sidebarUniverseCount">--')

code = code.replace('<span class="font-semibold">Matriz Munger 2x2</span>',
                    '<span class="font-semibold">Matriz Estratégica 2x2</span>')

# Sidebar filtros rápidos formais
code = code.replace('border-t border-white/10 flex-1 overflow-y-auto', 'border-t border-slate-200 flex-1 overflow-y-auto')
code = code.replace('<span class="flex items-center gap-2"><span class="text-yellow-400">💎</span> Ultra-Crítico</span>',
                    '<span class="flex items-center gap-2 font-medium"><span class="text-amber-600">💎</span> Máxima Solvência</span>')
code = code.replace('bg-yellow-950/60', 'bg-amber-50 text-amber-800 border border-amber-200')

code = code.replace('<span class="flex items-center gap-2"><span class="text-amber-400">🏆</span> Tier 1 Munger</span>',
                    '<span class="flex items-center gap-2 font-medium"><span class="text-emerald-600">🏆</span> Líderes Setoriais (T1)</span>')
code = code.replace('bg-amber-950/60', 'bg-emerald-50 text-emerald-800 border border-emerald-200')

code = code.replace('<span class="flex items-center gap-2"><span class="text-cyan-400">📈</span> Assimetria Real</span>',
                    '<span class="flex items-center gap-2 font-medium"><span class="text-sky-600">📈</span> Assimetria de Valuation</span>')
code = code.replace('bg-cyan-950/60', 'bg-sky-50 text-sky-800 border border-sky-200')

code = code.replace('<span class="flex items-center gap-2"><span class="text-emerald-400">💰</span> Vacas Leiteiras</span>',
                    '<span class="flex items-center gap-2 font-medium"><span class="text-teal-600">💰</span> Dividendos Consistentes</span>')
code = code.replace('bg-emerald-950/60', 'bg-teal-50 text-teal-800 border border-teal-200')

code = code.replace('<span class="flex items-center gap-2"><span class="text-sky-400">🛡️</span> Caixa Líquido</span>',
                    '<span class="flex items-center gap-2 font-medium"><span class="text-indigo-600">🛡️</span> Balanço Desalavancado</span>')
code = code.replace('bg-sky-950/60', 'bg-indigo-50 text-indigo-800 border border-indigo-200')

code = code.replace('text-slate-300 hover:text-white hover:bg-white/5', 'text-slate-600 hover:text-slate-900 hover:bg-slate-100')

# Rodapé Sidebar
code = code.replace('border-t border-white/10 bg-[#060A10]/50 text-[10px] font-mono text-slate-400',
                    'border-t border-slate-200 bg-slate-50 text-[10px] font-mono text-slate-600')
code = code.replace('text-emerald-400 font-bold', 'text-emerald-700 font-bold')

# 6. Topbar Layout
old_topbar = """    <!-- TOPBAR MINIMALISTA & UNIVERSAL (GLASS) -->
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
    </header>"""

new_topbar = """    <!-- TOPBAR INSTITUCIONAL (CLEAN FINTECH LIGHT) -->
    <header class="bg-white/95 backdrop-blur-md border-b border-slate-200 px-6 py-3 flex items-center justify-between gap-4 z-10 flex-shrink-0 shadow-xs">
      <!-- Título Dinâmico do Workspace Ativo -->
      <div>
        <div class="font-mono font-bold text-sm text-slate-900 flex items-center gap-2" id="topbarTitle">
          <span>🏠</span> <span>PANORAMA GERAL</span>
        </div>
        <div class="text-[11px] text-slate-500" id="topbarSubtitle">Cockpit executivo e inteligência fundamentalista B3</div>
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
        <button id="btn-refresh-data" onclick="triggerDataRefresh()" class="px-4 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white font-mono font-bold rounded-full text-xs transition flex items-center gap-1.5 cursor-pointer shadow-sm">
          <span id="btn-refresh-icon">🔄</span> <span id="btn-refresh-text">Atualizar</span>
        </button>

        <!-- Botão Reset -->
        <button onclick="resetData()" class="px-3 py-1.5 bg-slate-100 hover:bg-slate-200 border border-slate-200 text-slate-700 rounded-full text-xs font-mono cursor-pointer transition">
          Reset
        </button>
      </div>
    </header>"""

code = code.replace(old_topbar, new_topbar)

# 7. Rearranjo da Home (Panorama Geral) - Desafogamento dos Cards
old_home_banner = """        <!-- 1. Banner de Boas-Vindas e Ação Rápida -->
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
        </div>"""

new_home_banner = """        <!-- 1. Header Executivo Limpo (Sem poluição de botões duplicados) -->
        <div class="flex flex-wrap items-center justify-between gap-4 p-5 glass-card rounded-2xl flex-shrink-0 bg-white border border-slate-200">
          <div>
            <div class="flex items-center gap-2.5">
              <span class="text-sm font-mono font-bold text-slate-900 uppercase tracking-wider flex items-center gap-2">
                <span>🏠</span> COCKPIT EXECUTIVO B3 • ANÁLISE FUNDAMENTALISTA
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

code = code.replace(old_home_banner, new_home_banner)

# Termômetro Macro da B3 (Cards bem formatados para Light)
old_macro_cards = """        <!-- 2. Termômetro Macro da B3 (A Régua Sovereign) -->
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
        </div>"""

new_macro_cards = """        <!-- 2. Termômetro Macro da B3 (Indicadores Soberanos e de Mercado) -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 flex-shrink-0">
          <!-- NTN-B Sovereign Benchmark -->
          <div class="glass-card rounded-2xl p-4 bg-sky-50/50 border border-sky-200">
            <div class="flex items-center justify-between text-xs text-slate-600 font-mono font-semibold">
              <span>BENCHMARK LIVRE DE RISCO</span>
              <span class="text-sky-700 font-bold">NTN-B 2035</span>
            </div>
            <div class="text-2xl font-bold font-mono text-sky-800 mt-1.5">IPCA + 6,50%</div>
            <div class="text-xs text-slate-600 mt-1">Custo de oportunidade soberano de longo prazo do Brasil.</div>
          </div>
          <!-- P/L Mediano B3 -->
          <div class="glass-card rounded-2xl p-4 bg-white border border-slate-200">
            <div class="flex items-center justify-between text-xs text-slate-600 font-mono font-semibold">
              <span>P/L MEDIANO B3</span>
              <span class="text-amber-800 bg-amber-50 px-2 py-0.5 rounded font-bold" id="home-stat-pl-tag">Barato</span>
            </div>
            <div class="text-2xl font-bold font-mono text-slate-900 mt-1.5" id="home-stat-pl">9,1x</div>
            <div class="text-xs text-slate-600 mt-1">Múltiplo mediano sobre o lucro contábil LTM.</div>
          </div>
          <!-- ROIC Mediano B3 -->
          <div class="glass-card rounded-2xl p-4 bg-emerald-50/50 border border-emerald-200">
            <div class="flex items-center justify-between text-xs text-slate-600 font-mono font-semibold">
              <span>ROIC / ROE MEDIANO</span>
              <span class="text-emerald-800 bg-emerald-100/60 px-2 py-0.5 rounded font-bold">Retorno do Capital</span>
            </div>
            <div class="text-2xl font-bold font-mono text-emerald-800 mt-1.5" id="home-stat-roic">10,2%</div>
            <div class="text-xs text-slate-600 mt-1">Retorno médio gerado pelo capital empregado na B3.</div>
          </div>
          <!-- Spread Mediano vs NTN-B -->
          <div class="glass-card rounded-2xl p-4 bg-teal-50/50 border border-teal-200">
            <div class="flex items-center justify-between text-xs text-slate-600 font-mono font-semibold">
              <span>SPREAD REAL VS NTN-B</span>
              <span class="text-teal-800 bg-teal-100/60 px-2 py-0.5 rounded font-bold" id="home-stat-spread-tag">Prêmio Positivo</span>
            </div>
            <div class="text-2xl font-bold font-mono text-teal-800 mt-1.5" id="home-stat-spread">+4,1%</div>
            <div class="text-xs text-slate-600 mt-1">Prêmio de risco real das ações sobre o Tesouro IPCA+.</div>
          </div>
        </div>"""

code = code.replace(old_macro_cards, new_macro_cards)

# Seção 2.5 Vitrine Ultra-Crítica -> Máxima Solvência & Resiliência
old_ultra = """        <!-- 2.5 Vitrine de Convicção: Régua Ultra-Crítica CFA / Munger -->
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
        </div>"""

new_ultra = """        <!-- 2.5 Vitrine Institucional: Máxima Solvência & Resiliência -->
        <div class="glass-panel rounded-2xl p-5 flex-shrink-0 border border-amber-200 bg-amber-50/40">
          <div class="flex flex-wrap items-center justify-between gap-3 border-b border-amber-200/80 pb-3 mb-3">
            <div class="flex items-center gap-2.5">
              <span class="text-xl">💎</span>
              <div>
                <div class="text-xs font-mono font-bold text-amber-900 uppercase tracking-wider flex items-center gap-2">
                  <span>SELEÇÃO DE MÁXIMA SOLVÊNCIA &amp; QUALIDADE</span>
                  <span class="text-[10px] px-2 py-0.5 rounded-full bg-white text-amber-800 border border-amber-300 font-mono font-semibold">100% CVM AUDITADO</span>
                </div>
                <p class="text-xs text-slate-600 font-sans mt-0.5">
                  Filtro institucional de alta exigência: Score &ge; 75 + Conversão Caixa (EBIT/EBITDA &ge; 75% ou Bancos ROE &ge; 15%) + Dívida Controlada (&le; 1,0x ou Caixa Líquido) + Spread Real &ge; +1,5% + Balanço 2T26 Regular.
                </p>
              </div>
            </div>
            <button onclick="filterByCategory('CAT_ULTRA_CRITIC')" id="btn-cat-ultracritic" class="px-4 py-1.5 rounded-full bg-white hover:bg-amber-100/60 border border-amber-300 text-amber-900 text-xs font-mono font-bold transition flex items-center gap-1.5 cursor-pointer shadow-xs">
              <span>Ver Seleção Completa</span> <span id="cnt-cat-ultracritic">(--)</span> <span>➜</span>
            </button>
          </div>
          <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-3 font-mono text-xs" id="home-list-ultracritic">
            <!-- Renderizado via JS -->
          </div>
        </div>"""

code = code.replace(old_ultra, new_ultra)

# Seção 3 Rankings Automáticos - Titulos Formais
code = code.replace('Top 5 "Filé Mignon" Munger', 'Top 5 Líderes de Setor (Tier 1)')
code = code.replace('Top 5 Assimetrias Reais', 'Top 5 Assimetrias de Valuation')
code = code.replace('Top 5 Vacas Leiteiras Perenes', 'Top 5 Dividendos Consistentes')

# Dispersão de Mercado
code = code.replace('<span>📐</span> DISPERSÃO DE MERCADO &amp; CURVA DE FAIR VALUE (UNIVERSO B3)',
                    '<span>📐</span> DISPERSÃO DE MERCADO &amp; CURVA DE EQUILÍBRIO (B3)')
code = code.replace('VACAS LEITEIRAS', 'DIVIDENDOS CONSISTENTES')

# 8. Matriz Estratégica HTML
code = code.replace('<span>📊</span> MATRIZ MUNGER 2X2 DE VALOR vs QUALIDADE',
                    '<span>📊</span> MATRIZ ESTRATÉGICA: VALOR vs QUALIDADE')
code = code.replace('Score Munger (20-105)', 'Score de Qualidade (20-105)')
code = code.replace('bg-[#05070A]/80', 'bg-white')
code = code.replace('bg-[#06080C]/80', 'bg-slate-50')
code = code.replace('class="bg-[#0A0E1A]"', 'class="bg-white text-slate-800"')
code = code.replace('class="bg-[#0A0E1A] text-emerald-300"', 'class="bg-white text-slate-800"')
code = code.replace('class="bg-[#0A0E1A] text-slate-200"', 'class="bg-white text-slate-800"')

# 9. Carteiras Recomendadas HTML
code = code.replace('<span class="text-base">🏆</span> CHARLIE MUNGER',
                    '<span class="text-base">🏆</span> LÍDERES DE MERCADO (TIER 1)')
code = code.replace('<span class="text-base">💰</span> VACAS LEITEIRAS',
                    '<span class="text-base">💰</span> DIVIDENDOS CONSISTENTES')
code = code.replace('<span class="text-base">📈</span> ASSIMETRIA REAL',
                    '<span class="text-base">📈</span> ASSIMETRIA DE VALUATION')
code = code.replace('<span class="text-base">💎</span> CFA ULTRA-CRÍTICA',
                    '<span class="text-base">💎</span> MÁXIMA SOLVÊNCIA & RESILIÊNCIA')
code = code.replace('Score Munger', 'Score de Qualidade')

# 10. Drawer HTML
code = code.replace('bg-[#080C14]/95 backdrop-blur-2xl border-l border-white/10 z-50 shadow-[-25px_0_60px_rgba(0,0,0,0.85)]',
                    'bg-white border-l border-slate-200 z-50 shadow-2xl')

# 11. Substituições em JavaScript para o novo estilo de cores e nomes formais
code = code.replace("'CAT_ULTRA_CRITIC': { name: '💎 Régua Ultra-Crítica (CFA & Munger)', cls: 'bg-yellow-950 text-yellow-300 border-yellow-500' }",
                    "'CAT_ULTRA_CRITIC': { name: '💎 Máxima Solvência & Qualidade', cls: 'bg-amber-50 text-amber-800 border-amber-300 font-bold' }")

code = code.replace("'CAT_MUNGER': { name: '🏆 Filé Mignon Munger', cls: 'bg-amber-950 text-amber-300 border-amber-600' }",
                    "'CAT_MUNGER': { name: '🏆 Líderes de Mercado (Tier 1)', cls: 'bg-emerald-50 text-emerald-800 border-emerald-300 font-bold' }")

code = code.replace("'CAT_ASYMMETRY': { name: '📈 Assimetrias Reais', cls: 'bg-cyan-950 text-cyan-300 border-cyan-600' }",
                    "'CAT_ASYMMETRY': { name: '📈 Assimetrias de Valuation', cls: 'bg-sky-50 text-sky-800 border-sky-300 font-bold' }")

code = code.replace("'CAT_DIVIDENDS': { name: '💰 Vacas Leiteiras Perenes', cls: 'bg-emerald-950 text-emerald-300 border-emerald-600' }",
                    "'CAT_DIVIDENDS': { name: '💰 Dividendos Consistentes', cls: 'bg-teal-50 text-teal-800 border-teal-300 font-bold' }")

code = code.replace("'CAT_NET_CASH': { name: '🛡️ Balanço Forte (Caixa Líquido)', cls: 'bg-emerald-950 text-emerald-300 border-emerald-600' }",
                    "'CAT_NET_CASH': { name: '🛡️ Balanço Desalavancado (Caixa Líquido)', cls: 'bg-blue-50 text-blue-800 border-blue-300 font-bold' }")

code = code.replace("'QUAD_ABOVE': { name: '📈 Acima da Curva (Desconto Relativo)', cls: 'bg-emerald-950 text-emerald-300 border-emerald-600' }",
                    "'QUAD_ABOVE': { name: '📈 Acima da Curva (Desconto)', cls: 'bg-emerald-50 text-emerald-800 border-emerald-300 font-bold' }")

code = code.replace("'QUAD_BELOW': { name: '📉 Abaixo da Curva (Prêmio Exigente)', cls: 'bg-amber-950 text-amber-300 border-amber-600' }",
                    "'QUAD_BELOW': { name: '📉 Abaixo da Curva (Prêmio)', cls: 'bg-amber-50 text-amber-800 border-amber-300 font-bold' }")

# Salvar o novo build_standalone_html.py
with open(OUTPUT_BUILDER, "w", encoding="utf-8") as f:
    f.write(code)

print(f"Sucesso! {OUTPUT_BUILDER} gerado com o novo tema branco institucional e nomenclatura formal.")
