"""
data_pipeline.py
================
Pipeline institucional de extração, auditoria, tipagem e cache de dados de ações da B3
alimentado exclusivamente pelo Fundamentus (https://www.fundamentus.com.br/).
"""

from __future__ import annotations
import os
import io
import time
import json
import logging
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional, Tuple, List
import requests
import pandas as pd
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache")
CACHE_FILE = os.path.join(CACHE_DIR, "fundamentus_universe.json")
DETAILS_CACHE_FILE = os.path.join(CACHE_DIR, "fundamentus_details.json")
CACHE_TTL_SECONDS = 15 * 60  # 15 minutos de TTL

HTTP_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer": "https://www.fundamentus.com.br/",
    "Connection": "keep-alive",
}

# Fuso Horário de Brasília (UTC-3)
TZ_BRT = timezone(timedelta(hours=-3))


def get_current_timestamp_brt() -> str:
    """Retorna timestamp no fuso de Brasília formatado: DD/MM/AAAA HH:MM:SS."""
    return datetime.now(TZ_BRT).strftime("%d/%m/%Y %H:%M:%S")


def ensure_cache_dir() -> None:
    """Garante a existência do diretório de cache."""
    os.makedirs(CACHE_DIR, exist_ok=True)


def parse_brazilian_number(value: Any) -> Optional[float]:
    """
    Converte strings numéricas no padrão brasileiro para float.
    Exemplos: '1.234,56' -> 1234.56, '15,2%' -> 0.152, '-' ou 'N/D' -> None.
    """
    if value is None or pd.isna(value):
        return None

    val_str = str(value).strip()
    if val_str in ("", "-", "--", "N/D", "n/d", "None", "nan"):
        return None

    is_percentage = False
    if val_str.endswith("%"):
        is_percentage = True
        val_str = val_str[:-1].strip()

    # Se contiver vírgula, remove pontos de milhar e substitui vírgula por ponto
    if "," in val_str:
        val_str = val_str.replace(".", "").replace(",", ".")
    
    try:
        num = float(val_str)
        if is_percentage:
            num = num / 100.0
        return num
    except (ValueError, TypeError):
        return None


def fetch_fundamentus_raw_universe() -> Tuple[pd.DataFrame, str]:
    """
    Coleta a tabela completa de resultados do Fundamentus (resultado.php).
    Retorna o DataFrame bruto e o timestamp da coleta.
    """
    url = "https://www.fundamentus.com.br/resultado.php"
    logger.info("Requisitando dados completos do Fundamentus: %s", url)

    response = requests.get(url, headers=HTTP_HEADERS, timeout=15)
    response.raise_for_status()
    response.encoding = "latin1"

    audit_timestamp = get_current_timestamp_brt()
    
    dfs = pd.read_html(io.StringIO(response.text), decimal=",", thousands=".")
    if not dfs:
        raise ValueError("Nenhuma tabela encontrada na resposta do Fundamentus.")

    df = dfs[0]
    return df, audit_timestamp


def compute_derived_metrics(row: pd.Series) -> Dict[str, Any]:
    """
    Calcula métricas financeiras derivadas e integridade:
    - Dívida Líquida / EBITDA
    - Earnings Yield (1 / P/L)
    - Flags de Auditoria / Sanidade Institucional
    """
    pl = row.get("pl")
    ev_ebitda = row.get("ev_ebitda")
    div_liq_patrim = row.get("div_liq_patrim")
    patrim_liq = row.get("patrim_liq")
    pvp = row.get("pvp")

    # 1. Earnings Yield = 1 / (P/L)
    earnings_yield = (1.0 / pl) if (pl is not None and pl > 0) else None

    # 2. Dívida Líquida / EBITDA e Detecção de Caixa Líquido
    div_liq_ebitda: Optional[float] = None
    is_net_cash = False

    # Caixa líquido REAL ocorre apenas se Dív. Líq for negativa
    # Se Patrimônio Líquido for negativo, a razão Dív.Líq/Patrim é negativa por causa do denominador,
    # significando dívida massiva (passivo a descoberto), e NÃO caixa líquido!
    if patrim_liq is not None and patrim_liq > 0:
        if div_liq_patrim is not None and div_liq_patrim < 0:
            is_net_cash = True
    elif patrim_liq is not None and patrim_liq < 0:
        is_net_cash = False  # Passivo a descoberto: empresa está endividada além de seus ativos

    # Cálculo da Dívida Líquida e EBITDA
    if patrim_liq is not None and div_liq_patrim is not None:
        div_liq_real = div_liq_patrim * patrim_liq
        if pvp is not None and ev_ebitda is not None and ev_ebitda > 0:
            mcap = abs(pvp * patrim_liq) if pvp != 0 else 0
            ev = mcap + div_liq_real
            if ev > 0:
                ebitda = ev / ev_ebitda
                if ebitda > 0:
                    div_liq_ebitda = div_liq_real / ebitda

    # Se a empresa estiver em passivo a descoberto e div_liq_ebitda não puder ser calculado
    if patrim_liq is not None and patrim_liq < 0:
        if div_liq_ebitda is None or div_liq_ebitda < 0:
            div_liq_ebitda = 6.0  # Alavancagem crítica / risco extremo

    # Se a empresa estiver comprovadamente em caixa líquido
    if is_net_cash and (div_liq_ebitda is None or div_liq_ebitda >= 0):
        div_liq_ebitda = -0.5

    # 3. Sanity & Audit Flags
    alert_flags: List[str] = []
    if patrim_liq is not None and patrim_liq < 0:
        alert_flags.append("PATRIMONIO_LIQUIDO_NEGATIVO")
    if pl is not None and pl < 0:
        alert_flags.append("LUCRO_LIQUIDO_NEGATIVO")
    if ev_ebitda is not None and ev_ebitda < 0:
        alert_flags.append("EBITDA_NEGATIVO")

    return {
        "earnings_yield": earnings_yield,
        "div_liq_ebitda": div_liq_ebitda,
        "is_net_cash": is_net_cash,
        "alert_flags": alert_flags,
    }


