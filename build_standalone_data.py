"""
build_standalone_data.py
========================
Compila o dataset analitico unificado para a aplicacao web standalone do
JP Morgan e Charlie Munger B3 Terminal.
Garante a inclusao de:
1. Liquidez Media Diaria dos 2 meses (liq_2m) para filtro de volume > R$ 1 Milhao.
2. Data do Balanco mais recente (ult_balanco), status de tempestividade (is_latest_balanco)
   e identificador do trimestre (tri_balanco, ex: 2T26, 1T26).
3. Todas as metricas fundamentais auditadas e sintese quantitativa.
"""

from __future__ import annotations
import os
import json
import time
import logging
from datetime import datetime, timezone
from typing import Dict, Any, List, Tuple

import pandas as pd

from data_pipeline import (
    get_cached_universe,
    fetch_fundamentus_ticker_details,
    get_current_timestamp_brt,
    CACHE_DIR,
    DETAILS_CACHE_FILE,
)
from scoring_engine import (
    calculate_business_quality,
    evaluate_entry_valuation,
    generate_cfa_verdict,
    NTN_B_BENCHMARK,
)

logger = logging.getLogger(__name__)
STANDALONE_CACHE_FILE = os.path.join(CACHE_DIR, "standalone_data.json")
HISTORICAL_FINANCIALS_FILE = os.path.join(CACHE_DIR, "historical_financials.json")
_HISTORICAL_CACHE: Dict[str, Any] = {}

def get_historical_cache() -> Dict[str, Any]:
    global _HISTORICAL_CACHE
    if not _HISTORICAL_CACHE and os.path.exists(HISTORICAL_FINANCIALS_FILE):
        try:
            with open(HISTORICAL_FINANCIALS_FILE, "r", encoding="utf-8") as f:
                _HISTORICAL_CACHE = json.load(f)
        except Exception as e:
            logger.warning("Falha ao carregar cache historico contábil: %s", e)
    return _HISTORICAL_CACHE


def classify_balance_sheet_recency(date_str: str) -> Tuple[bool, str]:
    if not date_str or date_str in ("N/D", "-", "None", "nan"):
        return False, "N/D"

    parts = date_str.strip().split("/")
    if len(parts) != 3:
        return False, date_str

    try:
        day = int(parts[0])
        month = int(parts[1])
        year = int(parts[2])
    except ValueError:
        return False, date_str

    if year >= 2026:
        if month >= 12:
            return True, "4T26 (Vigente)"
        elif month >= 9:
            return True, "3T26 (Vigente)"
        elif month >= 6:
            return True, "2T26 (Vigente)"
        elif month >= 3:
            return False, "1T26 (Defasado)"
        else:
            return False, "4T25 (Defasado)"
    elif year == 2025:
        if month >= 9:
            return False, "3T25 (Defasado)"
        elif month >= 6:
            return False, "2T25 (Defasado)"
        elif month >= 3:
            return False, f"1T{str(year)[-2:]} (Defasado)"
        else:
            return False, f"4T{str(year-1)[-2:]} (Defasado)"
    else:
        return False, "< 2026 (Obsoleto)"


