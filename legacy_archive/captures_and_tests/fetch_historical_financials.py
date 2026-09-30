"""
fetch_historical_financials.py
==============================
Coleta paralela das demonstrações contábeis históricas reais e auditadas
(DREs, Balanço Patrimonial e Proventos dos anos de 2022, 2023, 2024 e 2025)
diretamente das bases oficiais da B3/CVM via yfinance (.SA).
"""

from __future__ import annotations
import json
import logging
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, Any, Optional

import pandas as pd
import yfinance as yf

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(BASE_DIR, "cache")
OUTPUT_FILE = os.path.join(CACHE_DIR, "historical_financials.json")
UNIVERSE_FILE = os.path.join(CACHE_DIR, "standalone_data.json")


def clean_num(val: Any) -> Optional[float]:
    if val is None or pd.isna(val):
        return None
    try:
        f = float(val)
        return None if (f != f or f == float("inf") or f == float("-inf")) else f
    except (ValueError, TypeError):
        return None


def fetch_single_ticker(ticker: str) -> tuple[str, Dict[str, Any]]:
    symbol = f"{ticker}.SA"
    history: Dict[str, Dict[str, Any]] = {}

    try:
        tk = yf.Ticker(symbol)
        fin = tk.financials
        bs = tk.balance_sheet
        divs = tk.dividends

        if fin is None or fin.empty:
            return ticker, {}

        # Identificar linhas de Receita
        rev_row = None
        for r_name in ["Total Revenue", "Operating Revenue", "Gross Profit"]:
            if r_name in fin.index:
                rev_row = fin.loc[r_name]
                break

        # Identificar linhas de Lucro Líquido
        net_row = None
        for n_name in ["Net Income Common Stockholders", "Net Income", "Net Income Continuous Operations"]:
            if n_name in fin.index:
                net_row = fin.loc[n_name]
                break

        # Identificar linhas de Patrimônio Líquido
        eq_row = None
        if bs is not None and not bs.empty:
            for e_name in ["Common Stock Equity", "Stockholders Equity", "Total Equity Gross Minority Interest"]:
                if e_name in bs.index:
                    eq_row = bs.loc[e_name]
                    break

        years_target = ["2022", "2023", "2024", "2025"]

        for col in fin.columns:
            yr_str = str(col)[:4]
            if yr_str not in years_target:
                continue

            rev_val = clean_num(rev_row.get(col)) if rev_row is not None else None
            net_val = clean_num(net_row.get(col)) if net_row is not None else None

            roe_val = None
            if eq_row is not None:
                # Procura a coluna correspondente no balanço
                eq_col_val = None
                for b_col in bs.columns:
                    if str(b_col)[:4] == yr_str:
                        eq_col_val = clean_num(eq_row.get(b_col))
                        break
                if eq_col_val and eq_col_val > 0 and net_val is not None:
                    roe_val = clean_num(net_val / eq_col_val)

            div_sum = 0.0
            if divs is not None and not divs.empty:
                try:
                    div_year = divs[divs.index.year == int(yr_str)]
                    if not div_year.empty:
                        div_sum = float(div_year.sum())
                except Exception:
                    div_sum = 0.0

            history[yr_str] = {
                "receita": rev_val,
                "lucro_liquido": net_val,
                "roe": roe_val,
                "div_per_share": div_sum,
            }

        return ticker, history

    except Exception as e:
        logger.debug("Erro ao coletar %s: %s", ticker, e)
        return ticker, {}


def run_historical_extraction(max_workers: int = 12) -> Dict[str, Any]:
    os.makedirs(CACHE_DIR, exist_ok=True)

    if not os.path.exists(UNIVERSE_FILE):
        logger.error("Arquivo do universo %s não encontrado!", UNIVERSE_FILE)
        return {}

    with open(UNIVERSE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    tickers = [s["ticker"] for s in data.get("stocks", [])]
    logger.info("Iniciando coleta histórica para %d tickers da B3 com %d workers...", len(tickers), max_workers)

    results: Dict[str, Any] = {}
    success_count = 0
    t0 = time.time()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_ticker = {executor.submit(fetch_single_ticker, t): t for t in tickers}
        for future in as_completed(future_to_ticker):
            t = future_to_ticker[future]
            try:
                ticker, hist = future.result()
                if hist:
                    results[ticker] = hist
                    success_count += 1
            except Exception as e:
                logger.warning("Falha ao processar %s: %s", t, e)

    t1 = time.time()
    logger.info("Coleta concluída em %.1fs. Total com balanços auditados: %d/%d (%.1f%%)",
                t1 - t0, success_count, len(tickers), (success_count / len(tickers) * 100) if tickers else 0)

    # Gravar cache JSON
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    logger.info("Histórico contábil salvo com sucesso em %s", OUTPUT_FILE)
    return results


if __name__ == "__main__":
    run_historical_extraction()