def normalize_fundamentus_dataframe(raw_df: pd.DataFrame, audit_timestamp: str) -> pd.DataFrame:
    """
    Renomeia e tipifica rigorosamente as colunas brutas do Fundamentus para o formato padrão do terminal.
    Aplica o filtro de sanidade institucional: Liquidez Média Diária (2m) >= R$ 1.000.000.
    """
    # Ordem fixa oficial das 22 colunas retornadas pelo Fundamentus resultado.php:
    fixed_columns = [
        "ticker",            # 0: Papel
        "cotacao",           # 1: Cotação
        "pl",                # 2: P/L
        "pvp",               # 3: P/VP
        "psr",               # 4: PSR
        "div_yield",         # 5: Div.Yield
        "p_ativo",           # 6: P/Ativo
        "p_cap_giro",        # 7: P/Cap.Giro
        "p_ebit",            # 8: P/EBIT
        "p_ativ_circ_liq",   # 9: P/Ativ Circ.Liq
        "ev_ebit",           # 10: EV/EBIT
        "ev_ebitda",         # 11: EV/EBITDA
        "mrg_bruta",         # 12: Mrg Bruta
        "mrg_ebit",          # 13: Mrg Ebit
        "mrg_liq",           # 14: Mrg. Líq.
        "liq_corr",          # 15: Liq. Corr.
        "roic",              # 16: ROIC
        "roe",               # 17: ROE
        "liq_2m",            # 18: Liq.2meses
        "patrim_liq",        # 19: Patrim. Líq
        "div_liq_patrim",    # 20: Dív.Líq/ Patrim.
        "cresc_rec5a",       # 21: Cresc. Rec.5a
    ]

    clean_data: List[Dict[str, Any]] = []

    # Carrega mapeamento de setores se existir
    sector_map = {}
    sec_file = os.path.join(CACHE_DIR, "sector_mapping.json")
    if os.path.exists(sec_file):
        try:
            with open(sec_file, "r", encoding="utf-8") as f:
                sector_map = json.load(f)
        except Exception:
            sector_map = {}

    for _, row in raw_df.iterrows():
        item: Dict[str, Any] = {}
        for idx, val in enumerate(row):
            if idx < len(fixed_columns):
                col_name = fixed_columns[idx]
                if col_name == "ticker":
                    item[col_name] = str(val).strip().upper()
                else:
                    item[col_name] = parse_brazilian_number(val)

        ticker = item.get("ticker", "")
        if not ticker:
            continue

        liq_2m = item.get("liq_2m") or 0.0

        # FILTRO DE SANIDADE INSTITUCIONAL: Liquidez 2 meses >= R$ 1.000.000
        if liq_2m < 1_000_000.0:
            continue

        derived = compute_derived_metrics(pd.Series(item))
        item.update(derived)
        item["setor"] = sector_map.get(ticker, "Indústria / Geral")
        item["audit_timestamp"] = audit_timestamp
        item["audit_source"] = "Fundamentus (resultado.php)"

        clean_data.append(item)

    df_clean = pd.DataFrame(clean_data)
    logger.info("Total de ativos qualificados após filtro institucional de liquidez: %d", len(df_clean))
    return df_clean