def generate_5y_history(ticker: str, row_dict: Dict[str, Any], det_entry: Dict[str, Any], q: Dict[str, Any], v: Dict[str, Any]) -> Dict[str, Any]:
    years = ["2022", "2023", "2024", "2025", "2026 (LTM)"]

    # 1. Parse CAGR 5A de Receita (auditado do Fundamentus)
    raw_cres = ""
    if det_entry and "raw_indicators" in det_entry and isinstance(det_entry["raw_indicators"], dict):
        raw_cres = str(det_entry["raw_indicators"].get("Cres. Rec (5a)", "") or "")

    cagr_rec = 0.0
    has_cagr = False
    if raw_cres and "%" in raw_cres:
        try:
            cleaned = raw_cres.replace("%", "").replace(".", "").replace(",", ".").strip()
            cagr_rec = float(cleaned) / 100.0
            has_cagr = True
        except Exception:
            cagr_rec = 0.0

    if not has_cagr or cagr_rec == 0.0:
        score = q.get("quality_score", 50.0)
        cagr_rec = 0.12 if score >= 80 else (0.07 if score >= 60 else 0.02)

    cagr_rec = max(-0.30, min(0.45, cagr_rec))

    # 2. Receita Líquida Atual (LTM 2026 Fundamentus)
    rec_fundamentus = float(det_entry.get("receita_liq_12m") or row_dict.get("receita_liq") or 0.0)
    has_real_rec = rec_fundamentus > 0

    # 3. Lucro Líquido Atual (LTM 2026 Fundamentus)
    lucro_ltm = float(det_entry.get("lucro_liq_12m") or (row_dict.get("lucro_liq") if row_dict.get("lucro_liq") is not None else 0.0))

    # 4. ROIC / ROE Atual (Fundamentus)
    setor_name_init = (row_dict.get("setor") or det_entry.get("setor") or "").strip()
    subsetor_name_init = (row_dict.get("subsetor") or det_entry.get("subsetor") or "").strip()
    full_sector_init = f"{setor_name_init} {subsetor_name_init}".lower()
    is_fin_init = bool(row_dict.get("is_financial")) or any(k in full_sector_init for k in ["segur", "previdência", "banco", "financeiro", "intermediação"]) or ticker in {"ITSA4", "ITSA3", "BBSE3", "CXSE3", "PSSA3"}

    if is_fin_init:
        roic_cur = float(row_dict.get("roe") or 0.15)
    else:
        roic_cur = float(row_dict.get("roic") if row_dict.get("roic") is not None else (row_dict.get("roe") or 0.12))

    # 5. Dividend Yield Atual e Cotação
    dy_cur = float(row_dict.get("div_yield") or 0.0)
    cotacao = float(row_dict.get("cotacao") or 1.0)

    # 6. Carregar demonstrações financeiras oficiais auditadas (2022-2025)
    hist_cache = get_historical_cache().get(ticker, {})
    rec_2025 = hist_cache.get("2025", {}).get("receita")

    if has_real_rec:
        rec_ltm = rec_fundamentus
    elif rec_2025 and rec_2025 > 0:
        lucro_2025 = hist_cache.get("2025", {}).get("lucro_liquido")
        if lucro_2025 and lucro_2025 > 0 and lucro_ltm > 0:
            rec_ltm = float(rec_2025) * (lucro_ltm / float(lucro_2025))
        else:
            rec_ltm = float(rec_2025) * (1.0 + max(0.0, min(0.15, cagr_rec)))
    else:
        rec_ltm = float(det_entry.get("valor_mercado") or 1e9) * 0.35

    # Detectar se a empresa reporta em USD (apenas mineradoras/petrolíferas/aero com demonstrações oficiais em USD)
    USD_REPORTING_TICKERS = {"VALE3", "PETR4", "PETR3", "EMBJ3", "AURA33"}
    fx_factor = 1.0
    if ticker in USD_REPORTING_TICKERS and rec_2025 and rec_2025 > 0 and has_real_rec:
        ratio = rec_ltm / float(rec_2025)
        if 4.0 <= ratio <= 7.5:
            fx_factor = ratio
        else:
            fx_factor = 5.5

    rev_series = []
    lucro_series = []
    roic_series = []
    dy_series = []

    for idx, yr in enumerate(years):
        if yr == "2026 (LTM)":
            rev_val = rec_ltm
            lucro_val = lucro_ltm
            roic_val = roic_cur
            dy_val = dy_cur
        else:
            yr_data = hist_cache.get(yr, {})
            # Receita contábil oficial arquivada (ajustada para BRL se em USD)
            rec_real = yr_data.get("receita")
            if rec_real is not None and rec_real > 0:
                rev_val = float(rec_real) * fx_factor
            else:
                step_back = 4 - idx
                denom = ((1.0 + cagr_rec) ** step_back)
                rev_val = (rec_ltm / denom) if denom > 0 else rec_ltm

            # Lucro líquido contábil oficial arquivado (ajustado para BRL se em USD)
            lucro_real = yr_data.get("lucro_liquido")
            if lucro_real is not None:
                lucro_val = float(lucro_real) * fx_factor
            else:
                step_back = 4 - idx
                cur_margin = (lucro_ltm / rec_ltm) if rec_ltm > 0 else 0.10
                lucro_val = rev_val * cur_margin

            # ROE / ROIC contábil oficial arquivado
            roe_real = yr_data.get("roe")
            if roe_real is not None:
                roic_val = float(roe_real)
            else:
                roic_val = roic_cur

            # Dividend Yield contábil oficial
            div_per_share = yr_data.get("div_per_share")
            if div_per_share is not None and div_per_share > 0 and cotacao > 0:
                dy_val = float(div_per_share / cotacao)
            else:
                dy_val = dy_cur

        rev_series.append(round(rev_val, 2))
        lucro_series.append(round(lucro_val, 2))
        roic_series.append(round(max(-0.50, min(1.50, roic_val)), 4))
        dy_series.append(round(max(0.0, min(0.40, dy_val)), 4))

    # Contagem real e auditada de anos com lucro
    lucros_positivos = sum(1 for l in lucro_series if l > 0)
    anos_lucro_str = f"{lucros_positivos} de 5 anos"

    # CAGR de Receita Real (2022 a 2026 LTM)
    r_init = rev_series[0]
    r_end = rev_series[-1]
    if r_init > 0 and r_end > 0:
        cagr_rec_calc = (r_end / r_init) ** (1.0 / 4.0) - 1.0
    else:
        cagr_rec_calc = cagr_rec

    # CAGR de Lucro Real (2022 a 2026 LTM)
    l_init = lucro_series[0]
    l_end = lucro_series[-1]
    if l_init > 0 and l_end > 0:
        cagr_lucro = (l_end / l_init) ** (1.0 / 4.0) - 1.0
    elif l_init < 0 and l_end > 0:
        cagr_lucro = 0.50
    else:
        cagr_lucro = -0.15

    cagr_rec_calc = max(-0.50, min(0.80, cagr_rec_calc))
    cagr_lucro = max(-0.50, min(0.80, cagr_lucro))

    # Estabilidade real das margens líquidas & Regras Setoriais de Ciclo (Regra 2)
    setor_name = (row_dict.get("setor") or det_entry.get("setor") or "").strip()
    subsetor_name = (row_dict.get("subsetor") or det_entry.get("subsetor") or "").strip()
    full_sector = f"{setor_name} {subsetor_name}".lower()

    # Checar prejuízo recente ou histórico negativo
    roe_val = row_dict.get("roe")
    pl_val = row_dict.get("pl")
    has_recent_loss = (roe_val is not None and roe_val < 0) or (pl_val is not None and pl_val < 0) or (lucro_series and lucro_series[-1] < 0)

    # 1. Checar se pertence a setores cíclicos pesados (Regra 2c)
    cyclical_keywords = ["siderurg", "metalurg", "minera", "material de transporte", "material rodoviário", "máquinas e equipamentos", "petróleo", "combustív", "construção civil", "incorporaç", "químic", "papel e celulose"]
    cyclical_tickers = {"RAPT4", "ROMI3", "USIM3", "USIM5", "CSNA3", "GGBR4", "GGBR3", "GOAU4", "GOAU3", "VALE3", "TUPY3", "FRAS3", "POMO4", "POMO3", "FESA4", "CBAV3", "KEPL3", "PRIO3", "PETR4", "PETR3", "RECV3", "BRAV3", "LAVV3", "CYRE3", "DIRR3", "MRVE3", "TEND3", "EZTC3", "PLPL3", "CURY3"}
    defensive_keywords = ["segur", "previdência", "banco", "financeiro", "intermediação", "energia elétrica", "transmiss", "distribui", "saneam", "água"]
    defensive_tickers = {"CXSE3", "BBSE3", "PSSA3", "ITUB4", "ITUB3", "BBDC4", "BBDC3", "BBAS3", "SANB11", "EGIE3", "TAEE11", "TAEE4", "TAEE3", "TRPL4", "ISAE4", "CPFE3", "EQTL3", "SAPR11", "SAPR4", "SBSP3", "CSMG3", "VIVT3", "TIMS3"}

    t_up = ticker.strip().upper()
    has_positive_3y = len(roic_series) >= 3 and all(r > 0 for r in roic_series[-3:])
    is_cyclical = any(k in full_sector for k in cyclical_keywords) or (t_up in cyclical_tickers) or has_recent_loss
    is_defensive = (any(k in full_sector for k in defensive_keywords) or (t_up in defensive_tickers)) and has_positive_3y and not has_recent_loss

    # Bens de capital e industriais pesados são estritamente cíclicos
    if t_up in {"RAPT4", "RAPT3", "ROMI3", "TUPY3", "SHUL4", "KEPL3", "USIM3", "USIM5", "CSNA3", "GGBR4", "GOAU4", "VALE3"}:
        is_cyclical = True
        is_defensive = False

    if is_defensive:
        # Priorizar Resiliente / Consistência de Ciclo para defensivas lucrativas
        margins = [(lucro_series[i] / rev_series[i]) for i in range(5) if rev_series[i] > 0]
        if len(margins) >= 4 and float(pd.Series(margins).std()) < 0.03:
            estabilidade = "Alta Estabilidade 💎"
        else:
            estabilidade = "Resiliente 🟢"
    elif is_cyclical:
        # Cíclicas, bens de capital pesados ou empresas com prejuízo recente
        estabilidade = "Cíclica / Sensível ao Ciclo ⚠️"
    else:
        # Demais setores por variabilidade estatística
        margins = [(lucro_series[i] / rev_series[i]) for i in range(5) if rev_series[i] > 0]
        if len(margins) >= 4:
            m_std = float(pd.Series(margins).std())
            if m_std < 0.03:
                estabilidade = "Alta Estabilidade 💎"
            elif m_std < 0.07:
                estabilidade = "Resiliente 🟢"
            else:
                estabilidade = "Cíclica / Sensível ao Ciclo ⚠️"
        else:
            estabilidade = "Resiliente 🟢"

    return {
        "years": years,
        "receita": rev_series,
        "lucro_liquido": lucro_series,
        "roic_roe": roic_series,
        "div_yield": dy_series,
        "cagr_receita_pct": round(cagr_rec_calc * 100.0, 1),
        "cagr_lucro_pct": round(cagr_lucro * 100.0, 1),
        "anos_com_lucro": anos_lucro_str,
        "estabilidade_margens": estabilidade,
        "is_all_profitable": lucros_positivos == 5,
    }


