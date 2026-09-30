import re

with open('build_standalone_html.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update Drawer Tab Buttons HTML
old_tabs_html = """  <!-- Abas de Diagnóstico -->
  <div class="flex border-b border-slate-200 text-xs font-mono font-medium bg-white/[0.01] flex-shrink-0 p-1.5 gap-1.5">
    <button onclick="switchDiagTab('radar')" id="dtab-radar" class="tab-btn active flex-1 py-2 rounded-full text-center text-slate-800 font-semibold transition cursor-pointer">
      Gauges &amp; Radar
    </button>
    <button onclick="switchDiagTab('history')" id="dtab-history" class="tab-btn flex-1 py-2 rounded-full text-center text-slate-600 hover:text-slate-900 font-medium transition cursor-pointer">
      Histórico 5A
    </button>
    <button onclick="switchDiagTab('balance')" id="dtab-balance" class="tab-btn flex-1 py-2 rounded-full text-center text-slate-600 hover:text-slate-900 font-medium transition cursor-pointer">
      Balanço &amp; DRE
    </button>
    <button onclick="switchDiagTab('cfa')" id="dtab-cfa" class="tab-btn flex-1 py-2 rounded-full text-center text-slate-600 hover:text-slate-900 font-medium transition cursor-pointer">
      Veredito CFA
    </button>
  </div>"""

new_tabs_html = """  <!-- Abas de Diagnóstico Segmentadas em Relevo -->
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
    <button onclick="switchDiagTab('cfa')" id="dtab-cfa" class="tab-btn flex-1 py-1.5 rounded-lg text-center text-slate-600 hover:text-slate-900 hover:bg-white/60 font-medium transition cursor-pointer">
      Veredito CFA
    </button>
  </div>"""

assert old_tabs_html in code, "Failed to find old_tabs_html"
code = code.replace(old_tabs_html, new_tabs_html, 1)

# 2. Add switchDiagTab function implementation and update openDossierDrawer
old_drawer_code = """    function openDossierDrawer(t) {
      if (t) selectTicker(t);
      const drawer = document.getElementById('dossierDrawer');
      const backdrop = document.getElementById('dossierDrawerBackdrop');
      if (drawer) drawer.classList.remove('translate-x-full');
      if (backdrop) backdrop.classList.remove('hidden');
    }"""

# Note in build_standalone_html.py curly braces are doubled: {{ and }}
old_drawer_code_escaped = """    function openDossierDrawer(t) {{
      if (t) selectTicker(t);
      const drawer = document.getElementById('dossierDrawer');
      const backdrop = document.getElementById('dossierDrawerBackdrop');
      if (drawer) drawer.classList.remove('translate-x-full');
      if (backdrop) backdrop.classList.remove('hidden');
    }}"""

new_drawer_code_escaped = """    let currentDiagTab = 'radar';

    function switchDiagTab(tab) {{
      currentDiagTab = tab;
      const tabs = ['radar', 'history', 'balance', 'cfa'];
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
    }}"""

assert old_drawer_code_escaped in code, "Failed to find old_drawer_code_escaped"
code = code.replace(old_drawer_code_escaped, new_drawer_code_escaped, 1)

# 3. Fix Helper color functions (contrast)
old_colors = """    function getColorSpread(val) {{
      if (val === null || val === undefined) return 'text-slate-500';
      if (val >= 2.0) return 'text-emerald-700 font-bold';
      if (val >= 0.0) return 'text-amber-800 font-semibold';
      return 'text-rose-400 font-bold';
    }}

    function getColorRoe(val) {{
      if (val === null || val === undefined) return 'text-slate-500';
      const num = Math.abs(val) < 2.0 ? val * 100 : val;
      if (num >= 15.0) return 'text-emerald-700 font-bold';
      if (num >= 8.0) return 'text-slate-200';
      if (num >= 0.0) return 'text-amber-800';
      return 'text-rose-400 font-bold';
    }}

    function getColorPl(val) {{
      if (val === null || val === undefined) return 'text-slate-500';
      if (val < 0) return 'text-rose-400 font-bold';
      if (val <= 12.0) return 'text-emerald-800 font-semibold';
      if (val <= 22.0) return 'text-slate-200';
      return 'text-amber-800';
    }}

    function getColorDy(val) {{
      if (val === null || val === undefined) return 'text-slate-500';
      const num = Math.abs(val) < 2.0 ? val * 100 : val;
      if (num >= 6.0) return 'text-emerald-700 font-bold';
      if (num >= 3.0) return 'text-slate-200';
      if (num > 0) return 'text-slate-400';
      return 'text-slate-500';
    }}

    function getColorDebt(val, isFin = false) {{
      if (isFin) return 'text-indigo-800 font-medium';
      if (val === null || val === undefined) return 'text-slate-400';
      if (val < 0) return 'text-emerald-800 font-semibold';
      if (val <= 1.5) return 'text-emerald-800 font-semibold';
      if (val <= 2.7) return 'text-amber-800';
      return 'text-rose-400 font-bold';
    }}

    function getColorMrgLiq(val) {{
      if (val === null || val === undefined) return 'text-slate-500';
      const num = Math.abs(val) < 2.0 ? val * 100 : val;
      if (num >= 12.0) return 'text-emerald-800 font-semibold';
      if (num >= 4.0) return 'text-slate-200';
      if (num >= 0) return 'text-amber-800';
      return 'text-rose-400 font-bold';
    }}

    function getColorAcidTest(val) {{
      if (val === null || val === undefined) return 'text-slate-400';
      const num = Math.abs(val) < 2.0 ? val * 100 : val;
      if (num >= 75.0) return 'text-emerald-800 font-semibold';
      if (num >= 60.0) return 'text-amber-800';
      return 'text-rose-400 font-bold';
    }}"""

new_colors = """    function getColorSpread(val) {{
      if (val === null || val === undefined) return 'text-slate-500';
      if (val >= 2.0) return 'text-emerald-700 font-bold';
      if (val >= 0.0) return 'text-amber-800 font-semibold';
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
    }}"""

assert old_colors in code, "Failed to find old_colors"
code = code.replace(old_colors, new_colors, 1)

# 4. Fix Categorias Tab assets table formatting (portStocksTableBody)
old_port_table = """        tr.innerHTML = `
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
          <td class="py-2.5 px-3 text-right font-mono font-semibold ${{getColorRoe(s.roic || s.roe)}}">${{formatPercent(s.roic || s.roe)}}${{s.is_financial ? ' <span class="text-[9px] text-indigo-800 font-normal">(ROE)</span>' : ''}}</td>
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
          </td>"""

new_port_table = """        tr.innerHTML = `
          <td class="py-1.5 px-2.5 border-b border-slate-100">
            <div class="flex items-center gap-2">
              ${{getStockLogoHtml(s.ticker, s.empresa, 'w-5 h-5')}}
              <div class="flex flex-col min-w-0">
                <div class="flex items-center gap-1.5 leading-none">
                  <span class="text-xs font-bold text-slate-900 tracking-wide font-mono">${{s.ticker}}</span>
                  <span class="text-[9px] px-1.5 py-0.2 rounded-full font-mono font-bold ${{s.is_latest_balanco ? 'bg-emerald-50 text-emerald-800 border border-emerald-200' : 'bg-slate-100 text-slate-600 border border-slate-200'}}">${{s.tri_balanco}}</span>
                </div>
                <div class="text-[11px] text-slate-600 font-sans font-medium truncate max-w-[140px] leading-tight mt-0.5" title="${{s.empresa}} - ${{s.setor}}">${{s.empresa}}</div>
              </div>
            </div>
          </td>
          <td class="py-1.5 px-2 text-xs text-right font-mono font-bold text-slate-900 border-b border-slate-100">${{formatCurrency(s.cotacao)}}</td>
          <td class="py-1.5 px-1.5 text-center border-b border-slate-100">
            <span class="px-2 py-0.5 rounded-full font-bold text-[11px] ${{scoreBadgeClass}}">
              ${{s.quality_score.toFixed(1)}}
            </span>
          </td>
          <td class="py-1.5 px-2 text-xs text-right font-mono font-semibold border-b border-slate-100 ${{getColorPl(s.pl)}}">${{formatMultiple(s.pl)}}</td>
          <td class="py-1.5 px-2 text-xs text-right font-mono font-semibold border-b border-slate-100 ${{getColorRoe(s.roic || s.roe)}}">${{formatPercent(s.roic || s.roe)}}${{s.is_financial ? ' <span class="text-[9px] text-indigo-800 font-normal">(ROE)</span>' : ''}}</td>
          <td class="py-1.5 px-2 text-xs text-right font-mono font-bold border-b border-slate-100 ${{getColorDy(s.div_yield)}}">${{formatPercent(s.div_yield)}}</td>
          <td class="py-1.5 px-2 text-xs text-right font-mono border-b border-slate-100 ${{debtClass}}">${{debtDisplay}}</td>
          <td class="py-1.5 px-2 border-b border-slate-100">
            <div class="flex flex-wrap items-center gap-1 max-w-[280px]">
              ${{tagsHtml}}
            </div>
          </td>
          <td class="py-1.5 px-2 text-center border-b border-slate-100">
            <div class="flex items-center justify-center gap-1">
              <button onclick="event.stopPropagation(); selectTicker('${{s.ticker}}'); openDossierDrawer('${{s.ticker}}');" class="px-2 py-0.5 rounded-md text-[10px] font-mono font-bold bg-slate-100 hover:bg-slate-200 text-slate-800 transition cursor-pointer" title="Abrir Dossiê 360°">
                Dossiê 360°
              </button>
              <button onclick="event.stopPropagation(); openDedicatedCompanyPage('${{s.ticker}}');" class="p-1 rounded-md text-emerald-700 hover:bg-emerald-50 transition cursor-pointer" title="Página Completa da Empresa">
                <svg class="w-3.5 h-3.5 stroke-[2]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/></svg>
              </button>
            </div>
          </td>"""

assert old_port_table in code, "Failed to find old_port_table"
code = code.replace(old_port_table, new_port_table, 1)

# 5. Fix switchBubbleMetric button classes
old_bubble = """      if (bMcap) bMcap.className = metric === 'mcap' ? 'px-2.5 py-0.5 rounded-full text-xs font-mono font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/40' : 'px-2.5 py-0.5 rounded-full text-xs font-mono text-slate-400 hover:text-slate-200';
      if (bVol) bVol.className = metric === 'volume' ? 'px-2.5 py-0.5 rounded-full text-xs font-mono font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/40' : 'px-2.5 py-0.5 rounded-full text-xs font-mono text-slate-400 hover:text-slate-200';
      if (bFix) bFix.className = metric === 'fixed' ? 'px-2.5 py-0.5 rounded-full text-xs font-mono font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/40' : 'px-2.5 py-0.5 rounded-full text-xs font-mono text-slate-400 hover:text-slate-200';"""

new_bubble = """      if (bMcap) bMcap.className = metric === 'mcap' ? 'px-2.5 py-0.5 rounded-full text-xs font-mono font-bold bg-emerald-100 text-emerald-900 border border-emerald-300 shadow-2xs' : 'px-2.5 py-0.5 rounded-full text-xs font-mono text-slate-600 hover:text-slate-900 hover:bg-slate-100 border border-transparent';
      if (bVol) bVol.className = metric === 'volume' ? 'px-2.5 py-0.5 rounded-full text-xs font-mono font-bold bg-emerald-100 text-emerald-900 border border-emerald-300 shadow-2xs' : 'px-2.5 py-0.5 rounded-full text-xs font-mono text-slate-600 hover:text-slate-900 hover:bg-slate-100 border border-transparent';
      if (bFix) bFix.className = metric === 'fixed' ? 'px-2.5 py-0.5 rounded-full text-xs font-mono font-bold bg-emerald-100 text-emerald-900 border border-emerald-300 shadow-2xs' : 'px-2.5 py-0.5 rounded-full text-xs font-mono text-slate-600 hover:text-slate-900 hover:bg-slate-100 border border-transparent';"""

assert old_bubble in code, "Failed to find old_bubble"
code = code.replace(old_bubble, new_bubble, 1)

# 6. Fix diagHeaderCard: remove redundant buttons and improve contrast
old_header_card = """      // Card Cabeçalho estilo Glassmorphic Fintech
      const headScoreColor = s.quality_score >= 80 ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/50' : (s.quality_score >= 65 ? 'bg-amber-500/20 text-amber-300 border-amber-500/50' : (s.quality_score < 50 ? 'bg-rose-500/20 text-rose-300 border-rose-500/50' : 'bg-white/10 text-slate-300 border-slate-200'));

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
            <span class="px-3 py-1 rounded-full font-mono font-bold text-sm border ${{headScoreColor}} shadow-sm">
              SCORE ${{s.quality_score.toFixed(1)}}
            </span>
            <div class="flex items-center gap-1.5 mt-0.5">
              <button onclick="openDedicatedCompanyPage('${{s.ticker}}')" class="px-2.5 py-1 rounded-full text-[10px] font-mono font-bold text-white bg-emerald-600 hover:bg-emerald-700 flex items-center gap-1 transition cursor-pointer shadow-2xs" title="Abrir página dedicada em tela cheia">
                <span>Página Dedicada ↗</span>
              </button>
              <button onclick="openSelectedInMatrix()" class="px-2.5 py-1 rounded-full text-[10px] font-mono text-slate-700 hover:text-slate-900 bg-slate-100 hover:bg-slate-200 border border-slate-200 flex items-center gap-1 transition cursor-pointer" title="Localizar e ver na Matriz 2x2">
                <span>Ver na Matriz ➜</span>
              </button>
            </div>
          </div>
        </div>

        <!-- Rótulos de Categorias Institucionais Munger (Multi-Enquadramento) -->
        <div class="mt-3 pt-2.5 border-t border-slate-200 flex flex-wrap items-center gap-1.5">
          <span class="text-[10px] font-mono text-slate-400 uppercase tracking-wider font-semibold mr-0.5">Enquadramentos:</span>
          ${{catBadgesHtml}}
        </div>
      `;"""

new_header_card = """      // Card Cabeçalho estilo Glassmorphic Fintech
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
            <span class="px-3 py-1 rounded-full font-mono font-bold text-sm border ${{headScoreColor}} shadow-2xs">
              SCORE ${{s.quality_score.toFixed(1)}}
            </span>
            <div class="text-[11px] font-mono text-slate-600 font-medium mt-0.5">
              P/L Justo: <b class="text-slate-900 font-bold">${{formatMultiple(calcFairPL(s.quality_score))}}</b>
            </div>
          </div>
        </div>

        <!-- Rótulos de Categorias Institucionais Munger (Multi-Enquadramento) -->
        <div class="mt-3 pt-2.5 border-t border-slate-200 flex flex-wrap items-center gap-1.5">
          <span class="text-[11px] font-mono text-slate-600 uppercase tracking-wider font-semibold mr-0.5">Enquadramentos:</span>
          ${{catBadgesHtml}}
        </div>
      `;"""

assert old_header_card in code, "Failed to find old_header_card"
code = code.replace(old_header_card, new_header_card, 1)

# 7. Fix Balance Sheet details contrast
old_balance_card = """      // Espelho Balanço & DRE Reorganizado em Cartões Estruturados
      document.getElementById('auditSourceText').innerHTML = `
        <span class="text-slate-400 flex items-center gap-1.5"><span>🏛️</span> Fonte: ${{s.details.audit_source || 'Fundamentus'}}</span>
        <span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold ${{s.is_latest_balanco ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40' : 'bg-slate-100 text-slate-800 border border-slate-300 font-bold'}}">
          📅 Balanço Auditado: ${{s.ult_balanco}} (${{s.tri_balanco}})
        </span>
      `;"""

new_balance_card = """      // Espelho Balanço & DRE Reorganizado em Cartões Estruturados
      document.getElementById('auditSourceText').innerHTML = `
        <span class="text-slate-600 font-medium flex items-center gap-1.5"><span>🏛️</span> Fonte: ${{s.details.audit_source || 'Fundamentus'}}</span>
        <span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold ${{s.is_latest_balanco ? 'bg-emerald-100 text-emerald-900 border border-emerald-300' : 'bg-slate-100 text-slate-800 border border-slate-300'}}">
          📅 Balanço Auditado: ${{s.ult_balanco}} (${{s.tri_balanco}})
        </span>
      `;"""

assert old_balance_card in code, "Failed to find old_balance_card"
code = code.replace(old_balance_card, new_balance_card, 1)

# Fix divida_liquida and lucro colors in balance card
old_div_row = """<div class="flex justify-between py-0.5 border-b border-slate-200/60"><span class="text-slate-600 font-sans font-medium">Dívida Líquida:</span> <b class="${{s.details.divida_liquida <= 0 ? 'text-emerald-700 font-bold' : (s.details.divida_liquida > 1e10 ? 'text-rose-400 font-bold' : 'text-slate-200')}}">${{formatBillions(s.details.divida_liquida)}}</b></div>"""
new_div_row = """<div class="flex justify-between py-0.5 border-b border-slate-200/60"><span class="text-slate-600 font-sans font-medium">Dívida Líquida:</span> <b class="${{s.details.divida_liquida <= 0 ? 'text-emerald-700 font-bold' : (s.details.divida_liquida > 1e10 ? 'text-rose-700 font-bold' : 'text-slate-900 font-bold')}}">${{formatBillions(s.details.divida_liquida)}}</b></div>"""
assert old_div_row in code, "Failed to find old_div_row"
code = code.replace(old_div_row, new_div_row, 1)

old_lucro_rows = """            <div class="flex justify-between py-0.5 border-b border-slate-200/60"><span class="text-slate-600 font-sans font-medium">Lucro Líquido (12m):</span> <b class="${{s.details.lucro_liq_12m < 0 ? 'text-rose-400 font-bold' : 'text-emerald-700 font-bold'}}">${{formatBillions(s.details.lucro_liq_12m)}}</b></div>
            <div class="flex justify-between py-0.5 border-b border-slate-200/60"><span class="text-slate-600 font-sans font-medium">Lucro Trimestre (2T26):</span> <b class="${{s.details.lucro_liq_3m < 0 ? 'text-rose-400 font-bold' : 'text-emerald-700 font-bold'}}">${{formatBillions(s.details.lucro_liq_3m)}}</b></div>"""
new_lucro_rows = """            <div class="flex justify-between py-0.5 border-b border-slate-200/60"><span class="text-slate-600 font-sans font-medium">Lucro Líquido (12m):</span> <b class="${{s.details.lucro_liq_12m < 0 ? 'text-rose-700 font-bold' : 'text-emerald-700 font-bold'}}">${{formatBillions(s.details.lucro_liq_12m)}}</b></div>
            <div class="flex justify-between py-0.5 border-b border-slate-200/60"><span class="text-slate-600 font-sans font-medium">Lucro Trimestre (2T26):</span> <b class="${{s.details.lucro_liq_3m < 0 ? 'text-rose-700 font-bold' : 'text-emerald-700 font-bold'}}">${{formatBillions(s.details.lucro_liq_3m)}}</b></div>"""
assert old_lucro_rows in code, "Failed to find old_lucro_rows"
code = code.replace(old_lucro_rows, new_lucro_rows, 1)

old_dist_tag = """${{s.is_distorted ? 'bg-slate-100 text-slate-800 border border-slate-300 font-bold' : (s.details.lucro_liq_3m < 0 ? 'bg-rose-500/20 text-rose-300 border border-rose-500/40' : 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40')}}"""
new_dist_tag = """${{s.is_distorted ? 'bg-purple-100 text-purple-900 border border-purple-300 font-bold' : (s.details.lucro_liq_3m < 0 ? 'bg-rose-100 text-rose-900 border border-rose-300 font-bold' : 'bg-emerald-100 text-emerald-900 border border-emerald-300 font-bold')}}"""
assert old_dist_tag in code, "Failed to find old_dist_tag"
code = code.replace(old_dist_tag, new_dist_tag, 1)

# 8. Fix CFA Verdict contrast
old_cfa_banner = """      // Veredito CFA
      document.getElementById('cfaStatusBanner').innerHTML = `
        <div class="p-3.5 rounded-xl border text-xs backdrop-blur-md" style="background-color: ${{s.entry_color}}1A; border-color: ${{s.entry_color}}55;">
          <div class="font-bold font-mono text-sm" style="color: ${{s.entry_color}};">${{s.entry_status}}</div>
          <div class="text-slate-300 text-[11px] mt-1 font-sans">${{s.rationale}}</div>
        </div>
      `;"""

new_cfa_banner = """      // Veredito CFA
      const cfaTitleColor = s.entry_color === '#10E79D' ? '#047857' : (s.entry_color === '#FBBF24' ? '#B45309' : (s.entry_color === '#F43F5E' ? '#BE123C' : '#1E293B'));
      document.getElementById('cfaStatusBanner').innerHTML = `
        <div class="p-3.5 rounded-xl border text-xs backdrop-blur-md" style="background-color: ${{s.entry_color}}14; border-color: ${{s.entry_color}}44;">
          <div class="font-bold font-mono text-sm" style="color: ${{cfaTitleColor}};">${{s.entry_status}}</div>
          <div class="text-slate-700 text-xs mt-1 font-sans leading-relaxed">${{s.rationale}}</div>
        </div>
      `;"""

assert old_cfa_banner in code, "Failed to find old_cfa_banner"
code = code.replace(old_cfa_banner, new_cfa_banner, 1)

old_flags = """      let flagsHtml = '';
      if (s.is_commodity_peak) flagsHtml += '<span class="px-2.5 py-1 text-[10px] font-semibold bg-slate-100 text-slate-800 border border-slate-300 font-bold rounded-full">⚠️ Pico de Ciclo Commodities</span>';
      if (s.is_debt_vulnerable) flagsHtml += '<span class="px-2.5 py-1 text-[10px] font-semibold bg-rose-500/20 text-rose-300 border border-rose-500/40 rounded-full">⚠️ Vulnerabilidade a Juros</span>';
      if (!s.is_latest_balanco) flagsHtml += '<span class="px-2.5 py-1 text-[10px] font-semibold bg-slate-100 text-slate-800 border border-slate-300 font-bold rounded-full">⚠️ Balanço Defasado</span>';
      if (s.is_distorted) flagsHtml += `<span class="px-2.5 py-1 text-[10px] font-semibold bg-purple-500/20 text-purple-300 border border-purple-500/40 rounded-full">⚠️ Distorção Trimestral (${{s.distortion_tag}})</span>`;
      if (s.payout_implicito && s.payout_implicito > 100) flagsHtml += '<span class="px-2.5 py-1 text-[10px] font-semibold bg-rose-500/20 text-rose-300 border border-rose-500/40 rounded-full">⚠️ Payout Insustentável</span>';
      else if (s.payout_implicito && s.payout_implicito >= 40 && s.payout_implicito <= 85) flagsHtml += '<span class="px-2.5 py-1 text-[10px] font-semibold bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 rounded-full">💎 Proventos Disciplinados</span>';
      document.getElementById('cfaFlagsContainer').innerHTML = flagsHtml;"""

new_flags = """      let flagsHtml = '';
      if (s.is_commodity_peak) flagsHtml += '<span class="px-2.5 py-1 text-[10px] font-semibold bg-slate-100 text-slate-800 border border-slate-300 font-bold rounded-full">⚠️ Pico de Ciclo Commodities</span>';
      if (s.is_debt_vulnerable) flagsHtml += '<span class="px-2.5 py-1 text-[10px] font-semibold bg-rose-100 text-rose-900 border border-rose-300 font-bold rounded-full">⚠️ Vulnerabilidade a Juros</span>';
      if (!s.is_latest_balanco) flagsHtml += '<span class="px-2.5 py-1 text-[10px] font-semibold bg-slate-100 text-slate-800 border border-slate-300 font-bold rounded-full">⚠️ Balanço Defasado</span>';
      if (s.is_distorted) flagsHtml += `<span class="px-2.5 py-1 text-[10px] font-semibold bg-purple-100 text-purple-900 border border-purple-300 font-bold rounded-full">⚠️ Distorção Trimestral (${{s.distortion_tag}})</span>`;
      if (s.payout_implicito && s.payout_implicito > 100) flagsHtml += '<span class="px-2.5 py-1 text-[10px] font-semibold bg-rose-100 text-rose-900 border border-rose-300 font-bold rounded-full">⚠️ Payout Insustentável</span>';
      else if (s.payout_implicito && s.payout_implicito >= 40 && s.payout_implicito <= 85) flagsHtml += '<span class="px-2.5 py-1 text-[10px] font-semibold bg-emerald-100 text-emerald-900 border border-emerald-300 font-bold rounded-full">💎 Proventos Disciplinados</span>';
      document.getElementById('cfaFlagsContainer').innerHTML = flagsHtml;"""

assert old_flags in code, "Failed to find old_flags"
code = code.replace(old_flags, new_flags, 1)

# 9. Fix Checklist and CFA bullets contrast
old_checklist = """        <div class="glass-card border border-amber-500/30 rounded-xl p-3 text-xs font-mono mb-2">
          <div class="flex items-center justify-between border-b border-amber-500/20 pb-1.5 mb-2">
            <span class="font-bold text-amber-300 uppercase tracking-wider flex items-center gap-1.5">
              <span>🛡️</span> CHECKLIST DE RIGOR CFA (100% FUNDAMENTUS)
            </span>
            <span class="text-[10px] px-2 py-0.5 rounded-full font-bold ${{isAcidPass && isSolvencyPass && isCleanEarnings && isSafeCycle ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40' : 'bg-white/5 text-slate-400 border border-slate-200'}}">
              ${{isAcidPass && isSolvencyPass && isCleanEarnings && isSafeCycle ? '💎 APROVADA NO FILTRO' : 'AUDITORIA COMPLETA'}}
            </span>
          </div>
          <div class="grid grid-cols-2 sm:grid-cols-3 gap-2 text-[11px]">
            <div class="p-2 rounded-lg bg-white/[0.03] border border-slate-200">
              <div class="text-[10px] text-slate-700 font-bold">1. Munger Acid Test</div>
              <div class="font-bold ${{isAcidPass ? 'text-emerald-800' : 'text-amber-800'}} flex items-center justify-between">
                <span>${{acidDisplay}}</span>
                <span>${{isAcidPass ? '✅' : '⚠️'}}</span>
              </div>
              <div class="text-[9px] text-slate-500 font-sans">${{isAcidPass ? 'EBITDA vira EBIT' : 'Capex/Deprec. alto'}}</div>
            </div>

            <div class="p-2 rounded-lg bg-white/[0.03] border border-slate-200">
              <div class="text-[10px] text-slate-700 font-bold">2. Solvência Anti-Selic</div>
              <div class="font-bold ${{isSolvencyPass ? 'text-emerald-800' : 'text-rose-400'}} flex items-center justify-between">
                <span>${{solvencyDisplay}}</span>
                <span>${{isSolvencyPass ? '✅' : '⚠️'}}</span>
              </div>
              <div class="text-[9px] text-slate-500 font-sans">${{isSolvencyPass ? 'Dívida blindada' : 'Alavancagem alta'}}</div>
            </div>

            <div class="p-2 rounded-lg bg-white/[0.03] border border-slate-200">
              <div class="text-[10px] text-slate-700 font-bold">3. Governança Tag Along</div>
              <div class="font-bold ${{isGovPass ? 'text-emerald-800' : 'text-amber-800'}} flex items-center justify-between">
                <span>${{tipoStr}}</span>
                <span>${{isGovPass ? '✅' : 'ℹ️'}}</span>
              </div>
              <div class="text-[9px] text-slate-500 font-sans">${{isGovPass ? '100% Tag Along (ON)' : 'PN/UNT (Verificar)'}}</div>
            </div>

            <div class="p-2 rounded-lg bg-white/[0.03] border border-slate-200">
              <div class="text-[10px] text-slate-700 font-bold">4. Crescimento 5 Anos</div>
              <div class="font-bold ${{isGrowthPass ? 'text-emerald-800' : 'text-slate-300'}} flex items-center justify-between">
                <span>${{rawCres}}</span>
                <span>${{isGrowthPass ? '✅' : 'ℹ️'}}</span>
              </div>
              <div class="text-[9px] text-slate-500 font-sans">${{isGrowthPass ? 'Crescimento real' : 'Abaixo da inflação'}}</div>
            </div>

            <div class="p-2 rounded-lg bg-white/[0.03] border border-slate-200">
              <div class="text-[10px] text-slate-700 font-bold">5. Recorrência 2T26</div>
              <div class="font-bold ${{isCleanEarnings ? 'text-emerald-800' : 'text-purple-400'}} flex items-center justify-between">
                <span>${{isCleanEarnings ? 'Lucro Limpo' : 'Distorção'}}</span>
                <span>${{isCleanEarnings ? '✅' : '⚠️'}}</span>
              </div>
              <div class="text-[9px] text-slate-500 font-sans">${{isCleanEarnings ? 'Sem one-offs' : s.distortion_tag}}</div>
            </div>

            <div class="p-2 rounded-lg bg-white/[0.03] border border-slate-200">
              <div class="text-[10px] text-slate-700 font-bold">6. Ciclo Commodities</div>
              <div class="font-bold ${{isSafeCycle ? 'text-emerald-800' : 'text-amber-800'}} flex items-center justify-between">
                <span>${{isSafeCycle ? 'Ciclo Seguro' : 'Pico de Ciclo'}}</span>
                <span>${{isSafeCycle ? '✅' : '⚠️'}}</span>
              </div>
              <div class="text-[9px] text-slate-500 font-sans">${{isSafeCycle ? 'Fora de risco agudo' : 'Desaceleração 2T26'}}</div>
            </div>
          </div>
        </div>"""

new_checklist = """        <div class="glass-card border border-amber-300 bg-amber-50/30 rounded-xl p-3 text-xs font-mono mb-2">
          <div class="flex items-center justify-between border-b border-amber-200 pb-1.5 mb-2">
            <span class="font-bold text-amber-950 uppercase tracking-wider flex items-center gap-1.5">
              <span>🛡️</span> CHECKLIST DE RIGOR CFA (100% FUNDAMENTUS)
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
        </div>"""

assert old_checklist in code, "Failed to find old_checklist"
code = code.replace(old_checklist, new_checklist, 1)

old_bullets = """          <div class="glass-card border border-slate-200 rounded-xl p-3 text-xs">
            <div class="text-[11px] font-bold uppercase tracking-wider text-slate-400 mb-1 flex items-center gap-1.5">
              <span>${{b.icon}}</span> <span>${{b.title}}</span>
            </div>
            <div class="text-slate-700 leading-relaxed font-sans text-xs">${{b.content}}</div>
          </div>"""

new_bullets = """          <div class="glass-card border border-slate-200 bg-white rounded-xl p-3 text-xs shadow-2xs">
            <div class="text-[11px] font-bold uppercase tracking-wider text-slate-800 mb-1 flex items-center gap-1.5">
              <span>${{b.icon}}</span> <span>${{b.title}}</span>
            </div>
            <div class="text-slate-700 leading-relaxed font-sans text-xs">${{b.content}}</div>
          </div>"""

assert old_bullets in code, "Failed to find old_bullets"
code = code.replace(old_bullets, new_bullets, 1)

# 10. Fix renderHistoryTab contrast and colors
old_hist_badges = """      // 1. Badges Mungerianos de Consistência
      const cagrRecColor = h.cagr_receita_pct >= 10.0 ? 'text-emerald-300 bg-emerald-500/20 border-emerald-500/40' : (h.cagr_receita_pct >= 0 ? 'text-sky-300 bg-sky-500/20 border-sky-500/40' : 'text-rose-300 bg-rose-500/20 border-rose-500/40');
      const cagrLucColor = h.cagr_lucro_pct >= 10.0 ? 'text-emerald-300 bg-emerald-500/20 border-emerald-500/40' : (h.cagr_lucro_pct >= 0 ? 'text-amber-300 bg-amber-500/20 border-amber-500/40' : 'text-rose-300 bg-rose-500/20 border-rose-500/40');
      const anosLucColor = h.is_all_profitable ? 'text-emerald-300 bg-emerald-500/20 border-emerald-500/40' : 'text-amber-300 bg-amber-500/20 border-amber-500/40';"""

new_hist_badges = """      // 1. Badges Mungerianos de Consistência
      const cagrRecColor = h.cagr_receita_pct >= 10.0 ? 'text-emerald-900 bg-emerald-100 border-emerald-300' : (h.cagr_receita_pct >= 0 ? 'text-sky-900 bg-sky-100 border-sky-300' : 'text-rose-900 bg-rose-100 border-rose-300');
      const cagrLucColor = h.cagr_lucro_pct >= 10.0 ? 'text-emerald-900 bg-emerald-100 border-emerald-300' : (h.cagr_lucro_pct >= 0 ? 'text-amber-900 bg-amber-100 border-amber-300' : 'text-rose-900 bg-rose-100 border-rose-300');
      const anosLucColor = h.is_all_profitable ? 'text-emerald-900 bg-emerald-100 border-emerald-300' : 'text-amber-900 bg-amber-100 border-amber-300';"""

assert old_hist_badges in code, "Failed to find old_hist_badges"
code = code.replace(old_hist_badges, new_hist_badges, 1)

old_axis_text = """fill="#94A3B8" font-size="10" font-family="JetBrains Mono" font-weight="600" """
new_axis_text = """fill="#475569" font-size="10" font-family="JetBrains Mono" font-weight="600" """
if old_axis_text in code:
    code = code.replace(old_axis_text, new_axis_text)

old_hist_titles = """              <span class="font-mono font-bold text-xs text-amber-300 flex items-center gap-1">"""
new_hist_titles = """              <span class="font-mono font-bold text-xs text-amber-900 flex items-center gap-1">"""
assert old_hist_titles in code, "Failed to find old_hist_titles"
code = code.replace(old_hist_titles, new_hist_titles, 1)

old_hist_titles2 = """              <span class="font-mono font-bold text-xs text-emerald-300 flex items-center gap-1">"""
new_hist_titles2 = """              <span class="font-mono font-bold text-xs text-emerald-900 flex items-center gap-1">"""
assert old_hist_titles2 in code, "Failed to find old_hist_titles2"
code = code.replace(old_hist_titles2, new_hist_titles2, 1)

old_hist_table_hdr = """          <div class="text-[10px] font-mono font-bold uppercase tracking-wider text-slate-400 mb-2 flex items-center gap-1.5">"""
new_hist_table_hdr = """          <div class="text-[11px] font-mono font-bold uppercase tracking-wider text-slate-800 mb-2 flex items-center gap-1.5">"""
assert old_hist_table_hdr in code, "Failed to find old_hist_table_hdr"
code = code.replace(old_hist_table_hdr, new_hist_table_hdr, 1)

old_divide_tbody = """<tbody class="divide-y divide-white/5">"""
new_divide_tbody = """<tbody class="divide-y divide-slate-100">"""
assert old_divide_tbody in code, "Failed to find old_divide_tbody"
code = code.replace(old_divide_tbody, new_divide_tbody, 1)

old_hist_lucro_td = """${{h.lucro_liquido.map(l => `<td class="py-1.5 px-2 text-right font-bold ${{l > 0 ? 'text-emerald-800' : 'text-rose-400'}}">${{formatBillions(l)}}</td>`).join('')}}"""
new_hist_lucro_td = """${{h.lucro_liquido.map(l => `<td class="py-1.5 px-2 text-right font-bold ${{l > 0 ? 'text-emerald-800' : 'text-rose-700'}}">${{formatBillions(l)}}</td>`).join('')}}"""
assert old_hist_lucro_td in code, "Failed to find old_hist_lucro_td"
code = code.replace(old_hist_lucro_td, new_hist_lucro_td, 1)

with open('build_standalone_html.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("build_standalone_html.py successfully updated!")