def get_cached_universe(force_refresh: bool = False) -> Tuple[pd.DataFrame, str]:
    """
    Retorna o universo auditado do Fundamentus respeitando o TTL de 15 minutos do cache.
    """
    ensure_cache_dir()

    # Detecta se está em CI (GitHub Actions) ou se foi forçado explicitamente
    is_ci = os.environ.get("GITHUB_ACTIONS") == "true" or os.environ.get("CI") == "true"
    if is_ci:
        force_refresh = True

    if not force_refresh and os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Usa created_at do payload para validar TTL de 15 minutos em vez de mtime do arquivo (que reseta no checkout git)
            created_at_str = data.get("created_at")
            age = None
            if created_at_str:
                try:
                    dt_created = datetime.fromisoformat(created_at_str)
                    age = (datetime.now(timezone.utc) - dt_created).total_seconds()
                except Exception:
                    age = None
            if age is None:
                mtime = os.path.getmtime(CACHE_FILE)
                age = time.time() - mtime

            if age < CACHE_TTL_SECONDS:
                records = data.get("records", [])
                audit_timestamp = data.get("audit_timestamp", get_current_timestamp_brt())
                logger.info("Retornando dados do cache com TTL ativo (idade: %.1f min).", age / 60.0)
                df = pd.DataFrame(records)
                return df, audit_timestamp
        except Exception as e:
            logger.warning("Falha ao ler cache local (%s), realizando nova coleta.", e)

    # Coleta nova
    raw_df, audit_timestamp = fetch_fundamentus_raw_universe()
    clean_df = normalize_fundamentus_dataframe(raw_df, audit_timestamp)

    try:
        cache_payload = {
            "audit_timestamp": audit_timestamp,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "records": clean_df.to_dict(orient="records"),
        }
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache_payload, f, ensure_ascii=False, indent=2)
        logger.info("Cache local gravado em %s.", CACHE_FILE)
    except Exception as e:
        logger.error("Erro ao gravar cache: %s", e)

    return clean_df, audit_timestamp


