import json
import os
import shutil

def build_company_page():
    base_dir = r"C:\Users\dougl\.gemini\antigravity\scratch\jpm_munger_terminal"
    data_path = os.path.join(base_dir, "cache", "standalone_data.json")
    
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    json_data_str = json.dumps(data, ensure_ascii=False)
    
    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="Dossiê fundamentalista institucional de ações B3: decomposição DuPont, histórico auditado de 5 anos, valuation Graham e Bazin, e análise de fosso econômico (Economic Moat).">
  <meta name="keywords" content="dossiê de ações, análise de balanço B3, valuation, Graham, Décio Bazin, ROIC, ROE, DuPont, fosso econômico, Moat Score">
  <meta name="author" content="MOAT TERMINAL">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="https://moatterminal.com.br/empresa.html">

  <!-- Open Graph -->
  <meta property="og:type" content="article">
  <meta property="og:url" content="https://moatterminal.com.br/empresa.html">
  <meta property="og:title" id="ogTitle" content="Dossiê de Empresa • Moat Terminal">
  <meta property="og:description" content="Análise fundamentalista institucional e vantagens competitivas (Moats) da B3.">
  <meta property="og:site_name" content="MOAT TERMINAL">
  <meta property="og:locale" content="pt_BR">

  <!-- Twitter / X -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" id="twTitle" content="Dossiê de Empresa • Moat Terminal">
  <meta name="twitter:description" content="Análise fundamentalista completa e vantagens competitivas (Moats) da B3.">

  <!-- Schema.org JSON-LD -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "FinancialProduct",
    "name": "Dossiê Fundamentalista B3",
    "description": "Análise quantitativa e qualitativa de vantagens competitivas duradouras (Economic Moats) na B3",
    "provider": {{
      "@type": "Organization",
      "name": "MOAT TERMINAL",
      "url": "https://moatterminal.com.br"
    }}
  }}
  </script>

  <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23059669' stroke-width='2.2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M3 21h18M3 10h18M5 10v11M19 10v11M9 10v11M15 10v11M4 10l2-6h12l2 6M9 4v3M15 4v3'/%3E%3C/svg%3E">
  
  <!-- Inter & JetBrains Mono Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  
  <!-- GOOGLE ADSENSE (Descomente e insira seu ID de cliente ca-pub-XXXXXXXXXXXXXXXX fornecido pelo Google) -->
  <!--
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXXXXXXXXXXXX" crossorigin="anonymous"></script>
  -->

  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {{
      theme: {{
        extend: {{
          fontFamily: {{
            sans: ['Inter', 'sans-serif'],
            mono: ['JetBrains Mono', 'monospace'],
          }},
          colors: {{
            jpSlate: '#0F172A',
            jpBorder: '#E2E8F0',
            jpCard: '#FFFFFF',
          }}
        }}
      }}
    }}
  </script>

  <style>
    body {{
      background-color: #F8FAFC;
      color: #0F172A;
      font-family: 'Inter', sans-serif;
      -webkit-font-smoothing: antialiased;
    }}
    .glass-card {{
      background-color: #FFFFFF;
      border: 1px solid #E2E8F0;
      box-shadow: 0 1px 3px rgba(0,0,0,0.03), 0 1px 2px rgba(0,0,0,0.02);
    }}
    .glass-pill {{
      background-color: #F8FAFC;
      border: 1px solid #E2E8F0;
    }}
    .custom-scrollbar::-webkit-scrollbar {{
      width: 6px;
      height: 6px;
    }}
    .custom-scrollbar::-webkit-scrollbar-track {{
      background: #F1F5F9;
    }}
    .custom-scrollbar::-webkit-scrollbar-thumb {{
      background: #CBD5E1;
      border-radius: 4px;
    }}
    .custom-scrollbar::-webkit-scrollbar-thumb:hover {{
      background: #94A3B8;
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
    }}
    .info-badge:hover {{
      color: #0F172A;
      background-color: #E2E8F0;
      border-color: #94A3B8;
      transform: scale(1.1);
    }}
  </style>
