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
<html lang="pt-BR" class="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>MOAT TERMINAL • Inteligência Fundamentalista &amp; Qualidade B3</title>
  <meta name="description" content="Terminal institucional de inteligência fundamentalista e análise de vantagens competitivas duradouras (Economic Moats), solidez patrimonial e alocação prudente de capital. Triagem completa de 196 ações da B3.">
  <meta name="keywords" content="análise fundamentalista, ações B3, valuation, Graham, Bazin, ROIC, ROE, Economic Moats, fosso econômico, Ibovespa, dividend yield, múltiplos de mercado, terminal de investimentos">
  <meta name="author" content="MOAT TERMINAL">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="https://moatterminal.com.br/">

  <!-- Open Graph / Facebook / WhatsApp / LinkedIn -->
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://moatterminal.com.br/">
  <meta property="og:title" content="MOAT TERMINAL • Inteligência Fundamentalista &amp; Qualidade B3">
  <meta property="og:description" content="Terminal institucional de triagem fundamentalista de 196 ações da B3. Matriz 2x2 Valor vs Qualidade, Moat Score e múltiplos auditados CVM.">
  <meta property="og:site_name" content="MOAT TERMINAL">
  <meta property="og:locale" content="pt_BR">

  <!-- Twitter / X Cards -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:url" content="https://moatterminal.com.br/">
  <meta name="twitter:title" content="MOAT TERMINAL • Inteligência Fundamentalista &amp; Qualidade B3">
  <meta name="twitter:description" content="Terminal de análise de ações da B3 focado em vantagens competitivas duradouras (Economic Moats) e alocação prudente de capital.">

  <!-- Schema.org JSON-LD Structured Data for Google Rich Results -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@graph": [
      {{
        "@type": "WebSite",
        "@id": "https://moatterminal.com.br/#website",
        "url": "https://moatterminal.com.br/",
        "name": "MOAT TERMINAL",
        "description": "Terminal institucional de inteligência fundamentalista e vantagens competitivas (Economic Moats) da B3",
        "inLanguage": "pt-BR",
        "publisher": {{
          "@type": "Organization",
          "name": "MOAT TERMINAL",
          "url": "https://moatterminal.com.br/"
        }},
        "potentialAction": {{
          "@type": "SearchAction",
          "target": "https://moatterminal.com.br/empresa.html?ticker={{search_term_string}}",
          "query-input": "required name=search_term_string"
        }}
      }},
      {{
        "@type": "SoftwareApplication",
        "name": "MOAT TERMINAL",
        "applicationCategory": "FinanceApplication",
        "operatingSystem": "Web",
        "url": "https://moatterminal.com.br/",
        "offers": {{
          "@type": "Offer",
          "price": "0",
          "priceCurrency": "BRL"
        }}
      }}
    ]
  }}
  </script>

  <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23059669' stroke-width='2.2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M3 21h18M3 10h18M5 10v11M19 10v11M9 10v11M15 10v11M4 10l2-6h12l2 6M9 4v3M15 4v3'/%3E%3C/svg%3E">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;0,6..72,700;1,6..72,400&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">

  <!-- GOOGLE ADSENSE -->
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8661500874049196" crossorigin="anonymous"></script>

  <!-- Google Analytics 4 (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-QJPB4NM5PW"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());

    gtag('config', 'G-QJPB4NM5PW');
  </script>

  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {{
      darkMode: 'class',
      theme: {{
        extend: {{
          fontFamily: {{
            serif: ['Newsreader', 'Georgia', 'serif'],
            sans: ['Plus Jakarta Sans', 'Inter', 'sans-serif'],
            mono: ['JetBrains Mono', 'monospace'],
          }},
          colors: {{
            bcgForest: '#004B49',
            bcgDeep: '#003836',
            bcgMint: '#00A887',
            bcgLightMint: '#E6F4F1',
            bcgWarmBg: '#FBFBF9',
            bcgCard: '#FFFFFF',
            bcgBorder: '#E7E7E2',
            bcgMuted: '#5A6A68',
            bcgDark: '#111827',
          }}
        }}
      }}
    }}
  </script>
  <style>
    body {{
      background-color: #FBFBF9;
      background-image: 
        radial-gradient(circle at 10% 15%, rgba(0, 75, 73, 0.025) 0%, transparent 45%),
        radial-gradient(circle at 90% 80%, rgba(0, 168, 135, 0.025) 0%, transparent 45%);
      background-attachment: fixed;
      color: #1A202C;
      font-family: 'Plus Jakarta Sans', 'Inter', sans-serif;
    }}
    .font-editorial {{
      font-family: 'Newsreader', Georgia, serif;
    }}
    .glass-panel {{
      background: #FFFFFF;
      border: 1px solid #E7E7E2;
      box-shadow: 0 4px 20px -2px rgba(0, 56, 54, 0.03);
    }}
    .glass-card {{
      background: #FFFFFF;
      border: 1px solid #E7E7E2;
      box-shadow: 0 1px 3px 0 rgba(0, 56, 54, 0.03);
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }}
    .glass-card:hover {{
      background: #FFFFFF;
      border-color: #BCE5DC;
      box-shadow: 0 12px 28px -5px rgba(0, 56, 54, 0.07);
      transform: translateY(-1px);
    }}
    .glass-pill {{
      background: #F4F4F0;
      border: 1px solid #E7E7E2;
      color: #334155;
    }}
    .glass-pill:hover {{
      background: #EAEAE4;
      color: #0F172A;
    }}
    .mono-num {{
      font-family: 'JetBrains Mono', monospace;
    }}
    ::-webkit-scrollbar {{
      width: 6px;
      height: 6px;
    }}
    ::-webkit-scrollbar-track {{
      background: #F8FAFC;
    }}
    ::-webkit-scrollbar-thumb {{
      background: #CBD5E1;
      border-radius: 9999px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
      background: #94A3B8;
    }}
    .sidebar-nav-btn {{
      color: #475569;
      border: 1px solid transparent;
      border-radius: 0.875rem;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }}
    .sidebar-nav-btn:hover {{
      color: #0F172A;
      background: #F1F5F9;
      border-color: #E2E8F0;
    }}
    .sidebar-nav-btn.active {{
      background: #004B49;
      color: #FFFFFF;
      border: 1px solid #004B49;
      font-weight: 700;
      box-shadow: 0 2px 8px rgba(0, 75, 73, 0.25);
    }}
    .tab-btn {{
      border-radius: 9999px;
      transition: all 0.2s ease;
      color: #64748B;
    }}
    .tab-btn.active {{
      background: #004B49;
      color: #FFFFFF;
      border: 1px solid #004B49;
      font-weight: 700;
    }}
    .filter-btn {{
      border-radius: 9999px;
      transition: all 0.2s ease;
      color: #475569;
    }}
    .filter-btn.active {{
      background: #004B49;
      border-color: #004B49;
      color: #FFFFFF;
      box-shadow: 0 2px 8px rgba(0, 75, 73, 0.25);
      font-weight: 700;
    }}
    .drawer-backdrop {{
      background-color: rgba(15, 23, 42, 0.45);
      backdrop-filter: blur(4px);
    }}
    .dot-pulse {{
      box-shadow: 0 0 10px rgba(16, 185, 129, 0.6);
    }}
    @keyframes spin-slow {{
      from {{ transform: rotate(0deg); }}
      to {{ transform: rotate(360deg); }}
    }}
    .spin-active {{
      animation: spin-slow 1s linear infinite;
    }}

    .topbar-nav-btn {{
      color: rgba(255, 255, 255, 0.75);
      border: 1px solid transparent;
      transition: all 0.15s ease;
      cursor: pointer;
    }}
    .topbar-nav-btn:hover {{
      color: #FFFFFF;
      background-color: rgba(255, 255, 255, 0.12);
    }}
    .topbar-nav-btn.active {{
      background-color: #00A887;
      color: #FFFFFF;
      border-color: #00A887;
      box-shadow: 0 2px 8px rgba(0, 168, 135, 0.35);
      font-weight: 700;
    }}
    .info-badge {{
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
      user-select: none;
    }}
    .info-badge:hover {{
      color: #0F172A;
      background-color: #E2E8F0;
      border-color: #94A3B8;
      transform: scale(1.15);
    }}
  </style>
</head>
<body class="h-screen text-[#1A202C] bg-[#FBFBF9] flex flex-col overflow-hidden font-sans antialiased selection:bg-[#00A887]/20 selection:text-[#003836]">

  <!-- GLOBAL INTERACTIVE EDUCATIONAL TOOLTIP (BALÃOZINHO INSTITUCIONAL) -->
  <div id="globalTooltip" class="fixed hidden z-[999999] max-w-xs sm:max-w-sm bg-slate-900 text-white p-3.5 rounded-2xl shadow-2xl border border-slate-700 pointer-events-none transition-opacity duration-150 text-xs font-sans">
    <div class="font-bold text-emerald-400 font-mono text-xs flex items-center gap-1.5 border-b border-slate-700/80 pb-1.5 mb-1.5" id="gtTitle"></div>
    <div class="text-slate-200 text-[11.5px] leading-relaxed font-sans" id="gtDesc"></div>
    <div class="text-slate-400 text-[10px] font-mono mt-2 pt-1.5 border-t border-slate-800 flex items-center justify-between" id="gtFoot"></div>
  </div>

  <!-- TOPBAR INSTITUCIONAL FULL-WIDTH (BRANDING + NAVEGAÇÃO SUPERIOR + BUSCA + CONTROLES • BCG AESTHETIC) -->
  <header class="bg-[#003836] border-b border-[#004B49] text-white px-3 sm:px-6 py-2 sm:py-2.5 flex flex-wrap items-center justify-between gap-2 sm:gap-3 z-30 flex-shrink-0 shadow-sm">
    
    <!-- Esquerda: Brand Institucional & Status Moat -->
    <div onclick="goToHome()" class="flex items-center gap-2.5 sm:gap-3.5 cursor-pointer group select-none transition" title="Ir para o Panorama Geral (Home)">
      <div class="w-8 h-8 sm:w-9 sm:h-9 rounded-xl bg-[#004B49] flex items-center justify-center text-white shadow-xs border border-emerald-500/30 flex-shrink-0 group-hover:scale-105 transition-transform" title="Moat Terminal • Vantagens Competitivas B3">
        <svg class="w-4 h-4 text-[#00A887] stroke-[2.4]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 21h18M3 10h18M5 10v11M19 10v11M9 10v11M15 10v11M4 10l2-6h12l2 6M9 4v3M15 4v3"/></svg>
      </div>
      <div class="flex flex-col">
        <div class="flex items-center gap-1.5">
          <span class="font-bold text-white text-xs sm:text-sm tracking-wider font-mono leading-none group-hover:text-emerald-300 transition">MOAT TERMINAL</span>
          <span class="px-1.5 py-0.2 text-[8px] bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 font-bold font-mono rounded">STRATEGY</span>
        </div>
        <div class="flex items-center gap-1.5 sm:gap-2 text-[10px] text-emerald-100/70 font-mono mt-0.5">
          <span class="text-emerald-100/90 font-medium hidden sm:inline">Economic Moats &amp; Capital Allocation</span>
          <span class="text-emerald-400/40 hidden sm:inline">•</span>
          <span class="text-emerald-300 font-bold flex items-center gap-1">
            <span class="w-1.5 h-1.5 rounded-full bg-[#00A887] animate-pulse"></span> 2T26 CVM
          </span>
        </div>
      </div>
    </div>

    <!-- Centro: Segmented Navigation Pills (3 Abas Diretas & Essenciais) -->
    <nav class="flex items-center bg-black/25 p-0.5 sm:p-1 rounded-xl border border-white/10 gap-0.5 sm:gap-1 font-mono text-xs">
      <button id="nav-home" onclick="switchWorkspace('home')" class="topbar-nav-btn active flex items-center gap-1.5 px-2.5 sm:px-3.5 py-1.5 rounded-lg text-xs font-semibold transition cursor-pointer flex-shrink-0">
        <svg class="w-3.5 h-3.5 stroke-[1.75]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>
        <span class="hidden sm:inline">Panorama Geral</span>
        <span class="sm:hidden">Home</span>
      </button>
      <button id="nav-matrix" onclick="switchWorkspace('matrix')" class="topbar-nav-btn flex items-center gap-1.5 px-2.5 sm:px-3.5 py-1.5 rounded-lg text-xs font-semibold transition cursor-pointer flex-shrink-0">
        <svg class="w-3.5 h-3.5 stroke-[1.75]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4 4v16h16M4 12h16M12 4v16"/></svg>
        <span class="hidden sm:inline">Matriz Estratégica 2x2</span>
        <span class="sm:hidden">Matriz</span>
      </button>
      <button id="nav-table" onclick="switchWorkspace('table')" class="topbar-nav-btn flex items-center gap-1.5 px-2.5 sm:px-3.5 py-1.5 rounded-lg text-xs font-semibold transition cursor-pointer flex-shrink-0">
        <svg class="w-3.5 h-3.5 stroke-[1.75]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-4.35-4.35"/></svg>
        <span>Scanner</span>
        <span class="text-[10px] text-emerald-950 font-mono bg-emerald-200 px-1.5 py-0.2 rounded font-bold border border-emerald-300 hidden md:inline-block" id="sidebarUniverseCount">--</span>
      </button>
    </nav>

    <!-- Direita: Busca Universal, Ativo Ativo e Ações -->
    <div class="flex items-center gap-1.5 sm:gap-2.5 ml-auto sm:ml-0">
      <div class="relative" id="searchWrapper">
        <div class="relative flex items-center">
          <span class="absolute left-2.5 text-emerald-200/60 pointer-events-none">
            <svg class="w-3.5 h-3.5 stroke-[2]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-4.35-4.35"/></svg>
          </span>
          <input type="text" id="searchInput" 
                 oninput="handleSearchInput(this.value)" 
                 onkeydown="handleSearchKeydown(event)" 
                 onfocus="handleSearchFocus()" 
                 placeholder="Buscar Ativo..." 
                 autocomplete="off"
                 class="w-28 sm:w-48 md:w-64 bg-white/10 border border-white/20 rounded-lg pl-8 pr-2 sm:pr-7 py-1.5 text-xs text-white placeholder-emerald-100/50 focus:outline-none focus:bg-white focus:text-slate-900 focus:border-[#00A887] font-mono transition shadow-2xs">
          <kbd class="hidden sm:inline-block absolute right-2 text-[10px] font-mono text-emerald-200/70 bg-white/10 border border-white/20 px-1 rounded shadow-3xs pointer-events-none select-none">/</kbd>
        </div>

        <!-- Dropdown de Sugestões em Tempo Real -->
        <div id="searchDropdown" class="hidden absolute right-0 sm:left-0 w-80 sm:w-96 mt-1.5 bg-white border border-slate-200/90 rounded-2xl shadow-2xl z-[99999] max-h-96 overflow-y-auto overflow-x-hidden divide-y divide-slate-100 font-sans text-slate-800">
          <!-- Injetado dinamicamente via JS -->
        </div>
      </div>

      <div class="text-xs font-mono text-emerald-100 hidden md:flex items-center gap-1.5 bg-white/10 px-2.5 py-1.5 rounded-lg border border-white/15 shadow-2xs">
        <span class="text-emerald-200/70 text-[11px]">Ativo:</span>
        <b class="text-white font-bold" id="topSelectedTickerBadge">--</b>
      </div>

      <div class="text-xs font-mono text-emerald-100/80 hidden xl:block bg-white/10 px-2.5 py-1.5 rounded-lg border border-white/15 shadow-2xs">
        <b class="text-emerald-300 font-bold" id="displayedCount">--</b>/<span id="totalUniverseCount">--</span>
      </div>

      <!-- Selo 'Atualizado' com Balãozinho de Data e Hora no Hover -->
      <div class="relative group cursor-pointer" id="lastUpdateBadgeWrapper" onclick="const p=this.querySelector('.update-tooltip-popup'); if(p) p.classList.toggle('!block');">
        <div class="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-[#004B49] hover:bg-[#005C59] border border-[#00A887]/40 text-white font-mono text-xs shadow-2xs transition select-none">
          <span class="w-2 h-2 rounded-full bg-[#00A887] animate-pulse flex-shrink-0"></span>
          <span class="font-bold text-emerald-200 text-[11px] sm:text-xs">Atualizado</span>
        </div>

        <!-- Balãozinho Suspenso no Hover (Data e Hora) -->
        <div class="update-tooltip-popup absolute right-0 top-full mt-2 hidden group-hover:block z-[999999] w-64 p-3 bg-slate-900 text-white rounded-xl shadow-2xl border border-slate-700 text-xs font-sans transition-all duration-200">
          <div class="font-mono font-bold text-emerald-400 text-[11.5px] flex items-center gap-1.5 border-b border-slate-700/80 pb-1.5 mb-1.5">
            <svg class="w-3.5 h-3.5 stroke-[2]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
            <span>Última Atualização dos Dados</span>
          </div>
          <div class="text-slate-200 text-[11px] space-y-1">
            <div class="font-mono font-bold text-white text-xs" id="badgeUpdateDateTime">--/--/---- às 07:20</div>
            <p class="text-slate-400 leading-tight text-[10.5px]">
              Rotina processada diariamente na nuvem (07:20, 12:20 e 18:45 BRT).
            </p>
          </div>
          <div class="mt-2 pt-1.5 border-t border-slate-800 text-[9.5px] font-mono text-slate-400 flex items-center justify-between">
            <span>Base CVM 2T26</span>
            <span class="text-emerald-400 font-bold">194 Ações B3</span>
          </div>
        </div>
      </div>

      <button onclick="openWelcomeGuide()" class="px-2 sm:px-2.5 py-1.5 bg-white/10 hover:bg-white/20 border border-white/20 text-white font-semibold rounded-lg text-xs font-mono cursor-pointer transition flex items-center gap-1.5 shadow-2xs" title="Apresentação do Terminal, Guia e Termo de Responsabilidade CVM">
        <svg class="w-3.5 h-3.5 text-emerald-300 stroke-[2]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path stroke-linecap="round" stroke-linejoin="round" d="M12 16v-4m0-4h.01"/></svg>
        <span class="hidden sm:inline">Guia &amp; Isenção</span>
      </button>
    </div>

  </header>

  <!-- PAINEL PRINCIPAL FULL-WIDTH COM SCROLL NATURAL -->
  <div class="flex-1 flex flex-col min-w-0 overflow-hidden">

    <!-- BANNER DE STATUS / TOAST DE ATUALIZAÇÃO -->
    <div id="statusToast" class="hidden mx-6 mt-3 p-2.5 rounded-lg border text-xs font-mono flex items-center justify-between transition-all flex-shrink-0">
      <div class="flex items-center gap-2" id="statusToastContent"></div>
      <button onclick="hideToast()" class="text-slate-400 hover:text-slate-900 text-xs">✕</button>
    </div>

    <!-- CANVAS DOS WORKSPACES COM SCROLL NATURAL E ESPAÇOSO -->
    <main class="flex-1 min-h-0 relative overflow-y-auto p-4 sm:p-6 bg-[#FBFBF9]" id="workspaceContainer">

      <!-- WORKSPACE 0: 🏠 HOME (PANORAMA GERAL EXECUTIVO • BCG EDITORIAL DESIGN) -->
      <section id="view-home" class="w-full rounded-3xl flex flex-col space-y-8 max-w-7xl mx-auto">
        
        <!-- 1. BCG HERO EDITORIAL BRIEFING -->
        <div class="p-8 sm:p-12 rounded-3xl bg-white border border-[#E7E7E2] shadow-sm relative overflow-hidden flex-shrink-0">
          <div class="absolute -top-24 -right-24 w-96 h-96 bg-[#00A887]/8 rounded-full blur-3xl pointer-events-none"></div>
          <div class="absolute bottom-0 right-1/4 w-64 h-64 bg-[#003836]/5 rounded-full blur-2xl pointer-events-none"></div>
          
          <div class="relative z-10 max-w-4xl space-y-5">
            <div class="inline-flex items-center gap-2.5 px-3.5 py-1 rounded-full bg-[#E6F4F1] border border-[#BCE5DC] text-[#004B49] text-xs font-mono font-bold tracking-wider uppercase">
              <span class="w-2 h-2 rounded-full bg-[#00A887] animate-pulse"></span>
              <span>Inteligência Estratégica B3 • 2T26 Auditado</span>
            </div>
            
            <h1 class="text-3xl sm:text-5xl lg:text-6xl font-editorial font-bold text-slate-950 tracking-tight leading-[1.12]">
              Onde o fosso competitivo encontra a disciplina de valor.
            </h1>
            
            <p class="text-sm sm:text-lg text-slate-600 font-sans leading-relaxed max-w-3xl pt-1">
              Terminal de alta convicção analítica inspirado em <b>Charlie Munger e Benjamin Graham</b>. Triagem fundamentalista de <b>194 ações brasileiras</b> com foco em vantagens competitivas duráveis (<i>Economic Moats</i>), retorno sobre capital (<i>ROIC &amp; ROE</i>) e prêmio real sobre o custo soberano.
            </p>

            <!-- Ações Executivas Diretas -->
            <div class="flex flex-wrap items-center gap-3.5 pt-3">
              <button type="button" onclick="switchWorkspace('table')" class="inline-flex items-center gap-2.5 px-6 py-3 rounded-xl bg-[#003836] hover:bg-[#004B49] text-white font-mono text-xs font-bold shadow-md transition-all cursor-pointer hover:shadow-lg hover:-translate-y-0.5">
                <span>Explorar Scanner B3 (194 Ativos)</span>
                <span class="text-emerald-300">➜</span>
              </button>
              <button type="button" onclick="switchWorkspace('matrix')" class="inline-flex items-center gap-2 px-5 py-3 rounded-xl bg-[#F4F4F0] hover:bg-[#EAEAE4] border border-[#E7E7E2] text-slate-800 font-mono text-xs font-semibold transition cursor-pointer">
                <span>Matriz Estratégica 2x2</span>
                <span class="text-slate-500">📊</span>
              </button>
              <button type="button" onclick="setFilterAndGoTable('IBOV')" class="inline-flex items-center gap-2 px-4 py-3 rounded-xl bg-white hover:bg-[#F4F4F0] border border-[#E7E7E2] text-slate-700 font-mono text-xs font-medium transition cursor-pointer">
                <span>🇧🇷 Carteira Ibovespa (76)</span>
              </button>
              <button type="button" onclick="openWelcomeGuide()" class="inline-flex items-center gap-2 px-3.5 py-3 rounded-xl text-slate-500 hover:text-slate-800 text-xs font-mono transition cursor-pointer underline underline-offset-4">
                <span>Guia Regulatório CVM 20/2021</span>
              </button>
            </div>
          </div>
        </div>

        <!-- 2. TRÊS PILARES MACRO (ESCALA EDITORIAL BCG) -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-5 flex-shrink-0">
          
          <!-- Pilar 1: Sovereign Benchmark -->
          <div class="glass-card rounded-3xl p-7 border border-[#E7E7E2] flex flex-col justify-between hover:border-[#00A887] transition-all bg-white group">
            <div class="space-y-3">
              <div class="flex items-center justify-between text-xs font-mono">
                <span class="text-slate-400 uppercase tracking-widest text-[10.5px] font-bold">Régua Soberana Livre de Risco</span>
                <span class="px-2.5 py-0.5 rounded-full bg-slate-100 text-slate-800 text-[10px] font-bold font-mono">NTN-B 2035</span>
              </div>
              <div class="text-4xl font-mono font-bold text-[#003836] tracking-tight group-hover:text-[#00A887] transition-colors">IPCA + 6,50%</div>
              <p class="text-xs text-slate-600 leading-relaxed font-sans pt-1">
                O custo de oportunidade soberano do Brasil. Qualquer investimento na bolsa precisa entregar retorno operacional excedente para justificar o prêmio de risco do equity.
              </p>
            </div>
            <div class="pt-5 mt-5 border-t border-[#F2F2ED] flex items-center justify-between text-xs font-mono text-slate-500">
              <span class="text-[11px]">Benchmark Soberano</span>
              <span class="text-[#004B49] font-bold flex items-center gap-1">
                <span>Taxa Real</span> <span class="text-xs">🛡️</span>
              </span>
            </div>
          </div>

          <!-- Pilar 2: Market Multiple -->
          <div class="glass-card rounded-3xl p-7 border border-[#E7E7E2] flex flex-col justify-between hover:border-[#00A887] transition-all bg-white group">
            <div class="space-y-3">
              <div class="flex items-center justify-between text-xs font-mono">
                <span class="text-slate-400 uppercase tracking-widest text-[10.5px] font-bold">Valuation Consolidado B3</span>
                <span class="px-2.5 py-0.5 rounded-full bg-amber-50 text-amber-900 border border-amber-200 text-[10px] font-bold font-mono" id="home-stat-pl-tag">Barato</span>
              </div>
              <div class="text-4xl font-mono font-bold text-slate-900 tracking-tight" id="home-stat-pl">9,1x P/L</div>
              <p class="text-xs text-slate-600 leading-relaxed font-sans pt-1">
                Múltiplo mediano Preço/Lucro LTM do universo monitorado. Sinaliza dispersão favorável de múltiplos com desconto em relação à média decenal da B3.
              </p>
            </div>
            <div class="pt-5 mt-5 border-t border-[#F2F2ED] flex items-center justify-between text-xs font-mono text-slate-500">
              <span class="text-[11px]">Preço / Lucro Mediano</span>
              <span class="text-amber-800 font-bold flex items-center gap-1">
                <span>Desconto Histórico</span> <span class="text-xs">📉</span>
              </span>
            </div>
          </div>

          <!-- Pilar 3: Return on Capital -->
          <div class="glass-card rounded-3xl p-7 border border-[#E7E7E2] flex flex-col justify-between hover:border-[#00A887] transition-all bg-white group">
            <div class="space-y-3">
              <div class="flex items-center justify-between text-xs font-mono">
                <span class="text-slate-400 uppercase tracking-widest text-[10.5px] font-bold">Eficiência &amp; Retorno do Capital</span>
                <span class="px-2.5 py-0.5 rounded-full bg-[#E6F4F1] text-[#004B49] border border-[#BCE5DC] text-[10px] font-bold font-mono" id="home-stat-spread-tag">Prêmio Positivo</span>
              </div>
              <div class="text-4xl font-mono font-bold text-[#00A887] tracking-tight" id="home-stat-roic">10,2% ROIC</div>
              <p class="text-xs text-slate-600 leading-relaxed font-sans pt-1">
                Retorno médio gerado pelo capital empregado. Ativos classificados como Tier 1 (Wide Moat) operam com ROIC acima de 18% a.a., ampliando a barreira contra concorrentes.
              </p>
            </div>
            <div class="pt-5 mt-5 border-t border-[#F2F2ED] flex items-center justify-between text-xs font-mono text-slate-500">
              <span class="text-[11px]">Spread Médio vs NTN-B</span>
              <span class="text-[#004B49] font-bold flex items-center gap-1">
                <span id="home-stat-spread">+4,1%</span> <span class="text-xs">🏰</span>
              </span>
            </div>
          </div>

        </div>

        <!-- 3. DESTAQUES ESTRATÉGICOS (BRIEFINGS EXECUTIVOS TIER 1 & BAZIN) -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 flex-shrink-0">
          
          <!-- Card 1: Wide Moat Tier 1 -->
          <div class="glass-card rounded-3xl flex flex-col overflow-hidden border border-[#E7E7E2] shadow-xs bg-white p-6 sm:p-7 space-y-4">
            <div class="border-b border-[#F2F2ED] pb-4 flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <div class="space-y-1">
                <span class="text-[10.5px] font-mono font-bold tracking-widest uppercase text-amber-900 bg-amber-50 border border-amber-200 px-3 py-1 rounded-full inline-block">
                  ALTA CONVICÇÃO • TIER 1
                </span>
                <h3 class="text-xl sm:text-2xl font-editorial font-bold text-slate-900 pt-1">
                  Empresas com Fosso Econômico (Wide Moat)
                </h3>
                <p class="text-xs text-slate-600 font-sans leading-relaxed">
                  Negócios líderes com barreiras competitivas duradouras, precificação resiliente e alto retorno sobre o capital.
                </p>
              </div>
              <button onclick="setFilterAndGoTable('CAT_TIER1')" class="text-xs font-mono font-bold text-[#004B49] hover:text-[#00A887] transition cursor-pointer flex items-center gap-1 self-start sm:self-center flex-shrink-0">
                <span>Ver Todos</span> <span>➜</span>
              </button>
            </div>
            <div class="space-y-2.5 font-mono text-xs pt-1" id="home-list-munger">
              <!-- Renderizado via JS -->
            </div>
          </div>

          <!-- Card 2: Vacas Leiteiras Bazin -->
          <div class="glass-card rounded-3xl flex flex-col overflow-hidden border border-[#E7E7E2] shadow-xs bg-white p-6 sm:p-7 space-y-4">
            <div class="border-b border-[#F2F2ED] pb-4 flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <div class="space-y-1">
                <span class="text-[10.5px] font-mono font-bold tracking-widest uppercase text-[#004B49] bg-[#E6F4F1] border border-[#BCE5DC] px-3 py-1 rounded-full inline-block">
                  FLUXO DE CAIXA • BAZIN
                </span>
                <h3 class="text-xl sm:text-2xl font-editorial font-bold text-slate-900 pt-1">
                  Dividendos Sustentáveis (&gt; 6% a.a.)
                </h3>
                <p class="text-xs text-slate-600 font-sans leading-relaxed">
                  Companhias maduras e geradoras de caixa com histórico de proventos regulares protegidos por balanços sólidos.
                </p>
              </div>
              <button onclick="setFilterAndGoTable('CAT_DIVIDENDS')" class="text-xs font-mono font-bold text-[#004B49] hover:text-[#00A887] transition cursor-pointer flex items-center gap-1 self-start sm:self-center flex-shrink-0">
                <span>Ver Todos</span> <span>➜</span>
              </button>
            </div>
            <div class="space-y-2.5 font-mono text-xs pt-1" id="home-list-dividends">
              <!-- Renderizado via JS -->
            </div>
          </div>

        </div>

        <!-- 3. Momentos Contábeis 2T26 & Solvência Munger -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 flex-shrink-0">
          
          <!-- Lucro Acelerando (Expansão) -->
          <div class="glass-card rounded-2xl flex flex-col overflow-hidden border border-slate-200/90 shadow-2xs bg-white">
            <div class="p-3 border-b border-slate-100 flex items-center justify-between">
              <div class="flex items-center gap-1.5 min-w-0">
                <span class="text-teal-600 flex items-center"><svg class="w-4 h-4 stroke-[1.75]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg></span>
                <span class="text-xs font-mono font-bold text-slate-900 uppercase truncate">Lucro Acelerando (Expansão)</span>
                <span class="text-[10px] font-mono text-teal-700 font-bold" id="cnt-cat-accel">(--)</span>
              </div>
              <button onclick="setFilterAndGoTable('CAT_EXPANSION')" class="text-[10px] font-mono font-bold text-teal-700 hover:text-teal-900 transition cursor-pointer flex-shrink-0" title="Ver todas as empresas com lucro acelerando">
                Ver todos ➜
              </button>
            </div>
            <div class="p-2.5 flex-1 space-y-1.5 font-mono text-xs" id="home-list-accelerating"></div>
          </div>

          <!-- Lucro em Retração (Desaceleração) -->
          <div class="glass-card rounded-2xl flex flex-col overflow-hidden border border-slate-200/90 shadow-2xs bg-white">
            <div class="p-3 border-b border-slate-100 flex items-center justify-between">
              <div class="flex items-center gap-1.5 min-w-0">
                <span class="text-amber-600 flex items-center"><svg class="w-4 h-4 stroke-[1.75]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 9v4m0 4h.01M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/></svg></span>
                <span class="text-xs font-mono font-bold text-slate-900 uppercase truncate">Lucro em Retração (Desaceleração)</span>
                <span class="text-[10px] font-mono text-amber-700 font-bold" id="cnt-cat-decel">(--)</span>
              </div>
              <button onclick="setFilterAndGoTable('CAT_DECELERATION')" class="text-[10px] font-mono font-bold text-amber-700 hover:text-amber-900 transition cursor-pointer flex-shrink-0" title="Ver todas as empresas com lucro em desaceleração">
                Ver todos ➜
              </button>
            </div>
            <div class="p-2.5 flex-1 space-y-1.5 font-mono text-xs" id="home-list-decelerating"></div>
          </div>

          <!-- Balanço Forte (Caixa Líquido) -->
          <div class="glass-card rounded-2xl flex flex-col overflow-hidden border border-slate-200/90 shadow-2xs bg-white">
            <div class="p-3 border-b border-slate-100 flex items-center justify-between">
              <div class="flex items-center gap-1.5 min-w-0">
                <span class="text-emerald-600 flex items-center"><svg class="w-4 h-4 stroke-[1.75]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg></span>
                <span class="text-xs font-mono font-bold text-slate-900 uppercase truncate">Caixa Líquido</span>
                <span class="text-[10px] font-mono text-emerald-700 font-bold" id="cnt-cat-netcash">(--)</span>
              </div>
              <button onclick="setFilterAndGoTable('CAT_NET_CASH')" class="text-[10px] font-mono font-bold text-emerald-700 hover:text-emerald-900 transition cursor-pointer flex-shrink-0" title="Ver todas as empresas com caixa líquido">
                Ver todos ➜
              </button>
            </div>
            <div class="p-2.5 flex-1 space-y-1.5 font-mono text-xs" id="home-list-netcash"></div>
          </div>

          <!-- Sensibilidade Selic (Dívida Alta) -->
          <div class="glass-card rounded-2xl flex flex-col overflow-hidden border border-slate-200/90 shadow-2xs bg-white">
            <div class="p-3 border-b border-slate-100 flex items-center justify-between">
              <div class="flex items-center gap-1.5 min-w-0">
                <span class="text-rose-600 flex items-center"><svg class="w-4 h-4 stroke-[1.75]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 9v4m0 4h.01M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/></svg></span>
                <span class="text-xs font-mono font-bold text-slate-900 uppercase truncate">Alavancagem Alta (> 2.5x)</span>
                <span class="text-[10px] font-mono text-rose-700 font-bold" id="cnt-cat-highdebt">(--)</span>
              </div>
              <button onclick="setFilterAndGoTable('CAT_HIGH_DEBT')" class="text-[10px] font-mono font-bold text-rose-700 hover:text-rose-900 transition cursor-pointer flex-shrink-0" title="Ver todas as empresas com dívida alta">
                Ver todos ➜
              </button>
            </div>
            <div class="p-2.5 flex-1 space-y-1.5 font-mono text-xs" id="home-list-highdebt"></div>
          </div>

        </div>

        <!-- 5. Carteira Teórica Ibovespa Vigente (76 Ativos Oficiais B3) -->
        <div class="glass-card rounded-2xl p-5 border border-slate-200/90 shadow-2xs flex-shrink-0">
          <!-- Cabeçalho com Título, Badges e Botão de Ação -->
          <div class="flex flex-col md:flex-row md:items-center justify-between gap-3 mb-4 pb-3 border-b border-slate-100">
            <div>
              <div class="flex items-center gap-2">
                <span class="px-2 py-0.5 rounded-md bg-indigo-100 text-indigo-900 border border-indigo-200 text-[10px] font-mono font-bold uppercase tracking-wider">Índice Oficial B3</span>
                <span class="text-xs font-mono font-bold text-slate-900 uppercase tracking-wider flex items-center gap-1.5">
                  CARTEIRA TEÓRICA IBOVESPA VIGENTE (SET-DEZ/2026)
                </span>
              </div>
              <p class="text-xs text-slate-500 font-sans mt-0.5">
                Os 76 ativos com maior representatividade e liquidez do mercado brasileiro. Selecione um filtro ou ativo abaixo:
              </p>
            </div>
            <div class="flex items-center gap-2">
              <button onclick="setFilterAndGoTable('IBOV')" class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-white text-xs font-mono font-bold transition shadow-xs cursor-pointer group" title="Filtrar os 76 componentes do Ibovespa no Scanner">
                <svg class="w-3.5 h-3.5 stroke-[2] text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z"/></svg>
                <span>Filtrar 76 Ativos no Scanner B3</span>
                <span class="group-hover:translate-x-0.5 transition-transform text-slate-400">➜</span>
              </button>
            </div>
          </div>

          <!-- Micro-Dashboard de Estatísticas do Ibovespa -->
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-2.5 mb-4">
            <div class="p-2.5 rounded-xl bg-slate-50/80 border border-slate-200/70">
              <div class="text-[10px] font-mono uppercase text-slate-500 font-semibold">Total de Ativos</div>
              <div class="text-lg font-bold font-mono text-slate-900" id="home-ibov-count">76 papéis</div>
              <div class="text-[10px] text-slate-500 font-sans">74 empresas listadas</div>
            </div>
            <div class="p-2.5 rounded-xl bg-slate-50/80 border border-slate-200/70">
              <div class="text-[10px] font-mono uppercase text-slate-500 font-semibold">Concentração Top 5</div>
              <div class="text-lg font-bold font-mono text-indigo-800">36,9%</div>
              <div class="text-[10px] text-slate-500 font-sans">VALE, ITUB, PETR (x2), AXIA</div>
            </div>
            <div class="p-2.5 rounded-xl bg-slate-50/80 border border-slate-200/70">
              <div class="text-[10px] font-mono uppercase text-slate-500 font-semibold">P/L Mediano Ibov</div>
              <div class="text-lg font-bold font-mono text-emerald-800" id="home-ibov-median-pl">12,1x</div>
              <div class="text-[10px] text-slate-500 font-sans">Múltiplo de lucro corrente</div>
            </div>
            <div class="p-2.5 rounded-xl bg-slate-50/80 border border-slate-200/70">
              <div class="text-[10px] font-mono uppercase text-slate-500 font-semibold">DY Médio Ponderado</div>
              <div class="text-lg font-bold font-mono text-teal-800" id="home-ibov-dy-ponderado">5,5%</div>
              <div class="text-[10px] text-slate-500 font-sans">Remuneração em proventos</div>
            </div>
          </div>

          <!-- Barra de Filtros Internos do Card e Busca -->
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2.5 mb-3">
            <div class="flex flex-wrap items-center gap-1.5 font-mono text-[11px]" id="home-ibov-filter-buttons">
              <button onclick="setHomeIbovFilter('ALL')" id="hibov-flt-ALL" class="hibov-btn active px-2.5 py-1 rounded-lg border border-slate-900 bg-slate-900 text-white font-bold transition cursor-pointer">
                Todos (76)
              </button>
              <button onclick="setHomeIbovFilter('TOP15')" id="hibov-flt-TOP15" class="hibov-btn px-2.5 py-1 rounded-lg border border-slate-200 bg-white text-slate-700 font-semibold hover:border-slate-300 transition cursor-pointer">
                Top 15 Pesos (62,5%)
              </button>
              <button onclick="setHomeIbovFilter('ASSIMETRIA')" id="hibov-flt-ASSIMETRIA" class="hibov-btn px-2.5 py-1 rounded-lg border border-emerald-300 bg-emerald-50 text-emerald-900 font-semibold hover:bg-emerald-100 transition cursor-pointer">
                🟢 Múltiplos Descontados (<span id="hibov-cnt-assimetria">14</span>)
              </button>
              <button onclick="setHomeIbovFilter('PRECO_JUSTO')" id="hibov-flt-PRECO_JUSTO" class="hibov-btn px-2.5 py-1 rounded-lg border border-amber-300 bg-amber-50 text-amber-900 font-semibold hover:bg-amber-100 transition cursor-pointer">
                🟡 Valuation em Linha (<span id="hibov-cnt-precojusto">28</span>)
              </button>
              <button onclick="setHomeIbovFilter('ESTICADA')" id="hibov-flt-ESTICADA" class="hibov-btn px-2.5 py-1 rounded-lg border border-rose-300 bg-rose-50 text-rose-900 font-semibold hover:bg-rose-100 transition cursor-pointer">
                🔴 Múltiplos Elevados (<span id="hibov-cnt-esticada">34</span>)
              </button>
            </div>
            <div class="relative w-full sm:w-48">
              <input type="text" id="homeIbovSearchInput" oninput="handleHomeIbovSearch()" placeholder="Buscar ação no Ibov..." class="w-full bg-slate-50 border border-slate-200 rounded-lg px-2.5 py-1 text-xs font-mono text-slate-800 placeholder-slate-400 focus:outline-hidden focus:border-indigo-400">
            </div>
          </div>

          <!-- Grid dos Ativos do Ibovespa -->
          <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-2 max-h-[380px] overflow-y-auto pr-1" id="home-ibov-grid">
            <!-- Renderizado dinamicamente via JS -->
          </div>

          <!-- Rodapé do Card -->
          <div class="mt-3 pt-2.5 border-t border-slate-100 flex flex-col sm:flex-row items-center justify-between gap-2 text-[11px] font-mono text-slate-500">
            <span>💡 Clique em qualquer ativo para abrir o Dossiê 360° com histórico, múltiplos e indicadores contábeis.</span>
            <button onclick="setFilterAndGoTable('IBOV')" class="text-indigo-700 hover:text-indigo-900 font-bold hover:underline cursor-pointer">
              Ver todos os 76 no Scanner Fundamentalista ➜
            </button>
          </div>
        </div>

        <!-- ESPAÇO PUBLICITÁRIO / PARCERIAS ESTRATÉGICAS (GOOGLE ADSENSE / AFILIADOS CORRETORAS) -->
        <div class="p-4 rounded-xl border border-slate-200 bg-white shadow-2xs space-y-2 flex-shrink-0">
          <div class="flex items-center justify-between border-b border-slate-100 pb-1.5 text-[10px] font-mono text-slate-400 uppercase tracking-wider">
            <span class="flex items-center gap-1.5"><span class="text-amber-500">📢</span> PUBLICIDADE &amp; PARCERIAS ESTRATÉGICAS</span>
            <span class="text-slate-400 hover:text-slate-600 transition">Espaço Patrocinado</span>
          </div>
          <div id="ad-slot-home" class="min-h-[80px] w-full flex flex-col md:flex-row items-center justify-between gap-3 p-3.5 rounded-lg bg-slate-50 border border-dashed border-slate-300 text-slate-600">
            <div class="flex items-center gap-3">
              <div class="w-9 h-9 rounded-lg bg-emerald-100 text-emerald-800 flex items-center justify-center font-bold text-base flex-shrink-0">
                🏦
              </div>
              <div>
                <div class="font-bold text-xs text-slate-800 font-mono">Espaço Reservado para Google AdSense ou Corretora Parceira</div>
                <div class="text-[11px] text-slate-500">Banner responsivo pronto para receber o bloco do AdSense (728x90 / 320x50) ou campanha de parceiro afiliado (BTG, Avenue, etc.).</div>
              </div>
            </div>
            <div class="flex items-center gap-2 flex-shrink-0">
              <span class="px-2.5 py-1 rounded bg-white border border-slate-200 text-[10px] font-mono text-slate-500 font-medium">Slot: #AD-HOME-BANNER</span>
            </div>
          </div>
        </div>

        <!-- Rodapé Regulatório Legal CVM e Metodologia na Home -->
        <footer class="p-4 rounded-xl border border-slate-200 bg-slate-50 text-slate-600 text-xs leading-relaxed space-y-2 flex-shrink-0">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-1 border-b border-slate-200/80 pb-1.5">
            <div class="font-mono font-bold text-slate-800 flex items-center gap-1.5 text-[11px]">
              <span>⚖️</span> CONFORMIDADE REGULATÓRIA &amp; AUDITORIA CONTÁBIL (RESOLUÇÃO CVM Nº 20/2021)
            </div>
            <div class="flex items-center gap-3 text-[11px] font-mono">
              <a href="termos.html" class="text-slate-600 hover:text-emerald-700 underline underline-offset-2">Termos de Uso</a>
              <span>•</span>
              <a href="privacidade.html" class="text-slate-600 hover:text-emerald-700 underline underline-offset-2">Política de Privacidade</a>
            </div>
          </div>
          <p class="text-[11px] text-slate-500">
            O <b>MOAT TERMINAL</b> é uma ferramenta computacional independente para triagem quantitativa e análise fundamentalista. 
            Todas as métricas, múltiplos e scores resultam exclusivamente de modelagem matemática sobre dados públicos divulgados pelas companhias abertas.
            <b>Este conteúdo tem finalidade estritamente educacional e informativa, não constituindo consultoria, análise individualizada, oferta pública ou recomendação de compra e venda de valores mobiliários</b>. 
            Rentabilidade e lucros passados não garantem retornos futuros. A alocação de recursos deve respeitar seu perfil de risco e critérios próprios de investimento.
          </p>
          <div class="pt-1.5 border-t border-slate-200/60 flex flex-col sm:flex-row items-center justify-between text-[10px] font-mono text-slate-500 gap-1">
            <span>© 2026 MOAT TERMINAL • Todos os direitos reservados.</span>
            <span>Contato institucional: <a href="mailto:contato@moatterminal.com.br" class="hover:text-emerald-700 underline">contato@moatterminal.com.br</a></span>
          </div>
        </footer>

      </section>

    <!-- WORKSPACE 1: 📊 MATRIZ MUNGER 2X2 EM TELA CHEIA (100% DA VIEWPORT) -->
    <section id="view-matrix" class="hidden w-full h-full glass-panel rounded-2xl flex flex-col min-h-0 overflow-hidden shadow-2xl">
      <!-- Header da Matriz: Título e Ações Rápidas -->
      <div class="px-3 sm:px-4 py-2 sm:py-2.5 border-b border-slate-200 flex flex-wrap items-center justify-between gap-2 sm:gap-3 bg-slate-50 flex-shrink-0">
        <div class="flex items-center gap-2 sm:gap-3">
          <span class="text-xs sm:text-sm font-mono font-bold uppercase tracking-wider text-slate-900 flex items-center gap-2">
            <span class="text-emerald-700"><svg class="w-4 h-4 stroke-[2] inline-block" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4 4v16h16M4 12h16M12 4v16"/></svg></span>
            <span class="hidden sm:inline">MATRIZ ESTRATÉGICA 2x2: VALOR vs QUALIDADE</span>
            <span class="sm:hidden">MATRIZ 2X2</span>
          </span>
          <span class="text-[11px] font-mono text-slate-700 bg-white border border-slate-200 px-3 py-0.5 rounded-full hidden md:inline font-medium shadow-2xs">
            Eixo X: <b class="text-slate-900" id="lbl-matrix-axis-x">P/L (0-25x)</b> | Eixo Y: <b class="text-slate-900">Score de Qualidade (20-100)</b>
          </span>
        </div>

        <div class="flex items-center gap-1.5 sm:gap-2.5 text-xs font-mono ml-auto">
          <!-- Botão de Atalho para Filtros no Celular -->
          <button type="button" onclick="scrollToMatrixFilters()" class="lg:hidden px-2.5 h-7 flex items-center gap-1 text-slate-700 bg-white border border-slate-200 rounded-lg text-xs font-medium hover:bg-slate-100 shadow-2xs cursor-pointer" title="Ver filtros da matriz">
            <span>⚙️ Filtros</span>
          </button>

          <!-- Zoom & Pan -->
          <div class="flex items-center gap-1">
            <button onclick="zoomMatrix(1.3)" class="w-7 h-7 flex items-center justify-center text-slate-700 hover:text-slate-900 bg-white border border-slate-200 rounded-lg font-bold transition hover:bg-slate-100 shadow-2xs cursor-pointer" title="Zoom +">+</button>
            <button onclick="zoomMatrix(0.77)" class="w-7 h-7 flex items-center justify-center text-slate-700 hover:text-slate-900 bg-white border border-slate-200 rounded-lg font-bold transition hover:bg-slate-100 shadow-2xs cursor-pointer" title="Zoom -">−</button>
            <button onclick="resetMatrixZoom()" class="px-2 sm:px-2.5 h-7 flex items-center gap-1 text-slate-700 hover:text-slate-900 bg-white border border-slate-200 rounded-lg text-xs font-medium transition hover:bg-slate-100 shadow-2xs cursor-pointer" title="Reset Zoom">
              <span>↺</span> <span id="matrixZoomLabel" class="hidden sm:inline">100%</span>
            </button>
          </div>
          <span id="matrixVisibleCount" class="hidden">0</span>

          <!-- Ação Rápida: Abrir Selecionada no Dossiê -->
          <button onclick="openSelectedInDossier()" class="px-2.5 sm:px-3.5 h-7 flex items-center gap-1.5 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded-lg text-xs transition shadow-sm cursor-pointer" title="Ver Dossiê da Empresa Selecionada">
            <span class="hidden sm:inline">Ver no Dossiê ➜</span>
            <span class="sm:hidden">Dossiê ➜</span>
          </button>
        </div>
      </div>

      <!-- Corpo da Matriz: Gráfico Amplo SVG + Painel Lateral de Filtros (Empilhado no Mobile, Lateral no Desktop) -->
      <div id="matrixMainWrapper" class="flex-1 flex flex-col lg:flex-row overflow-y-auto lg:overflow-hidden min-h-0 bg-white">
        
        <!-- ÁREA PRINCIPAL DO GRÁFICO (NO TOPO NO MOBILE, À DIREITA NO DESKTOP) -->
        <main id="matrixContainer" class="order-1 lg:order-2 relative w-full lg:flex-1 h-[340px] sm:h-[440px] lg:h-full bg-white flex-shrink-0 flex items-center justify-center select-none border-b lg:border-b-0">
          <svg id="matrixSvg" class="w-full h-full cursor-crosshair select-none touch-none" viewBox="0 0 1200 700">
            <!-- Renderizado dinamicamente via JS -->
          </svg>
          <div id="matrixTooltip" class="absolute pointer-events-none hidden bg-white/95 backdrop-blur-md rounded-xl p-3.5 text-xs text-slate-900 shadow-2xl z-50 font-mono border border-slate-300"></div>
        </main>

        <!-- SIDEBAR LATERAL DE FILTROS & CONFIGURAÇÕES (ABAIXO NO MOBILE, À ESQUERDA NO DESKTOP) -->
        <aside id="matrixSidebar" class="order-2 lg:order-1 w-full lg:w-72 xl:w-80 border-t lg:border-t-0 lg:border-r border-slate-200 bg-slate-50/70 p-3.5 flex flex-col gap-3.5 overflow-y-visible lg:overflow-y-auto flex-shrink-0 text-xs font-mono">
          
          <!-- Seção 1: Filtros da Matriz -->
          <div class="flex flex-col gap-1.5">
            <div class="flex items-center justify-between text-xs font-mono font-bold uppercase tracking-wider text-slate-700 px-1 mb-0.5">
              <span>Filtros da Matriz</span>
              <span class="text-[11px] font-normal text-slate-500">Plotados: <b class="text-emerald-700 font-bold" id="matrixPlotCount">--</b></span>
            </div>

            <!-- Botões Verticais de Filtro -->
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-1 gap-1.5">
              <button id="btn-mat-ALL" onclick="setMatrixFilter('ALL')" class="w-full flex items-center justify-between px-3 py-2 rounded-xl border border-slate-200 bg-white hover:bg-slate-100 text-slate-800 text-xs font-semibold transition cursor-pointer text-left shadow-2xs">
                <span class="flex items-center gap-2"><span>🌐</span><span>Todos os Ativos</span></span>
                <span class="bg-slate-100 text-slate-700 px-2 py-0.5 rounded-full text-[10px] font-bold" id="stat-mat-all">--</span>
              </button>

              <button id="btn-mat-CAT_TIER1" onclick="setMatrixFilter('CAT_TIER1')" class="w-full flex items-center justify-between px-3 py-2 rounded-xl border border-emerald-200 bg-white hover:bg-emerald-50 text-emerald-950 text-xs font-semibold transition cursor-pointer text-left shadow-2xs">
                <span class="flex items-center gap-2"><span>🏆</span><span>Wide Moat (Tier 1)</span></span>
                <span class="bg-emerald-100 text-emerald-900 px-2 py-0.5 rounded-full text-[10px] font-bold" id="stat-mat-tier1">--</span>
              </button>

              <button id="btn-mat-CAT_DISCOUNT" onclick="setMatrixFilter('CAT_DISCOUNT')" class="w-full flex items-center justify-between px-3 py-2 rounded-xl border border-emerald-200 bg-white hover:bg-emerald-50 text-emerald-950 text-xs font-semibold transition cursor-pointer text-left shadow-2xs">
                <span class="flex items-center gap-2"><span>🟢</span><span>Múltiplos Descontados</span></span>
                <span class="bg-emerald-100 text-emerald-900 px-2 py-0.5 rounded-full text-[10px] font-bold" id="stat-mat-discount">--</span>
              </button>

              <button id="btn-mat-CAT_NET_CASH" onclick="setMatrixFilter('CAT_NET_CASH')" class="w-full flex items-center justify-between px-3 py-2 rounded-xl border border-slate-200 bg-white hover:bg-slate-100 text-slate-800 text-xs font-semibold transition cursor-pointer text-left shadow-2xs">
                <span class="flex items-center gap-2"><span>🛡️</span><span>Caixa Líquido</span></span>
                <span class="bg-slate-100 text-slate-700 px-2 py-0.5 rounded-full text-[10px] font-bold" id="stat-mat-cash">--</span>
              </button>

              <button id="btn-mat-CAT_EXPANSION" onclick="setMatrixFilter('CAT_EXPANSION')" class="w-full flex items-center justify-between px-3 py-2 rounded-xl border border-teal-200 bg-white hover:bg-teal-50 text-teal-950 text-xs font-semibold transition cursor-pointer text-left shadow-2xs">
                <span class="flex items-center gap-2"><span>⚡</span><span>Lucro Acelerando</span></span>
                <span class="bg-teal-100 text-teal-900 px-2 py-0.5 rounded-full text-[10px] font-bold" id="stat-expansion">--</span>
              </button>

              <button id="btn-mat-CAT_DIVIDENDS" onclick="setMatrixFilter('CAT_DIVIDENDS')" class="w-full flex items-center justify-between px-3 py-2 rounded-xl border border-cyan-200 bg-white hover:bg-cyan-50 text-cyan-950 text-xs font-semibold transition cursor-pointer text-left shadow-2xs">
                <span class="flex items-center gap-2"><span>💰</span><span>Dividendos &gt; 6%</span></span>
                <span class="bg-cyan-100 text-cyan-900 px-2 py-0.5 rounded-full text-[10px] font-bold" id="stat-dividends">--</span>
              </button>

              <button id="btn-mat-CAT_SPREAD_NTNB" onclick="setMatrixFilter('CAT_SPREAD_NTNB')" class="w-full flex items-center justify-between px-3 py-2 rounded-xl border border-sky-200 bg-white hover:bg-sky-50 text-sky-950 text-xs font-semibold transition cursor-pointer text-left shadow-2xs">
                <span class="flex items-center gap-2"><span>📈</span><span>Prêmio Real NTN-B</span></span>
                <span class="bg-sky-100 text-sky-900 px-2 py-0.5 rounded-full text-[10px] font-bold" id="stat-mat-spread">--</span>
              </button>
            </div>
          </div>

          <!-- Seção 2: Parâmetros dos Eixos & Dimensões -->
          <div class="flex flex-col gap-2 pt-3 border-t border-slate-200">
            <span class="text-xs font-mono font-bold uppercase tracking-wider text-slate-700 px-1">Eixos &amp; Visualização</span>
            
            <div class="grid grid-cols-1 sm:grid-cols-3 lg:grid-cols-1 gap-2">
              <!-- Eixo X -->
              <div class="flex items-center justify-between bg-white p-2 rounded-xl border border-slate-200 shadow-2xs">
                <span class="text-[11px] text-slate-600 font-semibold">Métrica Eixo X:</span>
                <div class="inline-flex bg-slate-100 border border-slate-200 rounded-lg p-0.5">
                  <button type="button" id="btn-x-pl" onclick="switchMatrixX('pl')" class="px-2.5 py-0.5 rounded-md bg-amber-100 text-amber-900 font-bold border border-amber-300">P/L</button>
                  <button type="button" id="btn-x-ey" onclick="switchMatrixX('ey')" class="px-2.5 py-0.5 rounded-md text-slate-600 hover:text-slate-900 font-medium">EY%</button>
                </div>
              </div>

              <!-- Tamanho da Bolha -->
              <div class="flex items-center justify-between bg-white p-2 rounded-xl border border-slate-200 shadow-2xs">
                <span class="text-[11px] text-slate-600 font-semibold">Tamanho Bolha:</span>
                <select id="sel-bubble-metric" onchange="switchBubbleMetric(this.value)" class="bg-slate-50 border border-slate-200 rounded-lg px-2 py-1 text-slate-800 text-[11px] font-medium focus:outline-none cursor-pointer">
                  <option value="mcap">Valor Mercado</option>
                  <option value="volume">Volume Diário</option>
                  <option value="fixed">Fixo</option>
                </select>
              </div>

              <!-- Cor da Bolha -->
              <div class="flex items-center justify-between bg-white p-2 rounded-xl border border-slate-200 shadow-2xs">
                <span class="text-[11px] text-slate-600 font-semibold">Colorir por:</span>
                <select id="sel-bubble-color" onchange="switchBubbleColor(this.value)" class="bg-slate-50 border border-slate-200 rounded-lg px-2 py-1 text-slate-900 font-bold text-[11px] focus:outline-none cursor-pointer max-w-[140px]">
                  <option value="asymmetry" selected>Valuation</option>
                  <option value="quadrant">Quadrantes 2x2</option>
                  <option value="momentum">Momento 2T26</option>
                  <option value="dividend">Dividend Yield</option>
                  <option value="sector">Setores B3</option>
                </select>
              </div>
            </div>
          </div>

          <!-- Seção 3: Legenda Dinâmica -->
          <div class="flex flex-col gap-1.5 pt-3 border-t border-slate-200">
            <span class="text-xs font-mono font-bold uppercase tracking-wider text-slate-700 px-1">Legenda da Cor</span>
            <div id="matrixLegendContainer" class="flex flex-col gap-1.5 bg-white p-2.5 rounded-xl border border-slate-200 shadow-2xs">
              <!-- Legenda dinâmica inserida via JS -->
            </div>
          </div>

          <div class="text-[11px] text-slate-400 font-sans p-2 bg-slate-100/60 rounded-xl border border-slate-200/60 leading-tight">
            💡 <b>Dica:</b> Arraste para navegar (pan) e use os botões + e − para zoom. Toque na bolha para selecionar.
          </div>

        </aside>

      </div>
    </section>

    <!-- WORKSPACE 2: 🔍 SCANNER B3 & ATIVOS (TABELA FULL-WIDTH COM TOOLBAR INTEGRADA) -->
    <section id="view-table" class="hidden w-full space-y-4">
      
      <!-- TOOLBAR INTEGRADA E MINIMALISTA DO SCANNER B3 -->
      <div id="global-filters-toolbar" class="bg-white border border-slate-200 rounded-2xl p-3 flex flex-wrap items-center justify-between gap-3 shadow-xs">
        
        <!-- Esquerda: Presets Essenciais -->
        <div class="flex items-center gap-1.5 flex-wrap">
          <span class="text-xs font-mono text-slate-400 font-bold uppercase mr-1">Filtro:</span>
          
          <button onclick="setFilter('ALL')" id="flt-ALL" class="filter-btn active rounded-full px-3 py-1 text-xs font-mono font-medium hover:text-slate-900 cursor-pointer">
            Todos (<span id="cnt-ALL">--</span>)
          </button>
          
          <button onclick="setFilter('IBOV')" id="flt-IBOV" class="filter-btn rounded-full px-3 py-1 text-xs font-mono font-bold hover:text-slate-900 text-indigo-900 bg-indigo-50 border border-indigo-200 hover:bg-indigo-100 transition cursor-pointer flex items-center gap-1.5" title="Filtrar os 76 componentes oficiais do Ibovespa">
            <span class="w-1.5 h-1.5 rounded-full bg-indigo-600"></span>
            <span>Ibovespa</span>
            <span class="bg-indigo-200/70 text-indigo-950 px-1.5 py-0.2 rounded-full text-[10px]" id="cnt-IBOV">--</span>
          </button>

          <button onclick="setFilter('CAT_TIER1')" id="flt-CAT_TIER1" class="filter-btn rounded-full px-3 py-1 text-xs font-mono font-semibold hover:text-slate-900 text-slate-700 bg-slate-50 border border-slate-200 hover:bg-slate-100 transition cursor-pointer flex items-center gap-1.5" title="Empresas com Wide Moat (Tier 1: Score ≥ 80, ROIC/ROE elevado e balanço forte)">
            <span>🏆 Wide Moat (Tier 1)</span>
            <span class="text-slate-500 text-[10px]" id="cnt-TIER1">--</span>
          </button>

          <button onclick="setFilter('CAT_DIVIDENDS')" id="flt-CAT_DIVIDENDS" class="filter-btn rounded-full px-3 py-1 text-xs font-mono font-semibold hover:text-slate-900 text-slate-700 bg-slate-50 border border-slate-200 hover:bg-slate-100 transition cursor-pointer flex items-center gap-1.5" title="Dividend Yield > 6% com payout seguro">
            <span>💰 Dividendos > 6%</span>
            <span class="text-slate-500 text-[10px]" id="sb-cnt-div">--</span>
          </button>

          <button onclick="setFilter('CAT_NET_CASH')" id="flt-CAT_NET_CASH" class="filter-btn rounded-full px-3 py-1 text-xs font-mono font-semibold hover:text-slate-900 text-slate-700 bg-slate-50 border border-slate-200 hover:bg-slate-100 transition cursor-pointer flex items-center gap-1.5" title="Empresas com Caixa Líquido (Dívida zero)">
            <span>🛡️ Caixa Líquido</span>
            <span class="text-slate-500 text-[10px]" id="cnt-NET_CASH">--</span>
          </button>

          <!-- Seletor Rápido de Outras Categorias -->
          <div class="relative inline-flex items-center">
            <select id="secondaryCategorySelect" onchange="if(this.value) setFilter(this.value)" class="bg-slate-50 border border-slate-200 rounded-full px-3 py-1 text-xs text-slate-700 font-mono focus:outline-none focus:border-emerald-500 cursor-pointer">
              <option value="" disabled selected>+ Mais Filtros...</option>
              <option value="CAT_EXPANSION">⚡ Lucro Acelerando (Expansão 2T26)</option>
              <option value="CAT_DECELERATION">⚠️ Lucro em Retração (Desaceleração 2T26)</option>
              <option value="CAT_NET_CASH">🛡️ Caixa Líquido (Dívida Zero)</option>
              <option value="CAT_HIGH_DEBT">🚨 Alavancagem Alta (Crítica > 2.5x)</option>
              <option value="CAT_CLEAN_EARNINGS">💎 Lucro Limpo &amp; Recorrente</option>
              <option value="CAT_HIGH_ROIC">🏰 Super ROIC (≥ 18%)</option>
              <option value="CAT_GRAHAM">📐 Desconto Graham</option>
              <option value="CAT_SPREAD_NTNB">📈 Prêmio Real sobre NTN-B</option>
              <option value="CAT_ULTRA_CRITIC">🛡️ Máxima Solvência &amp; Resiliência</option>
              <option value="QUAD_ABOVE">✨ Acima da Curva (Desconto Valuation)</option>
              <option value="QUAD_BELOW">⚠️ Abaixo da Curva (Prêmio Valuation)</option>
            </select>
          </div>
        </div>

        <!-- Direita: Setor + Contadores + Critérios -->
        <div class="flex items-center gap-2.5 flex-wrap">
          <div class="flex items-center gap-1.5">
            <span class="text-xs font-mono text-slate-400 font-semibold uppercase">Setor:</span>
            <select id="sectorSelect" onchange="handleSectorChange(this.value)" class="bg-slate-50 border border-slate-200 rounded-full px-3 py-1 text-xs text-slate-800 font-mono focus:outline-none focus:border-emerald-500 cursor-pointer">
              <option value="ALL">Todos os Setores</option>
            </select>
          </div>

          <div class="h-4 w-px bg-slate-200 hidden sm:block"></div>

          <!-- Filtros de Qualidade Institucional (Compactos) -->
          <div class="hidden xl:flex items-center gap-2.5 text-xs font-mono text-slate-600">
            <label class="flex items-center gap-1 cursor-pointer select-none" data-tooltip="liq">
              <input type="checkbox" id="chkLiquidity1M" checked onchange="toggleGatekeeper()" class="w-3.5 h-3.5 rounded text-emerald-600 border-slate-300">
              <span class="text-[11px]">Liq ≥ 1M</span>
              <span class="info-badge cursor-pointer">ⓘ</span>
            </label>
            <label class="flex items-center gap-1 cursor-pointer select-none" data-tooltip="recency">
              <input type="checkbox" id="chkLatestBalance" checked onchange="toggleGatekeeper()" class="w-3.5 h-3.5 rounded text-emerald-600 border-slate-300">
              <span class="text-[11px]">2T26</span>
              <span class="info-badge cursor-pointer">ⓘ</span>
            </label>
            <label class="flex items-center gap-1 cursor-pointer select-none" data-tooltip="tag_along">
              <input type="checkbox" id="chkOnlyON" onchange="toggleGatekeeper()" class="w-3.5 h-3.5 rounded text-emerald-600 border-slate-300">
              <span class="text-[11px]">Só ON</span>
              <span class="info-badge cursor-pointer">ⓘ</span>
            </label>
          </div>

          <span class="text-xs font-mono font-bold text-emerald-800 bg-emerald-50 border border-emerald-200 px-2.5 py-0.5 rounded-full" id="tableCountBadge">-- ativos</span>
        </div>

      </div>

      <!-- BARRA DE CHIPS DE FILTRO ATIVO COM LIMPEZA RÁPIDA [✕] -->
      <div id="activeFilterChipsContainer" class="hidden flex items-center gap-2 flex-wrap text-xs font-mono py-1 px-1"></div>

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
            <span class="text-emerald-700 font-bold flex items-center gap-1 font-mono text-[10px]">
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span> Auditado 2T26
            </span>
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
          <div class="text-xs font-mono text-slate-500 hidden sm:block">
            💡 Clique em qualquer linha para abrir o <b class="text-slate-800">Dossiê 360°</b> ou na etiqueta para filtrar
          </div>
          <div class="sm:hidden text-[11px] font-mono text-emerald-950 bg-emerald-50/80 border border-emerald-200 px-2.5 py-1 rounded-lg flex items-center justify-between w-full">
            <span>👉 <b>Dica:</b> Deslize para o lado para ver todos os múltiplos</span>
            <span class="font-bold text-emerald-700">➔</span>
          </div>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full text-left border-collapse text-xs">
            <thead class="bg-[#F4F4F0] border-b border-[#E7E7E2] font-mono text-[#003836] uppercase text-[10.5px] font-bold tracking-wider">
              <tr>
                <th onclick="sortTable('ticker')" class="py-3 px-3 cursor-pointer hover:text-[#00A887] select-none" title="Ordenar por Ticker">Ativo / Empresa ↕</th>
                <th onclick="sortTable('cotacao')" class="py-3 px-2 text-right cursor-pointer hover:text-[#00A887] select-none" title="Ordenar por Cotação">Cotação ↕</th>
                <th onclick="sortTable('quality_score')" class="py-3 px-2 text-center cursor-pointer hover:text-[#00A887] select-none" title="Moat Score (0 a 100): Avaliação da largura e sustentabilidade do fosso econômico">Moat Score <span class="info-badge cursor-pointer" data-tooltip="quality_score">ⓘ</span> ↕</th>
                <th onclick="sortTable('pl')" class="py-3 px-2.5 text-right cursor-pointer hover:text-[#00A887] select-none" title="Ordenar por P/L Histórico &amp; Run-Rate">P/L (12M &amp; RR) <span class="info-badge cursor-pointer" data-tooltip="pl_ltm">ⓘ</span> ↕</th>
                <th onclick="sortTable('ev_ebitda')" class="py-3 px-2 text-right cursor-pointer hover:text-[#00A887] select-none" title="Múltiplo EV / EBITDA (Valor da Firma)">EV/EBITDA <span class="info-badge cursor-pointer" data-tooltip="ev_ebitda">ⓘ</span> ↕</th>
                <th onclick="sortTable('roic')" class="py-3 px-2 text-right cursor-pointer hover:text-[#00A887] select-none" title="Retorno sobre Capital Investido">ROIC <span class="info-badge cursor-pointer" data-tooltip="roic">ⓘ</span> ↕</th>
                <th onclick="sortTable('roe')" class="py-3 px-2 text-right cursor-pointer hover:text-[#00A887] select-none" title="Retorno sobre Patrimônio Líquido">ROE <span class="info-badge cursor-pointer" data-tooltip="roe">ⓘ</span> ↕</th>
                <th onclick="sortTable('div_yield')" class="py-3 px-2 text-right cursor-pointer hover:text-[#00A887] select-none" title="Ordenar por Dividend Yield">Div. Yield <span class="info-badge cursor-pointer" data-tooltip="payout">ⓘ</span> ↕</th>
                <th onclick="sortTable('div_liq_ebitda')" class="py-3 px-2 text-right cursor-pointer hover:text-[#00A887] select-none" title="Dívida Líquida / EBITDA (Alavancagem ou Caixa Líquido)">Dív. Líq. <span class="info-badge cursor-pointer" data-tooltip="debt">ⓘ</span> ↕</th>
                <th onclick="sortTable('ey_spread')" class="py-3 px-2.5 text-right cursor-pointer hover:text-[#00A887] select-none" title="Spread Real sobre a NTN-B 2035 (IPCA + 6,5% a.a.)">Spread NTN-B <span class="info-badge cursor-pointer" data-tooltip="ey_spread">ⓘ</span> ↕</th>
                <th class="py-3 px-3 text-[#003836] font-bold">Enquadramentos &amp; Momento</th>
              </tr>
            </thead>
            <tbody id="stocksTableBody" class="divide-y divide-[#E7E7E2] font-sans"></tbody>
          </table>
        </div>
      </div>

      <!-- Rodapé Regulatório Legal CVM -->
      <footer class="p-4 rounded-xl border border-slate-200 bg-slate-50 text-slate-600 text-xs leading-relaxed space-y-2">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-1 border-b border-slate-200/80 pb-1.5">
          <div class="font-mono font-bold text-slate-800 flex items-center gap-1.5 text-[11px]">
            <span>⚖️</span> AVISO DE CONFORMIDADE REGULATÓRIA (RESOLUÇÃO CVM Nº 20/2021)
          </div>
          <div class="flex items-center gap-3 text-[11px] font-mono">
            <a href="termos.html" class="text-slate-600 hover:text-emerald-700 underline underline-offset-2">Termos de Uso</a>
            <span>•</span>
            <a href="privacidade.html" class="text-slate-600 hover:text-emerald-700 underline underline-offset-2">Política de Privacidade</a>
          </div>
        </div>
        <p class="text-[11px] text-slate-500">
          As categorias, filtros quantitativos e notas fundamentalistas exibidos nesta plataforma decorrem de cálculos matemáticos objetivos e algoritmos públicos aplicados a dados contábeis auditados disponibilizados pela CVM e Fundamentus. 
          Este conteúdo tem caráter <b>exclusivamente educacional, de pesquisa e análise quantitativa independente</b>. 
          Não constitui oferta de compra ou venda de ativos, consultoria, recomendação de investimento ou relatório de análise na acepção da Resolução CVM nº 20/2021. 
          Decisões de investimento devem ser tomadas individualmente com base em juízo próprio de risco e adequação.
        </p>
        <div class="pt-1.5 border-t border-slate-200/60 flex flex-col sm:flex-row items-center justify-between text-[10px] font-mono text-slate-500 gap-1">
          <span>© 2026 MOAT TERMINAL • Todos os direitos reservados.</span>
          <span>Contato institucional: <a href="mailto:contato@moatterminal.com.br" class="hover:text-emerald-700 underline">contato@moatterminal.com.br</a></span>
        </div>
      </footer>

    </section>

  </main>
</div> <!-- Fechamento da coluna de conteúdo principal -->

<!-- SLIDE-OVER DRAWER PARA DOSSIÊ FUNDAMENTALISTA 360° -->
<div id="dossierDrawerBackdrop" onclick="closeDossierDrawer()" class="fixed inset-0 drawer-backdrop z-40 hidden transition-opacity duration-300"></div>
<aside id="dossierDrawer" class="fixed top-0 right-0 bottom-0 w-full sm:w-[580px] md:w-[640px] xl:w-[700px] bg-white border-l border-slate-200 z-50 shadow-2xl flex flex-col transform translate-x-full transition-transform duration-300 ease-in-out">
  <!-- Drawer Topbar -->
  <div class="p-4 border-b border-slate-200 bg-slate-50 flex items-center justify-between flex-shrink-0">
    <div class="flex items-center gap-2">
      <span class="w-2.5 h-2.5 rounded-full bg-emerald-400 shadow-md shadow-emerald-400/50"></span>
      <span class="font-mono font-bold text-xs text-slate-900 uppercase tracking-wider">Dossiê Fundamentalista 360°</span>
    </div>
    <div class="flex items-center gap-2">
      <button onclick="openDedicatedCompanyPage()" class="px-3 py-1.5 rounded-full text-[11px] font-mono text-white bg-emerald-600 hover:bg-emerald-700 transition cursor-pointer flex items-center gap-1.5 shadow-2xs font-semibold" title="Abrir página dedicada da empresa em tela cheia">
        <span>Página Completa ↗</span>
      </button>
      <button onclick="openSelectedInMatrix()" class="px-3 py-1.5 rounded-full text-[11px] font-mono text-slate-700 hover:text-slate-900 bg-white border border-slate-200 hover:border-slate-300 transition cursor-pointer flex items-center gap-1.5" title="Ver este ativo plotado na Matriz 2x2">
        <span><svg class="w-4 h-4 stroke-[1.75] inline-block text-emerald-700" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4 4v16h16M4 12h16M12 4v16"/></svg> Ver na Matriz</span>
      </button>
      <button onclick="closeDossierDrawer()" class="p-1 rounded-full text-slate-400 hover:text-slate-900 hover:bg-slate-100 text-sm font-bold transition px-2.5 cursor-pointer" title="Fechar (ESC)">✕</button>
    </div>
  </div>

  <!-- Header do Ativo Selecionado (Dossiê) -->
  <div class="p-4 border-b border-slate-200 bg-white/[0.01] flex-shrink-0" id="diagHeaderCard">
    <!-- Renderizado dinamicamente via renderDiagnosis() -->
  </div>

  <!-- Abas de Diagnóstico Segmentadas em Relevo -->
  <div class="flex border-b border-slate-200 text-xs font-mono font-medium bg-slate-100/80 flex-shrink-0 p-1.5 gap-1.5">
    <button onclick="switchDiagTab('radar')" id="dtab-radar" class="tab-btn active flex-1 py-1.5 rounded-lg text-center text-slate-900 bg-white font-bold shadow-xs border border-slate-200/90 transition cursor-pointer">
      Gauges &amp; Radar
    </button>
    <button onclick="switchDiagTab('history')" id="dtab-history" class="tab-btn flex-1 py-1.5 rounded-lg text-center text-slate-600 hover:text-slate-900 hover:bg-white/60 font-medium transition cursor-pointer">
      Histórico 5A
    </button>
    <button onclick="switchDiagTab('balance')" id="dtab-balance" class="tab-btn flex-1 py-1.5 rounded-lg text-center text-slate-600 hover:text-slate-900 hover:bg-white/60 font-medium transition cursor-pointer">
      Balanço &amp; DRE
    </button>
    <button onclick="switchDiagTab('sintese')" id="dtab-sintese" class="tab-btn flex-1 py-1.5 rounded-lg text-center text-slate-600 hover:text-slate-900 hover:bg-white/60 font-medium transition cursor-pointer">
      Síntese Contábil
    </button>
  </div>

  <!-- Conteúdo do Dossiê com Scroll Interno Próprio -->
  <div class="flex-1 overflow-y-auto p-4 flex flex-col gap-3.5">
    <!-- ABA 1: GAUGES & RADAR & KPIS -->
    <div id="dview-radar" class="flex flex-col gap-3.5">
      <!-- 3 GAUGES ANALÓGICOS BLOOMBERG -->
      <div class="glass-card rounded-xl p-4 border border-slate-200">
        <div class="text-[10px] font-mono font-bold uppercase tracking-wider text-slate-800 mb-2.5 flex items-center justify-between">
          <span>⚡ Indicadores Contábeis Auditados</span>
          <span class="text-[9px] text-slate-500 font-normal">100% Real • Fundamentus</span>
        </div>
        <div class="grid grid-cols-3 gap-1">
          <div class="flex flex-col items-center justify-center">
            <svg id="gaugeRoe" class="w-full h-[88px]" viewBox="0 0 160 92"></svg>
          </div>
          <div class="flex flex-col items-center justify-center border-x border-slate-200 px-1">
            <svg id="gaugeDebt" class="w-full h-[88px]" viewBox="0 0 160 92"></svg>
          </div>
          <div class="flex flex-col items-center justify-center">
            <svg id="gaugeSpread" class="w-full h-[88px]" viewBox="0 0 160 92"></svg>
          </div>
        </div>
      </div>

      <!-- RADAR PENTAGONAL DE 5 PILARES (ESTILO SIMPLY WALL ST) -->
      <div class="glass-card rounded-xl p-4 flex flex-col gap-3 border border-slate-200">
        <div class="text-[10px] font-mono font-bold uppercase tracking-wider text-emerald-800 flex items-center justify-between">
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

    <!-- ABA 4: SÍNTESE FUNDAMENTALISTA DE BALANÇO -->
    <div id="dview-sintese" class="hidden flex flex-col gap-3 text-xs">
      <div id="sinteseStatusBanner"></div>
      <div id="sinteseFlagsContainer" class="flex flex-wrap gap-1"></div>
      <div id="sinteseBulletsList" class="flex flex-col gap-2.5"></div>
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
    let currentPortfolioKey = 'CAT_TIER1'; // 'munger', 'dividends', 'asymmetry', 'cfa_ultra'
    let currentSimulatedCapital = 50000;

    // Estado da Matriz Interativa (Zoom, Pan, 3ª Dimensão)
    let matrixBubbleMetric = 'mcap'; // 'fixed', 'mcap', 'volume'
    let matrixColorMode = 'asymmetry'; // 'asymmetry', 'momentum', 'dividend', 'sector', 'relative'
    let matrixZoom = 1.0;
    let matrixCenterX = 12.5;
    let matrixCenterY = 60.0;
    let isPanning = false;
    let panStartX = 0;
    let panStartY = 0;
    let panStartCenterX = 12.5;
    let panStartCenterY = 60.0;
    let hasMovedDuringPan = false;

    // Curva Munger Compounder Pró-Qualidade:
    // P/L Teórico = 3.5 + 20.0 * ((Quality - 20) / 80) ^ 1.6
    function calcFairPL(qualityScore) {{
      const q = Math.max(20.0, Math.min(100.0, qualityScore || 50.0));
      const norm = (q - 20.0) / 80.0;
      return 3.5 + 20.0 * Math.pow(norm, 1.6);
    }}

    // Inicialização do cabeçalho
    function updateHeaderInfo() {{
      const ts = document.getElementById('auditTimestamp');
      if (ts) ts.innerText = 'Auditado em: ' + APP_DATA.audit_timestamp;
      const bdt = document.getElementById('badgeUpdateDateTime');
      if (bdt) {{
        let dStr = '29/09/2026';
        if (APP_DATA.audit_timestamp) {{
          dStr = APP_DATA.audit_timestamp.split(' ')[0];
        }}
        bdt.innerText = dStr + ' às 07:00 BRT';
      }}
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

    
    // BIBLIOTECA DE ÍCONES MINIMALISTAS EM TRAÇO ARABESCO (SVG LINE ICONS)
    const APP_ICONS = {{
      home: '<svg class="w-4 h-4 stroke-[1.75] inline-block" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>',
      briefcase: '<svg class="w-4 h-4 stroke-[1.75] inline-block" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M20 7h-4V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v3H4a2 2 0 00-2 2v11a2 2 0 002 2h16a2 2 0 002-2V9a2 2 0 00-2-2zM10 4h4v3h-4V4zM4 9h16v3.5a1.5 1.5 0 01-1.5 1.5h-13A1.5 1.5 0 014 12.5V9z"/></svg>',
      search: '<svg class="w-4 h-4 stroke-[1.75] inline-block" fill="none" stroke="currentColor" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-4.35-4.35"/></svg>',
      matrix: '<svg class="w-4 h-4 stroke-[1.75] inline-block" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4 4v16h16M4 12h16M12 4v16"/></svg>',
      trophy: '<svg class="w-4 h-4 stroke-[1.75] inline-block text-amber-700" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M8 21h8m-4-4v4m-6-13a4 4 0 008 0V4H6v4zm0 0H4a2 2 0 00-2 2v1a3 3 0 003 3h1m8-6h2a2 2 0 012 2v1a3 3 0 01-3 3h-1"/></svg>',
      diamond: '<svg class="w-4 h-4 stroke-[1.75] inline-block text-amber-700" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M6 3h12l4 6-10 12L2 9l4-6z"/></svg>',
      chartUp: '<svg class="w-4 h-4 stroke-[1.75] inline-block text-sky-700" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/></svg>',
      chartDown: '<svg class="w-4 h-4 stroke-[1.75] inline-block text-amber-700" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M13 17h8m0 0V9m0 8l-8-8-4 4-6-6"/></svg>',
      dividend: '<svg class="w-4 h-4 stroke-[1.75] inline-block text-emerald-700" fill="none" stroke="currentColor" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path stroke-linecap="round" stroke-linejoin="round" d="M12 7v10m-3-7.5a2.5 2.5 0 015 0c0 2-3 2-3 4h3"/></svg>',
      shield: '<svg class="w-4 h-4 stroke-[1.75] inline-block text-indigo-700" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
      zap: '<svg class="w-4 h-4 stroke-[1.75] inline-block text-teal-700" fill="none" stroke="currentColor" viewBox="0 0 24 24"><polygon stroke-linecap="round" stroke-linejoin="round" points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>',
      alert: '<svg class="w-3.5 h-3.5 stroke-[1.75] inline-block text-amber-700 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 9v4m0 4h.01M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/></svg>',
      alertRose: '<svg class="w-3.5 h-3.5 stroke-[1.75] inline-block text-rose-700 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 9v4m0 4h.01M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/></svg>',
      check: '<svg class="w-3.5 h-3.5 stroke-[2] inline-block text-emerald-700 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg>',
      building: '<svg class="w-4 h-4 stroke-[1.75] inline-block text-slate-700 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 21h18M5 21V5a2 2 0 012-2h10a2 2 0 012 2v16M9 9h1m4 0h1M9 13h1m4 0h1M9 17h1m4 0h1"/></svg>',
      fileText: '<svg class="w-4 h-4 stroke-[1.75] inline-block text-slate-700 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline stroke-linecap="round" stroke-linejoin="round" points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>',
      scale: '<svg class="w-4 h-4 stroke-[1.75] inline-block text-indigo-700 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 3v18m-7-5l7-13 7 13M5 16h14M3 19h4m10 0h4"/></svg>',
      calendar: '<svg class="w-3.5 h-3.5 stroke-[1.75] inline-block text-slate-600 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>',
      tag: '<svg class="w-3.5 h-3.5 stroke-[1.75] inline-block text-slate-600 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M20.59 13.41l-7.17 7.17a2 2 0 01-2.83 0L2 12V2h10l8.59 8.59a2 2 0 010 2.82z"/><line x1="7" y1="7" x2="7.01" y2="7"/></svg>'
    }};

    // HELPER PARA LOGOTIPO OFICIAL DE ATIVOS B3 COM FALLBACK GRACIOSO
    function getStockLogoHtml(ticker, companyName, sizeClass = 'w-7 h-7') {{
      if (!ticker) return '';
      const cleanTicker = ticker.trim().toUpperCase();
      const initials = cleanTicker.slice(0, 2);
      const logoUrl = `https://raw.githubusercontent.com/thefintz/icones-b3/main/icones/${{cleanTicker}}.png`;
      
      return `
        <div class="${{sizeClass}} rounded-lg bg-white border border-slate-200/90 flex-shrink-0 flex items-center justify-center p-0.5 shadow-xs overflow-hidden relative" title="${{cleanTicker}}">
          <img src="${{logoUrl}}" 
               alt="${{cleanTicker}}" 
               loading="lazy"
               class="w-full h-full object-contain"
               onerror="this.style.display='none'; if(this.nextElementSibling) this.nextElementSibling.style.display='flex';" />
          <div style="display:none;" class="w-full h-full bg-slate-100 text-slate-800 font-mono text-[10px] font-bold items-center justify-center select-none">
            ${{initials}}
          </div>
        </div>
      `;
    }}

    function formatMultiple(v) {{
      if (v === null || v === undefined) return 'N/D';
      return Number(v).toFixed(2) + 'x';
    }}

    // HIERARQUIA UNIVERSAL DE CORES SEMÂNTICAS (VERDE, VERMELHO, AMARELO, AZUL)
    function getColorSpread(val) {{
      if (val === null || val === undefined) return 'text-slate-500';
      if (val >= 2.0) return 'text-emerald-700 font-bold';
      if (val >= 0.0) return 'text-amber-800 font-semibold';
      return 'text-rose-700 font-bold';
    }}

    function getColorRoic(val, isFin = false) {{
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
    }}

    function getColorPl(val) {{
      if (val === null || val === undefined) return 'text-slate-500';
      if (val < 0) return 'text-rose-700 font-bold';
      if (val <= 12.0) return 'text-emerald-800 font-semibold';
      if (val <= 22.0) return 'text-slate-700 font-medium';
      return 'text-amber-800 font-medium';
    }}

    function getColorDy(val) {{
      if (val === null || val === undefined) return 'text-slate-500';
      const num = Math.abs(val) < 2.0 ? val * 100 : val;
      if (num >= 6.0) return 'text-emerald-700 font-bold';
      if (num >= 3.0) return 'text-slate-700 font-medium';
      if (num > 0) return 'text-slate-600 font-normal';
      return 'text-slate-500';
    }}

    function getColorDebt(val, isFin = false) {{
      if (isFin) return 'text-indigo-800 font-medium';
      if (val === null || val === undefined) return 'text-slate-500';
      if (val < 0) return 'text-emerald-800 font-semibold';
      if (val <= 1.5) return 'text-emerald-800 font-semibold';
      if (val <= 2.7) return 'text-amber-800 font-medium';
      return 'text-rose-700 font-bold';
    }}

    function getColorMrgLiq(val) {{
      if (val === null || val === undefined) return 'text-slate-500';
      const num = Math.abs(val) < 2.0 ? val * 100 : val;
      if (num >= 12.0) return 'text-emerald-800 font-semibold';
      if (num >= 4.0) return 'text-slate-700 font-medium';
      if (num >= 0) return 'text-amber-800 font-medium';
      return 'text-rose-700 font-bold';
    }}

    function getColorAcidTest(val) {{
      if (val === null || val === undefined) return 'text-slate-500';
      const num = Math.abs(val) < 2.0 ? val * 100 : val;
      if (num >= 75.0) return 'text-emerald-800 font-semibold';
      if (num >= 60.0) return 'text-amber-800 font-medium';
      return 'text-rose-700 font-bold';
    }}

    function getFilteredStocks() {{
      const require1M = document.getElementById('chkLiquidity1M') ? document.getElementById('chkLiquidity1M').checked : true;
      const requireLatestBal = document.getElementById('chkLatestBalance') ? document.getElementById('chkLatestBalance').checked : true;
      const requireRecurring = document.getElementById('chkFilterDistortions') ? document.getElementById('chkFilterDistortions').checked : false;
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

        // Presets Munger / Moat Terminal
        if (currentFilter === 'ALL') return true;
        if (currentFilter === 'IBOV') return !!s.is_ibov;
        if (currentFilter === 'TIER1' || currentFilter === 'CAT_TIER1') return s.quality_score >= 80.0;
        if (currentFilter === 'DIVIDENDS' || currentFilter === 'CAT_DIVIDENDS') {{
          return (s.div_yield !== null && s.div_yield >= 0.05) || getStockCategories(s).some(c => c.id === 'CAT_DIVIDENDS');
        }}
        if (currentFilter === 'NET_CASH' || currentFilter === 'CAT_NET_CASH') {{
          return (s.div_liq_ebitda !== null && s.div_liq_ebitda < 0) || (s.details && s.details.divida_liquida !== null && s.details.divida_liquida <= 0);
        }}
        if (currentFilter === 'ASYMMETRY') return s.quality_score >= 75.0 && s.pl > 0 && s.pl < 8.0;
        if (currentFilter === 'NTNB' || currentFilter === 'CAT_SPREAD_NTNB') return s.ey_spread !== null && s.ey_spread >= 5.0;
        if (currentFilter === 'CAT_EXPANSION') return s.run_rate_div_pct !== null && s.run_rate_div_pct >= 15.0;
        if (currentFilter === 'CAT_DECELERATION') return s.run_rate_div_pct !== null && s.run_rate_div_pct <= -20.0;
        if (currentFilter === 'CAT_HIGH_DEBT') return s.div_liq_ebitda !== null && s.div_liq_ebitda > 2.5 && !s.is_financial;
        if (currentFilter === 'CAT_CLEAN_EARNINGS') return !s.is_distorted && (s.years_consecutive_profit >= 5 || !s.has_loss_history);
        if (currentFilter === 'CAT_HIGH_ROIC') return (s.roic !== null && s.roic >= 0.18) || (s.is_financial && s.roe >= 0.18);
        if (currentFilter === 'CAT_FINANCIAL') return !!s.is_financial;
        if (currentFilter === 'CAT_GRAHAM') {{
          const lpa = (s.details && s.details.lpa) ? Number(s.details.lpa) : null;
          const vpa = (s.details && s.details.vpa) ? Number(s.details.vpa) : null;
          const cot = Number(s.cotacao);
          if (lpa && vpa && lpa > 0 && vpa > 0 && cot > 0) {{
            return Math.sqrt(22.5 * lpa * vpa) > cot * 1.15;
          }}
          return false;
        }}

        // 0. Categoria Ultra-Crítica (Régua Máxima Munger: Qualidade & Solvência)
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

        // Filtro Estratégico: Múltiplos Descontados
        if (currentFilter === 'CAT_DISCOUNT') {{
          return s.entry_tag === 'ASSIMETRIA_FAVORAVEL';
        }}

        // Filtros dos Quadrantes 2x2
        if (currentFilter === 'QUAD_Q1') {{
          return (s.quality_score || 0) >= 75 && (s.pl !== null && s.pl > 0 && s.pl <= 14.0);
        }}
        if (currentFilter === 'QUAD_Q2') {{
          return (s.quality_score || 0) >= 75 && (s.pl !== null && s.pl > 14.0);
        }}
        if (currentFilter === 'QUAD_Q3') {{
          return (s.quality_score || 0) < 75 && (s.pl !== null && s.pl > 0 && s.pl <= 14.0);
        }}
        if (currentFilter === 'QUAD_Q4') {{
          return (s.quality_score || 0) < 75 && (s.pl !== null && s.pl > 14.0);
        }}

        // Compatibilidade retroativa para filtros de quadrante
        if (currentFilter === 'QUAD_ABOVE' || currentFilter === 'QUAD_FILE' || currentFilter === 'QUAD_BARGAIN') {{
          return (s.quality_score || 0) >= 75 && (s.pl !== null && s.pl > 0 && s.pl <= 14.0);
        }}
        if (currentFilter === 'QUAD_BELOW' || currentFilter === 'QUAD_EXPENSIVE' || currentFilter === 'QUAD_TRAP') {{
          return (s.quality_score || 0) < 75 || (s.pl !== null && s.pl > 14.0);
        }}

        // Enquadramentos / Categorias Institucionais Padronizadas
        if (currentFilter.startsWith('CAT_')) {{
          const cats = getStockCategories(s);
          return cats.some(c => c.id === currentFilter);
        }}
        return true;
      }});
    }}

    // Rótulos e Categorias Institucionais Munger da Ação (Até 5 por ativo)
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
            label: 'Alavancagem Alta (Crítica > 2.5x)',
            shortLabel: 'Alavancagem Alta',
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
            label: 'Lucro Acelerando (Expansão 2T26)',
            shortLabel: 'Lucro Acelerando',
            icon: '⚡',
            bgClass: 'bg-emerald-50 text-emerald-950 border border-emerald-300 font-semibold'
          }});
        }} else if (s.run_rate_div_pct <= -20.0 && s.pl_run_rate > s.pl * 1.25) {{
          cats.push({{
            id: 'CAT_DECELERATION',
            label: 'Lucro em Retração (Desaceleração 2T26)',
            shortLabel: 'Lucro em Retração',
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
          label: 'Wide Moat (Tier 1)',
          shortLabel: 'Wide Moat (Tier 1)',
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
          label: 'Dividendos Consistentes (> 6%)',
          shortLabel: 'Dividendos > 6%',
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
            label: 'Referência Décio Bazin (DY 6%)',
            shortLabel: 'Ref. Bazin',
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
    }}

    function updateFilterCounts() {{
      const require1M = document.getElementById('chkLiquidity1M') ? document.getElementById('chkLiquidity1M').checked : true;
      const requireLatestBal = document.getElementById('chkLatestBalance') ? document.getElementById('chkLatestBalance').checked : true;
      const requireRecurring = document.getElementById('chkFilterDistortions') ? document.getElementById('chkFilterDistortions').checked : false;
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

      const filteredCount = getFilteredStocks().length;
      const elDisp = document.getElementById('displayedCount');
      if (elDisp) elDisp.innerText = filteredCount;
      const elBadge = document.getElementById('tableCountBadge');
      if (elBadge) elBadge.innerText = filteredCount + ' ativos';
      const elCntAll = document.getElementById('cnt-ALL');
      if (elCntAll) elCntAll.innerText = basePool.length;
      const elIbov = document.getElementById('cnt-IBOV'); if (elIbov) elIbov.innerText = basePool.filter(s => s.is_ibov).length;
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

      const cntT1 = basePool.filter(s => getStockCategories(s).some(c => c.id === 'CAT_TIER1')).length;
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
      if (sbSpread) sbSpread.innerText = cntSpread;

      const sbUniv = document.getElementById('sidebarUniverseCount');
      if (sbUniv) sbUniv.innerText = basePool.length + ' ativos';

      // Atualizar contadores da Matriz e Filtros Estratégicos
      const cntDiscount = basePool.filter(s => s.entry_tag === 'ASSIMETRIA_FAVORAVEL').length;
      const cntExpansion = basePool.filter(s => s.run_rate_div_pct && s.run_rate_div_pct >= 15.0).length;
      const cntDivs = basePool.filter(s => s.div_yield && s.div_yield >= 0.05).length;

      const elDiscount = document.getElementById('stat-mat-discount');
      if (elDiscount) elDiscount.innerText = cntDiscount;
      const elMatSpread = document.getElementById('stat-mat-spread');
      if (elMatSpread) elMatSpread.innerText = cntSpread;
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
      }}
    }}

    function updateSectorDropdown() {{
      const select = document.getElementById('sectorSelect');
      if (!select) return;

      const require1M = document.getElementById('chkLiquidity1M') ? document.getElementById('chkLiquidity1M').checked : true;
      const requireLatestBal = document.getElementById('chkLatestBalance') ? document.getElementById('chkLatestBalance').checked : true;
      const requireRecurring = document.getElementById('chkFilterDistortions') ? document.getElementById('chkFilterDistortions').checked : false;
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

      let html = `<option value="ALL">Todos os Setores (Geral) (${{qualified.length}})</option>`;
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

    function goToHome() {{
      closeDossierDrawer();
      switchWorkspace('home');
      const ws = document.getElementById('workspaceContainer');
      if (ws) ws.scrollTo({{ top: 0, behavior: 'smooth' }});
      window.scrollTo({{ top: 0, behavior: 'smooth' }});
    }}

    function setFilter(f) {{
      currentFilter = f;
      document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
      const activeBtn = document.getElementById('flt-' + f);
      if (activeBtn) activeBtn.classList.add('active');
      const secSel = document.getElementById('secondaryCategorySelect');
      if (secSel) {{
        const hasOpt = Array.from(secSel.options).some(o => o.value === f);
        secSel.value = hasOpt ? f : '';
      }}
      renderActiveFilterChips();
      render();
    }}

    function handleSearch() {{
      const inp = document.getElementById('searchInput');
      if (inp) handleSearchInput(inp.value);
    }}

    // ==========================================
    // 🔍 BUSCA PREDITIVA COM AUTOCOMPLETE FLUTUANTE
    // ==========================================
    let searchHighlightedIndex = -1;
    let currentSearchResults = [];

    function handleSearchInput(val) {{
      searchQuery = val.trim();
      const dd = document.getElementById('searchDropdown');
      if (!val || val.trim().length === 0) {{
        if (dd) dd.classList.add('hidden');
        currentSearchResults = [];
        searchHighlightedIndex = -1;
        renderActiveFilterChips();
        render();
        return;
      }}

      const q = val.trim().toLowerCase();
      // Classificar e pontuar correspondências
      const scored = APP_DATA.stocks.map(s => {{
        const t = s.ticker.toLowerCase();
        const emp = (s.empresa || '').toLowerCase();
        const set = (s.setor || '').toLowerCase();
        let score = -1;
        if (t === q) score = 1000;
        else if (t.startsWith(q)) score = 500 + (t.length - q.length);
        else if (t.includes(q)) score = 300;
        else if (emp.startsWith(q)) score = 200;
        else if (emp.includes(q)) score = 100;
        else if (set.includes(q)) score = 50;

        if (score > 0) score += (s.quality_score || 0) / 10;
        return {{ stock: s, score }};
      }}).filter(item => item.score > 0)
        .sort((a, b) => b.score - a.score)
        .map(item => item.stock);

      currentSearchResults = scored.slice(0, 8);
      searchHighlightedIndex = currentSearchResults.length > 0 ? 0 : -1;
      renderSearchDropdown();
      renderActiveFilterChips();

      if (currentWorkspace === 'table') {{
        renderTable();
      }}
    }}

    function handleSearchFocus() {{
      const inp = document.getElementById('searchInput');
      if (inp && inp.value.trim().length > 0) {{
        handleSearchInput(inp.value);
      }}
    }}

    function renderSearchDropdown() {{
      const dd = document.getElementById('searchDropdown');
      if (!dd) return;

      if (currentSearchResults.length === 0) {{
        dd.innerHTML = `
          <div class="p-4 text-center text-xs font-mono text-slate-500">
            <span>🔍</span> Nenhum ativo encontrado para "${{searchQuery}}"
          </div>
        `;
        dd.classList.remove('hidden');
        return;
      }}

      dd.innerHTML = `
        <div class="p-2 bg-slate-50 border-b border-slate-100 flex items-center justify-between text-[10px] font-mono text-slate-500">
          <span>${{currentSearchResults.length}} sugestões encontradas</span>
          <span>Navegue com <b>↑</b> <b>↓</b> e <b>Enter</b></span>
        </div>
        ${{currentSearchResults.map((s, idx) => {{
          const isHigh = idx === searchHighlightedIndex;
          const bg = isHigh ? 'bg-emerald-50/90 border-l-4 border-emerald-600' : 'hover:bg-slate-50';
          const scoreClass = s.quality_score >= 80 ? 'bg-emerald-100 text-emerald-950 border border-emerald-300' : (s.quality_score >= 65 ? 'bg-amber-100 text-amber-950 border border-amber-300' : 'bg-slate-100 text-slate-700 border border-slate-300');
          const plStr = (s.pl && s.pl > 0) ? s.pl.toFixed(1) + 'x' : 'N/D';
          const dyStr = s.div_yield ? (s.div_yield * 100).toFixed(1) + '%' : '0%';

          return `
            <div onclick="selectSearchStock('${{s.ticker}}')" class="p-2.5 ${{bg}} transition cursor-pointer flex items-center justify-between select-none">
              <div class="flex items-center gap-2.5 min-w-0">
                ${{getStockLogoHtml(s.ticker, s.empresa, 'w-7 h-7')}}
                <div class="flex flex-col min-w-0">
                  <div class="flex items-center gap-1.5 leading-none">
                    <span class="font-bold text-slate-900 font-mono text-xs">${{s.ticker}}</span>
                    <span class="text-[9px] px-1 py-0.2 rounded font-mono font-bold ${{s.is_latest_balanco ? 'bg-emerald-50 text-emerald-800 border border-emerald-200' : 'bg-slate-100 text-slate-600'}}">${{s.tri_balanco || '2T26'}}</span>
                  </div>
                  <div class="text-[11px] text-slate-700 font-sans font-medium truncate max-w-[150px] mt-0.5">${{s.empresa}}</div>
                  <div class="text-[9px] text-slate-400 font-sans truncate max-w-[150px]">${{s.setor}}</div>
                </div>
              </div>
              <div class="flex flex-col items-end gap-1 flex-shrink-0">
                <div class="flex items-center gap-1">
                  <span class="text-xs font-mono font-bold text-slate-900">${{formatCurrency(s.cotacao)}}</span>
                  <span class="text-[9.5px] font-mono font-bold px-1.5 py-0.2 rounded-full ${{scoreClass}}">${{s.quality_score.toFixed(0)}} pts</span>
                </div>
                <div class="text-[10px] font-mono text-slate-500">
                  P/L: <b class="text-slate-800">${{plStr}}</b> • DY: <b class="text-emerald-700">${{dyStr}}</b>
                </div>
              </div>
            </div>
          `;
        }}).join('')}}
      `;
      dd.classList.remove('hidden');
    }}

    function handleSearchKeydown(e) {{
      const dd = document.getElementById('searchDropdown');
      if (!dd || dd.classList.contains('hidden') || currentSearchResults.length === 0) {{
        if (e.key === 'Escape') {{
          clearSearchFilter();
          if (dd) dd.classList.add('hidden');
        }}
        return;
      }}

      if (e.key === 'ArrowDown') {{
        e.preventDefault();
        searchHighlightedIndex = (searchHighlightedIndex + 1) % currentSearchResults.length;
        renderSearchDropdown();
      }} else if (e.key === 'ArrowUp') {{
        e.preventDefault();
        searchHighlightedIndex = (searchHighlightedIndex - 1 + currentSearchResults.length) % currentSearchResults.length;
        renderSearchDropdown();
      }} else if (e.key === 'Enter') {{
        e.preventDefault();
        if (searchHighlightedIndex >= 0 && searchHighlightedIndex < currentSearchResults.length) {{
          selectSearchStock(currentSearchResults[searchHighlightedIndex].ticker);
        }}
      }} else if (e.key === 'Escape') {{
        dd.classList.add('hidden');
      }}
    }}

    function selectSearchStock(ticker) {{
      const dd = document.getElementById('searchDropdown');
      if (dd) dd.classList.add('hidden');
      selectTicker(ticker);
      openDossierDrawer(ticker);
    }}

    function clearSearchFilter() {{
      searchQuery = '';
      const inp = document.getElementById('searchInput');
      if (inp) inp.value = '';
      const dd = document.getElementById('searchDropdown');
      if (dd) dd.classList.add('hidden');
      renderActiveFilterChips();
      render();
    }}

    // =========================================================================
    // METADADOS E DESCRIÇÕES DOS FILTROS & CATEGORIAS (BASE COMPLETA)
    // =========================================================================
    const BASE_FILTER_META = {{
      'ALL': {{
        name: 'Universo Geral B3',
        icon: '🌐',
        rationale: 'Todas as empresas da B3 com liquidez diária negociada ≥ R$ 1 Milhão e balanço trimestral mais recente auditado pela CVM.'
      }},
      'IBOV': {{
        name: 'Componentes do Ibovespa',
        icon: '🇧🇷',
        rationale: 'Os ativos de maior liquidez e representatividade no mercado financeiro brasileiro, que compõem a carteira teórica oficial do Ibovespa.'
      }},
      'TIER1': {{
        name: 'Wide Moat (Tier 1)',
        icon: '🏆',
        rationale: 'Empresas de alta rentabilidade sobre capital (ROIC/ROE elevado), barreiras de entrada comprovadas, sólida alocação de capital e Moat Score ≥ 80.'
      }},
      'CAT_TIER1': {{
        name: 'Wide Moat (Tier 1)',
        icon: '🏆',
        rationale: 'Empresas de alta rentabilidade sobre capital (ROIC/ROE elevado), barreiras de entrada comprovadas, sólida alocação de capital e Moat Score ≥ 80.'
      }},
      'CAT_DIVIDENDS': {{
        name: 'Dividendos Consistentes (> 6%)',
        icon: '💰',
        rationale: 'Ações com Dividend Yield superior a 5%-6% ao ano, balanços saudáveis e fluxo de proventos sustentável dentro do payout seguro.'
      }},
      'DIVIDENDS': {{
        name: 'Dividendos Consistentes (> 6%)',
        icon: '💰',
        rationale: 'Ações com Dividend Yield superior a 5%-6% ao ano, balanços saudáveis e fluxo de proventos sustentável dentro do payout seguro.'
      }},
      'CAT_NET_CASH': {{
        name: 'Caixa Líquido (Dívida Zero)',
        icon: '🛡️',
        rationale: 'Empresas não-financeiras cujas disponibilidades financeiras superam a totalidade de suas dívidas brutas (Dívida Líquida ≤ 0).'
      }},
      'NET_CASH': {{
        name: 'Caixa Líquido (Dívida Zero)',
        icon: '🛡️',
        rationale: 'Empresas não-financeiras cujas disponibilidades financeiras superam a totalidade de suas dívidas brutas (Dívida Líquida ≤ 0).'
      }},
      'CAT_EXPANSION': {{
        name: 'Lucro Acelerando (Expansão 2T26)',
        icon: '⚡',
        rationale: 'Empresas cujo lucro run-rate anualizado do trimestre mais recente supera em mais de 15% o lucro histórico dos últimos 12 meses (LTM).'
      }},
      'CAT_DECELERATION': {{
        name: 'Lucro em Retração (Desaceleração 2T26)',
        icon: '⚠️',
        rationale: 'Empresas cujo lucro run-rate anualizado do trimestre mais recente recuou mais de 20% frente à média dos últimos 12 meses.'
      }},
      'CAT_HIGH_DEBT': {{
        name: 'Alavancagem Alta (Crítica > 2.5x)',
        icon: '🚨',
        rationale: 'Empresas não-financeiras com relação Dívida Líquida / EBITDA superior a 2,5x sob ambiente de Selic elevada.'
      }},
      'CAT_CLEAN_EARNINGS': {{
        name: 'Lucro Limpo & Recorrente',
        icon: '💎',
        rationale: 'Histórico auditado de 5 anos consecutivos sem prejuízos ou distorções contábeis extraordinárias nos últimos períodos.'
      }},
      'CAT_HIGH_ROIC': {{
        name: 'Super ROIC (≥ 18%)',
        icon: '🏰',
        rationale: 'Retorno sobre o Capital Investido superior a 18%, sinalizando fossos econômicos profundos e capacidade de reinvestimento acelerado.'
      }},
      'CAT_FINANCIAL': {{
        name: 'Intermediação Financeira (Bancos)',
        icon: '🏛️',
        rationale: 'Grandes instituições financeiras com sólida rentabilidade sobre o patrimônio líquido (ROE) e conformidade com o Índice de Basileia.'
      }},
      'CAT_GRAHAM': {{
        name: 'Desconto Fórmula de Graham',
        icon: '📐',
        rationale: 'Ações sendo negociadas com desconto superior a 15% em relação ao Valor Intrínseco clássico de Benjamin Graham (√(22.5 * LPA * VPA)).'
      }},
      'CAT_SPREAD_NTNB': {{
        name: 'Prêmio Real sobre NTN-B',
        icon: '📈',
        rationale: 'Empresas cujo Earnings Yield (Inverso do P/L) oferece um prêmio real atrativo (spread positivo) acima da taxa real do Tesouro IPCA+.'
      }},
      'CAT_ULTRA_CRITIC': {{
        name: 'Máxima Solvência & Resiliência',
        icon: '🛡️',
        rationale: 'Régua máxima inspirada em Charlie Munger: Moat Score ≥ 75, sem distorções contábeis, ROIC/ROE alto, caixa sólido e spread favorável.'
      }},
      'QUAD_ABOVE': {{
        name: 'Acima da Curva (Desconto Valuation)',
        icon: '✨',
        rationale: 'Ativos cujo múltiplo P/L atual situa-se abaixo da curva teórica de valuation para o seu respectivo Moat Score.'
      }},
      'QUAD_BELOW': {{
        name: 'Abaixo da Curva (Prêmio Valuation)',
        icon: '⚠️',
        rationale: 'Ativos cujo múltiplo P/L atual situa-se acima da curva teórica de referência, negociando com prêmio de múltiplos.'
      }}
    }};

    // ==========================================
    // 🏷️ CHIPS DE FILTRO ATIVO COM LIMPEZA [✕]
    // ==========================================
    function renderActiveFilterChips() {{
      const container = document.getElementById('activeFilterChipsContainer');
      if (!container) return;
      
      const chips = [];

      // Filtro de Categoria
      if (currentFilter !== 'ALL') {{
        const meta = BASE_FILTER_META[currentFilter] || {{ icon: '🏷️', name: currentFilter }};
        chips.push(`
          <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-100 text-emerald-950 font-bold border border-emerald-300 shadow-2xs">
            <span>${{meta.icon}}</span>
            <span>Filtro: ${{meta.name}}</span>
            <button onclick="setFilter('ALL')" class="hover:bg-emerald-200 text-emerald-800 rounded-full w-4 h-4 inline-flex items-center justify-center text-xs ml-1 cursor-pointer" title="Remover filtro">✕</button>
          </span>
        `);
      }}

      // Filtro de Setor
      if (currentSector !== 'ALL') {{
        chips.push(`
          <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-indigo-50 text-indigo-950 font-bold border border-indigo-200 shadow-2xs">
            <span>🏢</span>
            <span>Setor: ${{currentSector}}</span>
            <button onclick="handleSectorChange('ALL')" class="hover:bg-indigo-100 text-indigo-800 rounded-full w-4 h-4 inline-flex items-center justify-center text-xs ml-1 cursor-pointer" title="Remover filtro de setor">✕</button>
          </span>
        `);
      }}

      // Filtro de Busca por Texto
      if (searchQuery) {{
        chips.push(`
          <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-amber-50 text-amber-950 font-bold border border-amber-300 shadow-2xs">
            <span>🔍</span>
            <span>Busca: "${{searchQuery}}"</span>
            <button onclick="clearSearchFilter()" class="hover:bg-amber-100 text-amber-800 rounded-full w-4 h-4 inline-flex items-center justify-center text-xs ml-1 cursor-pointer" title="Limpar busca">✕</button>
          </span>
        `);
      }}

      if (chips.length > 0) {{
        chips.push(`
          <button onclick="resetData()" class="text-xs font-semibold text-slate-500 hover:text-slate-800 hover:underline px-2 py-1 cursor-pointer">
            Limpar Todos os Filtros
          </button>
        `);
        container.innerHTML = chips.join('');
        container.classList.remove('hidden');
      }} else {{
        container.innerHTML = '';
        container.classList.add('hidden');
      }}
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

      const wsContainer = document.getElementById('workspaceContainer');
      if (wsContainer) wsContainer.scrollTop = 0;

      const topTitle = document.getElementById('topbarTitle');
      const topSub = document.getElementById('topbarSubtitle');

      if (ws === 'home') {{
        if (vHome) vHome.classList.remove('hidden');
        if (btnHome) btnHome.classList.add('active');
        if (topTitle) topTitle.innerHTML = '<span><svg class="w-4 h-4 stroke-[1.75] inline-block" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg></span> <span>PANORAMA GERAL</span>';
        if (topSub) topSub.innerText = 'Cockpit executivo e inteligência fundamentalista B3';
        renderHomePage();
      }} else if (ws === 'portfolios') {{
        if (vPortfolios) vPortfolios.classList.remove('hidden');
        if (btnPortfolios) btnPortfolios.classList.add('active');
        if (topTitle) topTitle.innerHTML = '<span class="text-indigo-600"><svg class="w-4 h-4 stroke-[2] inline-block" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/></svg></span> <span>HUB DE CATEGORIAS QUANTITATIVAS</span>';
        if (topSub) topSub.innerText = 'Segmentação matemática, enquadramento de balanço e rastreador de fatores B3';
        renderPortfolios();
      }} else if (ws === 'matrix') {{
        if (vMatrix) vMatrix.classList.remove('hidden');
        if (btnMatrix) btnMatrix.classList.add('active');
        if (topTitle) topTitle.innerHTML = '<span class="text-slate-700">' + APP_ICONS.matrix + '</span> <span>MATRIZ ESTRATÉGICA 2X2</span>';
        if (topSub) topSub.innerText = 'Score de Qualidade Fundamentalista vs. Valuation e dispersão do mercado';
        renderMatrix();
      }} else {{
        if (vTable) vTable.classList.remove('hidden');
        if (btnTable) btnTable.classList.add('active');
        if (topTitle) topTitle.innerHTML = '<span class="text-slate-700">' + APP_ICONS.search + '</span> <span>SCANNER B3 &amp; ATIVOS</span>';
        if (topSub) topSub.innerText = 'Triagem fundamentalista, múltiplos, solvência e dossiê 360°';
        renderTable();
        renderDiagnosis();
      }}
    }}

    // ==========================================
    // APRESENTAÇÃO & BOAS-VINDAS DO TERMINAL
    // ==========================================
    function toggleWelcomeBanner() {{
      const body = document.getElementById('welcomeGuideBody');
      const txt = document.getElementById('txtToggleWelcome');
      const icon = document.getElementById('iconToggleWelcome');
      if (!body) return;
      const isHidden = body.classList.contains('hidden');
      if (isHidden) {{
        body.classList.remove('hidden');
        if (txt) txt.innerText = 'Minimizar';
        if (icon) icon.style.transform = 'rotate(0deg)';
        localStorage.setItem('moat_welcome_collapsed', 'false');
      }} else {{
        body.classList.add('hidden');
        if (txt) txt.innerText = 'Expandir';
        if (icon) icon.style.transform = 'rotate(180deg)';
        localStorage.setItem('moat_welcome_collapsed', 'true');
      }}
    }}

    function openWelcomeGuide() {{
      switchWorkspace('home');
      const body = document.getElementById('welcomeGuideBody');
      const txt = document.getElementById('txtToggleWelcome');
      const icon = document.getElementById('iconToggleWelcome');
      if (body && body.classList.contains('hidden')) {{
        body.classList.remove('hidden');
        if (txt) txt.innerText = 'Minimizar';
        if (icon) icon.style.transform = 'rotate(0deg)';
        localStorage.setItem('moat_welcome_collapsed', 'false');
      }}
      const banner = document.getElementById('welcomeGuideBanner');
      if (banner) {{
        banner.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
        banner.classList.add('ring-2', 'ring-emerald-400');
        setTimeout(() => {{
          banner.classList.remove('ring-2', 'ring-emerald-400');
        }}, 1800);
      }}
    }}

    function initWelcomeGuide() {{
      const isCollapsed = localStorage.getItem('moat_welcome_collapsed') === 'true';
      if (isCollapsed) {{
        const body = document.getElementById('welcomeGuideBody');
        const txt = document.getElementById('txtToggleWelcome');
        const icon = document.getElementById('iconToggleWelcome');
        if (body) body.classList.add('hidden');
        if (txt) txt.innerText = 'Expandir';
        if (icon) icon.style.transform = 'rotate(180deg)';
      }}
    }}

    function setFilterAndGoTable(f) {{
      closeDossierDrawer();
      setFilter(f);
      switchWorkspace('table');
      const tb = document.getElementById('global-filters-toolbar');
      if (tb) tb.scrollIntoView({{ behavior: 'smooth' }});
    }}

    let currentDiagTab = 'radar';

    function switchDiagTab(tab) {{
      currentDiagTab = tab;
      const tabs = ['radar', 'history', 'balance', 'sintese'];
      tabs.forEach(t => {{
        const btn = document.getElementById('dtab-' + t);
        const view = document.getElementById('dview-' + t);
        const isActive = (t === tab);
        if (btn) {{
          btn.classList.toggle('active', isActive);
          if (isActive) {{
            btn.className = 'tab-btn active flex-1 py-1.5 rounded-lg text-center text-slate-900 bg-white font-bold shadow-xs border border-slate-200/90 transition cursor-pointer';
          }} else {{
            btn.className = 'tab-btn flex-1 py-1.5 rounded-lg text-center text-slate-600 hover:text-slate-900 hover:bg-white/60 font-medium transition cursor-pointer';
          }}
        }}
        if (view) {{
          view.classList.toggle('hidden', !isActive);
        }}
      }});
    }}

    function openDossierDrawer(t) {{
      if (t) selectTicker(t);
      switchDiagTab(currentDiagTab || 'radar');
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

    function setMatrixFilter(f) {{
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
      const btnKeys = ['ALL', 'CAT_TIER1', 'CAT_DISCOUNT', 'CAT_NET_CASH', 'CAT_EXPANSION', 'CAT_DIVIDENDS', 'CAT_SPREAD_NTNB'];
      btnKeys.forEach(k => {{
        const btn = document.getElementById('btn-mat-' + k);
        if (btn) {{
          const isActive = (currentFilter === k || (k === 'ALL' && currentFilter === 'ALL'));
          if (isActive) {{
            btn.classList.add('ring-2', 'ring-emerald-600', 'bg-emerald-50', 'font-bold', 'border-emerald-400');
            btn.classList.remove('bg-white');
          }} else {{
            btn.classList.remove('ring-2', 'ring-emerald-600', 'bg-emerald-50', 'font-bold', 'border-emerald-400');
            btn.classList.add('bg-white');
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
        closeDossierDrawer();
        setFilter(cat);
        switchWorkspace('table');
        const tb = document.getElementById('global-filters-toolbar');
        if (tb) tb.scrollIntoView({{ behavior: 'smooth' }});
      }}
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
        elPl.innerText = medianPl.toFixed(1).replace('.', ',') + 'x P/L';
        elPl.className = 'text-4xl font-mono font-bold text-slate-900 tracking-tight';
      }}
      const elRoic = document.getElementById('home-stat-roic');
      if (elRoic) {{
        elRoic.innerText = (medianRoic * 100).toFixed(1).replace('.', ',') + '% ROIC';
        elRoic.className = 'text-4xl font-mono font-bold text-[#00A887] tracking-tight';
      }}
      const elSpread = document.getElementById('home-stat-spread');
      if (elSpread) {{
        elSpread.innerText = (medianSpread > 0 ? '+' : '') + medianSpread.toFixed(1).replace('.', ',') + '%';
        elSpread.className = 'font-bold font-mono';
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

      // 1.5 Seleção Ultra-Crítica (Régua Fundamentalista / Munger: 100% Fundamentus)
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
          const dlBadge = dl !== null && dl <= 0 ? '<span class="text-emerald-800 font-semibold">Caixa Líq</span>' : (s.div_liq_ebitda !== null ? `<span class="${{getColorDebt(s.div_liq_ebitda, s.is_financial)}}">${{s.div_liq_ebitda.toFixed(1)}}x</span>` : 'N/D');
          return `
            <div onclick="selectTickerAndNavigate('${{s.ticker}}')" class="p-2.5 rounded-xl glass-card hover:border-yellow-500/50 hover:bg-yellow-500/5 border border-yellow-500/20 transition duration-200 cursor-pointer flex flex-col justify-between shadow-sm">
              <div class="flex items-center justify-between">
                <span class="font-bold text-amber-800 font-mono text-xs">${{s.ticker}}</span>
                <span class="px-1.5 py-0.2 rounded-full text-[10px] font-bold bg-yellow-500/20 text-amber-800 border border-yellow-500/40">${{s.quality_score.toFixed(0)}}</span>
              </div>
              <div class="text-[11px] text-slate-600 font-sans truncate mt-1" title="${{s.empresa}}">${{s.empresa}}</div>
              <div class="mt-2 pt-1.5 border-t border-slate-200 flex items-center justify-between text-[10px] text-slate-400 font-mono">
                <span title="Munger Acid Test (EBIT/EBITDA)">Acid: <b class="${{s.is_financial ? 'text-indigo-800' : getColorAcidTest(s.capital_intensity)}}">${{capStr}}</b></span>
                <span title="Dívida Líquida / Solvência">${{dlBadge}}</span>
              </div>
            </div>
          `;
        }}).join('');
      }}

      // 2. Top 5 Munger Score (Empresas Wide Moat com Valuation Equilibrado: Score >= 80, Spread >= +1.5%, Dívida <= 2.5x)
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
          <div onclick="selectTickerAndNavigate('${{s.ticker}}')" class="flex items-center justify-between p-3.5 rounded-2xl glass-card hover:border-[#00A887] hover:bg-[#FBFBF9] border border-[#E7E7E2] transition-all duration-200 cursor-pointer shadow-3xs group">
            <div class="flex items-center gap-3 min-w-0">
              <span class="text-xs font-mono font-bold text-slate-400 group-hover:text-[#00A887]">0${{i+1}}</span>
              ${{getStockLogoHtml(s.ticker, s.empresa, 'w-8 h-8')}}
              <div class="flex flex-col min-w-0">
                <div class="flex items-center gap-2">
                  <span class="text-sm font-bold text-slate-900 font-mono leading-none group-hover:text-[#003836]">${{s.ticker}}</span>
                  <span class="text-[11px] text-slate-500 font-sans truncate max-w-[150px] hidden sm:inline">${{s.empresa}}</span>
                </div>
                <span class="text-[10px] text-slate-400 font-mono mt-0.5">ROIC ${{formatPercent(s.roic || s.roe)}} • P/L ${{formatMultiple(s.pl)}}</span>
              </div>
            </div>
            <div class="flex items-center gap-2.5 text-right font-mono flex-shrink-0">
              <span class="px-2.5 py-1 rounded-full text-xs font-bold bg-[#E6F4F1] text-[#004B49] border border-[#BCE5DC]">Score ${{s.quality_score.toFixed(1)}}</span>
              <span class="text-slate-400 text-xs group-hover:text-[#00A887] transition-transform group-hover:translate-x-0.5">➜</span>
            </div>
          </div>
        `).join('');
      }}

      // 3. Top 5 Múltiplos Descontados (Rigor Fundamentalista: Quality Score >= 75, P/L 3x a 15x, Spread >= +3.0%, Dívida <= 3.0x, sem distorção)
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
          <div onclick="selectTickerAndNavigate('${{s.ticker}}')" class="flex items-center justify-between p-3.5 rounded-2xl glass-card hover:border-[#00A887] hover:bg-[#FBFBF9] border border-[#E7E7E2] transition-all duration-200 cursor-pointer shadow-3xs group">
            <div class="flex items-center gap-3 min-w-0">
              <span class="text-xs font-mono font-bold text-slate-400 group-hover:text-[#00A887]">0${{i+1}}</span>
              ${{getStockLogoHtml(s.ticker, s.empresa, 'w-8 h-8')}}
              <div class="flex flex-col min-w-0">
                <div class="flex items-center gap-2">
                  <span class="text-sm font-bold text-slate-900 font-mono leading-none group-hover:text-[#003836]">${{s.ticker}}</span>
                  <span class="text-[11px] text-slate-500 font-sans truncate max-w-[150px] hidden sm:inline">${{s.empresa}}</span>
                </div>
                <span class="text-[10px] text-slate-400 font-mono mt-0.5">P/L ${{formatMultiple(s.pl)}} • Spread +${{s.ey_spread.toFixed(1)}}%</span>
              </div>
            </div>
            <div class="flex items-center gap-2.5 text-right font-mono flex-shrink-0">
              <span class="px-2.5 py-1 rounded-full text-xs font-bold bg-amber-50 text-amber-900 border border-amber-200">+${{s.ey_spread.toFixed(1)}}%</span>
              <span class="text-slate-400 text-xs group-hover:text-[#00A887] transition-transform group-hover:translate-x-0.5">➜</span>
            </div>
          </div>
        `).join('');
      }}

      // 4. Top 5 Proventos Sustentáveis (Vacas Leiteiras: DY > 6% e até 13%, Payout entre 35% e 85%, ROIC/ROE >= 12%, Score >= 70)
      const allDiv = validStocks.filter(s => s.div_yield !== null && s.div_yield > 0.06 && s.div_yield <= 0.13 && s.payout_implicito !== null && s.payout_implicito >= 35 && s.payout_implicito <= 85 && (s.roic || s.roe || 0) >= 0.12 && s.quality_score >= 70 && (s.is_financial || (s.div_liq_ebitda !== null && s.div_liq_ebitda <= 3.0)));
      const topDiv = dedupPreferLiquid(
        allDiv,
        (a, b) => b.div_yield - a.div_yield
      ).slice(0, 5);

      const cntCatDiv = document.getElementById('cnt-cat-div');
      if (cntCatDiv) cntCatDiv.innerText = '(' + allDiv.length + ')';

      const listDiv = document.getElementById('home-list-dividends');
      if (listDiv) {{
        listDiv.innerHTML = topDiv.map((s, i) => `
          <div onclick="selectTickerAndNavigate('${{s.ticker}}')" class="flex items-center justify-between p-3.5 rounded-2xl glass-card hover:border-[#00A887] hover:bg-[#FBFBF9] border border-[#E7E7E2] transition-all duration-200 cursor-pointer shadow-3xs group">
            <div class="flex items-center gap-3 min-w-0">
              <span class="text-xs font-mono font-bold text-slate-400 group-hover:text-[#00A887]">0${{i+1}}</span>
              ${{getStockLogoHtml(s.ticker, s.empresa, 'w-8 h-8')}}
              <div class="flex flex-col min-w-0">
                <div class="flex items-center gap-2">
                  <span class="text-sm font-bold text-slate-900 font-mono leading-none group-hover:text-[#003836]">${{s.ticker}}</span>
                  <span class="text-[11px] text-slate-500 font-sans truncate max-w-[150px] hidden sm:inline">${{s.empresa}}</span>
                </div>
                <span class="text-[10px] text-slate-400 font-mono mt-0.5">DY ${{formatPercent(s.div_yield)}} • Payout ${{s.payout_implicito ? s.payout_implicito.toFixed(0) + '%' : 'N/D'}}</span>
              </div>
            </div>
            <div class="flex items-center gap-2.5 text-right font-mono flex-shrink-0">
              <span class="px-2.5 py-1 rounded-full text-xs font-bold bg-[#E6F4F1] text-[#004B49] border border-[#BCE5DC]">DY ${{formatPercent(s.div_yield)}}</span>
              <span class="text-slate-400 text-xs group-hover:text-[#00A887] transition-transform group-hover:translate-x-0.5">➜</span>
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
          <div onclick="selectTickerAndNavigate('${{s.ticker}}')" class="flex items-center justify-between p-2.5 rounded-xl glass-card hover:border-teal-400/80 hover:bg-teal-50/50 border border-slate-200 transition duration-200 cursor-pointer shadow-xs">
            <div class="flex items-center gap-2 min-w-0">
              ${{getStockLogoHtml(s.ticker, s.empresa, 'w-6 h-6')}}
              <div class="flex flex-col min-w-0">
                <div class="flex items-center gap-1.5">
                  <span class="font-bold text-slate-900 text-xs font-mono leading-none">${{s.ticker}}</span>
                  <span class="text-[10px] text-slate-600 font-sans truncate max-w-[85px]" title="${{s.empresa}}">${{s.empresa}}</span>
                </div>
                <div class="text-[10px] text-slate-700 font-mono mt-0.5 font-medium">
                  P/L: ${{s.pl.toFixed(1)}}x ➜ <b class="text-emerald-800 font-bold">${{s.pl_run_rate.toFixed(1)}}x</b>
                </div>
              </div>
            </div>
            <span class="px-2 py-0.5 rounded-full text-[11px] font-bold font-mono bg-teal-100 text-teal-900 border border-teal-300 shadow-xs">+${{s.run_rate_div_pct.toFixed(0)}}%</span>
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
          <div onclick="selectTickerAndNavigate('${{s.ticker}}')" class="flex items-center justify-between p-2.5 rounded-xl glass-card hover:border-amber-400/80 hover:bg-amber-50/50 border border-slate-200 transition duration-200 cursor-pointer shadow-xs">
            <div class="flex items-center gap-2 min-w-0">
              ${{getStockLogoHtml(s.ticker, s.empresa, 'w-6 h-6')}}
              <div class="flex flex-col min-w-0">
                <div class="flex items-center gap-1.5">
                  <span class="font-bold text-slate-900 text-xs font-mono leading-none">${{s.ticker}}</span>
                  <span class="text-[10px] text-slate-600 font-sans truncate max-w-[85px]" title="${{s.empresa}}">${{s.empresa}}</span>
                </div>
                <div class="text-[10px] text-slate-700 font-mono mt-0.5 font-medium">
                  P/L: ${{s.pl.toFixed(1)}}x ➜ <b class="text-amber-800 font-bold">${{s.pl_run_rate.toFixed(1)}}x</b>
                </div>
              </div>
            </div>
            <span class="px-2 py-0.5 rounded-full text-[11px] font-bold font-mono bg-amber-100 text-amber-900 border border-amber-300 shadow-xs">${{s.run_rate_div_pct.toFixed(0)}}%</span>
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
          <div onclick="selectTickerAndNavigate('${{s.ticker}}')" class="flex items-center justify-between p-2.5 rounded-xl glass-card hover:border-emerald-400/80 hover:bg-emerald-50/50 border border-slate-200 transition duration-200 cursor-pointer shadow-xs">
            <div class="flex items-center gap-2 min-w-0">
              ${{getStockLogoHtml(s.ticker, s.empresa, 'w-6 h-6')}}
              <div class="flex flex-col min-w-0">
                <div class="flex items-center gap-1.5">
                  <span class="font-bold text-slate-900 text-xs font-mono leading-none">${{s.ticker}}</span>
                  <span class="text-[10px] text-slate-600 font-sans truncate max-w-[85px]" title="${{s.empresa}}">${{s.empresa}}</span>
                </div>
                <div class="text-[10px] text-slate-700 font-mono mt-0.5 font-medium">
                  ROIC: <b class="text-slate-900 font-bold">${{formatPercent(s.roic || s.roe)}}</b>
                </div>
              </div>
            </div>
            <span class="px-2 py-0.5 rounded-full text-[10px] font-bold font-mono bg-emerald-100 text-emerald-900 border border-emerald-300 shadow-xs">Caixa Líq.</span>
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
          <div onclick="selectTickerAndNavigate('${{s.ticker}}')" class="flex items-center justify-between p-2.5 rounded-xl glass-card hover:border-rose-400/80 hover:bg-rose-50/50 border border-slate-200 transition duration-200 cursor-pointer shadow-xs">
            <div class="flex items-center gap-2 min-w-0">
              ${{getStockLogoHtml(s.ticker, s.empresa, 'w-6 h-6')}}
              <div class="flex flex-col min-w-0">
                <div class="flex items-center gap-1.5">
                  <span class="font-bold text-slate-900 text-xs font-mono leading-none">${{s.ticker}}</span>
                  <span class="text-[10px] text-slate-600 font-sans truncate max-w-[85px]" title="${{s.empresa}}">${{s.empresa}}</span>
                </div>
                <div class="text-[10px] text-slate-700 font-mono mt-0.5 font-medium">
                  Score: <b class="text-rose-700 font-bold">${{s.quality_score.toFixed(1)}}</b>
                </div>
              </div>
            </div>
            <span class="px-2 py-0.5 rounded-full text-[10px] font-bold font-mono bg-rose-100 text-rose-900 border border-rose-300 shadow-xs">${{s.div_liq_ebitda.toFixed(1)}}x Dívida</span>
          </div>
        `).join('');
      }}

      // 7. Atualização e Renderização da Carteira Teórica do Ibovespa
      renderHomeIbovSection();
    }}

    // ==========================================
    // 🏛️ CONTROLE & FILTROS DA CARTEIRA IBOVESPA
    // ==========================================
    let currentHomeIbovFilter = 'ALL';
    let homeIbovSearchQuery = '';

    function setHomeIbovFilter(subFilter) {{
      currentHomeIbovFilter = subFilter;
      document.querySelectorAll('.hibov-btn').forEach(btn => {{
        btn.classList.remove('active', 'bg-slate-900', 'text-white', 'border-slate-900');
        btn.classList.add('bg-white', 'text-slate-700', 'border-slate-200');
      }});
      const activeBtn = document.getElementById('hibov-flt-' + subFilter);
      if (activeBtn) {{
        activeBtn.classList.remove('bg-white', 'text-slate-700', 'border-slate-200');
        activeBtn.classList.add('active', 'bg-slate-900', 'text-white', 'border-slate-900');
      }}
      renderHomeIbovGrid();
    }}

    function handleHomeIbovSearch() {{
      const input = document.getElementById('homeIbovSearchInput');
      homeIbovSearchQuery = input ? input.value.trim().toLowerCase() : '';
      renderHomeIbovGrid();
    }}

    function renderHomeIbovSection() {{
      const ibovStocks = (APP_DATA.stocks || []).filter(s => s.is_ibov);
      
      // Estatísticas gerais
      const elCount = document.getElementById('home-ibov-count');
      if (elCount) elCount.innerText = ibovStocks.length + ' papéis';

      const pls = ibovStocks.filter(s => s.pl && s.pl > 0 && s.pl <= 50).map(s => s.pl).sort((a, b) => a - b);
      const medianPl = pls.length ? pls[Math.floor(pls.length / 2)] : 12.1;
      const elPl = document.getElementById('home-ibov-median-pl');
      if (elPl) elPl.innerText = medianPl.toFixed(1) + 'x';

      let totalWeight = 0;
      let weightedDySum = 0;
      ibovStocks.forEach(s => {{
        const w = s.ibov_weight || 0;
        totalWeight += w;
        weightedDySum += w * (s.div_yield || 0);
      }});
      const weightedDy = totalWeight > 0 ? (weightedDySum / totalWeight) : 0.055;
      const elDy = document.getElementById('home-ibov-dy-ponderado');
      if (elDy) elDy.innerText = (weightedDy * 100).toFixed(1).replace('.', ',') + '%';

      // Atualiza contadores dos botões de filtro
      const nAssimetria = ibovStocks.filter(s => s.entry_tag === 'ASSIMETRIA_FAVORAVEL').length;
      const nPrecoJusto = ibovStocks.filter(s => s.entry_tag === 'PRECO_JUSTO').length;
      const nEsticada = ibovStocks.filter(s => s.entry_tag === 'ESTICADA').length;

      const elAss = document.getElementById('hibov-cnt-assimetria');
      if (elAss) elAss.innerText = nAssimetria;
      const elPj = document.getElementById('hibov-cnt-precojusto');
      if (elPj) elPj.innerText = nPrecoJusto;
      const elEst = document.getElementById('hibov-cnt-esticada');
      if (elEst) elEst.innerText = nEsticada;

      renderHomeIbovGrid();
    }}

    function renderHomeIbovGrid() {{
      const container = document.getElementById('home-ibov-grid');
      if (!container) return;

      const ibovStocks = (APP_DATA.stocks || [])
        .filter(s => s.is_ibov)
        .sort((a, b) => (b.ibov_weight || 0) - (a.ibov_weight || 0));

      let filtered = ibovStocks;
      if (currentHomeIbovFilter === 'TOP15') {{
        filtered = ibovStocks.slice(0, 15);
      }} else if (currentHomeIbovFilter === 'ASSIMETRIA') {{
        filtered = ibovStocks.filter(s => s.entry_tag === 'ASSIMETRIA_FAVORAVEL');
      }} else if (currentHomeIbovFilter === 'PRECO_JUSTO') {{
        filtered = ibovStocks.filter(s => s.entry_tag === 'PRECO_JUSTO');
      }} else if (currentHomeIbovFilter === 'ESTICADA') {{
        filtered = ibovStocks.filter(s => s.entry_tag === 'ESTICADA');
      }}

      if (homeIbovSearchQuery) {{
        filtered = filtered.filter(s =>
          s.ticker.toLowerCase().includes(homeIbovSearchQuery) ||
          (s.empresa && s.empresa.toLowerCase().includes(homeIbovSearchQuery)) ||
          (s.setor && s.setor.toLowerCase().includes(homeIbovSearchQuery))
        );
      }}

      if (filtered.length === 0) {{
        container.innerHTML = `
          <div class="col-span-full py-8 text-center text-xs font-mono text-slate-400">
            Nenhum ativo do Ibovespa encontrado para o critério selecionado.
          </div>
        `;
        return;
      }}

      container.innerHTML = filtered.map(s => {{
        let entryBg = 'bg-white hover:bg-slate-50 border-slate-200';
        let dotColor = 'bg-slate-400';
        let entryLabel = 'Valuation em Linha';
        if (s.entry_tag === 'ASSIMETRIA_FAVORAVEL') {{
          entryBg = 'bg-emerald-50/60 hover:bg-emerald-50 border-emerald-200/80';
          dotColor = 'bg-emerald-500';
          entryLabel = 'Múltiplos Descontados';
        }} else if (s.entry_tag === 'ESTICADA') {{
          entryBg = 'bg-rose-50/40 hover:bg-rose-50 border-rose-200/80';
          dotColor = 'bg-rose-500';
          entryLabel = 'Múltiplos Elevados';
        }} else if (s.entry_tag === 'PRECO_JUSTO') {{
          entryBg = 'bg-amber-50/40 hover:bg-amber-50 border-amber-200/80';
          dotColor = 'bg-amber-500';
          entryLabel = 'Valuation em Linha';
        }}

        const dyVal = s.div_yield ? (s.div_yield * 100).toFixed(1).replace('.', ',') + '%' : '0,0%';
        const plVal = s.pl && s.pl > 0 ? s.pl.toFixed(1) + 'x' : 'N/D';
        const weightVal = s.ibov_weight ? (s.ibov_weight * 100).toFixed(2).replace('.', ',') + '%' : '--';

        return `
          <div onclick="selectTickerAndNavigate('${{s.ticker}}')" class="${{entryBg}} border rounded-xl p-2.5 transition duration-150 cursor-pointer shadow-2xs group flex flex-col justify-between" title="${{s.empresa}} - Clique para abrir o Dossiê 360°">
            <div class="flex items-start justify-between gap-1 mb-1.5">
              <div>
                <div class="flex items-center gap-1.5">
                  <span class="font-mono font-bold text-xs text-slate-900 group-hover:text-indigo-600 transition">${{s.ticker}}</span>
                  <span class="w-1.5 h-1.5 rounded-full ${{dotColor}}"></span>
                </div>
                <div class="text-[10px] text-slate-500 truncate max-w-[95px]">${{s.empresa}}</div>
              </div>
              <span class="text-[9px] font-mono font-bold px-1.5 py-0.2 rounded bg-indigo-50 text-indigo-700 border border-indigo-200" title="Peso na Carteira Oficial">${{weightVal}}</span>
            </div>
            
            <div class="grid grid-cols-2 gap-1 pt-1.5 border-t border-slate-100 text-[10px] font-mono">
              <div>
                <span class="text-slate-400 block text-[8.5px]">P/L</span>
                <span class="font-semibold text-slate-700">${{plVal}}</span>
              </div>
              <div class="text-right">
                <span class="text-slate-400 block text-[8.5px]">DY</span>
                <span class="font-semibold text-teal-700">${{dyVal}}</span>
              </div>
            </div>
          </div>
        `;
      }}).join('');
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
      return `Ativo com Score Fundamentalista de ${{s.quality_score.toFixed(0)}} pts, ROIC/ROE de ${{roicStr}} e distribuição de dividendos estimada em ${{dyStr}}.`;
    }}

    // DEFINIÇÕES METODOLÓGICAS DAS CATEGORIAS QUANTITATIVAS
    const CATEGORY_DEFINITIONS = [
      {{
        id: 'CAT_TIER1',
        name: 'Wide Moat (Tier 1)',
        shortName: 'Wide Moat (Tier 1)',
        icon: '🏆',
        color: 'emerald',
        badgeClass: 'bg-emerald-50 text-emerald-950 border border-emerald-300',
        description: 'Empresas excepcionais com Score Fundamentalista ≥ 80 pts e ROIC/ROE ≥ 15%. Líderes de mercado com vantagens competitivas estruturais duráveis.',
        rationale: 'Filtro quantitativo que conjuga retorno sustentável sobre o capital próprio/investido acima da taxa livre de risco com solidez de balanço e qualidade contábil no percentil 80+ da B3.'
      }},
      {{
        id: 'CAT_NET_CASH',
        name: 'Caixa Líquido (Dívida Zero)',
        shortName: 'Caixa Líquido',
        icon: '🛡️',
        color: 'emerald',
        badgeClass: 'bg-emerald-50 text-emerald-950 border border-emerald-300',
        description: 'Empresas não-financeiras cuja disponibilidade financeira imediata supera o montante integral da dívida bruta bancária (Dívida Líquida ≤ 0).',
        rationale: 'Critério estritamente contábil de solvência máxima: risco de liquidez e solvência virtualmente nulo no curto e médio prazo, imunes ao ciclo restritivo da taxa Selic.'
      }},
      {{
        id: 'CAT_EXPANSION',
        name: 'Lucro Acelerando (Expansão 2T26)',
        shortName: 'Lucro Acelerando',
        icon: '⚡',
        color: 'emerald',
        badgeClass: 'bg-emerald-50 text-emerald-950 border border-emerald-300',
        description: 'Empresas cujo lucro líquido anualizado do 2T26 (Run-Rate) supera em mais de 15% a média dos últimos 12 meses acumulados.',
        rationale: 'Rastreador de aceleração operacional recente: identifica momento contábil positivo, expansão de margens e alavancagem operacional antes da reprecificação total pelo consenso.'
      }},
      {{
        id: 'CAT_DIVIDENDS',
        name: 'Dividendos Consistentes (> 6%)',
        shortName: 'Dividendos > 6%',
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
        description: 'Cotação com desconto superior a 15% em relação ao Valor Intrínseco calculado pela fórmula clássica de Graham: √(22,5 × LPA × VPA).',
        rationale: 'Modelo clássico de Value Investing: identifica ativos negociando abaixo do valor intrínseco resultante da combinação ponderada entre lucro por ação e patrimônio líquido auditado.'
      }},
      {{
        id: 'CAT_BAZIN',
        name: 'Referência Décio Bazin',
        shortName: 'Referência Bazin',
        icon: '🎯',
        color: 'sky',
        badgeClass: 'bg-sky-50 text-sky-950 border border-sky-300',
        description: 'Cotação de mercado abaixo da referência teórica Bazin (Proventos / 0,06) com margem de segurança de pelo menos 15%.',
        rationale: 'Metodologia tradicional brasileira de seleção por fluxo de dividendos com taxa de retorno teórica de 6,0% a.a. em proventos.'
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
        name: 'Lucro em Retração (Desaceleração 2T26)',
        shortName: 'Lucro em Retração',
        icon: '⚠️',
        color: 'amber',
        badgeClass: 'bg-amber-50 text-amber-950 border border-amber-300',
        description: 'Empresas cujo lucro trimestral recente anualizado está 20% ou mais abaixo do lucro acumulado nos últimos 12 meses.',
        rationale: 'Sinalizador preventivo de arrefecimento operacional ou pressão em margens que pode demandar cautela adicional.'
      }},
      {{
        id: 'CAT_HIGH_DEBT',
        name: 'Alavancagem Alta (Crítica > 2.5x)',
        shortName: 'Alavancagem Alta',
        icon: '🚨',
        color: 'rose',
        badgeClass: 'bg-rose-50 text-rose-950 border border-rose-300',
        description: 'Empresas não-financeiras com Dívida Líquida / EBITDA superior a 2,5x em ambiente de taxas de juros elevadas.',
        rationale: 'Marcador de risco de solvência: despesas financeiras absorvem fatia relevante do resultado operacional, comprimindo o lucro líquido.'
      }}
    ];

    function selectPortfolio(key) {{
      setFilter(key);
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
      // O Scanner B3 & Ativos unifica a visualização e KPIs das categorias via renderTable()
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

    function openDedicatedCompanyPage(ticker) {{
      const t = ticker || selectedTicker || 'WEGE3';
      window.open('empresa.html?ticker=' + encodeURIComponent(t), '_blank');
    }}

    function switchMatrixX(metric) {{
      currentXMetric = metric;
      const btnPl = document.getElementById('btn-x-pl');
      const btnEy = document.getElementById('btn-x-ey');
      const lblAxis = document.getElementById('lbl-matrix-axis-x');
      
      if (metric === 'pl') {{
        if (btnPl) btnPl.className = 'px-2.5 py-0.5 rounded-md bg-amber-100 text-amber-900 font-bold border border-amber-300';
        if (btnEy) btnEy.className = 'px-2.5 py-0.5 rounded-md text-slate-600 hover:text-slate-900 font-medium';
        if (lblAxis) lblAxis.innerText = 'P/L (0-25x)';
      }} else {{
        if (btnPl) btnPl.className = 'px-2.5 py-0.5 rounded-md text-slate-600 hover:text-slate-900 font-medium';
        if (btnEy) btnEy.className = 'px-2.5 py-0.5 rounded-md bg-amber-100 text-amber-900 font-bold border border-amber-300';
        if (lblAxis) lblAxis.innerText = 'EY% (0-25%)';
      }}
      resetMatrixZoom();
    }}

    function switchBubbleColor(color) {{
      matrixColorMode = color;
      const sel = document.getElementById('sel-bubble-color');
      if (sel) sel.value = color;
      updateMatrixLegend();
      renderMatrix();
    }}

    function switchBubbleMetric(metric) {{
      matrixBubbleMetric = metric;
      const sel = document.getElementById('sel-bubble-metric');
      if (sel) sel.value = metric;
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
      const baseXMax = isPl ? 25.0 : 25.0;
      matrixCenterX = baseXMax / 2;
      matrixCenterY = (100.0 + 20.0) / 2;
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
      const baseXMax = isPl ? 25.0 : 25.0;
      const baseYMin = 20.0;
      const baseYMax = 100.0;

      const padL = 70, padR = 30, padT = 35, padB = 55;
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
        let vA, vB;
        if (currentSortCol === 'roic') {{
          const aValid = !a.is_financial && a.roic !== null && a.roic !== undefined;
          const bValid = !b.is_financial && b.roic !== null && b.roic !== undefined;
          if (!aValid && !bValid) return 0;
          if (!aValid) return 1;
          if (!bValid) return -1;
          return currentSortAsc ? (a.roic - b.roic) : (b.roic - a.roic);
        }} else if (currentSortCol === 'roe') {{
          const aValid = a.roe !== null && a.roe !== undefined;
          const bValid = b.roe !== null && b.roe !== undefined;
          if (!aValid && !bValid) return 0;
          if (!aValid) return 1;
          if (!bValid) return -1;
          return currentSortAsc ? (a.roe - b.roe) : (b.roe - a.roe);
        }} else if (currentSortCol === 'pl') {{
          const aValid = a.pl !== null && a.pl !== undefined && a.pl > 0;
          const bValid = b.pl !== null && b.pl !== undefined && b.pl > 0;
          if (!aValid && !bValid) return 0;
          if (!aValid) return 1;
          if (!bValid) return -1;
          return currentSortAsc ? (a.pl - b.pl) : (b.pl - a.pl);
        }} else if (currentSortCol === 'div_liq_ebitda') {{
          const aValid = !a.is_financial && a.div_liq_ebitda !== null && a.div_liq_ebitda !== undefined;
          const bValid = !b.is_financial && b.div_liq_ebitda !== null && b.div_liq_ebitda !== undefined;
          if (!aValid && !bValid) return 0;
          if (!aValid) return 1;
          if (!bValid) return -1;
          return currentSortAsc ? (a.div_liq_ebitda - b.div_liq_ebitda) : (b.div_liq_ebitda - a.div_liq_ebitda);
        }} else if (currentSortCol === 'ev_ebitda') {{
          const aValid = !a.is_financial && a.ev_ebitda !== null && a.ev_ebitda !== undefined && a.ev_ebitda > 0;
          const bValid = !b.is_financial && b.ev_ebitda !== null && b.ev_ebitda !== undefined && b.ev_ebitda > 0;
          if (!aValid && !bValid) return 0;
          if (!aValid) return 1;
          if (!bValid) return -1;
          return currentSortAsc ? (a.ev_ebitda - b.ev_ebitda) : (b.ev_ebitda - a.ev_ebitda);
        }} else if (currentSortCol === 'ey_spread') {{
          const aValid = a.ey_spread !== null && a.ey_spread !== undefined;
          const bValid = b.ey_spread !== null && b.ey_spread !== undefined;
          if (!aValid && !bValid) return 0;
          if (!aValid) return 1;
          if (!bValid) return -1;
          return currentSortAsc ? (a.ey_spread - b.ey_spread) : (b.ey_spread - a.ey_spread);
        }} else {{
          vA = a[currentSortCol];
          vB = b[currentSortCol];
        }}
        if (vA === null || vA === undefined) return 1;
        if (vB === null || vB === undefined) return -1;
        if (typeof vA === 'string') return currentSortAsc ? vA.localeCompare(vB) : vB.localeCompare(vA);
        return currentSortAsc ? vA - vB : vB - vA;
      }});

      // 1. Metadados e Títulos da Categoria/Filtro
      const baseMeta = BASE_FILTER_META;

      const foundCat = (typeof CATEGORY_DEFINITIONS !== 'undefined') ? CATEGORY_DEFINITIONS.find(c => c.id === currentFilter) : null;
      const meta = baseMeta[currentFilter] || (foundCat ? {{ name: foundCat.name, icon: foundCat.icon, rationale: foundCat.rationale }} : {{ name: 'Filtro Ativo: ' + currentFilter, icon: '📋', rationale: 'Critério quantitativo fundamentalista auditado pela plataforma.' }});

      const activeTitleEl = document.getElementById('catActiveTitle');
      if (activeTitleEl) activeTitleEl.innerHTML = `<span>${{meta.icon}}</span> ${{meta.name.toUpperCase()}}`;

      const activeCountEl = document.getElementById('catActiveCount');
      if (activeCountEl) activeCountEl.innerText = `${{stocks.length}} ativos qualificados`;

      const activeRationaleEl = document.getElementById('catActiveRationale');
      if (activeRationaleEl) activeRationaleEl.innerText = meta.rationale;

      const tableTitleEl = document.getElementById('catTableTitle');
      if (tableTitleEl) tableTitleEl.innerHTML = `<span>${{meta.icon}}</span> ATIVOS ENQUADRADOS: ${{meta.name.toUpperCase()}}`;

      const tableSubtitleEl = document.getElementById('catTableSubtitle');
      if (tableSubtitleEl) tableSubtitleEl.innerText = `(${{stocks.length}} ativos na B3)`;

      // 2. Cálculo dos Indicadores Médios da Categoria
      let sumPl = 0, countPl = 0;
      let sumRoic = 0, countRoic = 0;
      let sumDy = 0, countDy = 0;
      let sumSpread = 0, countSpread = 0;
      let sumScore = 0;

      stocks.forEach(s => {{
        sumScore += (s.quality_score || 0);
        if (s.pl !== null && s.pl > 0 && s.pl < 60) {{
          sumPl += s.pl;
          countPl++;
        }}
        const roicVal = s.is_financial ? s.roe : (s.roic || s.roe);
        if (roicVal !== null && roicVal !== undefined && roicVal > 0) {{
          sumRoic += roicVal;
          countRoic++;
        }}
        if (s.div_yield !== null && s.div_yield > 0) {{
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
      const avgScore = stocks.length > 0 ? (sumScore / stocks.length) : 0;

      const elTotal = document.getElementById('kp-cat-total');
      if (elTotal) elTotal.innerText = stocks.length + ' ativos';

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

      const cntBadge = document.getElementById('tableCountBadge');
      if (cntBadge) cntBadge.innerText = stocks.length + ' ativos';

      // 3. Renderizar Linhas na Tabela de Ativos
      const tbody = document.getElementById('stocksTableBody');
      if (!tbody) return;
      tbody.innerHTML = '';

      if (stocks.length === 0) {{
        tbody.innerHTML = `
          <tr>
            <td colspan="11" class="py-12 text-center text-slate-500 font-mono text-xs">
              <div class="flex flex-col items-center justify-center gap-2">
                <span class="text-2xl">🔍</span>
                <span class="font-bold text-slate-700">Nenhum ativo encontrado para os filtros selecionados.</span>
                <span class="text-slate-400 text-[11px]">Tente desmarcar algum critério de liquidez ou selecionar "Todos os Setores".</span>
                <button onclick="setFilter('ALL')" class="mt-2 px-3 py-1 bg-emerald-50 hover:bg-emerald-100 text-emerald-800 font-bold rounded-lg text-xs border border-emerald-300 transition cursor-pointer">
                  Mostrar Todos os 194 Ativos
                </button>
              </div>
            </td>
          </tr>
        `;
        return;
      }}

      stocks.forEach((s, idx) => {{
        const isSelected = s.ticker === selectedTicker;
        const tr = document.createElement('tr');
        const rowBg = isSelected ? 'bg-[#E6F4F1] border-l-4 border-[#00A887] font-bold' : (idx % 2 === 0 ? 'bg-white' : 'bg-[#FAFAF7]');
        tr.className = `cursor-pointer transition duration-150 hover:bg-[#F4F9F8] ${{rowBg}}`;
        tr.onclick = (e) => {{
          if (e.target.closest('button')) return;
          selectTicker(s.ticker);
          openDossierDrawer(s.ticker);
        }};

        // P/L e Run-Rate
        let rrStr = '';
        let rrColor = 'text-slate-500';
        if (s.pl_run_rate !== null && s.pl_run_rate !== undefined) {{
          rrStr = 'RR: ' + Number(s.pl_run_rate).toFixed(1) + 'x';
          if (s.pl !== null && s.pl > 0) {{
            if (s.pl_run_rate < s.pl * 0.85) rrColor = 'text-[#004B49] font-bold';
            else if (s.pl_run_rate > s.pl * 1.25) rrColor = 'text-amber-700 font-bold';
          }}
        }}

        // ROIC e ROE
        const roicDisplay = s.is_financial ? '<span class="text-[10px] text-slate-400 font-sans font-normal">N/A (Bancos)</span>' : formatPercent(s.roic);
        const roicColor = s.is_financial ? 'text-slate-400' : getColorRoic(s.roic);
        const roeDisplay = formatPercent(s.roe);
        const roeColor = getColorRoe(s.roe);

        // Dívida Líquida
        let debtDisplay = 'N/D';
        let debtClass = getColorDebt(s.div_liq_ebitda, s.is_financial);
        if (s.is_financial) {{
          debtDisplay = '<span class="text-[10px] text-[#004B49] font-semibold">Banco (Basileia)</span>';
        }} else if ((s.details && s.details.divida_liquida !== null && s.details.divida_liquida <= 0) || (s.div_liq_ebitda !== null && s.div_liq_ebitda < 0)) {{
          debtDisplay = '<span class="px-2 py-0.5 rounded-full text-[9px] font-bold bg-[#E6F4F1] text-[#004B49] border border-[#BCE5DC]">Caixa Líq. 🛡️</span>';
        }} else if (s.div_liq_ebitda !== null) {{
          debtDisplay = Number(s.div_liq_ebitda).toFixed(1) + 'x';
        }}

        // Score Badge
        const scoreBadgeClass = s.quality_score >= 80 
          ? 'bg-[#E6F4F1] text-[#004B49] border border-[#BCE5DC] font-bold' 
          : (s.quality_score >= 65 ? 'bg-amber-50 text-amber-900 border border-amber-300 font-bold' : 'bg-slate-50 text-slate-700 border border-slate-200');

        // Categorias atribuídas (máximo 5)
        const categories = getStockCategories(s);
        const tagsHtml = categories.map(c => `
          <button onclick="event.stopPropagation(); setFilter('${{c.id}}')" class="inline-flex items-center gap-1 px-1.5 py-0.5 rounded-full text-[9px] font-mono font-bold ${{c.bgClass}} hover:brightness-110 transition cursor-pointer" title="Filtrar por ${{c.label}}">
            <span>${{c.icon}}</span> <span>${{c.shortLabel || c.label}}</span>
          </button>
        `).join('');

        const evDisplay = s.is_financial 
          ? '<span class="text-[10px] text-slate-400 font-sans font-normal">N/A (Bancos)</span>' 
          : ((s.ev_ebitda !== null && s.ev_ebitda !== undefined && s.ev_ebitda > 0) ? formatMultiple(s.ev_ebitda) : 'N/D');

        const spreadStr = (s.ey_spread !== null && s.ey_spread !== undefined) 
          ? (s.ey_spread > 0 ? '+' : '') + s.ey_spread.toFixed(1) + '%' 
          : 'N/D';
        const spreadClass = getColorSpread(s.ey_spread);

        tr.innerHTML = `
          <td class="py-3.5 px-3 border-b border-[#E7E7E2]">
            <div class="flex items-center gap-2.5">
              ${{getStockLogoHtml(s.ticker, s.empresa, 'w-7 h-7')}}
              <div class="flex flex-col min-w-0">
                <div class="flex items-center gap-1.5 leading-none">
                  <span class="text-xs font-bold text-slate-900 tracking-wide font-mono">${{s.ticker}}</span>
                  <span class="text-[9px] px-1.5 py-0.2 rounded-full font-mono font-bold ${{s.is_latest_balanco ? 'bg-[#E6F4F1] text-[#004B49] border border-[#BCE5DC]' : 'bg-slate-100 text-slate-600 border border-slate-200'}}">${{s.tri_balanco || '2T26'}}</span>
                  ${{s.is_distorted ? '<span class="text-[8px] px-1 py-0.2 rounded bg-amber-100 text-amber-900 font-semibold" title="' + (s.distortion_label || 'Distorção Contábil') + '">Dist.</span>' : ''}}
                  <a href="empresa.html?ticker=${{s.ticker}}" onclick="event.stopPropagation();" class="text-slate-400 hover:text-[#00A887] transition p-0.5" title="Abrir dossiê de ${{s.ticker}}">
                    <svg class="w-3.5 h-3.5 stroke-[2] inline-block" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/></svg>
                  </a>
                </div>
                <div class="text-[11.5px] text-slate-600 font-sans font-medium truncate max-w-[150px] leading-tight mt-0.5" title="${{s.empresa}} - ${{s.setor || ''}}">${{s.empresa}}</div>
              </div>
            </div>
          </td>
          <td class="py-3.5 px-2 text-xs text-right font-mono font-bold text-slate-900 border-b border-[#E7E7E2]">${{formatCurrency(s.cotacao)}}</td>
          <td class="py-3.5 px-2 text-center border-b border-[#E7E7E2]">
            <span class="px-2.5 py-0.5 rounded-full font-bold text-[11px] ${{scoreBadgeClass}}" title="Moat Score: ${{s.quality_score.toFixed(1)}} / 92.5">
              ${{s.quality_score.toFixed(1)}}
            </span>
          </td>
          <td class="py-3.5 px-2.5 text-right font-mono border-b border-[#E7E7E2]">
            <div class="text-xs font-semibold ${{getColorPl(s.pl)}} leading-tight">${{formatMultiple(s.pl)}}</div>
            ${{rrStr ? '<div class="text-[9px] ' + rrColor + ' leading-none mt-0.5" title="P/L Run-Rate">' + rrStr + '</div>' : ''}}
          </td>
          <td class="py-3.5 px-2 text-xs text-right font-mono border-b border-[#E7E7E2] text-slate-800 font-medium">
            ${{evDisplay}}
          </td>
          <td class="py-3.5 px-2 text-xs text-right font-mono font-semibold border-b border-[#E7E7E2] ${{roicColor}}">${{roicDisplay}}</td>
          <td class="py-3.5 px-2 text-xs text-right font-mono font-semibold border-b border-[#E7E7E2] ${{roeColor}}">${{roeDisplay}}</td>
          <td class="py-3.5 px-2 text-xs text-right font-mono font-bold border-b border-[#E7E7E2] ${{getColorDy(s.div_yield)}}">${{formatPercent(s.div_yield)}}</td>
          <td class="py-3.5 px-2 text-xs text-right font-mono border-b border-[#E7E7E2] ${{debtClass}}">${{debtDisplay}}</td>
          <td class="py-3.5 px-2.5 text-xs text-right font-mono font-bold border-b border-[#E7E7E2] ${{spreadClass}}">
            ${{spreadStr}}
          </td>
          <td class="py-3.5 px-3 border-b border-[#E7E7E2]">
            <div class="flex flex-wrap items-center gap-1 max-w-[280px]">
              ${{tagsHtml}}
            </div>
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

      const padL = 70, padR = 30, padT = 35, padB = 55;
      const w = 1200, h = 700;
      const innerW = w - padL - padR;
      const innerH = h - padT - padB;

      const baseXMin = 0;
      const baseXMax = isPl ? 25.0 : 25.0;
      const baseYMin = 20.0;
      const baseYMax = 100.0;

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
        if (matrixBubbleMetric === 'fixed') return 6.5;
        if (matrixBubbleMetric === 'mcap') {{
          const v = (s.details && s.details.valor_mercado) || 0;
          return 5.0 + Math.sqrt(Math.max(0, v) / maxBubbleVal) * 14.0;
        }}
        if (matrixBubbleMetric === 'volume') {{
          const v = s.liq_2m || 0;
          return 5.0 + Math.sqrt(Math.max(0, v) / maxBubbleVal) * 14.0;
        }}
        return 6.5;
      }}

      // Limiares dos 4 Quadrantes Estratégicos 2x2
      const limiarQuality = 75.0;
      const limiarValuation = isPl ? 14.0 : 7.14;
      const yCross = scaleY(limiarQuality);
      const xCross = scaleX(limiarValuation);

      // Estrutura SVG com ClipPath para que o Zoom & Pan nunca transborde os eixos
      let svgHtml = `
        <defs>
          <clipPath id="matrixPlotArea">
            <rect x="${{padL}}" y="${{padT}}" width="${{innerW}}" height="${{innerH}}" rx="4" />
          </clipPath>
        </defs>

        <!-- ÁREA DO GRÁFICO RESTRITA PELO CLIPPATH -->
        <g clip-path="url(#matrixPlotArea)">
          <!-- Fundo Branco Base Clean -->
          <rect x="${{padL - 3000}}" y="${{padT - 3000}}" width="6000" height="6000" fill="#FFFFFF" />

          <!-- Linhas Divisórias dos 4 Quadrantes 2x2 -->
          <line x1="${{padL}}" y1="${{yCross}}" x2="${{padL + innerW}}" y2="${{yCross}}" stroke="#10B981" stroke-width="1.8" stroke-dasharray="6,4" opacity="0.45" />
          <line x1="${{xCross}}" y1="${{padT}}" x2="${{xCross}}" y2="${{padT + innerH}}" stroke="#64748B" stroke-width="1.8" stroke-dasharray="6,4" opacity="0.4" />

          <!-- Rótulos dos Quadrantes 2x2 (Watermarks Institucionais) -->
          <g class="pointer-events-none select-none">
            <!-- Q1: Superior Esquerdo -->
            <text x="${{padL + 18}}" y="${{padT + 24}}" fill="#059669" font-size="13" font-family="JetBrains Mono" font-weight="800" opacity="0.75">Q1: ALTA QUALIDADE &amp; VALUATION ATRATIVO</text>
            <text x="${{padL + 18}}" y="${{padT + 40}}" fill="#64748B" font-size="11" font-family="Inter" font-weight="600" opacity="0.7">Score &ge; 75 | ${{isPl ? 'P/L &le; 14x' : 'EY &ge; 7.1%'}}</text>

            <!-- Q2: Superior Direito -->
            <text x="${{padL + innerW - 18}}" y="${{padT + 24}}" text-anchor="end" fill="#0284C7" font-size="13" font-family="JetBrains Mono" font-weight="800" opacity="0.75">Q2: QUALIDADE COM PRÊMIO DE CRESCIMENTO</text>
            <text x="${{padL + innerW - 18}}" y="${{padT + 40}}" text-anchor="end" fill="#64748B" font-size="11" font-family="Inter" font-weight="600" opacity="0.7">Score &ge; 75 | ${{isPl ? 'P/L &gt; 14x' : 'EY &lt; 7.1%'}}</text>

            <!-- Q3: Inferior Esquerdo -->
            <text x="${{padL + 18}}" y="${{padT + innerH - 30}}" fill="#D97706" font-size="13" font-family="JetBrains Mono" font-weight="800" opacity="0.75">Q3: MÚLTIPLOS BAIXOS (ATENÇÃO A MOAT)</text>
            <text x="${{padL + 18}}" y="${{padT + innerH - 14}}" fill="#64748B" font-size="11" font-family="Inter" font-weight="600" opacity="0.7">Score &lt; 75 | ${{isPl ? 'P/L &le; 14x' : 'EY &ge; 7.1%'}}</text>

            <!-- Q4: Inferior Direito -->
            <text x="${{padL + innerW - 18}}" y="${{padT + innerH - 30}}" text-anchor="end" fill="#E11D48" font-size="13" font-family="JetBrains Mono" font-weight="800" opacity="0.75">Q4: MÚLTIPLOS ELEVADOS &amp; BAIXO MOAT</text>
            <text x="${{padL + innerW - 18}}" y="${{padT + innerH - 14}}" text-anchor="end" fill="#64748B" font-size="11" font-family="Inter" font-weight="600" opacity="0.7">Score &lt; 75 | ${{isPl ? 'P/L &gt; 14x' : 'EY &lt; 7.1%'}}</text>
          </g>
        </g>
      `;

      // Eixos e Ticks
      svgHtml += `
        <!-- Eixos Principais -->
        <line x1="${{padL}}" y1="${{padT + innerH}}" x2="${{padL + innerW}}" y2="${{padT + innerH}}" stroke="#94A3B8" stroke-width="2" />
        <line x1="${{padL}}" y1="${{padT}}" x2="${{padL}}" y2="${{padT + innerH}}" stroke="#94A3B8" stroke-width="2" />

        <!-- Legenda dos Eixos com Fonte Ampliada -->
        <text x="${{padL + innerW/2}}" y="${{h - 14}}" text-anchor="middle" fill="#0F172A" font-size="16" font-family="JetBrains Mono" font-weight="800">
          ${{isPl ? 'Preço sobre Lucro (P/L) [← Mais Barato | Mais Caro →]' : 'Earnings Yield (% a.a.) [← Mais Caro | Maior Retorno/Barato →]'}}
        </text>
        <text x="24" y="${{padT + innerH/2}}" text-anchor="middle" fill="#0F172A" font-size="16" font-family="JetBrains Mono" font-weight="800" transform="rotate(-90 24 ${{padT + innerH/2}})">
          Quality Score (0 a 100) [↑ Maior Excelência]
        </text>
      `;

      // Gerar Grid Ticks dinâmicos
      // Y Ticks (Quality Score: 20 a 100)
      const yTickVals = [20, 30, 40, 50, 60, 70, 75, 80, 90, 100].filter(v => v >= curYMin - 2 && v <= curYMax + 2);
      yTickVals.forEach(v => {{
        const ty = scaleY(v);
        if (ty >= padT && ty <= padT + innerH) {{
          const isLimiar = (v === 75);
          svgHtml += `
            <line x1="${{padL}}" y1="${{ty}}" x2="${{padL + innerW}}" y2="${{ty}}" stroke="${{isLimiar ? '#A7F3D0' : '#E2E8F0'}}" stroke-width="${{isLimiar ? 1.5 : 1}}" stroke-dasharray="${{isLimiar ? '4,4' : '2,2'}}" />
            <text x="${{padL - 10}}" y="${{ty + 5}}" text-anchor="end" fill="${{isLimiar ? '#059669' : '#475569'}}" font-size="14" font-family="JetBrains Mono" font-weight="${{isLimiar ? '900' : '700'}}">${{v}}</text>
          `;
        }}
      }});

      // X Ticks
      const xSpan = curXMax - curXMin;
      let xStep = 5;
      if (xSpan <= 8) xStep = 1;
      else if (xSpan <= 15) xStep = 2;
      else if (xSpan <= 25) xStep = 5;

      const firstTick = Math.ceil(curXMin / xStep) * xStep;
      for (let v = firstTick; v <= curXMax; v += xStep) {{
        const tx = scaleX(v);
        if (tx >= padL && tx <= padL + innerW) {{
          svgHtml += `
            <line x1="${{tx}}" y1="${{padT}}" x2="${{tx}}" y2="${{padT + innerH}}" stroke="#E2E8F0" stroke-width="1" stroke-dasharray="2,2" />
            <text x="${{tx}}" y="${{padT + innerH + 24}}" text-anchor="middle" fill="#475569" font-size="14" font-family="JetBrains Mono" font-weight="700">${{v}}${{isPl ? 'x' : '%'}}</text>
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

        // Modo 0: Valuation & Múltiplos
        if (matrixColorMode === 'asymmetry') {{
          if (s.entry_tag === 'ASSIMETRIA_FAVORAVEL') {{
            return {{ fill: '#10B981', stroke: '#6EE7B7' }}; // 🟢 Verde Esmeralda: Múltiplos Descontados
          }}
          if (s.entry_tag === 'ESTICADA') {{
            return {{ fill: '#EF4444', stroke: '#FCA5A5' }}; // 🔴 Vermelho: Múltiplos Elevados
          }}
          return {{ fill: '#F59E0B', stroke: '#FDE68A' }};   // 🟡 Âmbar: Valuation em Linha
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

        // Modo 4: Quadrantes Estratégicos 2x2 (quadrant)
        if (matrixColorMode === 'quadrant') {{
          const isHighQuality = (s.quality_score || 0) >= 75;
          const isLowPl = isPl ? (s.pl <= 14.0) : (s.earnings_yield_pct >= 7.14);
          if (isHighQuality && isLowPl) return {{ fill: '#10B981', stroke: '#6EE7B7' }}; // Q1 Verde Esmeralda (Alta Qualidade + Múltiplos Baixos)
          if (isHighQuality && !isLowPl) return {{ fill: '#0284C7', stroke: '#7DD3FC' }}; // Q2 Azul Celeste (Alta Qualidade + Múltiplos Altos)
          if (!isHighQuality && isLowPl) return {{ fill: '#F59E0B', stroke: '#FDE68A' }}; // Q3 Âmbar (Baixo Moat + Múltiplos Baixos)
          return {{ fill: '#EF4444', stroke: '#FCA5A5' }}; // Q4 Vermelho (Baixo Moat + Múltiplos Altos)
        }}
      }}

      // Classificar empresas por relevância e liquidez para smart labeling adaptativo
      const sortedByRelevance = [...stocks].sort((a, b) => {{
        const valA = ((a.details && a.details.valor_mercado) || a.liq_2m || 0);
        const valB = ((b.details && b.details.valor_mercado) || b.liq_2m || 0);
        return valB - valA;
      }});

      let labelMax = 25;
      if (matrixZoom >= 3.0) labelMax = 999;
      else if (matrixZoom >= 2.0) labelMax = 120;
      else if (matrixZoom >= 1.5) labelMax = 65;
      else if (matrixZoom >= 1.2) labelMax = 40;

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
        if (s.div_yield && s.div_yield > 0.06) nDiv++;

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
            circle.setAttribute('stroke-width', isSelected ? '3' : '1.3');
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
        const isNearTop = (cy - r - 42 < padT);

        if (isSelected) {{
          const rectY = isNearTop ? (cy + r + 10) : (cy - r - 44);
          const text1Y = isNearTop ? (cy + r + 26) : (cy - r - 28);
          const text2Y = isNearTop ? (cy + r + 39) : (cy - r - 14);

          g.innerHTML = `
            ${{warningRingHtml}}
            <circle cx="${{cx}}" cy="${{cy}}" r="${{r + 9}}" fill="none" stroke="#F59E0B" stroke-width="3" class="animate-pulse pointer-events-none" />
            <circle cx="${{cx}}" cy="${{cy}}" r="${{r}}" fill="${{fillColor}}" stroke="#FFFFFF" stroke-width="3" class="main-bubble" />
            <g class="pointer-events-none select-none">
              <rect x="${{cx - 68}}" y="${{rectY}}" width="136" height="34" rx="6" fill="#080A0F" fill-opacity="0.95" stroke="#F59E0B" stroke-width="2" />
              <text x="${{cx}}" y="${{text1Y}}" text-anchor="middle" fill="#FBBF24" font-size="14" font-family="JetBrains Mono" font-weight="900">📍 ${{s.ticker}}</text>
              <text x="${{cx}}" y="${{text2Y}}" text-anchor="middle" fill="#F8FAFC" font-size="11.5" font-family="Inter" font-weight="700">${{shortName}}</text>
            </g>
          `;
          selectedGroup = g;
        }} else {{
          let labelHtml = '';
          if (shouldShowLabel) {{
            const lbl1Y = isNearTop ? (cy + r + 18) : (cy - r - 16);
            const lbl2Y = isNearTop ? (cy + r + 32) : (cy - r - 2);

            labelHtml = `
              <g class="pointer-events-none select-none">
                <text x="${{cx}}" y="${{lbl1Y}}" text-anchor="middle" fill="#0F172A" font-size="14" font-family="JetBrains Mono" font-weight="800" stroke="#FFFFFF" stroke-width="3.5" paint-order="stroke fill" stroke-linejoin="round">${{s.ticker}}</text>
                <text x="${{cx}}" y="${{lbl2Y}}" text-anchor="middle" fill="#0284C7" font-size="11.5" font-family="Inter" font-weight="700" stroke="#FFFFFF" stroke-width="2.8" paint-order="stroke fill" stroke-linejoin="round">${{shortName}}</text>
              </g>
            `;
          }}
          g.innerHTML = `
            ${{warningRingHtml}}
            <circle cx="${{cx}}" cy="${{cy}}" r="${{r}}" fill="${{fillColor}}" fill-opacity="0.88" stroke="${{strokeColor}}" stroke-width="1.3" class="main-bubble transition-transform" />
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
          <div class="flex items-center justify-between text-xs py-0.5">
            <span class="inline-flex items-center gap-2"><span class="w-3 h-3 rounded-full bg-emerald-500"></span><span class="text-emerald-900 font-bold">Múltiplos Descontados</span></span>
          </div>
          <div class="flex items-center justify-between text-xs py-0.5">
            <span class="inline-flex items-center gap-2"><span class="w-3 h-3 rounded-full bg-amber-500"></span><span class="text-amber-900 font-semibold">Valuation em Linha</span></span>
          </div>
          <div class="flex items-center justify-between text-xs py-0.5">
            <span class="inline-flex items-center gap-2"><span class="w-3 h-3 rounded-full bg-rose-500"></span><span class="text-rose-900 font-bold">Múltiplos Elevados</span></span>
          </div>
          <div class="flex items-center justify-between text-xs py-0.5">
            <span class="inline-flex items-center gap-2"><span class="w-3 h-3 rounded-full bg-red-900"></span><span class="text-red-900 font-semibold">Prejuízo</span></span>
          </div>
        `;
      }} else if (matrixColorMode === 'quadrant') {{
        leg.innerHTML = `
          <div class="flex items-center justify-between text-xs py-0.5">
            <span class="inline-flex items-center gap-2"><span class="w-3 h-3 rounded-full bg-emerald-500"></span><span class="text-emerald-900 font-bold">Q1: Alta Qualidade / Barato</span></span>
          </div>
          <div class="flex items-center justify-between text-xs py-0.5">
            <span class="inline-flex items-center gap-2"><span class="w-3 h-3 rounded-full bg-sky-500"></span><span class="text-sky-900 font-semibold">Q2: Qualidade / Prêmio</span></span>
          </div>
          <div class="flex items-center justify-between text-xs py-0.5">
            <span class="inline-flex items-center gap-2"><span class="w-3 h-3 rounded-full bg-amber-500"></span><span class="text-amber-900 font-semibold">Q3: Múltiplos Baixos / Risco</span></span>
          </div>
          <div class="flex items-center justify-between text-xs py-0.5">
            <span class="inline-flex items-center gap-2"><span class="w-3 h-3 rounded-full bg-rose-500"></span><span class="text-rose-900 font-bold">Q4: Preço Caro / Baixo Moat</span></span>
          </div>
        `;
      }} else if (matrixColorMode === 'momentum') {{
        leg.innerHTML = `
          <div class="flex items-center justify-between text-xs py-0.5">
            <span class="inline-flex items-center gap-2"><span class="w-3 h-3 rounded-full bg-emerald-500"></span><span class="text-emerald-900 font-bold">Acelerando (&ge; +15%)</span></span>
          </div>
          <div class="flex items-center justify-between text-xs py-0.5">
            <span class="inline-flex items-center gap-2"><span class="w-3 h-3 rounded-full bg-slate-400"></span><span class="text-slate-800 font-medium">Estável</span></span>
          </div>
          <div class="flex items-center justify-between text-xs py-0.5">
            <span class="inline-flex items-center gap-2"><span class="w-3 h-3 rounded-full bg-orange-500"></span><span class="text-orange-900 font-semibold">Comprimindo (&le; -20%)</span></span>
          </div>
          <div class="flex items-center justify-between text-xs py-0.5">
            <span class="inline-flex items-center gap-2"><span class="w-3 h-3 rounded-full bg-rose-500"></span><span class="text-rose-900 font-bold">Prejuízo 2T26</span></span>
          </div>
        `;
      }} else if (matrixColorMode === 'dividend') {{
        leg.innerHTML = `
          <div class="flex items-center justify-between text-xs py-0.5">
            <span class="inline-flex items-center gap-2"><span class="w-3 h-3 rounded-full bg-amber-500"></span><span class="text-amber-900 font-bold">DY &ge; 10%</span></span>
          </div>
          <div class="flex items-center justify-between text-xs py-0.5">
            <span class="inline-flex items-center gap-2"><span class="w-3 h-3 rounded-full bg-emerald-500"></span><span class="text-emerald-900 font-semibold">6% a 10%</span></span>
          </div>
          <div class="flex items-center justify-between text-xs py-0.5">
            <span class="inline-flex items-center gap-2"><span class="w-3 h-3 rounded-full bg-sky-400"></span><span class="text-sky-900 font-semibold">3% a 6%</span></span>
          </div>
          <div class="flex items-center justify-between text-xs py-0.5">
            <span class="inline-flex items-center gap-2"><span class="w-3 h-3 rounded-full bg-slate-400"></span><span class="text-slate-700">&lt; 3%</span></span>
          </div>
        `;
      }} else if (matrixColorMode === 'sector') {{
        leg.innerHTML = `
          <div class="flex items-center justify-between text-xs py-0.5">
            <span class="inline-flex items-center gap-2"><span class="w-3 h-3 rounded-full bg-sky-400"></span><span class="text-sky-900 font-semibold">Financeiro</span></span>
          </div>
          <div class="flex items-center justify-between text-xs py-0.5">
            <span class="inline-flex items-center gap-2"><span class="w-3 h-3 rounded-full bg-emerald-500"></span><span class="text-emerald-900 font-semibold">Elétricas/Util</span></span>
          </div>
          <div class="flex items-center justify-between text-xs py-0.5">
            <span class="inline-flex items-center gap-2"><span class="w-3 h-3 rounded-full bg-amber-500"></span><span class="text-amber-900 font-semibold">Commodities</span></span>
          </div>
          <div class="flex items-center justify-between text-xs py-0.5">
            <span class="inline-flex items-center gap-2"><span class="w-3 h-3 rounded-full bg-pink-500"></span><span class="text-pink-900 font-semibold">Consumo</span></span>
          </div>
          <div class="flex items-center justify-between text-xs py-0.5">
            <span class="inline-flex items-center gap-2"><span class="w-3 h-3 rounded-full bg-purple-500"></span><span class="text-purple-900 font-semibold">Indústria</span></span>
          </div>
        `;
      }}
    }}

    function showMatrixTooltip(e, s) {{
      const tt = document.getElementById('matrixTooltip');
      if (!tt) return;
      const spreadStr = s.ey_spread !== null ? (s.ey_spread > 0 ? '+' : '') + s.ey_spread.toFixed(1) + '%' : 'N/D';
      const volStr = formatBillions(s.liq_2m).replace('R$ ', '');
      const mcapStr = s.details && s.details.valor_mercado ? formatBillions(s.details.valor_mercado) : 'N/D';

      // Identificação do Quadrante 2x2
      const isHighQuality = (s.quality_score || 0) >= 75;
      const isLowPl = isPl ? (s.pl <= 14.0) : (s.earnings_yield_pct >= 7.14);
      let quadBadge = '';
      if (s.entry_tag === 'PASSIVO_DESCOBERTO') {{
        quadBadge = '<span class="px-2 py-0.5 rounded bg-rose-100 text-rose-900 border border-rose-300 font-bold text-[10px]">🛑 Passivo Descoberto</span>';
      }} else if (isHighQuality && isLowPl) {{
        quadBadge = '<span class="px-2 py-0.5 rounded bg-emerald-100 text-emerald-900 border border-emerald-300 font-bold text-[10px]">💎 Q1: Alta Qualidade &amp; Valuation Atrativo</span>';
      }} else if (isHighQuality && !isLowPl) {{
        quadBadge = '<span class="px-2 py-0.5 rounded bg-sky-100 text-sky-900 border border-sky-300 font-bold text-[10px]">🚀 Q2: Qualidade com Prêmio</span>';
      }} else if (!isHighQuality && isLowPl) {{
        quadBadge = '<span class="px-2 py-0.5 rounded bg-amber-100 text-amber-900 border border-amber-300 font-bold text-[10px]">⚖️ Q3: Múltiplos Baixos (Atenção a Moat)</span>';
      }} else {{
        quadBadge = '<span class="px-2 py-0.5 rounded bg-rose-100 text-rose-900 border border-rose-300 font-bold text-[10px]">⚠️ Q4: Múltiplos Elevados / Baixo Moat</span>';
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

      const expPL = calcFairPL(s.quality_score);

      tt.innerHTML = `
        <div class="font-bold text-slate-900 text-sm flex items-center justify-between gap-2">
          <span>${{s.ticker}} <span class="font-normal text-slate-600 font-sans text-xs">(${{s.empresa}})</span></span>
          <div class="flex items-center gap-1.5">
            ${{quadBadge}}
            <span class="text-[10px] font-sans px-1.5 py-0.5 rounded bg-slate-100 text-slate-700 font-medium border border-slate-200">${{s.setor}}</span>
          </div>
        </div>
        <div class="text-[11px] text-slate-600 font-sans my-1 border-b border-slate-200 pb-1">
          Cap: <b class="text-slate-900 font-bold">${{mcapStr}}</b> • Vol: <b class="text-slate-900 font-bold">R$ ${{volStr}}/d</b> • Bal: <b class="text-slate-800 font-semibold">${{s.ult_balanco}}</b>
        </div>
        <div class="text-slate-700">• Quality Score: <b class="text-slate-900 font-bold">${{s.quality_score.toFixed(1)}}/100</b> (${{s.quality_tier.split(':')[0]}})</div>
        <div class="text-slate-700">• P/L (12m): <b class="text-slate-900 font-bold">${{formatMultiple(s.pl)}}</b> (P/L Teórico: <b class="text-emerald-800 font-bold">${{expPL.toFixed(1)}}x</b>)</div>
        <div class="text-slate-700">• Momento 2T26: ${{momTag}}</div>
        <div class="text-slate-700">• Earnings Yield: <b class="text-slate-900 font-bold">${{formatPercent(s.earnings_yield_pct/100)}}</b> (Spread NTN-B: <b class="${{getColorSpread(s.ey_spread)}}">${{spreadStr}}</b>)</div>
        <div class="text-slate-700">• ROIC: <b class="text-slate-900 font-bold">${{s.is_financial ? 'N/A' : formatPercent(s.roic)}}</b> | ROE: <b class="text-slate-900 font-bold">${{formatPercent(s.roe)}}</b> | DY: <b class="text-emerald-800 font-bold">${{formatPercent(s.div_yield)}}</b></div>
        <div class="mt-1 text-[11px] font-sans font-semibold text-emerald-800">${{s.entry_status}}</div>
        ${{warningBanner}}
        <div class="mt-2 pt-1.5 border-t border-slate-200 flex items-center justify-between text-[10px] text-slate-500 font-sans">
          <span>Clique p/ selecionar ativo</span>
          <span class="text-emerald-700 font-bold font-mono">Ver Dossiê ➜</span>
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

    function scrollToMatrixFilters() {{
      const sb = document.getElementById('matrixSidebar');
      if (sb) {{
        sb.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
      }}
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
          const baseXMax = isPl ? 25.0 : 25.0;
          const baseXMin = 0;
          const baseYMax = 100.0;
          const baseYMin = 20.0;

          const padL = 70, padR = 30, padT = 35, padB = 55;
          const innerW = 1200 - padL - padR;
          const innerH = 700 - padT - padB;

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

      // Touch events para suporte completo a smartphones e tablets
      svg.addEventListener('touchstart', (e) => {{
        if (e.touches.length === 1) {{
          isPanning = true;
          hasMovedDuringPan = false;
          panStartX = e.touches[0].clientX;
          panStartY = e.touches[0].clientY;
          panStartCenterX = matrixCenterX;
          panStartCenterY = matrixCenterY;
        }}
      }}, {{ passive: true }});

      window.addEventListener('touchmove', (e) => {{
        if (!isPanning || e.touches.length !== 1) return;
        const dx = e.touches[0].clientX - panStartX;
        const dy = e.touches[0].clientY - panStartY;

        if (Math.abs(dx) > 4 || Math.abs(dy) > 4) {{
          hasMovedDuringPan = true;
          const isPl = currentXMetric === 'pl';
          const baseXMax = isPl ? 25.0 : 25.0;
          const baseXMin = 0;
          const baseYMax = 100.0;
          const baseYMin = 20.0;

          const padL = 70, padR = 30, padT = 35, padB = 55;
          const innerW = 1200 - padL - padR;
          const innerH = 700 - padT - padB;

          const spanX = (baseXMax - baseXMin) / matrixZoom;
          const spanY = (baseYMax - baseYMin) / matrixZoom;

          const dataDx = (dx / innerW) * spanX;
          const dataDy = (dy / innerH) * spanY;

          matrixCenterX = panStartCenterX - dataDx;
          matrixCenterY = panStartCenterY + dataDy;

          renderMatrix();
        }}
      }}, {{ passive: true }});

      window.addEventListener('touchend', () => {{
        if (isPanning) isPanning = false;
      }});

      svg.addEventListener('wheel', (e) => {{
        e.preventDefault();
        const factor = e.deltaY < 0 ? 1.15 : 0.87;
        zoomMatrixAt(factor, e.clientX, e.clientY);
      }}, {{ passive: false }});
    }}

    // RENDERIZADOR DE GAUGES ANALÓGICOS BLOOMBERG CALIBRADOS COM BENCHMARKS
    function renderAnalogGauge(svgId, val, minVal, maxVal, label, options = {{}}) {{
      const svg = document.getElementById(svgId);
      if (!svg) return;

      if (options.isFinancial) {{
        svg.innerHTML = `
          <g transform="translate(80, 48)">
            <path d="M -50 0 A 50 50 0 0 1 50 0" fill="none" stroke="#E2E8F0" stroke-width="7" stroke-linecap="round" />
            <text x="0" y="-14" text-anchor="middle" fill="#0284C7" font-size="11" font-family="JetBrains Mono" font-weight="700">BANCOS</text>
            <text x="0" y="0" text-anchor="middle" fill="#64748B" font-size="8.5" font-family="Inter">Intermediação</text>
            <text x="0" y="14" text-anchor="middle" fill="#059669" font-size="9" font-family="JetBrains Mono" font-weight="bold">Basileia Ok</text>
          </g>
          <text x="80" y="73" text-anchor="middle" fill="#334155" font-size="10" font-family="JetBrains Mono" font-weight="700" letter-spacing="0.5">${{label.toUpperCase()}}</text>
          <text x="80" y="85" text-anchor="middle" fill="#64748B" font-size="8.5" font-family="Inter" font-weight="500">Ref: Basileia &gt; 11%</text>
        `;
        return;
      }}

      if (val === null || val === undefined || isNaN(val)) {{
        svg.innerHTML = `
          <g transform="translate(80, 48)">
            <path d="M -50 0 A 50 50 0 0 1 50 0" fill="none" stroke="#E2E8F0" stroke-width="7" stroke-linecap="round" />
            <text x="0" y="0" text-anchor="middle" fill="#94A3B8" font-size="11" font-family="JetBrains Mono" font-weight="bold">N/D</text>
          </g>
          <text x="80" y="73" text-anchor="middle" fill="#334155" font-size="10" font-family="JetBrains Mono" font-weight="700" letter-spacing="0.5">${{label.toUpperCase()}}</text>
          <text x="80" y="85" text-anchor="middle" fill="#64748B" font-size="8.5" font-family="Inter" font-weight="500">${{options.refText || ''}}</text>
        `;
        return;
      }}

      const norm = Math.max(0, Math.min(1, (val - minVal) / (maxVal - minVal)));
      const angleDeg = -180 + norm * 180;
      const angleRad = (angleDeg * Math.PI) / 180;

      const r = 50;
      const needleLen = 38;
      const nx = needleLen * Math.cos(angleRad);
      const ny = needleLen * Math.sin(angleRad);

      let valText = options.displayVal || (options.isPercent ? (val * 100).toFixed(1) + '%' : (options.isMultiple ? val.toFixed(1) + 'x' : val.toFixed(1)));
      if (options.isSpread && !options.displayVal) valText = (val > 0 ? '+' : '') + val.toFixed(1) + '%';
      if (options.isDebt && val < 0) valText = 'Caixa Líq.';

      // Cor semântica do texto
      let fillColor = '#059669';
      if (options.isDebt) {{
        fillColor = val <= 1.0 ? '#059669' : (val <= 2.2 ? '#D97706' : '#DC2626');
      }} else if (options.isSpread) {{
        fillColor = val >= 2.0 ? '#059669' : (val >= 0 ? '#D97706' : '#DC2626');
      }} else {{
        // ROIC / ROE: >= 15% é Verde Top, 10-15% Neutro, < 10% Alerta
        fillColor = val >= 0.15 ? '#059669' : (val >= 0.10 ? '#D97706' : '#DC2626');
      }}

      // Referência visual no arco (Tick mark)
      let refTickHtml = '';
      if (options.refVal !== undefined && options.refVal !== null) {{
        const refNorm = Math.max(0, Math.min(1, (options.refVal - minVal) / (maxVal - minVal)));
        const refDeg = -180 + refNorm * 180;
        const refRad = (refDeg * Math.PI) / 180;
        const rx1 = (r - 6) * Math.cos(refRad);
        const ry1 = (r - 6) * Math.sin(refRad);
        const rx2 = (r + 6) * Math.cos(refRad);
        const ry2 = (r + 6) * Math.sin(refRad);
        refTickHtml = `<line x1="${{rx1.toFixed(1)}}" y1="${{ry1.toFixed(1)}}" x2="${{rx2.toFixed(1)}}" y2="${{ry2.toFixed(1)}}" stroke="#334155" stroke-width="2" stroke-linecap="round" opacity="0.85" />`;
      }}

      // Gradiente semântico: Se for Dívida, inverte! (Verde na esquerda/Caixa Líquido e Vermelho na direita/Dívida alta)
      const gradStops = options.isDebt ? `
        <stop offset="0%" stop-color="#059669" />
        <stop offset="35%" stop-color="#10B981" />
        <stop offset="65%" stop-color="#F59E0B" />
        <stop offset="100%" stop-color="#EF4444" />
      ` : `
        <stop offset="0%" stop-color="#EF4444" />
        <stop offset="40%" stop-color="#F59E0B" />
        <stop offset="70%" stop-color="#10B981" />
        <stop offset="100%" stop-color="#059669" />
      `;

      svg.innerHTML = `
        <defs>
          <linearGradient id="gaugeGrad_${{svgId}}" x1="0" y1="0" x2="1" y2="0">
            ${{gradStops}}
          </linearGradient>
        </defs>
        <g transform="translate(80, 48)">
          <path d="M -${{r}} 0 A ${{r}} ${{r}} 0 0 1 ${{r}} 0" fill="none" stroke="#E2E8F0" stroke-width="6.5" stroke-linecap="round" />
          <path d="M -${{r}} 0 A ${{r}} ${{r}} 0 0 1 ${{r}} 0" fill="none" stroke="url(#gaugeGrad_${{svgId}})" stroke-width="6.5" stroke-linecap="round" opacity="0.9" />
          ${{refTickHtml}}
          <line x1="0" y1="0" x2="${{nx.toFixed(1)}}" y2="${{ny.toFixed(1)}}" stroke="#0F172A" stroke-width="2.5" stroke-linecap="round" />
          <circle cx="0" cy="0" r="4" fill="#0F172A" />
          <circle cx="0" cy="0" r="1.5" fill="#FFFFFF" />
          <text x="0" y="16" text-anchor="middle" fill="${{fillColor}}" font-size="12" font-family="JetBrains Mono" font-weight="800">${{valText}}</text>
        </g>
        <text x="80" y="73" text-anchor="middle" fill="#334155" font-size="10" font-family="JetBrains Mono" font-weight="700" letter-spacing="0.5">${{label.toUpperCase()}}</text>
        <text x="80" y="85" text-anchor="middle" fill="#64748B" font-size="8.5" font-family="Inter" font-weight="500">${{options.refText || ''}}</text>
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
      const headScoreColor = s.quality_score >= 80 ? 'bg-emerald-100 text-emerald-900 border-emerald-300 font-bold' : (s.quality_score >= 65 ? 'bg-amber-100 text-amber-900 border-amber-300 font-bold' : (s.quality_score < 50 ? 'bg-rose-100 text-rose-900 border-rose-300 font-bold' : 'bg-slate-100 text-slate-800 border-slate-300 font-bold'));

      document.getElementById('diagHeaderCard').innerHTML = `
        <div class="flex justify-between items-start gap-3">
          <div class="flex items-center gap-3">
            ${{getStockLogoHtml(s.ticker, s.empresa, 'w-11 h-11')}}
            <div>
              <div class="text-2xl font-bold font-mono text-slate-900 tracking-tight flex items-center gap-2">
                <span>${{s.ticker}}</span>
                <span class="text-xs px-2.5 py-0.5 rounded-full font-sans font-bold ${{s.is_latest_balanco ? 'bg-emerald-100 text-emerald-900 border border-emerald-300' : 'bg-slate-100 text-slate-800 border border-slate-300'}}">
                  ${{s.tri_balanco}}
                </span>
              </div>
              <div class="text-sm font-bold text-slate-900 truncate max-w-[280px] mt-0.5">${{s.empresa}}</div>
              <div class="text-xs text-slate-600 font-sans mt-0.5 font-medium">${{s.is_financial ? 'Setor Financeiro' : (s.setor || 'Geral')}} • Cotação: <b class="text-slate-900 font-mono font-bold">${{formatCurrency(s.cotacao)}}</b> • Liq: ${{volStr}}/d</div>
            </div>
          </div>
          <div class="flex flex-col items-end gap-1.5">
            <span class="px-3 py-1 rounded-full font-mono font-bold text-xs sm:text-sm border ${{headScoreColor}} shadow-2xs flex items-center gap-1.5">
              <span>SCORE ${{s.quality_score.toFixed(1)}}</span>
              <span class="text-[10px] font-mono opacity-85">• ${{s.quality_score >= 80 ? 'Tier 1 (Wide Moat)' : (s.quality_score >= 65 ? 'Tier 2 (Narrow Moat)' : 'Tier 3 (No Moat)')}}</span>
            </span>
            <div class="text-[11px] font-mono text-slate-600 font-medium mt-0.5">
              P/L Teórico: <b class="text-slate-900 font-bold">${{formatMultiple(calcFairPL(s.quality_score))}}</b>
            </div>
          </div>
        </div>

        <!-- Rótulos de Categorias Institucionais Munger (Multi-Enquadramento) -->
        <div class="mt-3 pt-2.5 border-t border-slate-200 flex flex-wrap items-center gap-1.5">
          <span class="text-[11px] font-mono text-slate-600 uppercase tracking-wider font-semibold mr-0.5">Enquadramentos:</span>
          ${{catBadgesHtml}}
        </div>
      `;

      // Renderizar os 3 Semicircular Gauges Bloomberg Calibrados com Benchmarks
      const gaugeMetricVal = s.is_financial ? (s.roe !== null ? s.roe : 0) : (s.roic !== null ? s.roic : (s.roe || 0));
      const gaugeMetricLabel = s.is_financial ? 'ROE do Acionista' : 'ROIC Operacional';
      const gaugeMetricRef = s.is_financial ? 'Ref ROE: ≥ 15%' : 'Ref ROIC: ≥ 15%';
      renderAnalogGauge('gaugeRoe', gaugeMetricVal, 0.0, 0.35, gaugeMetricLabel, {{
        isPercent: true,
        displayVal: formatPercent(gaugeMetricVal),
        refVal: 0.15,
        refText: gaugeMetricRef
      }});

      renderAnalogGauge('gaugeDebt', s.div_liq_ebitda, -1.0, 3.5, 'Dív. Líq./EBITDA', {{
        isDebt: true,
        isFinancial: s.is_financial,
        refVal: 2.0,
        refText: 'Teto: 2.0x • Caixa = Top',
        displayVal: s.is_financial ? 'N/A' : (s.div_liq_ebitda !== null ? (s.div_liq_ebitda < 0 ? 'Caixa Líq.' : s.div_liq_ebitda.toFixed(2) + 'x') : 'N/D')
      }});

      renderAnalogGauge('gaugeSpread', s.ey_spread, -4.0, 10.0, 'Spread NTN-B', {{
        isSpread: true,
        refVal: 0.0,
        refText: 'Prêmio Real: > 0%',
        displayVal: s.ey_spread !== null ? (s.ey_spread > 0 ? '+' : '') + s.ey_spread.toFixed(1) + '%' : 'N/D'
      }});

      // Radar Polar SVG
      renderPolarRadar(s);

      // KPI Grid com Distinção Rigorosa entre ROIC e ROE
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
            <span class="info-badge cursor-pointer" data-tooltip="roic">ⓘ</span>
          </div>
          <div class="text-sm font-bold ${{roicColor}} mt-0.5">${{s.is_financial ? 'N/A (Bancos)' : formatPercent(s.roic)}}</div>
          <div class="text-[9px] text-slate-500 font-sans mt-0.5">${{s.is_financial ? 'Inaplicável a bancos' : 'Capital Investido'}}</div>
        </div>
        <div class="glass-card rounded-xl border border-slate-200 p-2.5 text-center">
          <div class="text-[10px] text-slate-700 uppercase font-bold flex items-center justify-center gap-1">
            <span>ROE (do Acionista)</span>
            <span class="info-badge cursor-pointer" data-tooltip="roe">ⓘ</span>
          </div>
          <div class="text-sm font-bold ${{roeColor}} mt-0.5">${{formatPercent(s.roe)}}</div>
          <div class="text-[9px] text-slate-500 font-sans mt-0.5">Retorno s/ Patrimônio</div>
        </div>
        <div class="glass-card rounded-xl border border-slate-200 p-2.5 text-center">
          <div class="text-[10px] text-slate-700 uppercase font-bold flex items-center justify-center gap-1">
            <span>Spread NTN-B</span>
            <span class="info-badge cursor-pointer" data-tooltip="ey_spread">ⓘ</span>
          </div>
          <div class="text-sm font-bold ${{spreadColor}} mt-0.5">${{spreadStr}}</div>
          <div class="text-[9px] text-slate-500 font-sans mt-0.5">Ref: 6,5% a.a.</div>
        </div>
        <div class="glass-card rounded-xl border border-slate-200 p-2.5 text-center">
          <div class="text-[10px] text-slate-700 uppercase font-bold flex items-center justify-center gap-1">
            <span>Dív.Líq / EBITDA</span>
            <span class="info-badge cursor-pointer" data-tooltip="debt">ⓘ</span>
          </div>
          <div class="text-sm font-bold ${{debtColor}} mt-0.5">${{debtStr}}</div>
          <div class="text-[9px] text-slate-500 font-sans mt-0.5">${{s.is_financial ? 'Regulação Bacen' : 'Solvência Auditada'}}</div>
        </div>
        <div class="glass-card rounded-xl border border-slate-200 p-2.5 text-center">
          <div class="text-[10px] text-slate-700 uppercase font-bold flex items-center justify-center gap-1">
            <span>Margem Líq.</span>
            <span class="info-badge cursor-pointer" data-tooltip="mrg_liq">ⓘ</span>
          </div>
          <div class="text-sm font-bold ${{mrgColor}} mt-0.5">${{formatPercent(s.mrg_liq)}}</div>
          <div class="text-[9px] text-slate-500 font-sans mt-0.5">Conversão em Lucro</div>
        </div>
        <div class="glass-card rounded-xl border border-slate-200 p-2.5 text-center">
          <div class="text-[10px] text-slate-700 uppercase font-bold flex items-center justify-center gap-1">
            <span>Payout Implícito</span>
            <span class="info-badge cursor-pointer" data-tooltip="payout">ⓘ</span>
          </div>
          <div class="text-sm font-bold ${{payoutColor}} mt-0.5">${{payoutStr}}</div>
          <div class="text-[9px] text-slate-500 font-sans mt-0.5">${{s.payout_tag ? s.payout_tag.split(' ')[1] || 'Normal' : 'Normal'}}</div>
        </div>
      `;

      // Espelho Balanço & DRE Reorganizado em Cartões Estruturados
      document.getElementById('auditSourceText').innerHTML = `
        <span class="text-slate-600 font-medium flex items-center gap-1.5"><span>🏛️</span> Fonte: ${{s.details.audit_source || 'Fundamentus'}}</span>
        <span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold ${{s.is_latest_balanco ? 'bg-emerald-100 text-emerald-900 border border-emerald-300' : 'bg-slate-100 text-slate-800 border border-slate-300'}}">
          📅 Balanço Auditado: ${{s.ult_balanco}} (${{s.tri_balanco}})
        </span>
      `;

      document.getElementById('balanceSheetDetails').innerHTML = `
        <!-- Card 1: Valuation & Mercado -->
        <div class="glass-card rounded-xl p-4 flex flex-col gap-2 border border-slate-200">
          <div class="font-bold text-amber-900 text-xs flex items-center gap-1.5 border-b border-slate-200 pb-1.5">
            <span><svg class="w-3.5 h-3.5 stroke-[1.75] inline-block text-amber-700" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M20.59 13.41l-7.17 7.17a2 2 0 01-2.83 0L2 12V2h10l8.59 8.59a2 2 0 010 2.82z"/><line x1="7" y1="7" x2="7.01" y2="7"/></svg></span> Valuation &amp; Mercado
          </div>
          <div class="space-y-1 text-[11px] font-mono">
            <div class="flex justify-between py-0.5 border-b border-slate-200/60"><span class="text-slate-600 font-sans font-medium">Cotação Atual:</span> <b class="text-slate-900 font-bold">${{formatCurrency(s.cotacao)}}</b></div>
            <div class="flex justify-between py-0.5 border-b border-slate-200/60"><span class="text-slate-600 font-sans font-medium">Liquidez Média (2m):</span> <b class="text-slate-900 font-bold">${{volStr}}/dia</b></div>
            <div class="flex justify-between py-0.5 border-b border-slate-200/60"><span class="text-slate-600 font-sans font-medium">Faixa 52 Semanas:</span> <b class="text-slate-800 font-semibold">${{formatCurrency(s.details.min_52sem)}} - ${{formatCurrency(s.details.max_52sem)}}</b></div>
            <div class="flex justify-between py-0.5 border-b border-slate-200/60"><span class="text-slate-600 font-sans font-medium">Valor de Mercado:</span> <b class="text-slate-900 font-bold">${{formatBillions(s.details.valor_mercado)}}</b></div>
            <div class="flex justify-between py-0.5 border-b border-slate-200/60"><span class="text-slate-600 font-sans font-medium">Valor da Firma (EV):</span> <b class="text-slate-900 font-bold">${{formatBillions(s.details.valor_firma)}}</b></div>
            <div class="flex justify-between py-0.5 border-b border-slate-200/60"><span class="text-slate-600 font-sans font-medium">P/L (12M LTM):</span> <b class="${{getColorPl(s.pl)}} font-bold">${{formatMultiple(s.pl)}}</b></div>
            <div class="flex justify-between py-0.5 border-b border-slate-200/60"><span class="text-slate-600 font-sans font-medium">P/L Run-Rate (2T26):</span> <b class="${{getColorPl(s.pl_run_rate)}} font-bold">${{s.pl_run_rate ? formatMultiple(s.pl_run_rate) : 'N/D'}}</b></div>
            <div class="flex justify-between py-0.5 border-b border-slate-200/60"><span class="text-slate-600 font-sans font-medium">P/VP:</span> <b class="text-slate-800 font-bold">${{formatMultiple(s.pvp)}}</b></div>
            <div class="flex justify-between py-0.5 border-b border-slate-200/60"><span class="text-slate-600 font-sans font-medium">EV / EBITDA:</span> <b class="text-slate-800 font-bold">${{s.is_financial ? 'N/A (Bancos)' : formatMultiple(s.ev_ebitda)}}</b></div>
            <div class="flex justify-between py-0.5 border-b border-slate-200/60"><span class="text-slate-600 font-sans font-medium">ROIC (Capital Investido):</span> <b class="${{s.is_financial ? 'text-slate-400 font-normal' : getColorRoic(s.roic)}} font-bold">${{s.is_financial ? 'N/A (Bancos)' : formatPercent(s.roic)}}</b></div>
            <div class="flex justify-between py-0.5 border-b border-slate-200/60"><span class="text-slate-600 font-sans font-medium">ROE (Patrimônio Líquido):</span> <b class="${{getColorRoe(s.roe)}} font-bold">${{formatPercent(s.roe)}}</b></div>
            <div class="flex justify-between py-0.5"><span class="text-slate-600 font-sans font-medium">Dividend Yield:</span> <b class="${{getColorDy(s.div_yield)}} font-bold">${{formatPercent(s.div_yield)}}</b></div>
          </div>
        </div>

        <!-- Card 2: Balanço Patrimonial & Solvência -->
        <div class="glass-card rounded-xl p-4 flex flex-col gap-2 border border-slate-200">
          <div class="font-bold text-sky-900 text-xs flex items-center gap-1.5 border-b border-slate-200 pb-1.5">
            <span><svg class="w-3.5 h-3.5 stroke-[1.75] inline-block text-sky-700" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg></span> Balanço &amp; Solvência
          </div>
          <div class="space-y-1 text-[11px] font-mono">
            <div class="flex justify-between py-0.5 border-b border-slate-200/60"><span class="text-slate-600 font-sans font-medium">Ativo Total:</span> <b class="text-slate-900 font-bold">${{formatBillions(s.details.ativo_total)}}</b></div>
            <div class="flex justify-between py-0.5 border-b border-slate-200/60"><span class="text-slate-600 font-sans font-medium">Ativo Circulante:</span> <b class="text-slate-900 font-bold">${{formatBillions(s.details.ativo_circulante)}}</b></div>
            <div class="flex justify-between py-0.5 border-b border-slate-200/60"><span class="text-slate-600 font-sans font-medium">Disponibilidades (Caixa):</span> <b class="text-emerald-700 font-bold">${{formatBillions(s.details.disponibilidades)}}</b></div>
            <div class="flex justify-between py-0.5 border-b border-slate-200/60"><span class="text-slate-600 font-sans font-medium">Dívida Bruta:</span> <b class="text-slate-800 font-bold">${{formatBillions(s.details.divida_bruta)}}</b></div>
            <div class="flex justify-between py-0.5 border-b border-slate-200/60"><span class="text-slate-600 font-sans font-medium">Dívida Líquida:</span> <b class="${{s.details.divida_liquida <= 0 ? 'text-emerald-700 font-bold' : (s.details.divida_liquida > 1e10 ? 'text-rose-700 font-bold' : 'text-slate-900 font-bold')}}">${{formatBillions(s.details.divida_liquida)}}</b></div>
            <div class="flex justify-between py-0.5 border-b border-slate-200/60"><span class="text-slate-600 font-sans font-medium">Dív. Líq. / EBITDA:</span> <b class="${{getColorDebt(s.div_liq_ebitda, s.is_financial)}} font-bold">${{s.is_financial ? 'N/A (Bancos)' : formatMultiple(s.div_liq_ebitda)}}</b></div>
            <div class="flex justify-between py-0.5 border-b border-slate-200/60"><span class="text-slate-600 font-sans font-medium">Patrimônio Líquido:</span> <b class="text-slate-900 font-bold">${{formatBillions(s.details.patrimonio_liquido)}}</b></div>
            <div class="flex justify-between py-0.5 border-b border-slate-200/60"><span class="text-slate-600 font-sans font-medium">Valor Patrimonial / Ação:</span> <b class="text-slate-800 font-bold">R$ ${{s.details.vpa || 'N/D'}}</b></div>
            <div class="flex justify-between py-0.5"><span class="text-slate-600 font-sans font-medium">Estrutura de Capital:</span> <b class="${{s.details.divida_liquida <= 0 ? 'text-emerald-800 font-semibold' : 'text-amber-800 font-semibold'}}">${{s.details.divida_liquida <= 0 ? 'Caixa Líquido Positivo 🛡️' : 'Alavancagem Normal'}}</b></div>
          </div>
        </div>

        <!-- Card 3: DRE & Geração de Resultados (12M) -->
        <div class="glass-card rounded-xl p-4 flex flex-col gap-2 border border-slate-200">
          <div class="font-bold text-emerald-900 text-xs flex items-center gap-1.5 border-b border-slate-200 pb-1.5">
            <span><svg class="w-3.5 h-3.5 stroke-[1.75] inline-block text-emerald-700" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4 4v16h16M4 12h16M12 4v16"/></svg></span> DRE &amp; Desempenho Operacional
          </div>
          <div class="space-y-1 text-[11px] font-mono">
            <div class="flex justify-between py-0.5 border-b border-slate-200/60"><span class="text-slate-600 font-sans font-medium">Receita Líquida (12m):</span> <b class="text-slate-900 font-bold">${{formatBillions(s.details.receita_liq_12m)}}</b></div>
            <div class="flex justify-between py-0.5 border-b border-slate-200/60"><span class="text-slate-600 font-sans font-medium">EBIT Operacional (12m):</span> <b class="${{s.details.ebit_12m < 0 ? 'text-rose-700 font-bold' : 'text-slate-900 font-bold'}}">${{formatBillions(s.details.ebit_12m)}}</b></div>
            <div class="flex justify-between py-0.5 border-b border-slate-200/60"><span class="text-slate-600 font-sans font-medium">Lucro Líquido (12m):</span> <b class="${{s.details.lucro_liq_12m < 0 ? 'text-rose-700 font-bold' : 'text-emerald-700 font-bold'}}">${{formatBillions(s.details.lucro_liq_12m)}}</b></div>
            <div class="flex justify-between py-0.5 border-b border-slate-200/60"><span class="text-slate-600 font-sans font-medium">Lucro Trimestre (2T26):</span> <b class="${{s.details.lucro_liq_3m < 0 ? 'text-rose-700 font-bold' : 'text-emerald-700 font-bold'}}">${{formatBillions(s.details.lucro_liq_3m)}}</b></div>
            <div class="flex justify-between py-0.5 border-b border-slate-200/60"><span class="text-slate-600 font-sans font-medium">LPA (Lucro por Ação):</span> <b class="text-slate-800 font-bold">R$ ${{s.details.lpa || 'N/D'}}</b></div>
            <div class="flex justify-between py-0.5 border-b border-slate-200/60"><span class="text-slate-600 font-sans font-medium">Margem Bruta:</span> <b class="${{s.mrg_bruta < 0 ? 'text-rose-700 font-bold' : 'text-slate-800 font-bold'}}">${{formatPercent(s.mrg_bruta)}}</b></div>
            <div class="flex justify-between py-0.5"><span class="text-slate-600 font-sans font-medium">Margem Líquida:</span> <b class="${{getColorMrgLiq(s.mrg_liq)}} font-bold">${{formatPercent(s.mrg_liq)}}</b></div>
          </div>
        </div>

        <!-- Card 4: Auditoria de Recorrência (2T26 vs 12M) -->
        <div class="glass-card rounded-xl p-4 flex flex-col gap-2 border border-slate-200">
          <div class="flex justify-between items-center border-b border-slate-200 pb-1.5">
            <span class="font-bold text-indigo-900 text-xs flex items-center gap-1.5 font-sans">
              <span><svg class="w-3.5 h-3.5 stroke-[1.75] inline-block text-indigo-700" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 3v18m-7-5l7-13 7 13M5 16h14M3 19h4m10 0h4"/></svg></span> Auditoria de Recorrência (2T26 vs 12M)
            </span>
            <span class="text-[10px] px-2 py-0.5 rounded-full font-bold font-mono ${{s.is_distorted ? 'bg-purple-100 text-purple-900 border border-purple-300 font-bold' : (s.details.lucro_liq_3m < 0 ? 'bg-rose-100 text-rose-900 border border-rose-300 font-bold' : 'bg-emerald-100 text-emerald-900 border border-emerald-300 font-bold')}}">
              ${{s.distortion_label}}
            </span>
          </div>
          <div class="space-y-1 text-[11px] font-mono">
            <div class="flex justify-between py-0.5 border-b border-slate-200/60"><span class="text-slate-600 font-sans font-medium">Lucro 3M (2T26):</span> <b class="${{s.details.lucro_liq_3m < 0 ? 'text-rose-700 font-bold' : 'text-slate-900 font-bold'}}">${{formatBillions(s.details.lucro_liq_3m)}}</b></div>
            <div class="flex justify-between py-0.5 border-b border-slate-200/60"><span class="text-slate-600 font-sans font-medium">Lucro 12M (LTM):</span> <b class="${{s.details.lucro_liq_12m < 0 ? 'text-rose-700 font-bold' : 'text-slate-900 font-bold'}}">${{formatBillions(s.details.lucro_liq_12m)}}</b></div>
            <div class="flex justify-between py-0.5 border-b border-slate-200/60"><span class="text-slate-600 font-sans font-medium">P/L LTM Histórico:</span> <b class="${{getColorPl(s.pl)}} font-semibold">${{formatMultiple(s.pl)}}</b></div>
            <div class="flex justify-between py-0.5 border-b border-slate-200/60"><span class="text-slate-600 font-sans font-medium">P/L Run-Rate 2T26:</span> <b class="${{getColorPl(s.pl_run_rate)}} font-semibold">${{s.pl_run_rate ? formatMultiple(s.pl_run_rate) : 'Prej/ND'}}</b></div>
            <div class="text-[10px] text-slate-600 font-sans pt-1 leading-relaxed font-medium">
              ${{s.is_distorted ? '⚠️ <b>Aviso Contábil:</b> Divergência relevante entre o lucro recente e os últimos 12 meses. O múltiplo LTM pode carregar efeito de one-off não recorrente.' : '💎 <b>Consistência Contábil:</b> O ritmo de lucro do 2T26 anualizado acompanha o histórico de 12 meses sem distorções anormais de ciclo.'}}
            </div>
          </div>
        </div>
      `;

      // Síntese Fundamentalista
      const diagTitleColor = s.entry_color === '#10E79D' ? '#047857' : (s.entry_color === '#FBBF24' ? '#B45309' : (s.entry_color === '#F43F5E' ? '#BE123C' : '#1E293B'));
      document.getElementById('sinteseStatusBanner').innerHTML = `
        <div class="p-3.5 rounded-xl border text-xs backdrop-blur-md" style="background-color: ${{s.entry_color}}14; border-color: ${{s.entry_color}}44;">
          <div class="font-bold font-mono text-sm" style="color: ${{diagTitleColor}};">${{s.entry_status}}</div>
          <div class="text-slate-700 text-xs mt-1 font-sans leading-relaxed">${{s.rationale}}</div>
        </div>
      `;

      let flagsHtml = '';
      if (s.is_commodity_peak) flagsHtml += '<span class="px-2.5 py-1 text-[10px] font-semibold bg-slate-100 text-slate-800 border border-slate-300 font-bold rounded-full">⚠️ Pico de Ciclo Commodities</span>';
      if (s.is_debt_vulnerable) flagsHtml += '<span class="px-2.5 py-1 text-[10px] font-semibold bg-rose-100 text-rose-900 border border-rose-300 font-bold rounded-full">⚠️ Vulnerabilidade a Juros</span>';
      if (!s.is_latest_balanco) flagsHtml += '<span class="px-2.5 py-1 text-[10px] font-semibold bg-slate-100 text-slate-800 border border-slate-300 font-bold rounded-full">⚠️ Balanço Defasado</span>';
      if (s.is_distorted) flagsHtml += `<span class="px-2.5 py-1 text-[10px] font-semibold bg-purple-100 text-purple-900 border border-purple-300 font-bold rounded-full">⚠️ Distorção Trimestral (${{s.distortion_tag}})</span>`;
      if (s.payout_implicito && s.payout_implicito > 100) flagsHtml += '<span class="px-2.5 py-1 text-[10px] font-semibold bg-rose-100 text-rose-900 border border-rose-300 font-bold rounded-full">⚠️ Payout Insustentável</span>';
      else if (s.payout_implicito && s.payout_implicito >= 40 && s.payout_implicito <= 85) flagsHtml += '<span class="px-2.5 py-1 text-[10px] font-semibold bg-emerald-100 text-emerald-900 border border-emerald-300 font-bold rounded-full">💎 Proventos Disciplinados</span>';
      document.getElementById('sinteseFlagsContainer').innerHTML = flagsHtml;

      // Checklist de Rigor Fundamentalista (Auditoria 100% Fundamentus & CVM)
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
        <div class="glass-card border border-amber-300 bg-amber-50/30 rounded-xl p-3 text-xs font-mono mb-2">
          <div class="flex items-center justify-between border-b border-amber-200 pb-1.5 mb-2">
            <span class="font-bold text-amber-950 uppercase tracking-wider flex items-center gap-1.5">
              <span>🛡️</span> CHECKLIST DE RIGOR FUNDAMENTALISTA (BASE AUDITADA CVM)
            </span>
            <span class="text-[10px] px-2 py-0.5 rounded-full font-bold ${{isAcidPass && isSolvencyPass && isCleanEarnings && isSafeCycle ? 'bg-emerald-100 text-emerald-900 border border-emerald-300' : 'bg-slate-100 text-slate-800 border border-slate-300'}}">
              ${{isAcidPass && isSolvencyPass && isCleanEarnings && isSafeCycle ? '💎 APROVADA NO FILTRO' : 'AUDITORIA COMPLETA'}}
            </span>
          </div>
          <div class="grid grid-cols-2 sm:grid-cols-3 gap-2 text-[11px]">
            <div class="p-2 rounded-lg bg-white border border-slate-200 shadow-2xs">
              <div class="text-[10px] text-slate-700 font-bold">1. Munger Acid Test</div>
              <div class="font-bold ${{isAcidPass ? 'text-emerald-800' : 'text-amber-800'}} flex items-center justify-between">
                <span>${{acidDisplay}}</span>
                <span>${{isAcidPass ? '✅' : '⚠️'}}</span>
              </div>
              <div class="text-[9px] text-slate-500 font-sans">${{isAcidPass ? 'EBITDA vira EBIT' : 'Capex/Deprec. alto'}}</div>
            </div>

            <div class="p-2 rounded-lg bg-white border border-slate-200 shadow-2xs">
              <div class="text-[10px] text-slate-700 font-bold">2. Solvência Anti-Selic</div>
              <div class="font-bold ${{isSolvencyPass ? 'text-emerald-800' : 'text-rose-700'}} flex items-center justify-between">
                <span>${{solvencyDisplay}}</span>
                <span>${{isSolvencyPass ? '✅' : '⚠️'}}</span>
              </div>
              <div class="text-[9px] text-slate-500 font-sans">${{isSolvencyPass ? 'Dívida blindada' : 'Alavancagem alta'}}</div>
            </div>

            <div class="p-2 rounded-lg bg-white border border-slate-200 shadow-2xs">
              <div class="text-[10px] text-slate-700 font-bold">3. Governança Tag Along</div>
              <div class="font-bold ${{isGovPass ? 'text-emerald-800' : 'text-amber-800'}} flex items-center justify-between">
                <span>${{tipoStr}}</span>
                <span>${{isGovPass ? '✅' : 'ℹ️'}}</span>
              </div>
              <div class="text-[9px] text-slate-500 font-sans">${{isGovPass ? '100% Tag Along (ON)' : 'PN/UNT (Verificar)'}}</div>
            </div>

            <div class="p-2 rounded-lg bg-white border border-slate-200 shadow-2xs">
              <div class="text-[10px] text-slate-700 font-bold">4. Crescimento 5 Anos</div>
              <div class="font-bold ${{isGrowthPass ? 'text-emerald-800' : 'text-slate-700'}} flex items-center justify-between">
                <span>${{rawCres}}</span>
                <span>${{isGrowthPass ? '✅' : 'ℹ️'}}</span>
              </div>
              <div class="text-[9px] text-slate-500 font-sans">${{isGrowthPass ? 'Crescimento real' : 'Abaixo da inflação'}}</div>
            </div>

            <div class="p-2 rounded-lg bg-white border border-slate-200 shadow-2xs">
              <div class="text-[10px] text-slate-700 font-bold">5. Recorrência 2T26</div>
              <div class="font-bold ${{isCleanEarnings ? 'text-emerald-800' : 'text-purple-800'}} flex items-center justify-between">
                <span>${{isCleanEarnings ? 'Lucro Limpo' : 'Distorção'}}</span>
                <span>${{isCleanEarnings ? '✅' : '⚠️'}}</span>
              </div>
              <div class="text-[9px] text-slate-500 font-sans">${{isCleanEarnings ? 'Sem one-offs' : s.distortion_tag}}</div>
            </div>

            <div class="p-2 rounded-lg bg-white border border-slate-200 shadow-2xs">
              <div class="text-[10px] text-slate-700 font-bold">6. Ciclo Commodities</div>
              <div class="font-bold ${{isSafeCycle ? 'text-emerald-800' : 'text-amber-800'}} flex items-center justify-between">
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
          <div class="glass-card border border-slate-200 bg-white rounded-xl p-3 text-xs shadow-2xs">
            <div class="text-[11px] font-bold uppercase tracking-wider text-slate-800 mb-1 flex items-center gap-1.5">
              <span>${{b.icon}}</span> <span>${{b.title}}</span>
            </div>
            <div class="text-slate-700 leading-relaxed font-sans text-xs">${{b.content}}</div>
          </div>
        `;
      }});
      document.getElementById('sinteseBulletsList').innerHTML = checklistHtml + bulletsHtml;

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
      const cagrRecColor = h.cagr_receita_pct >= 10.0 ? 'text-emerald-900 bg-emerald-100 border-emerald-300' : (h.cagr_receita_pct >= 0 ? 'text-sky-900 bg-sky-100 border-sky-300' : 'text-rose-900 bg-rose-100 border-rose-300');
      const cagrLucColor = h.cagr_lucro_pct >= 10.0 ? 'text-emerald-900 bg-emerald-100 border-emerald-300' : (h.cagr_lucro_pct >= 0 ? 'text-amber-900 bg-amber-100 border-amber-300' : 'text-rose-900 bg-rose-100 border-rose-300');
      const anosLucColor = h.is_all_profitable ? 'text-emerald-900 bg-emerald-100 border-emerald-300' : 'text-amber-900 bg-amber-100 border-amber-300';

      const badgesHtml = `
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-2.5">
          <div class="glass-card rounded-xl p-3 border border-slate-200 flex flex-col justify-between">
            <div class="text-[10px] text-slate-700 uppercase font-bold font-mono flex items-center justify-between">
              <span>CAGR Receita (5A)</span>
              <span>📈</span>
            </div>
            <div class="mt-1 flex items-baseline justify-between gap-1">
              <span class="text-lg font-bold font-mono text-slate-900">${{h.cagr_receita_pct > 0 ? '+' : ''}}${{h.cagr_receita_pct}}%</span>
              <span class="text-[10px] px-2 py-0.5 rounded-full font-bold font-mono border ${{cagrRecColor}} whitespace-nowrap">
                ${{h.cagr_receita_pct >= 10 ? 'Forte Expansão' : (h.cagr_receita_pct >= 0 ? 'Crescimento Real' : 'Contração')}}
              </span>
            </div>
            <div class="text-[9px] text-slate-500 font-sans mt-0.5">Taxa anualizada 2022-2026</div>
          </div>

          <div class="glass-card rounded-xl p-3 border border-slate-200 flex flex-col justify-between">
            <div class="text-[10px] text-slate-700 uppercase font-bold font-mono flex items-center justify-between">
              <span>Consistência de Lucro</span>
              <span>🛡️</span>
            </div>
            <div class="mt-1 flex items-baseline justify-between gap-1">
              <span class="text-lg font-bold font-mono text-emerald-800">${{h.anos_com_lucro}}</span>
              <span class="text-[10px] px-2 py-0.5 rounded-full font-bold font-mono border ${{anosLucColor}} whitespace-nowrap">
                ${{h.is_all_profitable ? 'Lucro Ininterrupto' : 'Com Oscilações'}}
              </span>
            </div>
            <div class="text-[9px] text-slate-500 font-sans mt-0.5">Ausência de queima de capital</div>
          </div>

          <div class="glass-card rounded-xl p-3 border border-slate-200 flex flex-col justify-between">
            <div class="text-[10px] text-slate-700 uppercase font-bold font-mono flex items-center justify-between">
              <span>CAGR Lucro (5A)</span>
              <span>⚖️</span>
            </div>
            <div class="mt-1 flex items-baseline justify-between gap-1">
              <span class="text-lg font-bold font-mono text-slate-900">${{h.cagr_lucro_pct > 0 ? '+' : ''}}${{h.cagr_lucro_pct}}%</span>
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
        <div class="glass-card rounded-xl p-4 border border-slate-200 flex flex-col gap-2">
          <div class="flex items-center justify-between border-b border-slate-200 pb-2">
            <div class="font-mono font-bold text-xs text-slate-900 flex items-center gap-1.5">
              <span>📊</span> EVOLUÇÃO 5 ANOS: RECEITA LÍQUIDA VS. LUCRO LÍQUIDO
            </div>
            <div class="flex items-center gap-3 text-[10px] font-mono">
              <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-full bg-[#38BDF8]"></span> <span class="text-slate-700 font-semibold">Receita</span></span>
              <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-full bg-[#10E79D]"></span> <span class="text-slate-700 font-semibold">Lucro Líquido</span></span>
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
              <line x1="${{padL}}" y1="${{padT}}" x2="${{padL + innerW1}}" y2="${{padT}}" stroke="#E2E8F0" stroke-dasharray="3,3" />
              <line x1="${{padL}}" y1="${{padT + innerH1/2}}" x2="${{padL + innerW1}}" y2="${{padT + innerH1/2}}" stroke="#E2E8F0" stroke-dasharray="3,3" />
              <line x1="${{padL}}" y1="${{padT + innerH1}}" x2="${{padL + innerW1}}" y2="${{padT + innerH1}}" stroke="#CBD5E1" stroke-width="1.2" />

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
          <div class="glass-card rounded-xl p-3.5 border border-slate-200 flex flex-col justify-between">
            <div class="flex items-center justify-between border-b border-slate-200 pb-1.5 mb-1">
              <span class="font-mono font-bold text-xs text-amber-900 flex items-center gap-1">
                <span>🎯</span> Retorno s/ Capital (ROIC/ROE)
              </span>
              <span class="text-[9px] font-mono text-amber-800 font-semibold">Tier 1 &ge; 15%</span>
            </div>
            <svg viewBox="0 0 ${{w2}} ${{h2}}" class="w-full h-28 select-none">
              <line x1="${{padL2}}" y1="${{roic15LineY.toFixed(1)}}" x2="${{padL2 + innerW2}}" y2="${{roic15LineY.toFixed(1)}}" stroke="#38BDF8" stroke-dasharray="2,2" opacity="0.6" />
              <text x="${{padL2 - 4}}" y="${{(roic15LineY + 3).toFixed(1)}}" text-anchor="end" fill="#38BDF8" font-size="8" font-family="JetBrains Mono">15%</text>
              <path d="${{roicPath}}" fill="none" stroke="#FBBF24" stroke-width="2" />
              ${{roicDotsHtml}}
              ${{yearsLabels2Html}}
            </svg>
          </div>

          <div class="glass-card rounded-xl p-3.5 border border-slate-200 flex flex-col justify-between">
            <div class="flex items-center justify-between border-b border-slate-200 pb-1.5 mb-1">
              <span class="font-mono font-bold text-xs text-emerald-900 flex items-center gap-1">
                <span>💰</span> Histórico Dividend Yield
              </span>
              <span class="text-[9px] font-mono text-emerald-800 font-semibold">Meta &ge; 6%</span>
            </div>
            <svg viewBox="0 0 ${{w2}} ${{h2}}" class="w-full h-28 select-none">
              <line x1="${{padL2}}" y1="${{padT2 + innerH2}}" x2="${{padL2 + innerW2}}" y2="${{padT2 + innerH2}}" stroke="#CBD5E1" stroke-width="1.2" />
              ${{dyBarsHtml}}
              ${{yearsLabels2Html}}
            </svg>
          </div>
        </div>
      `;

      // 4. Tabela Resumo Anual (2022 a 2026 LTM)
      const tableRowsHtml = `
        <div class="glass-card rounded-xl p-3 border border-slate-200 overflow-hidden">
          <div class="text-[11px] font-mono font-bold uppercase tracking-wider text-slate-800 mb-2 flex items-center gap-1.5">
            <span>📋</span> DEMONSTRAÇÃO COMPARATIVA QUINQUENAL (2022 - 2026)
          </div>
          <div class="overflow-x-auto">
            <table class="w-full text-left font-mono text-[11px] whitespace-nowrap">
              <thead class="border-b border-slate-200 bg-slate-100 text-slate-800 text-[10px] uppercase font-bold">
                <tr>
                  <th class="py-1.5 px-2">Métrica Contábil</th>
                  ${{h.years.map(y => `<th class="py-1.5 px-2 text-right">${{y}}</th>`).join('')}}
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100">
                <tr>
                  <td class="py-1.5 px-2 font-sans font-semibold text-slate-800">Receita Líquida</td>
                  ${{h.receita.map(r => `<td class="py-1.5 px-2 text-right text-slate-900 font-bold">${{formatBillions(r)}}</td>`).join('')}}
                </tr>
                <tr>
                  <td class="py-1.5 px-2 font-sans font-semibold text-slate-800">Lucro Líquido</td>
                  ${{h.lucro_liquido.map(l => `<td class="py-1.5 px-2 text-right font-bold ${{l > 0 ? 'text-emerald-800' : 'text-rose-700'}}">${{formatBillions(l)}}</td>`).join('')}}
                </tr>
                <tr>
                  <td class="py-1.5 px-2 font-sans font-semibold text-slate-800">Margem Líquida</td>
                  ${{h.lucro_liquido.map((l, i) => {{
                    const mrg = h.receita[i] > 0 ? (l / h.receita[i]) : 0;
                    return `<td class="py-1.5 px-2 text-right ${{getColorMrgLiq(mrg)}}">${{formatPercent(mrg)}}</td>`;
                  }}).join('')}}
                </tr>
                <tr>
                  <td class="py-1.5 px-2 font-sans font-semibold text-slate-800">ROIC / ROE</td>
                  ${{h.roic_roe.map(r => `<td class="py-1.5 px-2 text-right font-semibold ${{getColorRoe(r)}}">${{formatPercent(r)}}</td>`).join('')}}
                </tr>
                <tr>
                  <td class="py-1.5 px-2 font-sans font-semibold text-slate-800">Dividend Yield</td>
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
        return `<polygon points="${{pts}}" fill="none" stroke="${{isOuter ? '#CBD5E1' : '#E2E8F0'}}" stroke-width="${{isOuter ? 1.5 : 0.8}}" />`;
      }}).join('');

      // Benchmark Tier 1 (80 pts tracejado)
      const benchPts = [0, 1, 2, 3, 4].map(i => pt(i, 80).map(v => v.toFixed(1)).join(',')).join(' ');
      const benchmarkHtml = `<polygon points="${{benchPts}}" fill="none" stroke="#38BDF8" stroke-width="1.5" stroke-dasharray="3,3" opacity="0.65" />`;

      // Linhas radiais do centro até cada ponta
      const radialsHtml = [0, 1, 2, 3, 4].map(i => {{
        const [x, y] = pt(i, 100);
        return `<line x1="0" y1="0" x2="${{x.toFixed(1)}}" y2="${{y.toFixed(1)}}" stroke="#E2E8F0" stroke-width="1" />`;
      }}).join('');

      // Helper de Cores e Status dos Pilares
      function getPillarInfo(score) {{
        if (score >= 70) {{
          return {{
            hex: '#059669',
            color: 'text-emerald-950',
            border: 'border-emerald-300 bg-emerald-50/90',
            badge: 'bg-emerald-100 text-emerald-950 border-emerald-300',
            status: 'Forte'
          }};
        }} else if (score >= 50) {{
          return {{
            hex: '#D97706',
            color: 'text-amber-950',
            border: 'border-amber-300 bg-amber-50/90',
            badge: 'bg-amber-100 text-amber-950 border-amber-300',
            status: 'Neutro'
          }};
        }} else {{
          return {{
            hex: '#DC2626',
            color: 'text-rose-950',
            border: 'border-rose-300 bg-rose-50/90',
            badge: 'bg-rose-100 text-rose-950 border-rose-300',
            status: 'Atenção'
          }};
        }}
      }}

      // Polígono da Empresa
      const companyPts = scores.map((sc, i) => pt(i, sc).map(v => v.toFixed(1)).join(',')).join(' ');
      const companyPointsHtml = scores.map((sc, i) => {{
        const [x, y] = pt(i, sc);
        const info = getPillarInfo(sc);
        return `<circle cx="${{x.toFixed(1)}}" cy="${{y.toFixed(1)}}" r="4.5" fill="${{info.hex}}" stroke="#FFFFFF" stroke-width="1.8" />`;
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
        const info = getPillarInfo(l.val);
        return `
          <text x="${{(x + l.offX).toFixed(1)}}" y="${{(y + l.offY).toFixed(1)}}" text-anchor="${{l.anchor}}" fill="#334155" font-size="9.5" font-family="Inter" font-weight="700">
            ${{l.name}} <tspan fill="${{info.hex}}" font-family="JetBrains Mono" font-weight="bold">(${{l.val}})</tspan>
          </text>
        `;
      }}).join('');

      svg.innerHTML = `
        <defs>
          <radialGradient id="radarGrad" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stop-color="#10B981" stop-opacity="0.35" />
            <stop offset="100%" stop-color="#059669" stop-opacity="0.10" />
          </radialGradient>
        </defs>

        <!-- Anéis Concêntricos -->
        ${{ringsHtml}}

        <!-- Linhas Radiais -->
        ${{radialsHtml}}

        <!-- Benchmark Tier 1 (80 pts) -->
        ${{benchmarkHtml}}

        <!-- Polígono da Empresa -->
        <polygon points="${{companyPts}}" fill="url(#radarGrad)" stroke="#059669" stroke-width="2.5" stroke-linejoin="round" />
        ${{companyPointsHtml}}

        <!-- Rótulos Externos -->
        ${{labelsHtml}}
      `;

      // 2. Renderizar 5 Mini-Cards dos Pilares logo abaixo do SVG
      const pillarsGrid = document.getElementById('radarPillarsGrid');
      if (pillarsGrid) {{
        const pillarCards = [
          {{ label: 'Valuation', score: valScore, desc: s.ey_spread !== null ? (s.ey_spread > 0 ? '+' : '') + s.ey_spread.toFixed(1) + '% Real' : 'P/L ' + formatMultiple(s.pl), ...getPillarInfo(valScore) }},
          {{ label: 'Rentabilidade', score: rentScore, desc: formatPercent(s.roic || s.roe), ...getPillarInfo(rentScore) }},
          {{ label: 'Dividendos', score: divScore, desc: formatPercent(s.div_yield), ...getPillarInfo(divScore) }},
          {{ label: 'Saúde Fin.', score: solScore, desc: s.is_financial ? 'Basileia Ok' : (s.div_liq_ebitda !== null ? (s.div_liq_ebitda < 0 ? 'Caixa Líq.' : s.div_liq_ebitda.toFixed(1) + 'x') : 'N/D'), ...getPillarInfo(solScore) }},
          {{ label: 'Consistência', score: consScore, desc: s.is_distorted ? 'Distorção' : 'Lucro 2T26 Ok', ...getPillarInfo(consScore) }}
        ];

        pillarsGrid.innerHTML = pillarCards.map(c => `
          <div class="border ${{c.border}} rounded-xl p-2.5 flex flex-col items-center justify-between text-center shadow-2xs transition">
            <div class="text-[9.5px] text-slate-600 font-sans uppercase font-semibold truncate w-full">${{c.label}}</div>
            <div class="text-sm font-mono font-extrabold ${{c.color}} my-0.5">${{c.score}}</div>
            <span class="text-[8.5px] font-mono px-1.5 py-0.2 rounded-full font-bold ${{c.badge}}">${{c.status}}</span>
          </div>
        `).join('');
      }}
    }}

    function showToast(message, type = 'info') {{
      const toast = document.getElementById('statusToast');
      const content = document.getElementById('statusToastContent');
      
      let bg = 'bg-blue-950/80 border-blue-800 text-blue-300';
      if (type === 'success') bg = 'bg-emerald-50 border border-emerald-300 text-emerald-900 shadow-lg';
      if (type === 'error') bg = 'bg-rose-50 border border-rose-300 text-rose-900 shadow-lg';

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

    // =========================================================================
    // DICIONÁRIO DE TOOLTIPS DIDÁTICOS (BALÕEZINHOS EXPLICATIVOS MUNGER)
    // =========================================================================
    const METRIC_TOOLTIPS = {{
      quality_score: {{
        title: '🏆 Moat & Quality Score Munger (0 a 100)',
        desc: 'Avalia a força e largura do fosso competitivo econômico. Combina rentabilidade sobre capital (ROIC/ROE 40%), solidez patrimonial anti-crise (35%) e consistência histórica de lucros (25%).',
        foot: 'Tier 1 (≥ 80) = Wide Moat • Tier 2 (≥ 65) = Narrow Moat'
      }},
      ey_spread: {{
        title: '📈 Spread Real vs NTN-B Soberana (IPCA+ 6,5% a.a.)',
        desc: 'Compara o rendimento em lucros da ação (Earnings Yield = Lucro/Preço) contra a taxa livre de risco do Tesouro IPCA+ 2035. Indica o prêmio de risco real para ser sócio da empresa.',
        foot: 'Spread > 0% = Ação compensa o risco soberano do Brasil'
      }},
      pl_ltm: {{
        title: '📊 P/L Histórico (Preço sobre Lucro 12M)',
        desc: 'Número de anos necessários para reaver o capital investido se a empresa mantiver o lucro líquido médio dos últimos 4 trimestres reportados.',
        foot: 'P/L baixo + ROIC alto = Combinação clássica de Charlie Munger'
      }},
      pl_run_rate: {{
        title: '⏱️ P/L Run-Rate (Ritmo Anualizado 2T26)',
        desc: 'Anualiza o lucro do trimestre mais recente (4x 2T26). Se for menor que o P/L 12M (verde), indica que a operação recente está acelerando frente à média passada.',
        foot: 'Antecipa viradas de ciclo antes do mercado geral'
      }},
      graham: {{
        title: '📐 Valor Intrínseco de Benjamin Graham (V.I.)',
        desc: 'Fórmula clássica de Benjamin Graham: V = √(22,5 × LPA × VPA). Estipula uma referência intrínseca teórica ponderando lucros por ação e valor contábil.',
        foot: 'Cotação < Graham = Negociando abaixo do valor patrimonial ponderado'
      }},
      bazin: {{
        title: '🎯 Referência Décio Bazin (DY 6,0%)',
        desc: 'Modelo quantitativo de renda passiva: DPA / 0,06. Estima a cotação teórica em que o histórico de dividendos equivale a 6,0% ao ano em proventos.',
        foot: 'Cotação < Bazin = Yield implícito teórico superior a 6,0% a.a.'
      }},
      ev_ebitda: {{
        title: '🏢 EV / EBITDA (Múltiplo da Firma)',
        desc: 'Valor total da empresa (ações + dívidas líquidas) dividido pelo caixa operacional gerado. Excelente para indústrias e serviços; inaplicável a bancos.',
        foot: '< 6.0x = Múltiplo atrativo • > 12.0x = Exige forte crescimento'
      }},
      roic: {{
        title: '🏭 ROIC (Retorno sobre Capital Investido)',
        desc: 'Mede o lucro estritamente operacional (NOPAT) gerado sobre todo o capital produtivo empatado. O indicador supremo de Charlie Munger para atestar fossos competitivos duradouros.',
        foot: '≥ 15% ao ano = Excelência operacional e barreira de entrada'
      }},
      roe: {{
        title: '🏛️ ROE (Retorno sobre Patrimônio Líquido)',
        desc: 'Mede a velocidade com que o patrimônio dos sócios se multiplica a cada ano. Métrica soberana para bancos, seguradoras e holdings financeiras.',
        foot: '≥ 15% ao ano = Criação acelerada de valor para o acionista'
      }},
      mrg_liq: {{
        title: '💧 Margem Líquida (% de Conversão)',
        desc: 'Percentual da receita líquida que sobra livre no bolso da empresa após deduzir custos, salários, fornecedores, juros e tributos.',
        foot: '≥ 15% = Elevado poder de precificação e margem de segurança'
      }},
      debt: {{
        title: '🛡️ Dívida Líquida / EBITDA (Alavancagem)',
        desc: 'Quantos anos de caixa operacional seriam necessários para zerar o endividamento líquido. Valores negativos indicam Caixa Líquido (mais dinheiro em caixa que dívidas).',
        foot: '< 1.5x = Estrutura ultra-segura • > 3.0x = Risco em Selic alta'
      }},
      payout: {{
        title: '💰 Dividend Yield & Payout Implícito',
        desc: 'Dividend Yield é a taxa anual de proventos em dinheiro. Payout Implícito indica a fração do lucro líquido que foi distribuída aos acionistas.',
        foot: 'Payout entre 35% e 85% = Equilíbrio entre dividendos e reinvestimento'
      }},
      acid_test: {{
        title: '⚗️ Munger Acid Test (EBIT / EBITDA ≥ 75%)',
        desc: 'Mede quanto do EBITDA vira lucro antes de impostos após deduzir a depreciação. Negócios intensivos em capital pesado (Capex voraz) falham neste teste.',
        foot: 'Filtra empresas que corroem capital em manutenção constante'
      }},
      distortion: {{
        title: '🔍 Filtro de Distorções Contábeis & One-Offs',
        desc: 'Elimina empresas com lucros anormais causados por reversões fiscais extraordinárias, venda de ativos ou eventos isolados que não refletem a operação real.',
        foot: 'Garante que os múltiplos sejam baseados em lucros sustentáveis'
      }},
      liq: {{
        title: '💧 Liquidez Média Diária (≥ R$ 1 Milhão/dia)',
        desc: 'Volume médio negociado em bolsa nos últimos 2 meses. Garante que você consiga entrar e sair da posição sem distorcer o preço de mercado.',
        foot: 'Padrão mínimo institucional para liquidez de carteira'
      }},
      recency: {{
        title: '📅 Tempestividade do Balanço (2T26 Vigente)',
        desc: 'Filtra companhias que já reportaram o balanço mais recente auditado pela CVM (2T26), evitando avaliar ações com demonstrações defasadas.',
        foot: 'Garante 100% de precisão nos números correntes'
      }},
      tag_along: {{
        title: '⚖️ Ações Ordinárias (ON - Tag Along 100%)',
        desc: 'Ações com final 3 (ON) que conferem direito de voto e garantem por lei 100% do valor pago por ação no caso de venda do controle da companhia.',
        foot: 'Proteção fundamental de governança corporativa Munger'
      }},
      giro: {{
        title: '🔄 Giro do Ativo (Receita Líquida / Ativo Total)',
        desc: 'Mede a capacidade comercial de gerar vendas a partir de cada real em ativos. Parte integrante do desdobramento DuPont de rentabilidade.',
        foot: '> 1.0x = Alta eficiência na rotação dos ativos'
      }},
      alavancagem: {{
        title: '⚖️ Alavancagem Financeira (Ativo Total / Patrimônio)',
        desc: 'Fator multiplicador da análise DuPont: mostra em quanto o retorno aos sócios é amplificado por capital de terceiros.',
        foot: '< 2.5x = Alavancagem saudável e prudente'
      }}
    }};

    function initGlobalTooltips() {{
      const tooltip = document.getElementById('globalTooltip');
      const titleEl = document.getElementById('gtTitle');
      const descEl = document.getElementById('gtDesc');
      const footEl = document.getElementById('gtFoot');
      if (!tooltip || !titleEl || !descEl || !footEl) return;

      function show(target) {{
        const key = target.getAttribute('data-tooltip');
        const item = METRIC_TOOLTIPS[key];
        if (!item) return;

        titleEl.textContent = item.title;
        descEl.textContent = item.desc;
        footEl.textContent = item.foot || '';

        tooltip.classList.remove('hidden');
        position(target);
      }}

      function hide() {{
        tooltip.classList.add('hidden');
      }}

      function position(target) {{
        const rect = target.getBoundingClientRect();
        const tipRect = tooltip.getBoundingClientRect();
        const padding = 12;

        let top = rect.bottom + 8;
        let left = rect.left + (rect.width / 2) - (tipRect.width / 2);

        if (left + tipRect.width > window.innerWidth - padding) {{
          left = window.innerWidth - tipRect.width - padding;
        }}
        if (left < padding) left = padding;

        if (top + tipRect.height > window.innerHeight - padding) {{
          top = rect.top - tipRect.height - 8;
        }}
        if (top < padding) top = padding;

        tooltip.style.top = top + 'px';
        tooltip.style.left = left + 'px';
      }}

      document.addEventListener('mouseover', (e) => {{
        const target = e.target.closest('[data-tooltip]');
        if (target) {{
          show(target);
        }}
      }});

      document.addEventListener('mouseout', (e) => {{
        const target = e.target.closest('[data-tooltip]');
        if (target) {{
          if (e.relatedTarget && target.contains(e.relatedTarget)) return;
          hide();
        }}
      }});

      document.addEventListener('click', (e) => {{
        const target = e.target.closest('[data-tooltip]');
        if (target) {{
          e.stopPropagation();
          if (tooltip.classList.contains('hidden')) {{
            show(target);
          }} else {{
            hide();
          }}
        }} else {{
          hide();
        }}
      }});

      window.addEventListener('scroll', () => {{
        if (!tooltip.classList.contains('hidden')) hide();
      }}, {{ passive: true }});
    }}

    // Execução inicial
    updateHeaderInfo();
    updateSectorDropdown();
    initMatrixEvents();
    initGlobalTooltips();
    initWelcomeGuide();
    selectTicker(APP_DATA.stocks[0].ticker);
    switchWorkspace('home');
    render();

    // Leitura de parâmetros de URL (ex: ?filter=CAT_EXPANSION ou ?ticker=BLAU3)
    const urlParams = new URLSearchParams(window.location.search);
    const paramFilter = urlParams.get('filter');
    const paramTicker = urlParams.get('ticker');

    if (paramTicker) {{
      selectTicker(paramTicker);
      openDossierDrawer(paramTicker);
    }}

    if (paramFilter) {{
      setFilter(paramFilter);
      switchWorkspace('table');
    }}

    // Auto-refresh se redirecionado com auto_refresh=1
    if (urlParams.get('auto_refresh') === '1') {{
      window.history.replaceState(null, '', window.location.pathname);
      setTimeout(triggerDataRefresh, 300);
    }}

    // Atalhos Globais de Teclado (Power-User Hotkeys)
    document.addEventListener('keydown', (e) => {{
      if (['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement.tagName) || document.activeElement.isContentEditable) {{
        if (e.key === 'Escape') {{
          const dd = document.getElementById('searchDropdown');
          if (dd) dd.classList.add('hidden');
          document.activeElement.blur();
        }}
        return;
      }}

      if (e.key === '/') {{
        e.preventDefault();
        const inp = document.getElementById('searchInput');
        if (inp) {{
          inp.focus();
          inp.select();
        }}
      }} else if (e.key === 'Escape') {{
        const dd = document.getElementById('searchDropdown');
        if (dd) dd.classList.add('hidden');
        closeDossierDrawer();
      }} else if (e.key === '1') {{
        switchWorkspace('home');
      }} else if (e.key === '2') {{
        switchWorkspace('matrix');
      }} else if (e.key === '3') {{
        switchWorkspace('table');
      }}
    }});

    // Fechar dropdown de busca ao clicar fora
    document.addEventListener('click', (e) => {{
      const wrapper = document.getElementById('searchWrapper');
      const dd = document.getElementById('searchDropdown');
      if (wrapper && dd && !wrapper.contains(e.target)) {{
        dd.classList.add('hidden');
      }}
    }});
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
