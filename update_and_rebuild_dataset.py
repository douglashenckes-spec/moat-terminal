"""
update_and_rebuild_dataset.py
=============================
Script de Execução Direta:
1. Aplica o recálculo do Moat Score nos dados de cache/standalone_data.json:
   - Se roic < 10%: moat_score = min(moat_score, round(45 + roic * 1.3, 1))
   - Se 10 <= roic < 13.5%: moat_score = min(moat_score, 66.5)
   - Atualiza quality_tier e quality_tag
   - Atualiza entry_status e entry_tag (alinhamento rigoroso sem contradições)
2. Regera index.html, empresa.html e todas as 203 páginas de ações.
3. Saneamento regex em lote dos 203 arquivos HTML de ações.
"""

import os
import re
import json
import math
import subprocess

def run_step(cmd_list, desc):
    print(f"\n[STEP] {desc}...")
    res = subprocess.run(cmd_list, capture_output=True, text=True, errors="replace")
    if res.returncode != 0:
        print(f"Erro em {desc}:")
        print(res.stderr)
        raise RuntimeError(f"Falha no comando {cmd_list}")
    else:
        out = (res.stdout or '').strip()
        print(f"Sucesso: {out[:200]}")

def update_dataset():
    data_path = "cache/standalone_data.json"
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    stocks = data.get("stocks", [])
    print(f"Processando {len(stocks)} ativos em {data_path}...")

    financial_tickers = {
        "CXSE3", "BBSE3", "PSSA3", "ITUB4", "ITUB3", "BBDC4", "BBDC3",
        "BBAS3", "SANB11", "SANB4", "SANB3", "BPAC11", "BRSR6", "BMEB4",
        "BMGB4", "PINE4", "ABCB4", "BRBI11", "ITSA4", "ITSA3", "WIZC3"
    }

    for s in stocks:
        ticker = s.get("ticker", "").upper().strip()
        setor = s.get("setor", "")
        is_fin = bool(s.get("is_financial")) or (ticker in financial_tickers)
        s["is_financial"] = is_fin

        roic_val = s.get("roic")
        # 1. Trava de Moat Score para empresas não-financeiras
        if not is_fin and roic_val is not None:
            try:
                r_num = float(roic_val)
                r_pct = r_num * 100.0 if abs(r_num) < 2.0 else r_num
                cur_score = float(s.get("quality_score", 0))

                if r_pct < 10.0:
                    cap = round(45.0 + (r_pct * 1.3), 1)
                    s["quality_score"] = min(cur_score, cap)
                elif r_pct < 13.5:
                    s["quality_score"] = min(cur_score, 66.5)

                # Atualiza Tier e Tag
                qs = s["quality_score"]
                if qs >= 80.0:
                    s["quality_tier"] = "Tier 1: Classe Mundial (Wide/Narrow Moat)"
                    s["quality_tag"] = "CLASSE_MUNDIAL"
                elif qs >= 65.0:
                    s["quality_tier"] = "Tier 2: Empresa Sólida / Saudável"
                    s["quality_tag"] = "SOLIDA"
                elif qs >= 50.0:
                    s["quality_tier"] = "Tier 3: Sem Fosso Claro / Sensível ao Ciclo"
                    s["quality_tag"] = "MEDIOCRE"
                else:
                    s["quality_tier"] = "Tier 4: Fragilidade Operacional / Risco de Capital"
                    s["quality_tag"] = "RISCO_ESTRUTURAL"
            except Exception as e:
                pass

        # 2. Alinhamento de Badges de Valuation
        pl_val = s.get("pl")
        det = s.get("details", {}) or {}
        dl_val = det.get("divida_liquida")
        dl_num = float(dl_val) if dl_val is not None and str(dl_val).lower() not in ["none", "nan"] else None
        dle_val = s.get("div_liq_ebitda")
        dle_num = float(dle_val) if dle_val is not None and str(dle_val).lower() not in ["none", "nan"] else None
        eveb_val = s.get("ev_ebitda")
        eveb_num = float(eveb_val) if eveb_val is not None and str(eveb_val).lower() not in ["none", "nan"] else None
        is_net_cash = (dl_num is not None and dl_num < 0) or (dle_num is not None and dle_num < 0)

        is_high_debt = (not is_fin) and (dle_num is not None and dle_num > 2.5)
        is_net_cash_bonus = (not is_fin) and is_net_cash and (eveb_num is not None and 0 < eveb_num <= 6.0)

        qs_val = s.get("quality_score", 50.0)
        base_exp_pl = 3.5 + 20.0 * (((max(20.0, min(100.0, float(qs_val))) - 20.0) / 80.0) ** 1.6)
        exp_pl = base_exp_pl
        if is_high_debt:
            exp_pl = base_exp_pl * 0.75
        elif is_net_cash_bonus:
            exp_pl = max(base_exp_pl * 1.30, 16.5)

        is_above_curve = (pl_val is not None and float(pl_val) > 0 and float(pl_val) < exp_pl)

        if is_above_curve:
            if pl_val is not None and float(pl_val) <= 11.0:
                s["entry_status"] = "🟢 MÚLTIPLOS ATRATIVOS"
                s["entry_color"] = "#10B981"
            else:
                s["entry_status"] = "🔵 DESCONTO RELATIVO AO MOAT"
                s["entry_color"] = "#0284C7"
            s["entry_tag"] = "ASSIMETRIA_FAVORAVEL"
        else:
            if pl_val is not None and float(pl_val) > 15.0:
                s["entry_status"] = "🔴 MÚLTIPLOS EXIGENTES"
                s["entry_tag"] = "ESTICADA"
                s["entry_color"] = "#EF4444"
            else:
                s["entry_status"] = "🟡 PRÊMIO SOBRE A CURVA"
                s["entry_tag"] = "PRECO_JUSTO"
                s["entry_color"] = "#F59E0B"

    with open(data_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("Cache standalone_data.json atualizado com sucesso!")

def sanitize_acoes_htmls():
    acoes_dir = "acoes"
    if not os.path.exists(acoes_dir):
        return

    financial_tickers = {
        "cxse3", "bbse3", "pssa3", "itub4", "itub3", "bbdc4", "bbdc3",
        "bbas3", "sanb11", "sanb4", "sanb3", "bpac11", "brsr6", "bmeb4",
        "bmgb4", "pine4", "abcb4", "brbi11", "itsa4", "itsa3", "wizc3"
    }

    count = 0
    for folder in os.listdir(acoes_dir):
        html_file = os.path.join(acoes_dir, folder, "index.html")
        if not os.path.isfile(html_file):
            continue

        with open(html_file, "r", encoding="utf-8") as f:
            content = f.read()

        # a) Padronizar title
        content = re.sub(r'<title>(.*?)\s*[-|]\s*[Mm]oat\s*[Tt]erminal</title>', r'<title>\1 • Moat Terminal</title>', content)
        content = re.sub(r' - moat terminal</title>', r' • Moat Terminal</title>', content, flags=re.IGNORECASE)

        # b) Trocar ROIC por ROE em seguradoras/bancos (como cxse3)
        if folder.lower() in financial_tickers:
            content = re.sub(r'ROIC\s+de\s+([0-9]+[.,][0-9]+%)', r'ROE de \1', content, flags=re.IGNORECASE)
            content = re.sub(r'ROIC\s+([0-9]+[.,][0-9]+%)', r'ROE \1', content, flags=re.IGNORECASE)

        # c) Substituir pontuação antiga de Tier 3
        content = content.replace("Tier 3: Operação Medíocre / Concorrência Predatória", "Tier 3: Sem Fosso Claro / Sensível ao Ciclo")

        with open(html_file, "w", encoding="utf-8") as f:
            f.write(content)

        count += 1

    print(f"Saneados {count} arquivos HTML de ações.")

if __name__ == "__main__":
    update_dataset()
    run_step(["python", "build_standalone_html.py"], "Recompilar Home index.html")
    run_step(["python", "build_company_page.py"], "Recompilar empresa.html e todas as 203 páginas")
    sanitize_acoes_htmls()
    print("\nTODAS AS ETAPAS CONCLUÍDAS COM SUCESSO!")