</head>
<body class="min-h-screen flex flex-col custom-scrollbar">

  <!-- GLOBAL INTERACTIVE EDUCATIONAL TOOLTIP (BALÃOZINHO INSTITUCIONAL) -->
  <div id="globalTooltip" class="fixed hidden z-[999999] max-w-xs sm:max-w-sm bg-slate-900 text-white p-3.5 rounded-2xl shadow-2xl border border-slate-700 pointer-events-none transition-opacity duration-150 text-xs font-sans">
    <div class="font-bold text-emerald-400 font-mono text-xs flex items-center gap-1.5 border-b border-slate-700/80 pb-1.5 mb-1.5" id="gtTitle"></div>
    <div class="text-slate-200 text-[11.5px] leading-relaxed font-sans" id="gtDesc"></div>
    <div class="text-slate-400 text-[10px] font-mono mt-2 pt-1.5 border-t border-slate-800 flex items-center justify-between" id="gtFoot"></div>
  </div>

  <!-- TOPBAR INSTITUCIONAL GLOBAL -->
  <header class="sticky top-0 z-40 bg-white/95 backdrop-blur-md border-b border-slate-200 shadow-2xs">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between gap-4">
      
      <!-- Brand & Link Voltar -->
      <div class="flex items-center gap-3">
        <a href="index.html" class="flex items-center gap-2 px-3 py-1.5 rounded-full bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-mono font-semibold transition" title="Voltar ao Scanner e Panorama Geral">
          <svg class="w-4 h-4 stroke-[2]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M10 19l-7-7m0 0l7-7m-7 7h18"/></svg>
          <span class="hidden sm:inline">Voltar ao Terminal</span>
        </a>
        <div class="h-5 w-px bg-slate-200 hidden sm:block"></div>
        <a href="index.html" class="flex items-center gap-2.5 group cursor-pointer" title="Voltar ao Moat Terminal (Home)">
          <div class="w-8 h-8 rounded-xl bg-slate-950 flex items-center justify-center text-white shadow-xs border border-slate-800 flex-shrink-0 group-hover:scale-105 transition-transform">
            <svg class="w-4 h-4 text-emerald-400 stroke-[2.2]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 21h18M3 10h18M5 10v11M19 10v11M9 10v11M15 10v11M4 10l2-6h12l2 6M9 4v3M15 4v3"/></svg>
          </div>
          <div class="flex flex-col">
            <div class="flex items-center gap-1.5">
              <span class="font-bold text-slate-950 text-xs tracking-wider font-mono leading-none group-hover:text-emerald-700 transition">MOAT TERMINAL</span>
              <span class="px-1 py-0.2 text-[8px] bg-emerald-100 text-emerald-900 font-bold font-mono rounded">PRO</span>
            </div>
            <span class="text-[9px] text-slate-500 font-mono mt-0.5">Economic Moats &amp; Compounding</span>
          </div>
        </a>
      </div>

      <!-- Barra de Busca Rápida com Autocomplete -->
      <div class="flex-1 max-w-md relative" id="companySearchWrapper">
        <div class="relative flex items-center">
          <span class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400">
            <svg class="w-4 h-4 stroke-[1.75]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-4.35-4.35"/></svg>
          </span>
          <input type="text" id="companySearchInput" placeholder="Buscar outra ação (ex: ITUB4, CURY3, VALE3)... (/)" autocomplete="off" class="w-full bg-slate-50 border border-slate-200 focus:border-emerald-500 focus:bg-white rounded-full pl-9 pr-8 py-1.5 text-xs font-mono text-slate-900 placeholder-slate-400 focus:outline-none transition shadow-2xs" oninput="handleCompanySearch(this.value)" onkeydown="handleCompanySearchKeydown(event)" onfocus="showSearchDropdown()" />
          <kbd class="hidden sm:inline-block absolute right-3 text-[10px] font-mono text-slate-400 bg-white border border-slate-200 px-1 rounded shadow-3xs pointer-events-none select-none">/</kbd>
        </div>
        <!-- Dropdown de Busca -->
        <div id="searchResultsDropdown" class="absolute left-0 w-80 sm:w-96 top-full mt-1.5 bg-white border border-slate-200/90 rounded-2xl shadow-2xl max-h-80 overflow-y-auto overflow-x-hidden z-50 hidden divide-y divide-slate-100 font-sans"></div>
      </div>

      <!-- Ações: Compartilhar & Atualização -->
      <div class="flex items-center gap-2">
        <button onclick="copyAnalysisLink()" class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-slate-100 hover:bg-slate-200 border border-slate-200 text-slate-700 text-xs font-mono font-semibold transition cursor-pointer" title="Copiar link direto para esta análise">
          <svg class="w-3.5 h-3.5 stroke-[1.75] text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/></svg>
          <span id="copyLinkText" class="hidden sm:inline">Compartilhar Link</span>
        </button>
        <span class="text-[11px] font-mono text-emerald-800 bg-emerald-50 border border-emerald-300 px-2.5 py-1 rounded-full font-bold hidden md:inline">
          Base 2T26 Auditada
        </span>
      </div>

    </div>
  </header>

  <!-- CONTEÚDO PRINCIPAL (CONTAINER LARGURA TOTAL) -->
  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 flex-1 w-full space-y-6">

    <!-- 1. HERO SECTION: CABEÇALHO DO ATIVO -->
    <div id="companyHeroCard" class="glass-card rounded-2xl p-6 shadow-sm border border-slate-200">
      <!-- Renderizado via JS -->
    </div>

    <!-- 2. GRID DE MÚLTIPLOS ESSENCIAIS (8 CARDS DE ALTA LEITURA) -->
    <div class="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-8 gap-3" id="essentialMultiplesGrid">
      <!-- Renderizado via JS -->
    </div>

    <!-- 3. DUAS COLUNAS PRINCIPAIS: VALUATION & AUDITORIA DE CAPITAL -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">

      <!-- Coluna Esquerda (5/12): Gauges, Radar Pentagonal & Calculadoras de Valuation -->
      <div class="lg:col-span-5 space-y-6">

        <!-- Card A: Velocímetros Analógicos Bloomberg -->
        <div class="glass-card rounded-2xl p-5 border border-slate-200">
          <div class="flex items-center justify-between border-b border-slate-200 pb-2 mb-3">
            <span class="text-xs font-mono font-bold uppercase tracking-wider text-slate-900 flex items-center gap-1.5">
              <svg class="w-4 h-4 stroke-[1.75] text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
              Indicadores Auditados
            </span>
            <span class="text-[10px] text-slate-500 font-mono">100% Fundamentus</span>
          </div>
          <div class="grid grid-cols-3 gap-2">
            <div class="flex flex-col items-center">
              <svg id="heroGaugeRoe" class="w-full h-[105px]" viewBox="0 0 160 112"></svg>
            </div>
            <div class="flex flex-col items-center border-x border-slate-100 px-1">
              <svg id="heroGaugeDebt" class="w-full h-[105px]" viewBox="0 0 160 112"></svg>
            </div>
            <div class="flex flex-col items-center">
              <svg id="heroGaugeSpread" class="w-full h-[105px]" viewBox="0 0 160 112"></svg>
            </div>
          </div>
        </div>

        <!-- Card B: Radar de 5 Pilares (Simply Wall St Style) -->
        <div class="glass-card rounded-2xl p-5 border border-slate-200">
          <div class="flex items-center justify-between border-b border-slate-200 pb-2 mb-2">
            <span class="text-xs font-mono font-bold uppercase tracking-wider text-slate-900 flex items-center gap-1.5">
              <svg class="w-4 h-4 stroke-[1.75] text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
              Radar de 5 Pilares Fundamentais
            </span>
            <span class="text-[10px] text-slate-500 font-mono">Escala 0 a 100</span>
          </div>
          <div class="w-full h-56 flex items-center justify-center py-1">
            <svg id="heroRadarSvg" class="w-full h-56" viewBox="-145 -145 290 290"></svg>
          </div>
          <div class="grid grid-cols-5 gap-1.5 text-center mt-2" id="heroRadarPillarsGrid"></div>
        </div>

        <!-- Card C: Modelos Clássicos de Valuation (Graham, Bazin e Spread Real) -->
        <div class="glass-card rounded-2xl p-5 border border-slate-200 space-y-3.5">
          <div class="flex items-center justify-between border-b border-slate-200 pb-2">
            <span class="text-xs font-mono font-bold uppercase tracking-wider text-slate-900 flex items-center gap-1.5">
              <svg class="w-4 h-4 stroke-[1.75] text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z"/></svg>
              Calculadoras de Valuation Quantitativo
            </span>
            <span class="text-[10px] text-emerald-800 bg-emerald-50 px-2 py-0.5 rounded-full font-bold border border-emerald-200">Algoritmo Ativo</span>
          </div>
          <div id="valuationCalculatorsContainer" class="space-y-3">
            <!-- Renderizado via JS -->
          </div>
        </div>

      </div>

      <!-- Coluna Direita (7/12): Histórico 5 Anos, Balanço Auditado & Pares Setoriais -->
      <div class="lg:col-span-7 space-y-6">

        <!-- Card D: Gráfico Histórico 5 Anos (Receita vs Lucro) -->
        <div class="glass-card rounded-2xl p-5 border border-slate-200 space-y-4">
          <div class="flex flex-wrap items-center justify-between border-b border-slate-200 pb-3 gap-2">
            <div>
              <span class="text-xs font-mono font-bold uppercase tracking-wider text-slate-900 flex items-center gap-1.5">
                <svg class="w-4 h-4 stroke-[1.75] text-sky-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/></svg>
                Evolução Histórica de 5 Anos (2022 - 2026)
              </span>
              <p class="text-[11px] text-slate-500 font-sans mt-0.5" id="historySubtitle">Trajetória auditada de faturamento líquido contra resultado final.</p>
            </div>
            <div class="flex items-center gap-1 bg-slate-100 p-0.5 rounded-lg border border-slate-200 text-[11px] font-mono font-medium">
              <button id="btnHistRev" onclick="switchHistoryTab('rev_lucro')" class="px-2.5 py-1 rounded-md transition font-bold bg-white text-slate-900 shadow-2xs cursor-pointer">Receita × Lucro</button>
              <button id="btnHistRent" onclick="switchHistoryTab('rentabilidade')" class="px-2.5 py-1 rounded-md transition text-slate-600 hover:text-slate-900 cursor-pointer">ROIC / ROE</button>
              <button id="btnHistDiv" onclick="switchHistoryTab('dividendos')" class="px-2.5 py-1 rounded-md transition text-slate-600 hover:text-slate-900 cursor-pointer">Dividend Yield</button>
            </div>
          </div>
          
          <div id="historyChartContainer" class="w-full"></div>
          <div id="historyKpisGrid" class="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-2"></div>
        </div>

        <!-- Card E: Decomposição DuPont (Raio-X de Rentabilidade & ROE) -->
        <div class="glass-card rounded-2xl p-5 border border-slate-200 space-y-4">
          <div class="flex flex-wrap items-center justify-between border-b border-slate-200 pb-3 gap-2">
            <div>
              <span class="text-xs font-mono font-bold uppercase tracking-wider text-slate-900 flex items-center gap-1.5">
                <svg class="w-4 h-4 stroke-[1.75] text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/></svg>
                Raio-X DuPont • Decomposição do ROE
              </span>
              <p class="text-[11px] text-slate-500 font-sans mt-0.5">Desconstrução da rentabilidade: onde está o verdadeiro motor do retorno?</p>
            </div>
            <span class="text-[10px] text-indigo-900 bg-indigo-50 border border-indigo-200 font-mono font-bold px-2 py-0.5 rounded-full" id="dupontModelBadge">Modelo 3 Etapas</span>
          </div>

          <!-- Componentes DuPont -->
          <div id="dupontComponentsGrid"></div>

          <!-- Diagnóstico Analítico Munger -->
          <div id="dupontVerdictBox" class="p-3.5 rounded-xl border border-slate-200 bg-slate-50/70 text-xs font-sans text-slate-700 leading-relaxed"></div>
        </div>

        <!-- Card F: Espelho Contábil & Síntese Fundamentalista -->
        <div class="glass-card rounded-2xl p-5 border border-slate-200 space-y-4">
          <div class="flex items-center justify-between border-b border-slate-200 pb-2">
            <span class="text-xs font-mono font-bold uppercase tracking-wider text-slate-900 flex items-center gap-1.5">
              <svg class="w-4 h-4 stroke-[1.75] text-amber-700" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
              Balanço Auditado (2T26) &amp; Leitura dos Números
            </span>
            <span class="text-[10px] text-indigo-900 bg-indigo-50 border border-indigo-200 font-mono font-bold px-2 py-0.5 rounded-full">Auditoria CVM</span>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4" id="companyFinancialDetailsGrid"></div>
          
          <div id="companyCfaVerdictBox" class="pt-2"></div>
        </div>

      </div>

    </div>

    <!-- 4. SEÇÃO COMPLETA: COMPARADOR DE CONCORRENTES DIRETOS NO MESMO SETOR (12/12 LARGURA TOTAL) -->
    <div class="glass-card rounded-2xl p-6 border border-slate-200 space-y-4">
      <div class="flex flex-wrap items-center justify-between border-b border-slate-200 pb-3 gap-2">
        <div>
          <span class="text-sm font-mono font-bold uppercase tracking-wider text-slate-900 flex items-center gap-2">
            <svg class="w-4 h-4 stroke-[1.75] text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/></svg>
            Concorrentes Diretos no Mesmo Setor
          </span>
          <p class="text-xs text-slate-500 font-sans mt-0.5" id="sectorPeersSubtitle">Comparação relativa de múltiplos de valuation, retorno e endividamento.</p>
        </div>
        <span class="text-xs text-slate-700 bg-slate-100 font-mono px-3 py-1 rounded-full font-bold border border-slate-200" id="sectorPeersCount">-- concorrentes</span>
      </div>

      <div class="overflow-x-auto">
        <table class="w-full text-left text-xs font-mono border-collapse">
          <thead class="bg-slate-50 border-b border-slate-200 text-slate-700 uppercase font-bold text-[10px]">
            <tr>
              <th class="py-3 px-3">Ativo</th>
              <th class="py-3 px-2 text-center">Score</th>
              <th class="py-3 px-2 text-right">Cotação</th>
              <th class="py-3 px-2 text-right">P/L</th>
              <th class="py-3 px-2 text-right" title="Retorno sobre Capital Investido">ROIC</th>
              <th class="py-3 px-2 text-right" title="Retorno sobre Patrimônio Líquido">ROE</th>
              <th class="py-3 px-2 text-right">Margem Líq.</th>
              <th class="py-3 px-2 text-right">Dívida Líq.</th>
              <th class="py-3 px-2 text-right">Div. Yield</th>
              <th class="py-3 px-3 text-center">Ação</th>
            </tr>
          </thead>
          <tbody id="sectorPeersTableBody" class="divide-y divide-slate-100 font-sans"></tbody>
        </table>
      </div>
    </div>

    <!-- ESPAÇO PUBLICITÁRIO / PARCERIAS ESTRATÉGICAS (GOOGLE ADSENSE / AFILIADOS CORRETORAS) -->
    <div class="glass-card rounded-2xl p-5 border border-slate-200 space-y-2">
      <div class="flex items-center justify-between border-b border-slate-100 pb-1.5 text-[10px] font-mono text-slate-400 uppercase tracking-wider">
        <span class="flex items-center gap-1.5"><span class="text-amber-500">📢</span> PUBLICIDADE &amp; PARCERIAS ESTRATÉGICAS</span>
        <span class="text-slate-400 hover:text-slate-600 transition">Espaço Patrocinado</span>
      </div>
      <div id="ad-slot-company" class="min-h-[80px] w-full flex flex-col md:flex-row items-center justify-between gap-3 p-3.5 rounded-lg bg-slate-50 border border-dashed border-slate-300 text-slate-600">
        <div class="flex items-center gap-3">
          <div class="w-9 h-9 rounded-lg bg-indigo-100 text-indigo-800 flex items-center justify-center font-bold text-base flex-shrink-0">
            📊
          </div>
          <div>
            <div class="font-bold text-xs text-slate-800 font-mono">Espaço Reservado para Google AdSense ou Corretora Parceira</div>
            <div class="text-[11px] text-slate-500">Banner responsivo pronto para receber o bloco do AdSense (728x90 / 320x50) ou links de corretoras (BTG Pactual, Avenue, Nomad, etc.).</div>
          </div>
        </div>
        <div class="flex items-center gap-2 flex-shrink-0">
          <span class="px-2.5 py-1 rounded bg-white border border-slate-200 text-[10px] font-mono text-slate-500 font-medium">Slot: #AD-DOSSIER-BANNER</span>
        </div>
      </div>
    </div>

  </main>

  <!-- FOOTER INSTITUCIONAL -->
  <footer class="bg-white border-t border-slate-200 py-6 mt-12">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-3.5">
      <div class="flex flex-col sm:flex-row items-center justify-between gap-4 text-xs font-mono text-slate-500">
        <div class="flex items-center gap-2">
          <span class="font-bold text-slate-800">MOAT TERMINAL</span>
          <span>•</span>
          <span>Economic Moats &amp; Capital Compounding</span>
        </div>
        <div class="flex items-center gap-3 text-[11px] font-mono">
          <a href="termos.html" class="text-slate-600 hover:text-emerald-700 underline underline-offset-2">Termos de Uso</a>
          <span>•</span>
          <a href="privacidade.html" class="text-slate-600 hover:text-emerald-700 underline underline-offset-2">Política de Privacidade</a>
        </div>
      </div>
      <div class="p-3.5 rounded-xl border border-slate-200 bg-slate-50 text-slate-600 text-xs leading-relaxed space-y-1">
        <div class="font-mono font-bold text-slate-800 flex items-center gap-1.5 text-[11px]">
          <span>⚖️</span> CONFORMIDADE REGULATÓRIA (RESOLUÇÃO CVM Nº 20/2021)
        </div>
        <p class="text-[11px] text-slate-500">
          Este dossiê tem finalidade estritamente analítica e educacional com base em dados públicos contábeis. Não constitui consultoria, oferta pública, recomendação de compra ou venda de ações. Rentabilidade passada não é garantia de resultados futuros.
        </p>
      </div>
      <div class="pt-1.5 border-t border-slate-100 flex flex-col sm:flex-row items-center justify-between text-[10px] font-mono text-slate-500 gap-1">
        <span>© 2026 MOAT TERMINAL • Todos os direitos reservados.</span>
        <span>Contato institucional: <a href="mailto:contato@moatterminal.com.br" class="hover:text-emerald-700 underline">contato@moatterminal.com.br</a></span>
      </div>
    </div>
  </footer>

  <!-- DADOS EMBUTIDOS E MOTOR JS DA PÁGINA -->
  <script>
    const APP_DATA = {json_data_str};

    // Obter Ticker da URL (?ticker=WEGE3)
    const urlParams = new URLSearchParams(window.location.search);
    let currentTicker = (urlParams.get('ticker') || 'WEGE3').toUpperCase().trim();

    // Encontrar Ativo
    let currentStock = APP_DATA.stocks.find(s => s.ticker === currentTicker);
    if (!currentStock) {{
      currentStock = APP_DATA.stocks.find(s => s.ticker === 'WEGE3') || APP_DATA.stocks[0];
      currentTicker = currentStock.ticker;
    }}

    // Logo Helper com fallback monograma
    function getStockLogoHtml(ticker, companyName, sizeClass = 'w-8 h-8') {{
      const baseTicker = ticker ? ticker.toUpperCase() : 'B3';
      const initial = baseTicker.substring(0, 2);
      const logoUrl = `https://raw.githubusercontent.com/thefintz/icones-b3/main/icones/${{baseTicker}}.png`;
      return `
        <div class="${{sizeClass}} rounded-xl flex items-center justify-center overflow-hidden flex-shrink-0 bg-slate-100 border border-slate-200 relative shadow-2xs">
          <img src="${{logoUrl}}" alt="${{baseTicker}}" class="w-full h-full object-contain p-0.5" 
               onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';" />
          <div class="w-full h-full absolute inset-0 items-center justify-center font-mono font-bold text-slate-700 text-xs hidden bg-slate-100">
            ${{initial}}
          </div>
        </div>
      `;
    }}

    function formatCurrency(val) {{
      if (val === null || val === undefined || isNaN(val)) return 'R$ --';
      return 'R$ ' + Number(val).toLocaleString('pt-BR', {{ minimumFractionDigits: 2, maximumFractionDigits: 2 }});
    }}

    function formatPercent(val) {{
      if (val === null || val === undefined || isNaN(val)) return 'N/D';
      return (Number(val) * 100).toFixed(1) + '%';
    }}

    function formatMultiple(val) {{
      if (val === null || val === undefined || isNaN(val)) return 'N/D';
      return Number(val).toFixed(2) + 'x';
    }}

    function formatBillions(val) {{
      if (val === null || val === undefined || isNaN(val)) return 'R$ --';
      const num = Number(val);
      if (Math.abs(num) >= 1e9) return 'R$ ' + (num / 1e9).toFixed(2).replace('.', ',') + ' B';
      if (Math.abs(num) >= 1e6) return 'R$ ' + (num / 1e6).toFixed(1).replace('.', ',') + ' M';
      return 'R$ ' + num.toLocaleString('pt-BR');
    }}

    function calcFairPL(qualityScore) {{
      const q = Math.max(20.0, Math.min(100.0, qualityScore || 50.0));
      const norm = (q - 20.0) / 80.0;
      return 3.5 + 20.0 * Math.pow(norm, 1.6);
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
            label: 'Caixa Líquido (Dívida Zero)',
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

      // Retorna no máximo 5 etiquetas por empresa para manter alinhado com o Dossiê 360°
      return cats.slice(0, 5);
    }}

    // Diagnóstico Executivo Didático em Linguagem Humana
    function generateHumanExecutiveSummary(s) {{
      if (!s) return '';
      const isFin = s.is_financial;
      const roePct = s.roe ? (s.roe * 100).toFixed(1) + '%' : 'N/D';
      const roicPct = s.roic ? (s.roic * 100).toFixed(1) + '%' : null;
      const dyPct = s.div_yield ? (s.div_yield * 100).toFixed(1) + '%' : '0.0%';
      const tierShort = s.quality_score >= 80 ? 'Wide Moat (Tier 1)' : (s.quality_score >= 65 ? 'Narrow Moat (Tier 2)' : 'No Moat (Tier 3)');

      if (isFin) {{
        return `<b>${{s.empresa}} (${{s.ticker}})</b> é uma instituição financeira/holding regulada pelas métricas do Banco Central, avaliada no <b>${{tierShort}}</b> com nota <b>${{s.quality_score.toFixed(1)}}/100</b>. Entrega um retorno patrimonial (ROE) robusto de <b>${{roePct}}</b> ao ano e distribui dividendos regulares de <b>${{dyPct}}</b> a.a. Seu valuation atual oferece <b>${{s.entry_status}}</b> frente à renda fixa pública.`;
      }}

      const debtStatus = (s.div_liq_ebitda !== null && s.div_liq_ebitda < 0) ? 'opera com caixa líquido positivo (sem endividamento líquido)' : (s.div_liq_ebitda ? `alavancagem controlada de ${{s.div_liq_ebitda.toFixed(1)}}x EBITDA` : 'estrutura de capital auditada');
      const returnDesc = roicPct ? `retorno operacional (ROIC) de <b>${{roicPct}}</b> e retorno patrimonial (ROE) de <b>${{roePct}}</b>` : `ROE de <b>${{roePct}}</b>`;

      return `<b>${{s.empresa}} (${{s.ticker}})</b> atua no setor de <b>${{s.setor || 'Atividade Geral'}}</b>, classificada no <b>${{tierShort}}</b> com Score de <b>${{s.quality_score.toFixed(1)}}/100</b>. Apresenta ${{returnDesc}}, ${{debtStatus}} e remuneração em proventos de <b>${{dyPct}}</b> a.a., posicionando-se em <b>${{s.entry_status}}</b>.`;
    }}

    // Renderizar Hero Card
    function renderHero() {{
      const s = currentStock;
      document.getElementById('pageTitle').innerText = `${{s.ticker}} • ${{s.empresa}} • Leitura dos Números`;

      // Coloração Dinâmica do Hero Card conforme a Classificação de Entrada (3 Alternativas)
      let heroBgClass = 'bg-white border-slate-200';
      let entryBadgeClass = 'bg-slate-100 text-slate-800 border-slate-300';
      let diagBoxClass = 'bg-white/95 border-slate-200 text-slate-800 shadow-2xs';
      let diagTitleClass = 'text-slate-900';
      let diagIconSvg = '<svg class="w-4 h-4 stroke-[1.75] inline-block text-slate-600 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 18v1m0 0a2 2 0 002 2h0a2 2 0 002-2m-4 0h4m-4 0v-1m0-9a4 4 0 018 0c0 2.22-1.206 3.48-2 4.5-.33.424-.5 1-.5 1.5h-3c0-.5-.17-1.076-.5-1.5C9.206 12.48 8 11.22 8 9a4 4 0 014-4z"/></svg>';

      if (s.entry_tag === 'ASSIMETRIA_FAVORAVEL') {{
        heroBgClass = 'bg-emerald-50/70 border-emerald-300 shadow-xs';
        entryBadgeClass = 'bg-emerald-600 text-white font-bold shadow-2xs';
        diagBoxClass = 'bg-white/95 border-emerald-200/90 text-slate-800 shadow-2xs';
        diagTitleClass = 'text-emerald-950';
        diagIconSvg = '<svg class="w-4 h-4 stroke-[1.75] inline-block text-emerald-700 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 18v1m0 0a2 2 0 002 2h0a2 2 0 002-2m-4 0h4m-4 0v-1m0-9a4 4 0 018 0c0 2.22-1.206 3.48-2 4.5-.33.424-.5 1-.5 1.5h-3c0-.5-.17-1.076-.5-1.5C9.206 12.48 8 11.22 8 9a4 4 0 014-4z"/></svg>';
      }} else if (s.entry_tag === 'PRECO_JUSTO') {{
        heroBgClass = 'bg-amber-50/70 border-amber-300 shadow-xs';
        entryBadgeClass = 'bg-amber-500 text-white font-bold shadow-2xs';
        diagBoxClass = 'bg-white/95 border-amber-200/90 text-slate-800 shadow-2xs';
        diagTitleClass = 'text-amber-950';
        diagIconSvg = '<svg class="w-4 h-4 stroke-[1.75] inline-block text-amber-600 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 18v1m0 0a2 2 0 002 2h0a2 2 0 002-2m-4 0h4m-4 0v-1m0-9a4 4 0 018 0c0 2.22-1.206 3.48-2 4.5-.33.424-.5 1-.5 1.5h-3c0-.5-.17-1.076-.5-1.5C9.206 12.48 8 11.22 8 9a4 4 0 014-4z"/></svg>';
      }} else if (s.entry_tag === 'ESTICADA') {{
        heroBgClass = 'bg-rose-50/70 border-rose-300 shadow-xs';
        entryBadgeClass = 'bg-rose-600 text-white font-bold shadow-2xs';
        diagBoxClass = 'bg-white/95 border-rose-200/90 text-slate-800 shadow-2xs';
        diagTitleClass = 'text-rose-950';
        diagIconSvg = '<svg class="w-4 h-4 stroke-[1.75] inline-block text-rose-600 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 18v1m0 0a2 2 0 002 2h0a2 2 0 002-2m-4 0h4m-4 0v-1m0-9a4 4 0 018 0c0 2.22-1.206 3.48-2 4.5-.33.424-.5 1-.5 1.5h-3c0-.5-.17-1.076-.5-1.5C9.206 12.48 8 11.22 8 9a4 4 0 014-4z"/></svg>';
      }}

      const heroEl = document.getElementById('companyHeroCard');
      heroEl.className = `glass-card rounded-3xl p-6 sm:p-8 border transition-colors duration-200 shadow-sm ${{heroBgClass}}`;

      const expPL = calcFairPL(s.quality_score);
      const isAbove = s.pl && s.pl > 0 && s.pl < expPL;
      const curveBadge = isAbove 
        ? '<span class="px-2.5 py-1 rounded-full text-xs font-bold font-mono bg-white/90 text-slate-800 border border-slate-200">📈 Acima da Curva (Desconto)</span>'
        : '<span class="px-2.5 py-1 rounded-full text-xs font-bold font-mono bg-white/90 text-slate-800 border border-slate-200">📉 Abaixo da Curva (Prêmio)</span>';

      const scoreBadgeClass = 'bg-white/95 text-slate-900 border-slate-300 shadow-2xs';

      const categories = getStockCategories(s);
      let catBadgesHtml = '';
      if (categories.length > 0) {{
        catBadgesHtml = categories.map(c => `
          <a href="index.html?filter=${{c.id}}" class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-mono font-bold ${{c.bgClass}} shadow-2xs hover:brightness-110 transition cursor-pointer" title="Ver empresas em ${{c.label}}">
            <span>${{c.icon}}</span> <span>${{c.shortLabel || c.label}}</span>
          </a>
        `).join('');
      }} else {{
        catBadgesHtml = `<span class="text-xs font-mono text-slate-500 italic">Nenhum enquadramento especial nos filtros</span>`;
      }}

      heroEl.innerHTML = `
        <div class="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-6">
          <div class="flex items-center gap-4 min-w-0">
            ${{getStockLogoHtml(s.ticker, s.empresa, 'w-16 h-16')}}
            <div class="flex flex-col min-w-0">
              <div class="flex flex-wrap items-center gap-2">
                <h1 class="text-2xl sm:text-3xl font-bold font-mono text-slate-900 tracking-wide">${{s.ticker}}</h1>
                <span class="text-xs px-2.5 py-0.5 rounded-full font-mono font-bold bg-white/90 text-slate-800 border border-slate-200">2T26 Vigente</span>
                <span class="text-xs px-3 py-0.5 rounded-full font-sans ${{entryBadgeClass}}">${{s.entry_status}}</span>
                ${{curveBadge}}
                ${{s.is_distorted ? '<span class="text-xs px-2.5 py-0.5 rounded-full font-mono font-bold bg-amber-100 text-amber-900 border border-amber-300">' + (s.distortion_label || 'Distorção Contábil') + '</span>' : ''}}
              </div>
              <div class="text-sm font-semibold text-slate-700 mt-1 truncate">${{s.empresa}}</div>
              <div class="text-xs text-slate-500 font-sans mt-0.5 flex flex-wrap items-center gap-2">
                <span>Setor: <b class="text-slate-800">${{s.setor || 'Geral'}}</b></span>
                <span>•</span>
                <span>Segmento: <b class="text-slate-800">${{s.sub_setor || s.tipo || 'B3'}}</b></span>
                <span>•</span>
                <span>Liquidez Diária: <b class="text-slate-800">${{formatBillions(s.liq_2m)}}/dia</b></span>
              </div>
            </div>
          </div>

          <div class="flex flex-wrap items-center gap-4 sm:gap-6 self-stretch lg:self-auto justify-between lg:justify-end border-t lg:border-t-0 pt-4 lg:pt-0 border-slate-100">
            <div class="flex flex-col text-left lg:text-right">
              <span class="text-[11px] text-slate-500 uppercase font-mono font-semibold">Cotação Atual</span>
              <span class="text-2xl font-bold font-mono text-slate-900 mt-0.5">${{formatCurrency(s.cotacao)}}</span>
              <span class="text-[10px] text-slate-500 font-sans">Mercado B3 à vista</span>
            </div>

            <div class="flex flex-col text-left lg:text-right">
              <span class="text-[11px] text-slate-500 uppercase font-mono font-semibold">Valor de Mercado</span>
              <span class="text-lg font-bold font-mono text-slate-800 mt-0.5">${{s.details && s.details.valor_mercado ? formatBillions(s.details.valor_mercado) : 'N/D'}}</span>
              <span class="text-[10px] text-slate-500 font-sans">EV: ${{s.details && s.details.valor_firma ? formatBillions(s.details.valor_firma) : 'N/D'}}</span>
            </div>

            <div class="flex flex-col items-center justify-center p-3 rounded-2xl border ${{scoreBadgeClass}} min-w-[95px]">
              <span class="text-[10px] font-mono font-bold uppercase tracking-wider text-slate-500">Qualidade</span>
              <span class="text-2xl font-bold font-mono leading-none my-0.5">${{s.quality_score.toFixed(1)}}</span>
              <span class="text-[9px] font-mono font-semibold text-slate-700">${{s.quality_score >= 80 ? 'Tier 1 (Wide Moat)' : (s.quality_score >= 65 ? 'Tier 2 (Narrow Moat)' : 'Tier 3 (No Moat)')}}</span>
            </div>
          </div>
        </div>

        <!-- Box de Resumo Executivo Didático para o Investidor -->
        <div class="mt-4 p-4 border rounded-2xl flex items-start gap-3.5 text-xs font-sans text-slate-800 leading-relaxed shadow-2xs ${{diagBoxClass}}">
          <span class="mt-0.5">${{diagIconSvg}}</span>
          <div>
            <div class="font-bold ${{diagTitleClass}} font-mono text-[11px] uppercase tracking-wider mb-1 flex items-center gap-2">
              <span>Diagnóstico Executivo para o Investidor</span>
              <span class="px-2 py-0.2 rounded-full text-[9px] font-bold bg-white text-slate-800 border border-slate-300">Linguagem Simples</span>
            </div>
            <p class="text-slate-700 text-xs leading-relaxed font-sans">${{generateHumanExecutiveSummary(s)}}</p>
          </div>
        </div>

        <!-- Rótulos de Enquadramento Estratégico & Momento -->
        <div class="mt-3.5 pt-3 border-t border-slate-100 flex flex-wrap items-center gap-2">
          <span class="text-[11px] font-mono font-bold uppercase tracking-wider text-slate-500 mr-1 flex items-center gap-1.5">
            <svg class="w-3.5 h-3.5 stroke-[1.75] text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"/></svg>
            Enquadramentos &amp; Momento:
          </span>
          ${{catBadgesHtml}}
        </div>
      `;
    }}

    // Renderizar Grid de 8 Múltiplos
    function renderEssentialMultiples() {{
      const s = currentStock;
      const roicVal = s.roic || s.roe || 0;
      const dlVal = s.details ? s.details.divida_liquida : null;
      let debtText = 'N/D';
      if (s.is_financial) debtText = 'Bancos (Bacen)';
      else if (dlVal !== null && dlVal <= 0) debtText = 'Caixa Líquido 🛡️';
      else if (s.div_liq_ebitda !== null) debtText = s.div_liq_ebitda.toFixed(2) + 'x EBITDA';

      const items = [
        {{ label: 'P/L Histórico', val: formatMultiple(s.pl), desc: 'Preço sobre Lucro LTM', color: 'text-slate-900', tip: 'pl_ltm' }},
        {{ label: 'P/L Run-Rate', val: s.pl_run_rate ? formatMultiple(s.pl_run_rate) : 'N/D', desc: 'Ritmo anualizado 2T26', color: s.pl_run_rate && s.pl && s.pl_run_rate < s.pl ? 'text-emerald-800 font-bold' : 'text-slate-900', tip: 'pl_run_rate' }},
        {{ label: 'P / VP', val: formatMultiple(s.pvp), desc: 'Preço sobre Patrimônio', color: 'text-slate-900', tip: 'graham' }},
        {{ label: 'EV / EBITDA', val: s.is_financial ? 'N/A' : (s.ev_ebitda !== null ? formatMultiple(s.ev_ebitda) : 'N/D'), desc: 'Múltiplo da Firma', color: 'text-slate-900', tip: 'ev_ebitda' }},
        {{ label: 'ROIC Operacional', val: s.is_financial ? 'N/A (Bancos)' : formatPercent(s.roic), desc: 'Retorno Capital Investido (NOPAT/CI)', color: (!s.is_financial && s.roic >= 0.15) ? 'text-emerald-800 font-bold' : 'text-slate-900', tip: 'roic' }},
        {{ label: 'ROE do Acionista', val: formatPercent(s.roe), desc: 'Retorno s/ Patrimônio Líquido', color: s.roe >= 0.15 ? 'text-emerald-800 font-bold' : 'text-slate-900', tip: 'roe' }},
        {{ label: 'Margem Líquida', val: formatPercent(s.mrg_liq), desc: 'Conversão em Lucro Líquido', color: s.mrg_liq >= 0.15 ? 'text-emerald-800 font-bold' : 'text-slate-900', tip: 'mrg_liq' }},
        {{ label: 'Dividend Yield', val: formatPercent(s.div_yield), desc: 'Proventos pagos 12m', color: s.div_yield >= 0.06 ? 'text-emerald-800 font-bold' : 'text-slate-900', tip: 'payout' }}
      ];

      document.getElementById('essentialMultiplesGrid').innerHTML = items.map(c => `
        <div class="glass-card rounded-xl p-3 border border-slate-200 text-center flex flex-col justify-between">
          <div class="text-[10px] text-slate-500 uppercase font-mono font-semibold flex items-center justify-center gap-1">
            <span>${{c.label}}</span>
            ${{c.tip ? `<span class="info-badge cursor-pointer" data-tooltip="${{c.tip}}">ⓘ</span>` : ''}}
          </div>
          <div class="text-sm sm:text-base font-mono font-bold ${{c.color}} my-1">${{c.val}}</div>
          <div class="text-[9px] text-slate-500 font-sans truncate" title="${{c.desc}}">${{c.desc}}</div>
        </div>
      `).join('');
    }}

    // Renderizar Calculadoras de Valuation (Graham, Bazin, NTN-B)
    function renderValuationCalculators() {{
      const s = currentStock;
      const lpa = (s.details && s.details.lpa) ? Number(s.details.lpa) : null;
      const vpa = (s.details && s.details.vpa) ? Number(s.details.vpa) : null;
      const cot = Number(s.cotacao);

      // 1. Valor Intrínseco de Graham: sqrt(22.5 * LPA * VPA)
      let grahamPrice = null;
      let grahamMargin = null;
      if (lpa && vpa && lpa > 0 && vpa > 0) {{
        grahamPrice = Math.sqrt(22.5 * lpa * vpa);
        if (cot > 0) {{
          grahamMargin = ((grahamPrice - cot) / cot) * 100;
        }}
      }}

      // 2. Referência Décio Bazin: DPA Médio / 0.06 (Exige 6% de Dividend Yield Mínimo)
      let bazinPrice = null;
      let bazinMargin = null;
      if (s.div_yield && s.div_yield > 0 && cot > 0) {{
        const dpa = cot * s.div_yield;
        bazinPrice = dpa / 0.06;
        bazinMargin = ((bazinPrice - cot) / cot) * 100;
      }}

      // 3. Prêmio de Risco NTN-B
      const spreadVal = s.ey_spread !== null ? s.ey_spread : null;

      document.getElementById('valuationCalculatorsContainer').innerHTML = `
        <!-- Calculadora 1: Graham -->
        <div class="p-3.5 rounded-xl border border-slate-200 bg-slate-50/60 font-mono space-y-1.5">
          <div class="flex items-center justify-between">
            <span class="font-bold text-xs text-slate-900 font-sans flex items-center gap-1.5">
              <svg class="w-3.5 h-3.5 stroke-[1.75] text-sky-700 inline-block mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z"/></svg> Valor Intrínseco de Benjamin Graham (V.I.) <span class="info-badge cursor-pointer" data-tooltip="graham">ⓘ</span>
            </span>
            <span class="text-[10px] px-2 py-0.5 rounded-full font-bold ${{grahamMargin !== null && grahamMargin > 0 ? 'bg-emerald-100 text-emerald-950 border border-emerald-300' : 'bg-slate-200 text-slate-800'}}">
              ${{grahamMargin !== null ? (grahamMargin > 0 ? '+' : '') + grahamMargin.toFixed(1) + '% de Margem' : 'LPA/VPA Inválido'}}
            </span>
          </div>
          <div class="flex items-baseline justify-between text-xs pt-1">
            <span class="text-slate-600 font-sans">Valor Intrínseco Graham (V = √(22.5 × LPA × VPA)):</span>
            <b class="text-sm font-bold text-slate-900">${{grahamPrice ? formatCurrency(grahamPrice) : 'N/D'}}</b>
          </div>
          <p class="text-[10px] text-slate-500 font-sans">
            Referência teórica clássica de Benjamin Graham ponderando valor contábil e lucros passados.
          </p>
        </div>

        <!-- Calculadora 2: Bazin -->
        <div class="p-3.5 rounded-xl border border-slate-200 bg-slate-50/60 font-mono space-y-1.5">
          <div class="flex items-center justify-between">
            <span class="font-bold text-xs text-slate-900 font-sans flex items-center gap-1.5">
              <svg class="w-3.5 h-3.5 stroke-[1.75] text-emerald-700 inline-block mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path stroke-linecap="round" stroke-linejoin="round" d="M12 7v10m-3-7.5a2.5 2.5 0 015 0c0 2-3 2-3 4h3"/></svg> Referência Décio Bazin (DY 6%) <span class="info-badge cursor-pointer" data-tooltip="bazin">ⓘ</span>
            </span>
            <span class="text-[10px] px-2 py-0.5 rounded-full font-bold ${{bazinMargin !== null && bazinMargin > 0 ? 'bg-emerald-100 text-emerald-950 border border-emerald-300' : 'bg-slate-200 text-slate-800'}}">
              ${{bazinMargin !== null ? (bazinMargin > 0 ? '+' : '') + bazinMargin.toFixed(1) + '% vs Cotação' : 'Sem Proventos'}}
            </span>
          </div>
          <div class="flex items-baseline justify-between text-xs pt-1">
            <span class="text-slate-600 font-sans">Preço Teórico de Referência (DY 6%):</span>
            <b class="text-sm font-bold text-slate-900">${{bazinPrice ? formatCurrency(bazinPrice) : 'N/D'}}</b>
          </div>
          <p class="text-[10px] text-slate-500 font-sans">
            Modelo quantitativo de proventos: calcula a cotação em que a distribuição equivale a 6,0% ao ano.
          </p>
        </div>

        <!-- Calculadora 3: Prêmio Real vs NTN-B -->
        <div class="p-3.5 rounded-xl border border-slate-200 bg-slate-50/60 font-mono space-y-1.5">
          <div class="flex items-center justify-between">
            <span class="font-bold text-xs text-slate-900 font-sans flex items-center gap-1.5">
              <svg class="w-3.5 h-3.5 stroke-[1.75] text-indigo-700 inline-block mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 21v-8m0 0V5l-8 4v12h16V9l-8-4z"/></svg> Prêmio de Risco vs Tesouro NTN-B 2035 <span class="info-badge cursor-pointer" data-tooltip="ey_spread">ⓘ</span>
            </span>
            <span class="text-[10px] px-2 py-0.5 rounded-full font-bold ${{spreadVal !== null && spreadVal > 0 ? 'bg-emerald-100 text-emerald-950 border border-emerald-300' : 'bg-rose-100 text-rose-950 border border-rose-300'}}">
              ${{spreadVal !== null ? (spreadVal > 0 ? '+' : '') + spreadVal.toFixed(1) + '% Real' : 'N/D'}}
            </span>
          </div>
          <div class="flex items-baseline justify-between text-xs pt-1">
            <span class="text-slate-600 font-sans">Earnings Yield (Lucro/Preço):</span>
            <b class="text-sm font-bold text-slate-900">${{s.earnings_yield_pct !== null ? s.earnings_yield_pct.toFixed(1) + '%' : 'N/D'}}</b>
          </div>
          <p class="text-[10px] text-slate-500 font-sans">
            Compara o rendimento em lucros da empresa diretamente contra o custo de oportunidade do Tesouro IPCA+ 6,50%.
          </p>
        </div>

        <!-- Card Didático: Por que os Métodos de Valuation Divergem? -->
        <div class="p-3.5 rounded-xl border border-indigo-200 bg-indigo-50/60 font-sans space-y-2 mt-3 shadow-2xs">
          <div class="font-bold text-xs text-indigo-950 font-mono flex items-center gap-1.5 uppercase tracking-wider">
            <svg class="w-4 h-4 stroke-[1.75] text-indigo-700 inline-block mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 016-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0018 18a8.967 8.967 0 00-6 2.292m0-14.25v14.25"/></svg> Guia Didático: Por que os Métodos Divergem?
          </div>
          <div class="text-[11px] text-slate-700 space-y-1.5 leading-relaxed">
            <p>• <b>Benjamin Graham (Valor Intrínseco):</b> Foco em margem de segurança patrimonial e lucros sustentáveis passados. Exigente com empresas intensivas em capital ou holdings com ativos subavaliados.</p>
            <p>• <b>Décio Bazin (Referência de Proventos):</b> Foco exclusivo em fluxo histórico de dividendos. Estima a cotação teórica para obter 6% de retorno anual em dinheiro.</p>
            <p>• <b>Charlie Munger & Buffett (Qualidade & Moat):</b> Prioriza alta rentabilidade do capital reinvestido (ROIC/ROE > 15%). Uma empresa espetacular com múltiplos equilibrados supera um negócio medíocre a preço vil.</p>
          </div>
        </div>
      `;
    }}

    // Controle de Abas do Histórico de 5 Anos
    let currentHistTab = 'rev_lucro';

    function switchHistoryTab(tab) {{
      currentHistTab = tab;
      const bRev = document.getElementById('btnHistRev');
      const bRent = document.getElementById('btnHistRent');
      const bDiv = document.getElementById('btnHistDiv');
      
      const actCls = 'px-2.5 py-1 rounded-md transition font-bold bg-white text-slate-900 shadow-2xs cursor-pointer';
      const inactCls = 'px-2.5 py-1 rounded-md transition text-slate-600 hover:text-slate-900 cursor-pointer';

      if (bRev) bRev.className = tab === 'rev_lucro' ? actCls : inactCls;
      if (bRent) bRent.className = tab === 'rentabilidade' ? actCls : inactCls;
      if (bDiv) bDiv.className = tab === 'dividendos' ? actCls : inactCls;

      renderHistoryChart();
      renderDupont();
    }}

    // Renderizar Gráfico Histórico 5 Anos Interativo
    function renderHistoryChart() {{
      const s = currentStock;
      const h = s.historical_5y;
      if (!h || !h.years || h.years.length === 0) {{
        document.getElementById('historyChartContainer').innerHTML = '<div class="py-8 text-center text-xs font-mono text-slate-400">Histórico de 5 anos em processamento contábil.</div>';
        return;
      }}

      const subEl = document.getElementById('historySubtitle');
      const container = document.getElementById('historyChartContainer');
      const kpisGrid = document.getElementById('historyKpisGrid');

      const w = 620;
      const height = 175;
      const padL = 40;
      const padR = 25;
      const padT = 24;
      const padB = 25;
      const innerW = w - padL - padR;
      const innerH = height - padT - padB;
      const n = h.years.length;
      const scaleX = (i) => padL + (i / (n - 1)) * innerW;

      if (currentHistTab === 'rev_lucro') {{
        if (subEl) subEl.innerText = 'Trajetória auditada de faturamento líquido contra resultado final.';
        
        let maxVal = Math.max(...h.receita, ...h.lucro_liquido, 1);
        let minVal = Math.min(0, ...h.lucro_liquido);
        const range = maxVal - minVal;
        const scaleY = (v) => padT + innerH - ((v - minVal) / (range || 1)) * innerH;

        const revPts = h.receita.map((v, i) => [scaleX(i), scaleY(v)]);
        const revPath = revPts.map((p, i) => (i === 0 ? 'M' : 'L') + p[0].toFixed(1) + ',' + p[1].toFixed(1)).join(' ');
        const revArea = revPath + ` L${{scaleX(n-1).toFixed(1)}},${{(padT + innerH).toFixed(1)}} L${{scaleX(0).toFixed(1)}},${{(padT + innerH).toFixed(1)}} Z`;

        const lucroPts = h.lucro_liquido.map((v, i) => [scaleX(i), scaleY(v)]);
        const lucroPath = lucroPts.map((p, i) => (i === 0 ? 'M' : 'L') + p[0].toFixed(1) + ',' + p[1].toFixed(1)).join(' ');
        const lucroArea = lucroPath + ` L${{scaleX(n-1).toFixed(1)}},${{(padT + innerH).toFixed(1)}} L${{scaleX(0).toFixed(1)}},${{(padT + innerH).toFixed(1)}} Z`;

        const yearsLabelsHtml = h.years.map((y, i) => `
          <text x="${{scaleX(i).toFixed(1)}}" y="${{height - 6}}" text-anchor="middle" fill="#64748B" font-size="10" font-family="JetBrains Mono" font-weight="600">${{y.replace(' (LTM)','*')}}</text>
        `).join('');

        const revDotsHtml = revPts.map((p, i) => `
          <circle cx="${{p[0].toFixed(1)}}" cy="${{p[1].toFixed(1)}}" r="4" fill="#0EA5E9" stroke="#FFFFFF" stroke-width="2" />
          <text x="${{p[0].toFixed(1)}}" y="${{(p[1] - 8).toFixed(1)}}" text-anchor="middle" fill="#0369A1" font-size="9" font-family="JetBrains Mono" font-weight="700">${{formatBillions(h.receita[i]).replace('R$ ','')}}</text>
        `).join('');

        const lucroDotsHtml = lucroPts.map((p, i) => `
          <circle cx="${{p[0].toFixed(1)}}" cy="${{p[1].toFixed(1)}}" r="4" fill="#10B981" stroke="#FFFFFF" stroke-width="2" />
          <text x="${{p[0].toFixed(1)}}" y="${{(p[1] + 14).toFixed(1)}}" text-anchor="middle" fill="#047857" font-size="9" font-family="JetBrains Mono" font-weight="700">${{formatBillions(h.lucro_liquido[i]).replace('R$ ','')}}</text>
        `).join('');

        container.innerHTML = `
          <div class="flex items-center justify-end gap-3 text-[11px] font-mono font-bold mb-1">
            <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-sky-500"></span><span class="text-slate-700">Receita Líquida</span></span>
            <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-emerald-500"></span><span class="text-slate-700">Lucro Líquido</span></span>
          </div>
          <svg class="w-full h-44 select-none" viewBox="0 0 ${{w}} ${{height}}">
            <defs>
              <linearGradient id="gradRev" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="#0EA5E9" stop-opacity="0.25" />
                <stop offset="100%" stop-color="#0EA5E9" stop-opacity="0.0" />
              </linearGradient>
              <linearGradient id="gradLucro" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="#10B981" stop-opacity="0.3" />
                <stop offset="100%" stop-color="#10B981" stop-opacity="0.0" />
              </linearGradient>
            </defs>
            <line x1="${{padL}}" y1="${{padT}}" x2="${{w - padR}}" y2="${{padT}}" stroke="#E2E8F0" stroke-dasharray="3,3" />
            <line x1="${{padL}}" y1="${{padT + innerH / 2}}" x2="${{w - padR}}" y2="${{padT + innerH / 2}}" stroke="#E2E8F0" stroke-dasharray="3,3" />
            <line x1="${{padL}}" y1="${{padT + innerH}}" x2="${{w - padR}}" y2="${{padT + innerH}}" stroke="#CBD5E1" stroke-width="1.5" />
            <path d="${{revArea}}" fill="url(#gradRev)" />
            <path d="${{revPath}}" fill="none" stroke="#0EA5E9" stroke-width="2.5" stroke-linecap="round" />
            <path d="${{lucroArea}}" fill="url(#gradLucro)" />
            <path d="${{lucroPath}}" fill="none" stroke="#10B981" stroke-width="2.5" stroke-linecap="round" />
            ${{revDotsHtml}}
            ${{lucroDotsHtml}}
            ${{yearsLabelsHtml}}
          </svg>
        `;

        kpisGrid.innerHTML = `
          <div class="p-3 rounded-xl border border-slate-200 bg-slate-50 flex flex-col justify-between">
            <span class="text-[10px] text-slate-500 uppercase font-mono font-semibold">CAGR Receita (5A)</span>
            <div class="text-base font-bold font-mono text-slate-900 mt-1">${{h.cagr_receita_pct > 0 ? '+' : ''}}${{h.cagr_receita_pct}}%</div>
            <span class="text-[10px] text-slate-500 font-sans mt-0.5">${{h.cagr_receita_pct >= 10 ? 'Forte Expansão' : 'Crescimento Real'}}</span>
          </div>
          <div class="p-3 rounded-xl border border-slate-200 bg-slate-50 flex flex-col justify-between">
            <span class="text-[10px] text-slate-500 uppercase font-mono font-semibold">Anos com Lucro</span>
            <div class="text-base font-bold font-mono text-emerald-800 mt-1">${{h.anos_com_lucro}}</div>
            <span class="text-[10px] text-slate-500 font-sans mt-0.5">${{h.is_all_profitable ? 'Lucro Ininterrupto 5A' : 'Com Oscilações'}}</span>
          </div>
          <div class="p-3 rounded-xl border border-slate-200 bg-slate-50 flex flex-col justify-between">
            <span class="text-[10px] text-slate-500 uppercase font-mono font-semibold">CAGR Lucro (5A)</span>
            <div class="text-base font-bold font-mono text-slate-900 mt-1">${{h.cagr_lucro_pct > 0 ? '+' : ''}}${{h.cagr_lucro_pct}}%</div>
            <span class="text-[10px] text-slate-500 font-sans mt-0.5">${{h.estabilidade_margens}}</span>
          </div>
        `;

      }} else if (currentHistTab === 'rentabilidade') {{
        if (subEl) subEl.innerText = 'Trajetória de retorno sobre capital (ROIC/ROE) contra a taxa livre de risco (NTN-B 6,5%).';
        
        const vals = h.roic_roe || [s.roe || 0.1];
        let maxVal = Math.max(...vals, 0.20);
        let minVal = Math.min(0, ...vals);
        const range = maxVal - minVal;
        const scaleY = (v) => padT + innerH - ((v - minVal) / (range || 1)) * innerH;

        const pts = vals.map((v, i) => [scaleX(i), scaleY(v)]);
        const linePath = pts.map((p, i) => (i === 0 ? 'M' : 'L') + p[0].toFixed(1) + ',' + p[1].toFixed(1)).join(' ');
        const areaPath = linePath + ` L${{scaleX(n-1).toFixed(1)}},${{(padT + innerH).toFixed(1)}} L${{scaleX(0).toFixed(1)}},${{(padT + innerH).toFixed(1)}} Z`;

        const yNtnb = scaleY(0.065);

        const yearsLabelsHtml = h.years.map((y, i) => `
          <text x="${{scaleX(i).toFixed(1)}}" y="${{height - 6}}" text-anchor="middle" fill="#64748B" font-size="10" font-family="JetBrains Mono" font-weight="600">${{y.replace(' (LTM)','*')}}</text>
        `).join('');

        const dotsHtml = pts.map((p, i) => `
          <circle cx="${{p[0].toFixed(1)}}" cy="${{p[1].toFixed(1)}}" r="4.5" fill="#10B981" stroke="#FFFFFF" stroke-width="2" />
          <text x="${{p[0].toFixed(1)}}" y="${{(p[1] - 8).toFixed(1)}}" text-anchor="middle" fill="#047857" font-size="10" font-family="JetBrains Mono" font-weight="800">${{(vals[i] * 100).toFixed(1).replace('.', ',')}}%</text>
        `).join('');

        container.innerHTML = `
          <div class="flex items-center justify-end gap-3 text-[11px] font-mono font-bold mb-1">
            <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-emerald-500"></span><span class="text-slate-700">${{s.is_financial ? 'ROE Anual' : 'ROIC Anual'}}</span></span>
            <span class="flex items-center gap-1.5"><span class="w-4 h-0.5 border-t border-dashed border-slate-400"></span><span class="text-slate-500">NTN-B (+6,5%)</span></span>
          </div>
          <svg class="w-full h-44 select-none" viewBox="0 0 ${{w}} ${{height}}">
            <defs>
              <linearGradient id="gradRent" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="#10B981" stop-opacity="0.25" />
                <stop offset="100%" stop-color="#10B981" stop-opacity="0.0" />
              </linearGradient>
            </defs>
            <line x1="${{padL}}" y1="${{padT}}" x2="${{w - padR}}" y2="${{padT}}" stroke="#E2E8F0" stroke-dasharray="3,3" />
            <line x1="${{padL}}" y1="${{yNtnb}}" x2="${{w - padR}}" y2="${{yNtnb}}" stroke="#94A3B8" stroke-dasharray="4,4" stroke-width="1.5" />
            <text x="${{w - padR}}" y="${{yNtnb - 4}}" text-anchor="end" fill="#64748B" font-size="9" font-family="JetBrains Mono" font-weight="bold">NTN-B 6,5%</text>
            <line x1="${{padL}}" y1="${{padT + innerH}}" x2="${{w - padR}}" y2="${{padT + innerH}}" stroke="#CBD5E1" stroke-width="1.5" />
            <path d="${{areaPath}}" fill="url(#gradRent)" />
            <path d="${{linePath}}" fill="none" stroke="#10B981" stroke-width="2.5" stroke-linecap="round" />
            ${{dotsHtml}}
            ${{yearsLabelsHtml}}
          </svg>
        `;

        const avgRent = (vals.reduce((a, b) => a + b, 0) / vals.length) * 100;
        const minRent = Math.min(...vals) * 100;
        const maxRent = Math.max(...vals) * 100;

        kpisGrid.innerHTML = `
          <div class="p-3 rounded-xl border border-slate-200 bg-slate-50 flex flex-col justify-between">
            <span class="text-[10px] text-slate-500 uppercase font-mono font-semibold">Média 5 Anos (${{s.is_financial ? 'ROE' : 'ROIC'}})</span>
            <div class="text-base font-bold font-mono text-emerald-800 mt-1">${{avgRent.toFixed(1).replace('.', ',')}}%</div>
            <span class="text-[10px] text-slate-500 font-sans mt-0.5">${{avgRent >= 15 ? 'Rentabilidade Classe Mundial' : 'Acima da Renda Fixa'}}</span>
          </div>
          <div class="p-3 rounded-xl border border-slate-200 bg-slate-50 flex flex-col justify-between">
            <span class="text-[10px] text-slate-500 uppercase font-mono font-semibold">Pior Ano (Fundo de Ciclo)</span>
            <div class="text-base font-bold font-mono text-slate-900 mt-1">${{minRent.toFixed(1).replace('.', ',')}}%</div>
            <span class="text-[10px] text-slate-500 font-sans mt-0.5">${{minRent >= 10 ? 'Resiliente mesmo em crise' : 'Sensível ao ciclo'}}</span>
          </div>
          <div class="p-3 rounded-xl border border-slate-200 bg-slate-50 flex flex-col justify-between">
            <span class="text-[10px] text-slate-500 uppercase font-mono font-semibold">Melhor Ano (Pico)</span>
            <div class="text-base font-bold font-mono text-slate-900 mt-1">${{maxRent.toFixed(1).replace('.', ',')}}%</div>
            <span class="text-[10px] text-slate-500 font-sans mt-0.5">Potencial máximo comprovado</span>
          </div>
        `;

      }} else if (currentHistTab === 'dividendos') {{
        if (subEl) subEl.innerText = 'Evolução do Dividend Yield anual distribuído contra o teto Décio Bazin (6,0%).';
        
        const vals = h.div_yield || [s.div_yield || 0.05];
        let maxVal = Math.max(...vals, 0.12);
        let minVal = 0;
        const range = maxVal - minVal;
        const scaleY = (v) => padT + innerH - ((v - minVal) / (range || 1)) * innerH;

        const pts = vals.map((v, i) => [scaleX(i), scaleY(v)]);
        const linePath = pts.map((p, i) => (i === 0 ? 'M' : 'L') + p[0].toFixed(1) + ',' + p[1].toFixed(1)).join(' ');
        const areaPath = linePath + ` L${{scaleX(n-1).toFixed(1)}},${{(padT + innerH).toFixed(1)}} L${{scaleX(0).toFixed(1)}},${{(padT + innerH).toFixed(1)}} Z`;

        const yBazin = scaleY(0.06);

        const yearsLabelsHtml = h.years.map((y, i) => `
          <text x="${{scaleX(i).toFixed(1)}}" y="${{height - 6}}" text-anchor="middle" fill="#64748B" font-size="10" font-family="JetBrains Mono" font-weight="600">${{y.replace(' (LTM)','*')}}</text>
        `).join('');

        const dotsHtml = pts.map((p, i) => `
          <circle cx="${{p[0].toFixed(1)}}" cy="${{p[1].toFixed(1)}}" r="4.5" fill="#F59E0B" stroke="#FFFFFF" stroke-width="2" />
          <text x="${{p[0].toFixed(1)}}" y="${{(p[1] - 8).toFixed(1)}}" text-anchor="middle" fill="#B45309" font-size="10" font-family="JetBrains Mono" font-weight="800">${{(vals[i] * 100).toFixed(1).replace('.', ',')}}%</text>
        `).join('');

        container.innerHTML = `
          <div class="flex items-center justify-end gap-3 text-[11px] font-mono font-bold mb-1">
            <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-amber-500"></span><span class="text-slate-700">Dividend Yield Anual</span></span>
            <span class="flex items-center gap-1.5"><span class="w-4 h-0.5 border-t border-dashed border-emerald-500"></span><span class="text-emerald-700">Teto Bazin (6,0%)</span></span>
          </div>
          <svg class="w-full h-44 select-none" viewBox="0 0 ${{w}} ${{height}}">
            <defs>
              <linearGradient id="gradDiv" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="#F59E0B" stop-opacity="0.25" />
                <stop offset="100%" stop-color="#F59E0B" stop-opacity="0.0" />
              </linearGradient>
            </defs>
            <line x1="${{padL}}" y1="${{padT}}" x2="${{w - padR}}" y2="${{padT}}" stroke="#E2E8F0" stroke-dasharray="3,3" />
            <line x1="${{padL}}" y1="${{yBazin}}" x2="${{w - padR}}" y2="${{yBazin}}" stroke="#10B981" stroke-dasharray="4,4" stroke-width="1.5" />
            <text x="${{w - padR}}" y="${{yBazin - 4}}" text-anchor="end" fill="#047857" font-size="9" font-family="JetBrains Mono" font-weight="bold">Bazin 6%</text>
            <line x1="${{padL}}" y1="${{padT + innerH}}" x2="${{w - padR}}" y2="${{padT + innerH}}" stroke="#CBD5E1" stroke-width="1.5" />
            <path d="${{areaPath}}" fill="url(#gradDiv)" />
            <path d="${{linePath}}" fill="none" stroke="#F59E0B" stroke-width="2.5" stroke-linecap="round" />
            ${{dotsHtml}}
            ${{yearsLabelsHtml}}
          </svg>
        `;

        const avgDiv = (vals.reduce((a, b) => a + b, 0) / vals.length) * 100;
        const yearsAbove6 = vals.filter(v => v >= 0.06).length;

        kpisGrid.innerHTML = `
          <div class="p-3 rounded-xl border border-slate-200 bg-slate-50 flex flex-col justify-between">
            <span class="text-[10px] text-slate-500 uppercase font-mono font-semibold">DY Médio 5 Anos</span>
            <div class="text-base font-bold font-mono text-amber-800 mt-1">${{avgDiv.toFixed(1).replace('.', ',')}}%</div>
            <span class="text-[10px] text-slate-500 font-sans mt-0.5">${{avgDiv >= 6.0 ? 'Paga acima de 6% consistentemente' : 'Yield complementar'}}</span>
          </div>
          <div class="p-3 rounded-xl border border-slate-200 bg-slate-50 flex flex-col justify-between">
            <span class="text-[10px] text-slate-500 uppercase font-mono font-semibold">Anos Acima de 6% Bazin</span>
            <div class="text-base font-bold font-mono text-emerald-800 mt-1">${{yearsAbove6}} de ${{vals.length}} anos</div>
            <span class="text-[10px] text-slate-500 font-sans mt-0.5">${{yearsAbove6 >= 4 ? 'Excelente Vaca Leiteira' : 'Proventos Variáveis'}}</span>
          </div>
          <div class="p-3 rounded-xl border border-slate-200 bg-slate-50 flex flex-col justify-between">
            <span class="text-[10px] text-slate-500 uppercase font-mono font-semibold">DY Atual 12M</span>
            <div class="text-base font-bold font-mono text-slate-900 mt-1">${{s.div_yield ? (s.div_yield * 100).toFixed(1).replace('.', ',') + '%' : '0,0%'}}</div>
            <span class="text-[10px] text-slate-500 font-sans mt-0.5">Payout: ${{s.payout_implicito ? s.payout_implicito.toFixed(0) + '%' : 'N/D'}}</span>
          </div>
        `;
      }}
    }}

    // Renderizar Decomposição DuPont (Raio-X de Rentabilidade)
    function renderDupont() {{
      const s = currentStock;
      const isFin = s.is_financial;
      const dt = s.details || {{}};
      const lucro = dt.lucro_liq_12m || 0;
      const rec = dt.receita_liq_12m || 0;
      const ativo = dt.ativo_total || 0;
      const pl = dt.patrimonio_liquido || 0;
      const roeVal = s.roe || 0;

      const container = document.getElementById('dupontComponentsGrid');
      const verdictBox = document.getElementById('dupontVerdictBox');
      const badge = document.getElementById('dupontModelBadge');
      if (!container || !verdictBox) return;

      if (isFin) {{
        if (badge) badge.innerText = 'Modelo Bancário (Basileia)';
        const roa = ativo > 0 ? (lucro / ativo) : 0;
        const alav = pl > 0 ? (ativo / pl) : 0;

        container.innerHTML = `
          <div class="space-y-3 font-mono">
            <div class="flex flex-col sm:flex-row items-center justify-between gap-2.5">
              <!-- 1. ROA -->
              <div class="flex-1 w-full p-3.5 rounded-xl border border-slate-200 bg-white flex flex-col justify-between shadow-2xs">
                <div class="flex items-center justify-between text-[11px] text-slate-500 font-medium">
                  <span>1. ROA (Retorno Ativo)</span>
                  <span class="text-[10px] bg-slate-100 px-1.5 py-0.2 rounded font-bold">Lucro / Ativos</span>
                </div>
                <div class="text-xl font-bold text-slate-900 mt-2">${{(roa * 100).toFixed(2).replace('.', ',')}}%</div>
                <div class="text-[10px] text-slate-400 font-sans mt-1">Eficiência da carteira de crédito.</div>
              </div>

              <div class="text-slate-400 font-black text-sm px-1 hidden sm:block">✕</div>

              <!-- 2. Alavancagem de Balanço -->
              <div class="flex-1 w-full p-3.5 rounded-xl border border-slate-200 bg-white flex flex-col justify-between shadow-2xs">
                <div class="flex items-center justify-between text-[11px] text-slate-500 font-medium">
                  <span>2. Alavancagem de Balanço</span>
                  <span class="text-[10px] bg-slate-100 px-1.5 py-0.2 rounded font-bold">Ativo / PL</span>
                </div>
                <div class="text-xl font-bold text-slate-900 mt-2">${{alav.toFixed(2).replace('.', ',')}}x</div>
                <div class="text-[10px] text-slate-400 font-sans mt-1">Alavancagem regulatória prudencial.</div>
              </div>
            </div>

            <!-- Linha de Resultado -->
            <div class="flex items-center justify-between p-3.5 rounded-xl bg-indigo-50/70 border border-indigo-200">
              <div class="flex items-center gap-2">
                <span class="text-indigo-900 font-black text-base">=</span>
                <span class="text-xs font-mono text-indigo-950 font-bold uppercase tracking-wider">ROE Resultante:</span>
              </div>
              <div class="flex items-center gap-2">
                <span class="text-lg font-mono font-black text-indigo-900">${{(roeVal * 100).toFixed(1).replace('.', ',')}}% a.a.</span>
                <span class="text-[11px] font-sans text-indigo-700 font-medium hidden sm:inline">(Retorno s/ Patrimônio Líquido)</span>
              </div>
            </div>
          </div>
        `;

        verdictBox.innerHTML = `
          <div class="flex items-start gap-2">
            <span class="text-indigo-600 font-bold mt-0.5 text-base">ℹ️</span>
            <div>
              <b class="text-slate-900">Leitura Institucional DuPont (Setor Financeiro):</b>
              O banco entrega um ROE de <b>${{(roeVal * 100).toFixed(1).replace('.', ',')}}%</b> combinando uma margem sobre ativos totais (ROA) de <b>${{(roa * 100).toFixed(2).replace('.', ',')}}%</b> com alavancagem de <b>${{alav.toFixed(1).replace('.', ',')}}x</b>. 
              ${{alav <= 12 ? 'Estrutura de capital prudente e bem capitalizada segundo as regras de Basileia.' : 'Alavancagem requer acompanhamento dos índices de inadimplência.'}}
            </div>
          </div>
        `;
      }} else {{
        if (badge) badge.innerText = 'Modelo Clássico 3 Etapas';
        const mrg = rec > 0 ? (lucro / rec) : 0;
        const giro = ativo > 0 ? (rec / ativo) : 0;
        const alav = pl > 0 ? (ativo / pl) : 0;

        let engine = '';
        if (mrg >= 0.15 && alav <= 2.5) {{
          engine = '<b>Motor Saudável & Moat:</b> A rentabilidade é gerada majoritariamente por <b>forte margem líquida (' + (mrg*100).toFixed(1).replace('.', ',') + '%)</b> e poder de precificação, sem dependência arriscada de endividamento (alavancagem moderada de ' + alav.toFixed(1).replace('.', ',') + 'x). Padrão Charlie Munger.';
        }} else if (giro >= 1.0 && alav <= 2.8) {{
          engine = '<b>Motor de Giro Operacional:</b> A empresa compensa margens mais enxutas com <b>alto giro de ativos (' + giro.toFixed(2).replace('.', ',') + 'x)</b>, mostrando excelência na rotação de capital e eficiência comercial.';
        }} else if (alav > 3.0) {{
          engine = '<b>Atenção à Alavancagem:</b> Uma fração relevante do ROE decorre da <b>alavancagem financeira (' + alav.toFixed(1).replace('.', ',') + 'x)</b>. O retorno aos sócios é amplificado por capital de terceiros, tornando o lucro mais sensível às oscilações da Selic.';
        }} else {{
          engine = '<b>Estrutura Equilibrada:</b> O retorno é distribuído com equilíbrio entre margem de vendas (' + (mrg*100).toFixed(1).replace('.', ',') + '%), rotação dos ativos (' + giro.toFixed(2).replace('.', ',') + 'x) e alavancagem de ' + alav.toFixed(1).replace('.', ',') + 'x.';
        }}

        container.innerHTML = `
          <div class="space-y-3 font-mono">
            <div class="flex flex-col sm:flex-row items-center justify-between gap-2.5">
              <!-- 1. Margem Líquida -->
              <div class="flex-1 w-full p-3.5 rounded-xl border border-slate-200 bg-white flex flex-col justify-between shadow-2xs">
                <div class="flex items-center justify-between text-[11px] text-slate-500 font-medium">
                  <span class="flex items-center gap-1">1. Margem Líquida <span class="info-badge cursor-pointer" data-tooltip="mrg_liq">ⓘ</span></span>
                  <span class="text-[10px] bg-slate-100 px-1.5 py-0.2 rounded font-bold">Poder Preço</span>
                </div>
                <div class="text-xl font-bold ${{mrg >= 0.12 ? 'text-emerald-700' : 'text-slate-900'}} mt-2">${{(mrg * 100).toFixed(1).replace('.', ',')}}%</div>
                <div class="text-[10px] text-slate-400 font-sans mt-1">Lucro Líq. / Receita</div>
              </div>

              <div class="text-slate-400 font-black text-sm px-1 hidden sm:block">✕</div>

              <!-- 2. Giro do Ativo -->
              <div class="flex-1 w-full p-3.5 rounded-xl border border-slate-200 bg-white flex flex-col justify-between shadow-2xs">
                <div class="flex items-center justify-between text-[11px] text-slate-500 font-medium">
                  <span class="flex items-center gap-1">2. Giro do Ativo <span class="info-badge cursor-pointer" data-tooltip="giro">ⓘ</span></span>
                  <span class="text-[10px] bg-slate-100 px-1.5 py-0.2 rounded font-bold">Eficiência</span>
                </div>
                <div class="text-xl font-bold text-slate-900 mt-2">${{giro.toFixed(2).replace('.', ',')}}x</div>
                <div class="text-[10px] text-slate-400 font-sans mt-1">Receita / Ativo Total</div>
              </div>

              <div class="text-slate-400 font-black text-sm px-1 hidden sm:block">✕</div>

              <!-- 3. Alavancagem Financeira -->
              <div class="flex-1 w-full p-3.5 rounded-xl border border-slate-200 bg-white flex flex-col justify-between shadow-2xs">
                <div class="flex items-center justify-between text-[11px] text-slate-500 font-medium">
                  <span class="flex items-center gap-1">3. Alavancagem <span class="info-badge cursor-pointer" data-tooltip="alavancagem">ⓘ</span></span>
                  <span class="text-[10px] bg-slate-100 px-1.5 py-0.2 rounded font-bold">Balanço</span>
                </div>
                <div class="text-xl font-bold ${{alav > 3.0 ? 'text-amber-700' : 'text-slate-900'}} mt-2">${{alav.toFixed(2).replace('.', ',')}}x</div>
                <div class="text-[10px] text-slate-400 font-sans mt-1">Ativo Total / PL</div>
              </div>
            </div>

            <!-- Linha de Resultado -->
            <div class="flex items-center justify-between p-3.5 rounded-xl bg-indigo-50/70 border border-indigo-200">
              <div class="flex items-center gap-2">
                <span class="text-indigo-900 font-black text-base">=</span>
                <span class="text-xs font-mono text-indigo-950 font-bold uppercase tracking-wider">ROE DuPont Calculado:</span>
              </div>
              <div class="flex items-center gap-2">
                <span class="text-lg font-mono font-black text-indigo-900">${{(roeVal * 100).toFixed(1).replace('.', ',')}}% a.a.</span>
                <span class="text-[11px] font-sans text-indigo-700 font-medium hidden sm:inline">(Retorno s/ Patrimônio Líquido)</span>
              </div>
            </div>
          </div>
        `;

        verdictBox.innerHTML = `
          <div class="flex items-start gap-2">
            <span class="text-indigo-600 font-bold mt-0.5 text-base">💡</span>
            <div class="text-slate-800">
              ${{engine}}
            </div>
          </div>
        `;
      }}
    }}
    // Renderizar Pares Setoriais (Concorrentes no mesmo setor)
    function renderSectorPeers() {{
      const s = currentStock;
      const peers = APP_DATA.stocks
        .filter(o => o.setor === s.setor && o.ticker !== s.ticker && o.is_liquid_1m)
        .sort((a, b) => b.quality_score - a.quality_score)
        .slice(0, 6);

      document.getElementById('sectorPeersSubtitle').innerText = `Ativos do setor '${{s.setor}}' listados na B3 com liquidez diária.`;
      document.getElementById('sectorPeersCount').innerText = peers.length + ' concorrentes';

      const tbody = document.getElementById('sectorPeersTableBody');
      if (peers.length === 0) {{
        tbody.innerHTML = `<tr><td colspan="9" class="p-4 text-center text-xs text-slate-500">Nenhum concorrente direto com liquidez no mesmo setor.</td></tr>`;
        return;
      }}

      tbody.innerHTML = peers.map(p => `
        <tr class="hover:bg-slate-50 transition cursor-pointer" onclick="window.location.href='empresa.html?ticker=${{p.ticker}}'">
          <td class="py-2.5 px-3">
            <div class="flex items-center gap-2">
              ${{getStockLogoHtml(p.ticker, p.empresa, 'w-6 h-6')}}
              <div class="flex flex-col min-w-0">
                <span class="font-bold text-slate-900 font-mono text-xs leading-none">${{p.ticker}}</span>
                <span class="text-[10px] text-slate-500 font-sans truncate max-w-[120px]">${{p.empresa}}</span>
              </div>
            </div>
          </td>
          <td class="py-2.5 px-2 text-center">
            <span class="px-2 py-0.5 rounded-full font-mono font-bold text-[11px] bg-slate-100 text-slate-900 border border-slate-200">
              ${{p.quality_score.toFixed(1)}}
            </span>
          </td>
          <td class="py-2.5 px-2 text-right font-mono font-bold text-slate-900">${{formatCurrency(p.cotacao)}}</td>
          <td class="py-2.5 px-2 text-right font-mono font-semibold text-slate-800">${{formatMultiple(p.pl)}}</td>
          <td class="py-2.5 px-2 text-right font-mono font-semibold text-slate-800">${{p.is_financial ? 'N/A' : formatPercent(p.roic)}}</td>
          <td class="py-2.5 px-2 text-right font-mono font-semibold text-emerald-800">${{formatPercent(p.roe)}}</td>
          <td class="py-2.5 px-2 text-right font-mono text-slate-700">${{formatPercent(p.mrg_liq)}}</td>
          <td class="py-2.5 px-2 text-right font-mono text-slate-700">${{p.is_financial ? 'Bancos' : (p.div_liq_ebitda < 0 ? 'Caixa Líq.' : (p.div_liq_ebitda ? p.div_liq_ebitda.toFixed(1) + 'x' : 'N/D'))}}</td>
          <td class="py-2.5 px-2 text-right font-mono font-bold text-slate-900">${{formatPercent(p.div_yield)}}</td>
          <td class="py-2.5 px-3 text-center">
            <a href="empresa.html?ticker=${{p.ticker}}" class="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-slate-100 hover:bg-emerald-600 hover:text-white transition">
              Analisar ➜
            </a>
          </td>
        </tr>
      `).join('');
    }}

    // Renderizar Balanço e Síntese Fundamentalista
    function renderFinancialsAndCfa() {{
      const s = currentStock;
      const d = s.details || {{}};

      document.getElementById('companyFinancialDetailsGrid').innerHTML = `
        <div class="p-3.5 rounded-xl border border-slate-200 bg-slate-50/60 font-mono text-xs space-y-1.5">
          <div class="font-bold text-slate-900 font-sans border-b border-slate-200 pb-1 flex items-center justify-between">
            <span>🏛️ Balanço Patrimonial</span>
            <span class="text-[10px] text-slate-500 font-normal">Posição Líquida</span>
          </div>
          <div class="flex justify-between"><span class="text-slate-600 font-sans">Ativo Total:</span> <b>${{formatBillions(d.ativo_total)}}</b></div>
          <div class="flex justify-between"><span class="text-slate-600 font-sans">Disponibilidades (Caixa):</span> <b class="text-emerald-800 font-bold">${{formatBillions(d.disponibilidades)}}</b></div>
          <div class="flex justify-between"><span class="text-slate-600 font-sans">Dívida Bruta:</span> <b>${{formatBillions(d.divida_bruta)}}</b></div>
          <div class="flex justify-between"><span class="text-slate-600 font-sans">Dívida Líquida:</span> <b class="${{d.divida_liquida <= 0 ? 'text-emerald-800 font-bold' : 'text-slate-900'}}">${{formatBillions(d.divida_liquida)}}</b></div>
          <div class="flex justify-between"><span class="text-slate-600 font-sans">Patrimônio Líquido:</span> <b>${{formatBillions(d.patrimonio_liquido)}}</b></div>
          <div class="flex justify-between"><span class="text-slate-600 font-sans">VPA (Valor Patrimonial/Ação):</span> <b>R$ ${{d.vpa || 'N/D'}}</b></div>
        </div>

        <div class="p-3.5 rounded-xl border border-slate-200 bg-slate-50/60 font-mono text-xs space-y-1.5">
          <div class="font-bold text-slate-900 font-sans border-b border-slate-200 pb-1 flex items-center justify-between">
            <span>📊 Demonstração de Resultado (12M)</span>
            <span class="text-[10px] text-slate-500 font-normal">Desempenho</span>
          </div>
          <div class="flex justify-between"><span class="text-slate-600 font-sans">Receita Líquida (12m):</span> <b>${{formatBillions(d.receita_liq_12m)}}</b></div>
          <div class="flex justify-between"><span class="text-slate-600 font-sans">EBIT Operacional:</span> <b>${{formatBillions(d.ebit_12m)}}</b></div>
          <div class="flex justify-between"><span class="text-slate-600 font-sans">Lucro Líquido (12m):</span> <b class="text-emerald-800 font-bold">${{formatBillions(d.lucro_liq_12m)}}</b></div>
          <div class="flex justify-between"><span class="text-slate-600 font-sans">Lucro Trimestre (2T26):</span> <b>${{formatBillions(d.lucro_liq_3m)}}</b></div>
          <div class="flex justify-between"><span class="text-slate-600 font-sans">LPA (Lucro por Ação):</span> <b>R$ ${{d.lpa || 'N/D'}}</b></div>
          <div class="flex justify-between"><span class="text-slate-600 font-sans">Payout Médio Implícito:</span> <b>${{s.payout_implicito ? s.payout_implicito.toFixed(0) + '%' : 'N/D'}}</b></div>
        </div>
      `;

      let verdictBgClass = 'bg-slate-50 border-slate-200';
      let verdictBadgeClass = 'bg-slate-200 text-slate-800 border-slate-300';
      if (s.entry_tag === 'ASSIMETRIA_FAVORAVEL') {{
        verdictBgClass = 'bg-emerald-50/80 border-emerald-300';
        verdictBadgeClass = 'bg-emerald-600 text-white border-emerald-700';
      }} else if (s.entry_tag === 'PRECO_JUSTO') {{
        verdictBgClass = 'bg-amber-50/80 border-amber-300';
        verdictBadgeClass = 'bg-amber-600 text-white border-amber-700';
      }} else if (s.entry_tag === 'ESTICADA') {{
        verdictBgClass = 'bg-rose-50/80 border-rose-300';
        verdictBadgeClass = 'bg-rose-600 text-white border-rose-700';
      }}

      document.getElementById('companyCfaVerdictBox').innerHTML = `
        <div class="p-4 rounded-xl border ${{verdictBgClass}} font-sans space-y-2.5 transition-colors duration-200">
          <div class="flex items-center justify-between">
            <span class="font-bold text-xs text-slate-900 font-mono uppercase tracking-wider flex items-center gap-1.5">
              <svg class="w-4 h-4 text-slate-700 inline-block stroke-[1.75]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 3v18m9-12l-9-4-9 4m18 0l-9 4m9-4v6a4 4 0 01-4 4H7a4 4 0 01-4-4V7l9 4"/></svg> LEITURA DOS NÚMEROS (ANÁLISE QUANTITATIVA CVM)
            </span>
            <span class="text-[10px] px-2.5 py-0.5 rounded-full font-bold font-mono ${{verdictBadgeClass}} shadow-2xs">
              ${{s.entry_status}}
            </span>
          </div>
          <p class="text-xs text-slate-800 leading-relaxed font-sans">
            ${{s.rationale}}
          </p>
          <div class="text-[11px] text-slate-600 pt-1.5 border-t border-slate-200/80 flex flex-wrap items-center gap-3">
            <span>Tag Along: <b class="text-slate-900">100% Legal</b></span>
            <span>•</span>
            <span>Solvência: <b class="text-slate-900">${{d.divida_liquida <= 0 ? 'Caixa Líquido Positivo' : 'Endividamento sob Controle'}}</b></span>
            <span>•</span>
            <span>Consistência de Ciclo: <b class="text-slate-900">${{!s.is_distorted ? 'Lucro 2T26 Recorrente' : 'Atenção a One-offs'}}</b></span>
          </div>
        </div>
      `;
    }}

    // Renderizar Gauges Analógicos Bloomberg Calibrados
    function renderAnalogGauge(svgId, val, minVal, maxVal, label, options = {{}}) {{
      const svg = document.getElementById(svgId);
      if (!svg) return;

      if (options.isFinancial) {{
        svg.innerHTML = `
          <g transform="translate(80, 48)">
            <path d="M -40 0 A 40 40 0 0 1 40 0" fill="none" stroke="#E2E8F0" stroke-width="6" stroke-linecap="round" />
            <text x="0" y="-12" text-anchor="middle" fill="#0284C7" font-size="10" font-family="JetBrains Mono" font-weight="700">BANCOS</text>
            <text x="0" y="1" text-anchor="middle" fill="#64748B" font-size="8" font-family="Inter">Intermediação</text>
            <text x="0" y="15" text-anchor="middle" fill="#059669" font-size="9" font-family="JetBrains Mono" font-weight="bold">Basileia Ok</text>
          </g>
          <text x="80" y="85" text-anchor="middle" fill="#334155" font-size="9.5" font-family="JetBrains Mono" font-weight="700" letter-spacing="0.5">${{label.toUpperCase()}}</text>
          <text x="80" y="99" text-anchor="middle" fill="#64748B" font-size="8.5" font-family="Inter" font-weight="500">Ref: Basileia &gt; 11%</text>
        `;
        return;
      }}

      if (val === null || val === undefined || isNaN(val)) {{
        svg.innerHTML = `
          <g transform="translate(80, 48)">
            <path d="M -40 0 A 40 40 0 0 1 40 0" fill="none" stroke="#E2E8F0" stroke-width="6" stroke-linecap="round" />
            <text x="0" y="3" text-anchor="middle" fill="#94A3B8" font-size="11" font-family="JetBrains Mono" font-weight="bold">N/D</text>
          </g>
          <text x="80" y="85" text-anchor="middle" fill="#334155" font-size="9.5" font-family="JetBrains Mono" font-weight="700" letter-spacing="0.5">${{label.toUpperCase()}}</text>
          <text x="80" y="99" text-anchor="middle" fill="#64748B" font-size="8.5" font-family="Inter" font-weight="500">${{options.refText || ''}}</text>
        `;
        return;
      }}

      const norm = Math.max(0, Math.min(1, (val - minVal) / (maxVal - minVal)));
      const angleDeg = -180 + norm * 180;
      const angleRad = (angleDeg * Math.PI) / 180;

      const r = 40;
      const needleLen = 30;
      const nx = needleLen * Math.cos(angleRad);
      const ny = needleLen * Math.sin(angleRad);

      let valText = options.isPercent ? (val * 100).toFixed(1) + '%' : (options.isMultiple ? val.toFixed(1) + 'x' : val.toFixed(1));
      if (options.isSpread) valText = (val > 0 ? '+' : '') + val.toFixed(1) + '%';
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
        const rx1 = (r - 5) * Math.cos(refRad);
        const ry1 = (r - 5) * Math.sin(refRad);
        const rx2 = (r + 5) * Math.cos(refRad);
        const ry2 = (r + 5) * Math.sin(refRad);
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
          <path d="M -${{r}} 0 A ${{r}} ${{r}} 0 0 1 ${{r}} 0" fill="none" stroke="#E2E8F0" stroke-width="6" stroke-linecap="round" />
          <path d="M -${{r}} 0 A ${{r}} ${{r}} 0 0 1 ${{r}} 0" fill="none" stroke="url(#gaugeGrad_${{svgId}})" stroke-width="6" stroke-linecap="round" opacity="0.9" />
          ${{refTickHtml}}
          <line x1="0" y1="0" x2="${{nx.toFixed(1)}}" y2="${{ny.toFixed(1)}}" stroke="#0F172A" stroke-width="2.5" stroke-linecap="round" />
          <circle cx="0" cy="0" r="3.5" fill="#0F172A" />
          <circle cx="0" cy="0" r="1.2" fill="#FFFFFF" />
          <text x="0" y="16" text-anchor="middle" fill="${{fillColor}}" font-size="12" font-family="JetBrains Mono" font-weight="800">${{valText}}</text>
        </g>
        <text x="80" y="85" text-anchor="middle" fill="#334155" font-size="9.5" font-family="JetBrains Mono" font-weight="700" letter-spacing="0.5">${{label.toUpperCase()}}</text>
        <text x="80" y="99" text-anchor="middle" fill="#64748B" font-size="8.5" font-family="Inter" font-weight="500">${{options.refText || ''}}</text>
      `;
    }}

    // Renderizar Radar de 5 Pilares (Cálculo Idêntico e Unificado ao Dossiê 360°)
    function renderRadar() {{
      const s = currentStock;
      const svg = document.getElementById('heroRadarSvg');
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
      const labels = ['Valuation', 'Rentabilidade', 'Dividendos', 'Saúde Fin.', 'Consistência'];
      const pillarDescs = [
        s.ey_spread !== null ? (s.ey_spread > 0 ? '+' : '') + s.ey_spread.toFixed(1) + '% Real' : (s.pl ? 'P/L ' + formatMultiple(s.pl) : 'N/D'),
        formatPercent(s.roic || s.roe),
        formatPercent(s.div_yield),
        s.is_financial ? 'Basileia Ok' : (s.details && s.details.divida_liquida <= 0 ? 'Caixa Líq.' : (s.div_liq_ebitda !== null ? s.div_liq_ebitda.toFixed(1) + 'x' : 'N/D')),
        s.is_distorted ? 'Distorção' : 'Lucro 2T26 Ok'
      ];
      const r = 90;
      const angleStep = (Math.PI * 2) / 5;
      const startAngle = -Math.PI / 2;

      let webLines = '';
      [0.25, 0.5, 0.75, 1.0].forEach(level => {{
        const pts = [];
        for (let i = 0; i < 5; i++) {{
          const a = startAngle + i * angleStep;
          pts.push((Math.cos(a) * r * level).toFixed(1) + ',' + (Math.sin(a) * r * level).toFixed(1));
        }}
        webLines += `<polygon points="${{pts.join(' ')}}" fill="none" stroke="#E2E8F0" stroke-width="1" />`;
      }});

      let spokes = '';
      for (let i = 0; i < 5; i++) {{
        const a = startAngle + i * angleStep;
        spokes += `<line x1="0" y1="0" x2="${{(Math.cos(a) * r).toFixed(1)}}" y2="${{(Math.sin(a) * r).toFixed(1)}}" stroke="#CBD5E1" stroke-width="1" stroke-dasharray="2,2" />`;
      }}

      // Helper de Hierarquia de Cores dos Pilares
      function getPillarColorInfo(score) {{
        if (score >= 70) {{
          return {{
            hex: '#059669',
            textClass: 'text-emerald-950',
            bgClass: 'bg-emerald-50/90 border-emerald-300',
            badgeClass: 'bg-emerald-100 text-emerald-950 border-emerald-300',
            status: 'Forte'
          }};
        }} else if (score >= 50) {{
          return {{
            hex: '#D97706',
            textClass: 'text-amber-950',
            bgClass: 'bg-amber-50/90 border-amber-300',
            badgeClass: 'bg-amber-100 text-amber-950 border-amber-300',
            status: 'Neutro'
          }};
        }} else {{
          return {{
            hex: '#DC2626',
            textClass: 'text-rose-950',
            bgClass: 'bg-rose-50/90 border-rose-300',
            badgeClass: 'bg-rose-100 text-rose-950 border-rose-300',
            status: 'Atenção'
          }};
        }}
      }}

      const companyPts = scores.map((sc, i) => {{
        const a = startAngle + i * angleStep;
        const dist = (sc / 100) * r;
        return (Math.cos(a) * dist).toFixed(1) + ',' + (Math.sin(a) * dist).toFixed(1);
      }}).join(' ');

      const companyPointsHtml = scores.map((sc, i) => {{
        const info = getPillarColorInfo(sc);
        const a = startAngle + i * angleStep;
        const dist = (sc / 100) * r;
        return `<circle cx="${{(Math.cos(a) * dist).toFixed(1)}}" cy="${{(Math.sin(a) * dist).toFixed(1)}}" r="4" fill="${{info.hex}}" stroke="#FFFFFF" stroke-width="1.8" />`;
      }}).join('');

      const labelsHtml = labels.map((lbl, i) => {{
        const sc = scores[i];
        const info = getPillarColorInfo(sc);
        const a = startAngle + i * angleStep;
        const lx = Math.cos(a) * (r + 26);
        const ly = Math.sin(a) * (r + 14);
        const anchor = Math.abs(Math.cos(a)) < 0.25 ? 'middle' : (Math.cos(a) > 0 ? 'start' : 'end');
        return `<text x="${{lx.toFixed(1)}}" y="${{ly.toFixed(1)}}" text-anchor="${{anchor}}" fill="#334155" font-size="10" font-family="Inter" font-weight="600">${{lbl}} <tspan fill="${{info.hex}}" font-family="JetBrains Mono" font-weight="bold">(${{sc}})</tspan></text>`;
      }}).join('');

      svg.innerHTML = `
        <defs>
          <linearGradient id="heroRadarGrad" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="#10B981" stop-opacity="0.35" />
            <stop offset="100%" stop-color="#059669" stop-opacity="0.1" />
          </linearGradient>
        </defs>
        ${{webLines}}
        ${{spokes}}
        <polygon points="${{companyPts}}" fill="url(#heroRadarGrad)" stroke="#059669" stroke-width="2.5" stroke-linejoin="round" />
        ${{companyPointsHtml}}
        ${{labelsHtml}}
      `;

      document.getElementById('heroRadarPillarsGrid').innerHTML = labels.map((l, i) => {{
        const sc = scores[i];
        const info = getPillarColorInfo(sc);
        const desc = pillarDescs[i];
        return `
          <div class="border rounded-xl p-2 flex flex-col items-center justify-between text-center ${{info.bgClass}} shadow-2xs">
            <div class="text-[9.5px] text-slate-600 font-sans font-semibold uppercase tracking-wider truncate w-full">${{l}}</div>
            <div class="text-sm font-mono font-extrabold ${{info.textClass}} my-0.5">${{sc}}</div>
            <span class="text-[8.5px] font-mono px-1.5 py-0.2 rounded-full font-bold ${{info.badgeClass}} mb-0.5">${{info.status}}</span>
            <span class="text-[8.5px] font-sans text-slate-500 truncate w-full">${{desc}}</span>
          </div>
        `;
      }}).join('');
    }}

    // Busca de Ações no Header com Navegação por Teclado
    let companySearchHighlightedIndex = -1;
    let companySearchResults = [];

    function handleCompanySearch(query) {{
      const dd = document.getElementById('searchResultsDropdown');
      if (!query || query.trim().length === 0) {{
        dd.classList.add('hidden');
        companySearchResults = [];
        companySearchHighlightedIndex = -1;
        return;
      }}
      const q = query.trim().toLowerCase();
      companySearchResults = APP_DATA.stocks.map(s => {{
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
        .map(item => item.stock)
        .slice(0, 8);
      
      companySearchHighlightedIndex = companySearchResults.length > 0 ? 0 : -1;
      renderCompanySearchResults();
    }}

    function renderCompanySearchResults() {{
      const dd = document.getElementById('searchResultsDropdown');
      if (!dd) return;

      if (companySearchResults.length === 0) {{
        dd.innerHTML = `<div class="p-4 text-center text-xs font-mono text-slate-500">Nenhum ativo encontrado</div>`;
        dd.classList.remove('hidden');
        return;
      }}

      dd.innerHTML = `
        <div class="p-2 bg-slate-50 border-b border-slate-100 flex items-center justify-between text-[10px] font-mono text-slate-500">
          <span>${{companySearchResults.length}} sugestões encontradas</span>
          <span>Navegue com <b>↑</b> <b>↓</b> e <b>Enter</b></span>
        </div>
        ${{companySearchResults.map((s, idx) => {{
          const isHigh = idx === companySearchHighlightedIndex;
          const bg = isHigh ? 'bg-emerald-50/90 border-l-4 border-emerald-600' : 'hover:bg-slate-50';
          const scoreClass = s.quality_score >= 80 ? 'bg-emerald-100 text-emerald-950 border border-emerald-300' : (s.quality_score >= 65 ? 'bg-amber-100 text-amber-950 border border-amber-300' : 'bg-slate-100 text-slate-700 border border-slate-300');
          const plStr = (s.pl && s.pl > 0) ? s.pl.toFixed(1) + 'x' : 'N/D';
          const dyStr = s.div_yield ? (s.div_yield * 100).toFixed(1) + '%' : '0%';

          return `
            <a href="empresa.html?ticker=${{s.ticker}}" class="p-2.5 ${{bg}} transition cursor-pointer flex items-center justify-between select-none">
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
            </a>
          `;
        }}).join('')}}
      `;
      dd.classList.remove('hidden');
    }}

    function handleCompanySearchKeydown(e) {{
      const dd = document.getElementById('searchResultsDropdown');
      if (!dd || dd.classList.contains('hidden') || companySearchResults.length === 0) {{
        if (e.key === 'Escape') {{
          if (dd) dd.classList.add('hidden');
        }}
        return;
      }}

      if (e.key === 'ArrowDown') {{
        e.preventDefault();
        companySearchHighlightedIndex = (companySearchHighlightedIndex + 1) % companySearchResults.length;
        renderCompanySearchResults();
      }} else if (e.key === 'ArrowUp') {{
        e.preventDefault();
        companySearchHighlightedIndex = (companySearchHighlightedIndex - 1 + companySearchResults.length) % companySearchResults.length;
        renderCompanySearchResults();
      }} else if (e.key === 'Enter') {{
        e.preventDefault();
        if (companySearchHighlightedIndex >= 0 && companySearchHighlightedIndex < companySearchResults.length) {{
          window.location.href = 'empresa.html?ticker=' + encodeURIComponent(companySearchResults[companySearchHighlightedIndex].ticker);
        }}
      }} else if (e.key === 'Escape') {{
        dd.classList.add('hidden');
      }}
    }}

    function showSearchDropdown() {{
      const q = document.getElementById('companySearchInput').value;
      if (q && q.trim().length > 0) handleCompanySearch(q);
    }}

    document.addEventListener('click', (e) => {{
      const dd = document.getElementById('searchResultsDropdown');
      const input = document.getElementById('companySearchInput');
      if (dd && !dd.contains(e.target) && e.target !== input) {{
        dd.classList.add('hidden');
      }}
    }});

    // Atalhos Globais na Página da Empresa (/ para buscar, Esc para fechar)
    document.addEventListener('keydown', (e) => {{
      if (['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement.tagName) || document.activeElement.isContentEditable) {{
        if (e.key === 'Escape') {{
          const dd = document.getElementById('searchResultsDropdown');
          if (dd) dd.classList.add('hidden');
          document.activeElement.blur();
        }}
        return;
      }}

      if (e.key === '/') {{
        e.preventDefault();
        const inp = document.getElementById('companySearchInput');
        if (inp) {{
          inp.focus();
          inp.select();
        }}
      }} else if (e.key === 'Escape') {{
        const dd = document.getElementById('searchResultsDropdown');
        if (dd) dd.classList.add('hidden');
      }}
    }});

    // Compartilhar Link
    function copyAnalysisLink() {{
      const url = window.location.href;
      navigator.clipboard.writeText(url).then(() => {{
        const btnText = document.getElementById('copyLinkText');
        const orig = btnText.innerText;
        btnText.innerText = 'Copiado!';
        setTimeout(() => btnText.innerText = orig, 2000);
      }});
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
        desc: 'Fórmula clássica de Benjamin Graham: V = √(22,5 × LPA × VPA). Estipula uma referência teórica ponderando lucros por ação e valor contábil.',
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

    // Inicialização
    function init() {{
      renderHero();
      renderEssentialMultiples();
      renderValuationCalculators();
      renderHistoryChart();
      renderDupont();
      renderSectorPeers();
      renderFinancialsAndCfa();
      initGlobalTooltips();

      // Gauges Calibrados
      const s = currentStock;
      const roicOrRoe = s.roic || s.roe || 0;
      renderAnalogGauge('heroGaugeRoe', roicOrRoe, 0.0, 0.30, s.is_financial ? 'ROE' : 'ROIC', {{
        isPercent: true,
        refVal: 0.15,
        refText: 'Ref: ≥ 15%'
      }});
      renderAnalogGauge('heroGaugeDebt', s.div_liq_ebitda, -1.0, 3.5, 'Dív. Líq./EBITDA', {{
        isDebt: true,
        isFinancial: s.is_financial,
        refVal: 2.0,
        refText: 'Teto: 2.0x • Caixa = Top'
      }});
      renderAnalogGauge('heroGaugeSpread', s.ey_spread, -4.0, 10.0, 'Spread NTN-B', {{
        isSpread: true,
        refVal: 0.0,
        refText: 'Prêmio Real: > 0%'
      }});
      renderRadar();
    }}

    window.addEventListener('DOMContentLoaded', init);
  </script>
</body>
</html>
"""

    out_file = os.path.join(base_dir, "empresa.html")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Generated standalone company page: {out_file}")

    brain_dir = r"C:\Users\dougl\.gemini\antigravity\brain\19bf6b03-9073-46f6-9498-57b18f1f9a41"
    shutil.copyfile(out_file, os.path.join(brain_dir, "empresa.html"))
    print(f"Copied to brain artifact: {os.path.join(brain_dir, 'empresa.html')}")

if __name__ == '__main__':
    build_company_page()