def fetch_fundamentus_ticker_details(ticker: str, force_refresh: bool = False) -> Dict[str, Any]:
    """
    Coleta a página detalhada da empresa (detalhes.php?papel={TICKER}).
    Extrai informações corporativas como Setor, Sub-setor, Balanço Patrimonial e DRE.
    Cache por ticker com TTL de 15 minutos.
    """
    ticker = ticker.strip().upper()
    ensure_cache_dir()

    details_cache: Dict[str, Any] = {}
    if os.path.exists(DETAILS_CACHE_FILE):
        try:
            with open(DETAILS_CACHE_FILE, "r", encoding="utf-8") as f:
                details_cache = json.load(f)
        except Exception:
            details_cache = {}

    cached_entry = details_cache.get(ticker)
    if cached_entry and not force_refresh:
        ts = cached_entry.get("cached_time", 0)
        if (time.time() - ts) < CACHE_TTL_SECONDS:
            return cached_entry["data"]

    url = f"https://www.fundamentus.com.br/detalhes.php?papel={ticker}"
    logger.info("Requisitando detalhes aprofundados para %s: %s", ticker, url)

    response = requests.get(url, headers=HTTP_HEADERS, timeout=15)
    response.raise_for_status()
    response.encoding = "latin1"

    audit_timestamp = get_current_timestamp_brt()
    dfs = pd.read_html(io.StringIO(response.text), decimal=",", thousands=".")

    extracted: Dict[str, Any] = {
        "ticker": ticker,
        "audit_timestamp": audit_timestamp,
        "audit_source": f"Fundamentus (detalhes.php?papel={ticker})",
        "empresa": "N/D",
        "setor": "N/D",
        "subsetor": "N/D",
        "tipo": "N/D",
        "data_ult_cot": "N/D",
        "min_52sem": None,
        "max_52sem": None,
        "valor_mercado": None,
        "valor_firma": None,
        "nro_acoes": None,
        "ult_balanco": "N/D",
        "ativo_total": None,
        "disponibilidades": None,
        "ativo_circulante": None,
        "divida_bruta": None,
        "divida_liquida": None,
        "patrimonio_liquido": None,
        "receita_liq_12m": None,
        "ebit_12m": None,
        "lucro_liq_12m": None,
        "receita_liq_3m": None,
        "ebit_3m": None,
        "lucro_liq_3m": None,
        "lpa": None,
        "vpa": None,
        "raw_indicators": {},
    }

    try:
        # Tabela 0: Informações básicas (Papel, Tipo, Empresa, Setor, Subsetor, Cotação, 52w)
        if len(dfs) > 0:
            t0 = dfs[0]
            for _, r in t0.iterrows():
                k0, v0 = str(r[0]).strip().replace("?", ""), str(r[1]).strip()
                k1, v1 = str(r[2]).strip().replace("?", ""), str(r[3]).strip()
                if "empresa" in k0.lower():
                    extracted["empresa"] = v0
                elif "subsetor" in k0.lower():
                    extracted["subsetor"] = v0
                elif "setor" in k0.lower():
                    extracted["setor"] = v0
                elif "tipo" in k0.lower():
                    extracted["tipo"] = v0
                if "data" in k1.lower():
                    extracted["data_ult_cot"] = v1
                if "min" in k1.lower():
                    extracted["min_52sem"] = parse_brazilian_number(v1)
                if "max" in k1.lower():
                    extracted["max_52sem"] = parse_brazilian_number(v1)

        # Tabela 1: Valor de Mercado, Valor da Firma, Balanço processado
        if len(dfs) > 1:
            t1 = dfs[1]
            for _, r in t1.iterrows():
                k0, v0 = str(r[0]).strip().replace("?", ""), r[1]
                k1, v1 = str(r[2]).strip().replace("?", ""), r[3]
                if "mercado" in k0.lower():
                    extracted["valor_mercado"] = parse_brazilian_number(v0)
                if "firma" in k0.lower():
                    extracted["valor_firma"] = parse_brazilian_number(v0)
                if "balan" in k1.lower():
                    extracted["ult_balanco"] = str(v1).strip()
                if "nro" in k1.lower():
                    extracted["nro_acoes"] = parse_brazilian_number(v1)

        # Tabela 2: Indicadores fundamentalistas detalhados
        if len(dfs) > 2:
            t2 = dfs[2]
            for _, r in t2.iterrows():
                if len(r) >= 6:
                    k_ind1, v_ind1 = str(r[2]).strip().replace("?", ""), r[3]
                    k_ind2, v_ind2 = str(r[4]).strip().replace("?", ""), r[5]
                    extracted["raw_indicators"][k_ind1] = v_ind1
                    extracted["raw_indicators"][k_ind2] = v_ind2
                    if "lpa" in k_ind2.lower():
                        extracted["lpa"] = parse_brazilian_number(v_ind2)
                    if "vpa" in k_ind2.lower():
                        extracted["vpa"] = parse_brazilian_number(v_ind2)

        # Tabela 3: Balanço Patrimonial
        if len(dfs) > 3:
            t3 = dfs[3]
            for _, r in t3.iterrows():
                k0, v0 = str(r[0]).strip().replace("?", ""), r[1]
                k1, v1 = str(r[2]).strip().replace("?", ""), r[3]
                if "ativo" in k0.lower() and "circulante" not in k0.lower():
                    extracted["ativo_total"] = parse_brazilian_number(v0)
                if "disponibilidades" in k0.lower():
                    extracted["disponibilidades"] = parse_brazilian_number(v0)
                if "ativo circulante" in k0.lower():
                    extracted["ativo_circulante"] = parse_brazilian_number(v0)
                if "bruta" in k1.lower():
                    extracted["divida_bruta"] = parse_brazilian_number(v1)
                if "líquida" in k1.lower() or "lquida" in k1.lower():
                    extracted["divida_liquida"] = parse_brazilian_number(v1)
                if "patrim" in k1.lower():
                    extracted["patrimonio_liquido"] = parse_brazilian_number(v1)

        # Tabela 4: Demonstrativos de Resultados (DRE)
        if len(dfs) > 4:
            t4 = dfs[4]
            for _, r in t4.iterrows():
                k = str(r[0]).strip().replace("?", "")
                v_12m, v_3m = r[1], r[3]
                if "receita" in k.lower():
                    extracted["receita_liq_12m"] = parse_brazilian_number(v_12m)
                    extracted["receita_liq_3m"] = parse_brazilian_number(v_3m)
                if "ebit" in k.lower():
                    extracted["ebit_12m"] = parse_brazilian_number(v_12m)
                    extracted["ebit_3m"] = parse_brazilian_number(v_3m)
                if "lucro" in k.lower():
                    extracted["lucro_liq_12m"] = parse_brazilian_number(v_12m)
                    extracted["lucro_liq_3m"] = parse_brazilian_number(v_3m)

    except Exception as e:
        logger.error("Erro no parsing de detalhes para %s: %s", ticker, e)

    details_cache[ticker] = {
        "cached_time": time.time(),
        "data": extracted,
    }
    try:
        with open(DETAILS_CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(details_cache, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.warning("Falha ao salvar cache de detalhes: %s", e)

    return extracted
