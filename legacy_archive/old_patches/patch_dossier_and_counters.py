import re
import shutil

INDEX_FILE = "index.html"
BRAIN_ARTIFACT = r"C:\Users\dougl\.gemini\antigravity\brain\19bf6b03-9073-46f6-9498-57b18f1f9a41\munger_terminal.html"

with open(INDEX_FILE, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Injetar Resumo Executivo no diagHeaderCard
old_header_card = """        <!-- Rótulos de Categorias Institucionais Munger (Multi-Enquadramento) -->
        <div class="mt-3 pt-2.5 border-t border-slate-200 flex flex-wrap items-center gap-1.5">
          <span class="text-[11px] font-mono text-slate-600 uppercase tracking-wider font-semibold mr-0.5">Enquadramentos:</span>
          ${catBadgesHtml}
        </div>"""

new_header_card = """        <!-- Box Didático de Resumo Executivo para o Investidor -->
        <div class="mt-3 p-3 bg-emerald-50/70 border border-emerald-200/80 rounded-xl text-xs font-sans text-slate-800 leading-relaxed flex items-start gap-2.5">
          <span class="text-base mt-0.5">💡</span>
          <div>
            <span class="font-bold text-emerald-950 font-mono text-[10px] block uppercase tracking-wider mb-0.5">Diagnóstico para o Investidor</span>
            <span class="text-slate-700 text-xs">${generateHumanExecutiveSummary(s)}</span>
          </div>
        </div>

        <!-- Rótulos de Categorias Institucionais Munger (Multi-Enquadramento) -->
        <div class="mt-2.5 pt-2 border-t border-slate-200 flex flex-wrap items-center gap-1.5">
          <span class="text-[11px] font-mono text-slate-600 uppercase tracking-wider font-semibold mr-0.5">Enquadramentos:</span>
          ${catBadgesHtml}
        </div>"""

if old_header_card in text:
    text = text.replace(old_header_card, new_header_card)
    print("[OK] Resumo Executivo adicionado ao Dossiê!")
else:
    print("! Aviso: old_header_card nao encontrado exatamente.")

# 2. Tooltips no kpiGrid do Dossiê
old_kpi_grid = """        <div class="glass-card rounded-xl border border-slate-200 p-2.5 text-center">
          <div class="text-[10px] text-slate-700 uppercase font-bold flex items-center justify-center gap-1">
            <span>ROIC (Operacional)</span>
          </div>
          <div class="text-sm font-bold ${roicColor} mt-0.5">${s.is_financial ? 'N/A (Bancos)' : formatPercent(s.roic)}</div>
          <div class="text-[9px] text-slate-500 font-sans mt-0.5">${s.is_financial ? 'Inaplicável a bancos' : 'Capital Investido'}</div>
        </div>
        <div class="glass-card rounded-xl border border-slate-200 p-2.5 text-center">
          <div class="text-[10px] text-slate-700 uppercase font-bold flex items-center justify-center gap-1">
            <span>ROE (do Acionista)</span>
          </div>
          <div class="text-sm font-bold ${roeColor} mt-0.5">${formatPercent(s.roe)}</div>
          <div class="text-[9px] text-slate-500 font-sans mt-0.5">Retorno s/ Patrimônio</div>
        </div>
        <div class="glass-card rounded-xl border border-slate-200 p-2.5 text-center">
          <div class="text-[10px] text-slate-700 uppercase font-bold">Spread NTN-B</div>
          <div class="text-sm font-bold ${spreadColor} mt-0.5">${spreadStr}</div>
          <div class="text-[9px] text-slate-500 font-sans mt-0.5">Ref: 6,5% a.a.</div>
        </div>
        <div class="glass-card rounded-xl border border-slate-200 p-2.5 text-center">
          <div class="text-[10px] text-slate-700 uppercase font-bold">Dív.Líq / EBITDA</div>
          <div class="text-sm font-bold ${debtColor} mt-0.5">${debtStr}</div>
          <div class="text-[9px] text-slate-500 font-sans mt-0.5">${s.is_financial ? 'Regulação Bacen' : 'Solvência Auditada'}</div>
        </div>
        <div class="glass-card rounded-xl border border-slate-200 p-2.5 text-center">
          <div class="text-[10px] text-slate-700 uppercase font-bold">Margem Líq.</div>
          <div class="text-sm font-bold ${mrgColor} mt-0.5">${formatPercent(s.mrg_liq)}</div>
          <div class="text-[9px] text-slate-500 font-sans mt-0.5">Conversão em Lucro</div>
        </div>
        <div class="glass-card rounded-xl border border-slate-200 p-2.5 text-center">
          <div class="text-[10px] text-slate-700 uppercase font-bold">Payout Implícito</div>
          <div class="text-sm font-bold ${payoutColor} mt-0.5">${payoutStr}</div>
          <div class="text-[9px] text-slate-500 font-sans mt-0.5">${s.payout_tag ? s.payout_tag.split(' ')[1] || 'Normal' : 'Normal'}</div>
        </div>"""

new_kpi_grid = """        <div class="glass-card rounded-xl border border-slate-200 p-2.5 text-center">
          <div class="text-[10px] text-slate-700 uppercase font-bold flex items-center justify-center gap-1">
            <span>ROIC (Operacional)</span>
            <span class="info-badge" data-tooltip="roic">ⓘ</span>
          </div>
          <div class="text-sm font-bold ${roicColor} mt-0.5">${s.is_financial ? 'N/A (Bancos)' : formatPercent(s.roic)}</div>
          <div class="text-[9px] text-slate-500 font-sans mt-0.5">${s.is_financial ? 'Inaplicável a bancos' : 'Capital Investido'}</div>
        </div>
        <div class="glass-card rounded-xl border border-slate-200 p-2.5 text-center">
          <div class="text-[10px] text-slate-700 uppercase font-bold flex items-center justify-center gap-1">
            <span>ROE (do Acionista)</span>
            <span class="info-badge" data-tooltip="roe">ⓘ</span>
          </div>
          <div class="text-sm font-bold ${roeColor} mt-0.5">${formatPercent(s.roe)}</div>
          <div class="text-[9px] text-slate-500 font-sans mt-0.5">Retorno s/ Patrimônio</div>
        </div>
        <div class="glass-card rounded-xl border border-slate-200 p-2.5 text-center">
          <div class="text-[10px] text-slate-700 uppercase font-bold flex items-center justify-center gap-1">
            <span>Spread NTN-B</span>
            <span class="info-badge" data-tooltip="ey_spread">ⓘ</span>
          </div>
          <div class="text-sm font-bold ${spreadColor} mt-0.5">${spreadStr}</div>
          <div class="text-[9px] text-slate-500 font-sans mt-0.5">Ref: 6,5% a.a.</div>
        </div>
        <div class="glass-card rounded-xl border border-slate-200 p-2.5 text-center">
          <div class="text-[10px] text-slate-700 uppercase font-bold flex items-center justify-center gap-1">
            <span>Dív.Líq / EBITDA</span>
            <span class="info-badge" data-tooltip="debt">ⓘ</span>
          </div>
          <div class="text-sm font-bold ${debtColor} mt-0.5">${debtStr}</div>
          <div class="text-[9px] text-slate-500 font-sans mt-0.5">${s.is_financial ? 'Regulação Bacen' : 'Solvência Auditada'}</div>
        </div>
        <div class="glass-card rounded-xl border border-slate-200 p-2.5 text-center">
          <div class="text-[10px] text-slate-700 uppercase font-bold flex items-center justify-center gap-1">
            <span>Margem Líq.</span>
            <span class="info-badge" data-tooltip="mrg_liq">ⓘ</span>
          </div>
          <div class="text-sm font-bold ${mrgColor} mt-0.5">${formatPercent(s.mrg_liq)}</div>
          <div class="text-[9px] text-slate-500 font-sans mt-0.5">Conversão em Lucro</div>
        </div>
        <div class="glass-card rounded-xl border border-slate-200 p-2.5 text-center">
          <div class="text-[10px] text-slate-700 uppercase font-bold flex items-center justify-center gap-1">
            <span>Payout Implícito</span>
            <span class="info-badge" data-tooltip="payout">ⓘ</span>
          </div>
          <div class="text-sm font-bold ${payoutColor} mt-0.5">${payoutStr}</div>
          <div class="text-[9px] text-slate-500 font-sans mt-0.5">${s.payout_tag ? s.payout_tag.split(' ')[1] || 'Normal' : 'Normal'}</div>
        </div>"""

if old_kpi_grid in text:
    text = text.replace(old_kpi_grid, new_kpi_grid)
    print("[OK] KPI Grid do Dossiê enriquecido com balõezinhos!")
else:
    print("! Aviso: old_kpi_grid nao encontrado exatamente.")

# 3. Sincronizar contadores essenciais no updateFilterCounts
old_cnt_div = "const cntDiv = basePool.filter(s => getStockCategories(s).some(c => c.id === 'CAT_DIVIDENDS')).length;"
new_cnt_div = """const cntDiv = basePool.filter(s => getStockCategories(s).some(c => c.id === 'CAT_DIVIDENDS')).length;
      const elDivEss = document.getElementById('cnt-div-essential');
      if (elDivEss) elDivEss.textContent = cntDiv;
      const elSpreadEss = document.getElementById('cnt-spread-essential');
      if (elSpreadEss) elSpreadEss.textContent = cntSpread;"""

if old_cnt_div in text:
    text = text.replace(old_cnt_div, new_cnt_div)
    print("[OK] Contadores essenciais sincronizados!")

with open(INDEX_FILE, "w", encoding="utf-8") as f:
    f.write(text)

shutil.copy2(INDEX_FILE, BRAIN_ARTIFACT)
print("[OK] Arquivo index.html e artefato salvos com sucesso!")