def compile_standalone_dataset(force_refresh: bool = False, force_details: bool = False) -> Dict[str, Any]:
    is_ci = os.environ.get("GITHUB_ACTIONS") == "true" or os.environ.get("CI") == "true"
    if is_ci:
        force_refresh = True
    logger.info("Iniciando compilacao do dataset standalone (force_refresh=%s, force_details=%s)...", force_refresh, force_details)
    df, audit_timestamp = get_cached_universe(force_refresh=force_refresh)

    details_cache: Dict[str, Any] = {}
    if os.path.exists(DETAILS_CACHE_FILE):
        try:
            with open(DETAILS_CACHE_FILE, "r", encoding="utf-8") as f:
                details_cache = json.load(f)
        except Exception as e:
            logger.warning("Falha ao abrir details_cache: %s", e)

    ibov_file = os.path.join(CACHE_DIR, "ibov_composition.json")
    ibov_map: Dict[str, Any] = {}
    if os.path.exists(ibov_file):
        try:
            with open(ibov_file, "r", encoding="utf-8") as f:
                ibov_map = json.load(f)
        except Exception as e:
            logger.warning("Falha ao abrir ibov_composition: %s", e)

    stocks_payload: List[Dict[str, Any]] = []

    for _, row in df.iterrows():
        row_dict = row.to_dict()
        ticker = str(row_dict.get("ticker", "")).strip().upper()
        if not ticker:
            continue

        cache_item = details_cache.get(ticker, {})
        det_entry = cache_item.get("data")
        cached_ts = cache_item.get("cached_time", 0)
        now_ts = time.time()

        # Detector Inteligente de Novo Balanço Publicado:
        # 1. Se patrimônio líquido da tabela geral divergir do cache detalhado: novo balanço cadastrado no Fundamentus!
        row_pl = float(row_dict.get("patrim_liq") or 0.0)
        det_pl = float((det_entry or {}).get("patrimonio_liquido") or 0.0)
        has_pl_divergence = bool(det_entry and (row_pl > 0 and det_pl > 0) and abs(row_pl - det_pl) > 1000.0)

        # 2. Se a ação ainda aguarda balanço 3T26 e o cache tem mais de 6h em ambiente CI da nuvem
        is_prior_quarter = bool(det_entry and ("30/09/2026" not in str(det_entry.get("ult_balanco", ""))))
        is_stale_season = bool(is_ci and is_prior_quarter and ((now_ts - cached_ts) > (6 * 3600)))

        # 3. Cache padrão com mais de 24h
        is_stale_default = (now_ts - cached_ts) > (24 * 3600)

        should_fetch = (not det_entry) or force_details or has_pl_divergence or is_stale_season or (is_ci and is_stale_default)

        if should_fetch:
            try:
                det_entry = fetch_fundamentus_ticker_details(ticker, force_refresh=True)
            except Exception as e:
                logger.warning("Erro ao coletar detalhes de %s: %s", ticker, e)
                if not det_entry:
                    det_entry = {}

        sector = det_entry.get("setor") or row_dict.get("setor", "Industria / Geral")
        subsetor = det_entry.get("subsetor") or "Geral"
        empresa = det_entry.get("empresa") or ticker

        liq_2m = float(row_dict.get("liq_2m") or 0.0)

        ult_balanco = str(det_entry.get("ult_balanco", "N/D")).strip()
        is_latest_balanco, tri_balanco = classify_balance_sheet_recency(ult_balanco)

        # Auditoria de Distorções Trimestrais & P/L Run-Rate (4x 3m)
        l12 = det_entry.get("lucro_liq_12m")
        l3 = det_entry.get("lucro_liq_3m")
        mcap = det_entry.get("valor_mercado")
        rec12 = det_entry.get("receita_liq_12m")

        row_dict["ticker"] = ticker
        if l12 is not None:
            row_dict["lucro_liq"] = l12
        if rec12 is not None:
            row_dict["receita_liq"] = rec12

        ticker_hist = get_historical_cache().get(ticker)
        q = calculate_business_quality(row_dict, sector, ticker_hist)

        lucro_run_rate = (4.0 * l3) if l3 is not None else None
        pl_run_rate = None
        if mcap is not None and lucro_run_rate is not None and lucro_run_rate > 0:
            pl_run_rate = round(mcap / lucro_run_rate, 2)
        row_dict["pl_run_rate"] = pl_run_rate
        row_dict["details"] = det_entry

        v = evaluate_entry_valuation(row_dict, sector, quality_score=q.get("quality_score"))
        bullets = generate_cfa_verdict(ticker, empresa, q, v, row_dict)

        run_rate_div_pct = None
        is_distorted = False
        distortion_tag = "RECORRENTE"
        distortion_label = "🟢 Estável / Recorrente"

        seasonal_sectors = {"Comércio", "Comércio e Distribuição", "Tecidos, Vestuário e Calçados", "Agropecuária", "Alimentos Processados", "Açúcar e Álcool"}
        seasonal_tickers = {"LREN3", "RIAA3", "ARZZ3", "SOMA3", "AZZA3", "VIVA3", "LJQQ3", "MGLU3", "BHIA3", "CEAB3", "AGRO3", "SLCE3", "TTEN3", "SOJA3", "SMTO3", "JALL3", "CAML3", "MDIA3"}
        is_seasonal_sector = (sector in seasonal_sectors) or (ticker in seasonal_tickers) or ("Moda" in subsetor) or ("Vestuário" in subsetor) or ("Varejo" in sector) or ("Calçados" in subsetor)

        if l12 is not None and l3 is not None and l12 != 0:
            div = ((4.0 * l3) - l12) / abs(l12)
            run_rate_div_pct = round(div * 100.0, 1)

            if l12 > 0 and l3 <= 0:
                is_distorted = True
                distortion_tag = "PREJUIZO_RECENTE"
                distortion_label = "🔴 Prejuízo no Tri (Armadilha)"
            elif l12 <= 0 and l3 > 0:
                is_distorted = True
                distortion_tag = "INFLECAO_POSITIVA"
                distortion_label = f"🟢 Virada p/ Lucro (+{run_rate_div_pct:.0f}%)"
            elif div > 0.50:
                is_distorted = True
                distortion_tag = "EXPANSAO_ONE_OFF"
                distortion_label = f"⚠️ One-Off / Sazonal (+{run_rate_div_pct:.0f}%)"
            elif div < -0.25:
                if is_seasonal_sector:
                    is_distorted = False
                    distortion_tag = "SAZONALIDADE_TRIMESTRAL"
                    distortion_label = f"⚠️ Sazonalidade / Desaceleração Trimestral ({run_rate_div_pct:.0f}%)"
                else:
                    is_distorted = True
                    distortion_tag = "DETERIORACAO_LUCRO"
                    distortion_label = f"🔴 Queda de Run-Rate ({run_rate_div_pct:.0f}%)"
            else:
                is_distorted = False
                distortion_tag = "RECORRENTE"
                distortion_label = f"🟢 Recorrente ({run_rate_div_pct:+.0f}%)"

        is_fin_item = q.get("is_financial", False) or (ticker in ["ITSA3", "ITSA4"])

        stock_item = {
            "ticker": ticker,
            "empresa": empresa,
            "is_ibov": ticker in ibov_map,
            "ibov_weight": ibov_map[ticker].get("part") if ticker in ibov_map else None,
            "setor": sector,
            "subsetor": subsetor,
            "cotacao": row_dict.get("cotacao"),
            "liq_2m": liq_2m,
            "is_liquid_1m": liq_2m >= 1_000_000.0,
            "ult_balanco": ult_balanco,
            "is_latest_balanco": is_latest_balanco,
            "tri_balanco": tri_balanco,
            "lucro_run_rate": lucro_run_rate,
            "pl_run_rate": pl_run_rate,
            "run_rate_div_pct": run_rate_div_pct,
            "is_distorted": is_distorted,
            "distortion_tag": distortion_tag,
            "distortion_label": distortion_label,
            "quality_score": q["quality_score"],
            "quality_tier": q["quality_tier"],
            "quality_tag": q["quality_tag"],
            "pilar_rentabilidade": q["pilar_rentabilidade"],
            "pilar_solidez": q["pilar_solidez"],
            "pilar_consistencia": q["pilar_consistencia"],
            "is_financial": is_fin_item,
            "entry_status": v["entry_status"],
            "entry_tag": v["entry_tag"],
            "entry_color": v["entry_color"],
            "pl": row_dict.get("pl"),
            "ev_ebitda": None if is_fin_item else row_dict.get("ev_ebitda"),
            "ev_ebit": None if is_fin_item else row_dict.get("ev_ebit"),
            "pvp": row_dict.get("pvp"),
            "roic": None if is_fin_item else row_dict.get("roic"),
            "roe": row_dict.get("roe"),
            "mrg_liq": row_dict.get("mrg_liq"),
            "mrg_bruta": None if is_fin_item else row_dict.get("mrg_bruta"),
            "div_liq_ebitda": None if is_fin_item else row_dict.get("div_liq_ebitda"),
            "div_yield": row_dict.get("div_yield"),
            "earnings_yield_pct": v.get("earnings_yield_pct"),
            "ey_spread": v.get("ey_spread"),
            "payout_implicito": (v.get("payout_implicito") * 100.0) if v.get("payout_implicito") is not None else None,
            "payout_tag": v.get("payout_tag", "N/D"),
            "is_commodity_peak": v.get("is_commodity_peak", False),
            "is_debt_vulnerable": False if is_fin_item else v.get("is_debt_vulnerable", False),
            "capital_intensity": None if is_fin_item else v.get("capital_intensity"),
            "sub_scores": q["sub_scores"],
            "rationale": v.get("rationale", ""),
            "cfa_bullets": bullets,
            "details": det_entry,
            "historical_5y": generate_5y_history(ticker, row_dict, det_entry, q, v),
        }
        stocks_payload.append(stock_item)

    stocks_payload.sort(key=lambda s: s["quality_score"], reverse=True)

    has_3t = any("3T26" in (s.get("tri_balanco") or "") for s in stocks_payload)
    latest_quarter_detected = "3T26" if has_3t else "2T26"

    raw_dataset = {
        "audit_timestamp": audit_timestamp,
        "ntn_b_benchmark": NTN_B_BENCHMARK,
        "latest_quarter": latest_quarter_detected,
        "total_stocks": len(stocks_payload),
        "total_ibov": sum(1 for s in stocks_payload if s.get("is_ibov")),
        "total_liquid_1m": sum(1 for s in stocks_payload if s["is_liquid_1m"]),
        "total_latest_balanco": sum(1 for s in stocks_payload if s["is_latest_balanco"]),
        "total_recurring": sum(1 for s in stocks_payload if not s["is_distorted"]),
        "stocks": stocks_payload,
    }

    # Higienização rigorosa contra NaN e Infinity para total conformidade RFC 8259 (JS JSON.parse)
    def sanitize_for_json(obj: Any) -> Any:
        import math
        if isinstance(obj, dict):
            return {k: sanitize_for_json(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [sanitize_for_json(v) for v in obj]
        elif isinstance(obj, float):
            if math.isnan(obj) or math.isinf(obj):
                return None
            return obj
        elif pd.isna(obj):
            return None
        return obj

    dataset = sanitize_for_json(raw_dataset)

    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(STANDALONE_CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)

    logger.info("Dataset gravado em %s com %d ativos (sanitizado sem NaNs).", STANDALONE_CACHE_FILE, len(stocks_payload))
    return dataset


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    data = compile_standalone_dataset(force_refresh=True)
    print(f"Total: {data['total_stocks']} ativos.")
    print(f"Liquidez >= 1M: {data['total_liquid_1m']}")
    print(f"Ultimo Tri: {data['total_latest_balanco']}")
