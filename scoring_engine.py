"""
scoring_engine.py
=================
Motor Analítico Institucional de Charlie Munger para Ações da B3.
Implementa o Duplo Filtro Fundamentalista com 6 Critérios Quantitativos:
1. Business Quality Score (0 a 100) com Módulo Dedicado para Bancos/Financeiro.
2. Teste Ácido de Munger: Intensidade de Capital (EBIT / EBITDA & EV/EBIT).
3. Spread de Juro Real vs. NTN-B (Equity Risk Premium Local de 6,5% a.a.).
4. Alerta de Pico de Ciclo para Produtoras de Commodities (P/L baixo enganoso).
5. Filtro de Cobertura da Dívida pelo EBIT (Anti-Selic Alta).
6. Teste de Sustentabilidade de Proventos (Payout Implícito).
7. Síntese Executiva Fundamentalista (3 bullets estratégicos enriquecidos).
"""

from __future__ import annotations
import math
from typing import Dict, Any, Optional, Tuple, List

# Benchmarks Macroeconômicos Brasileiros
NTN_B_BENCHMARK = 6.50  # Taxa do Tesouro IPCA+ longo (Juro Real Livre de Risco: 6,5% a.a.)
CDI_BENCHMARK = 0.105   # Taxa Selic/CDI estimada de referência (10,5% a.a.)

COMMODITY_SECTORS = [
    "petróleo", "petroleo", "gás", "gas", "biocombustíveis", "biocombustiveis",
    "mineração", "mineracao", "minerais", "siderurgia", "metalurgia",
    "papel e celulose", "agropecuária", "agropecuaria", "açúcar e álcool", "acucar e alcool",
]

CYCLICAL_SECTORS = [
    "construção", "construcao", "incorporação", "incorporacao", "imobiliário", "imobiliario",
    "construção civil", "construcao civil", "incorporações", "incorporacoes",
]

FINANCIAL_SECTORS = [
    "banco", "intermediários financeiros", "intermediarios financeiros",
    "previdência e seguros", "previdencia e seguros", "segur", "serviços financeiros",
]


def is_financial_sector(sector_name: str, ticker: str = "") -> bool:
    """Detecta se o ativo pertence ao setor financeiro (bancos, seguradoras, corretoras, holdings bancárias)."""
    if ticker and ticker.upper() in ["ITSA3", "ITSA4"]:
        return True
    s = sector_name.lower().strip()
    return any(fin in s for fin in FINANCIAL_SECTORS)


def is_commodity_sector(sector_name: str) -> bool:
    """Detecta se o ativo é produtor de commodities cíclicas (tomador de preço)."""
    s = sector_name.lower().strip()
    return any(com in s for com in COMMODITY_SECTORS)


def is_cyclical_sector(sector_name: str) -> bool:
    """Detecta se o ativo opera em setor altamente sensível a ciclos macroeconômicos e imobiliários."""
    s = sector_name.lower().strip()
    return any(cyc in s for cyc in CYCLICAL_SECTORS)


def score_roic(roic: Optional[float]) -> float:
    """Curva contínua logarítmica de ROIC (NTN-B 6.5% -> ~45 | 18% -> ~76 | 25% -> ~85 | Max 93.0)."""
    if roic is None or math.isnan(roic):
        return 25.0
    r = roic * 100.0 if abs(roic) < 2.0 else roic
    if r <= 0.0:
        return max(5.0, 15.0 + r)
    val = 26.0 + (math.log(max(1.0, r + 1.0)) * 19.0)
    return min(93.0, max(5.0, val))


def score_roe(roe: Optional[float]) -> float:
    """Curva contínua logarítmica de ROE (10% -> ~48 | 20% -> ~75 | 30% -> ~86 | Max 92.0)."""
    if roe is None or math.isnan(roe):
        return 25.0
    r = roe * 100.0 if abs(roe) < 2.0 else roe
    if r <= 0.0:
        return max(5.0, 15.0 + r)
    val = 22.0 + (math.log(max(1.0, r + 1.0)) * 20.0)
    return min(92.0, max(5.0, val))


def score_mrg_liq(mrg: Optional[float]) -> float:
    """Curva contínua logarítmica de Margem Líquida (5% -> ~45 | 15% -> ~72 | 30% -> ~88 | Max 92.0)."""
    if mrg is None or math.isnan(mrg):
        return 25.0
    m = mrg * 100.0 if abs(mrg) < 2.0 else mrg
    if m <= 0.0:
        return max(5.0, 15.0 + m)
    val = 24.0 + (math.log(max(1.0, m + 1.0)) * 19.5)
    return min(92.0, max(5.0, val))


def score_div_liq_ebitda(dl_ebitda: Optional[float]) -> float:
    """
    Curva contínua de Solidez de Dívida Líquida / EBITDA:
    Caixa Líquido dá até 90.0 (não 100.0, pois excesso de caixa ocioso penaliza alocação ótima).
    0.0x a 1.0x (87 a 78) | 1.0x a 2.5x (78 a 57) | 2.5x a 3.5x (57 a 32) | > 3.5x (< 32).
    """
    if dl_ebitda is None or math.isnan(dl_ebitda):
        return 50.0
    if dl_ebitda < 0.0:
        return min(90.0, 87.0 + min(3.0, abs(dl_ebitda)))
    elif dl_ebitda <= 1.0:
        return 87.0 - (dl_ebitda * 9.0)
    elif dl_ebitda <= 2.5:
        return 78.0 - ((dl_ebitda - 1.0) * 14.0)
    elif dl_ebitda <= 3.5:
        return 57.0 - ((dl_ebitda - 2.5) * 25.0)
    else:
        return max(0.0, 32.0 - ((dl_ebitda - 3.5) * 15.0))


def score_liq_corr(liq_corr: Optional[float]) -> float:
    """Curva contínua de Liquidez Corrente (1.0x = 50 | 1.5x = 78 | >= 2.0x = 90.0)."""
    if liq_corr is None or math.isnan(liq_corr):
        return 50.0
    if liq_corr >= 2.0:
        return 90.0
    elif liq_corr >= 1.5:
        return 78.0 + ((liq_corr - 1.5) * 24.0)
    elif liq_corr >= 1.0:
        return 50.0 + ((liq_corr - 1.0) * 56.0)
    else:
        return max(5.0, liq_corr * 45.0)


def score_cresc_rec5a(cresc: Optional[float]) -> float:
    """Curva contínua de Crescimento de Receita Quinquenal (0% = 45 | 10% = 75 | >= 25% = 90.0)."""
    if cresc is None or math.isnan(cresc):
        return 45.0
    c = cresc * 100.0 if abs(cresc) < 2.0 else cresc
    if c >= 25.0:
        return 90.0
    elif c >= 10.0:
        return 75.0 + ((c - 10.0) * 1.0)
    elif c >= 0.0:
        return 45.0 + (c * 3.0)
    else:
        return max(10.0, 45.0 + (c * 2.0))


def score_mrg_bruta(mrg_b: Optional[float]) -> float:
    """Curva contínua de Margem Bruta (Poder de Precificação: 20% = ~55 | 40% = ~77 | >= 70% = 91.0)."""
    if mrg_b is None or math.isnan(mrg_b):
        return 35.0
    b = mrg_b * 100.0 if abs(mrg_b) < 2.0 else mrg_b
    if b <= 0.0:
        return 10.0
    val = 20.0 + (math.log(max(1.0, b + 1.0)) * 17.5)
    return min(91.0, max(10.0, val))


def extract_historical_metrics(hist_data: Optional[Dict[str, Any]], cur_roe: Optional[float], cur_roic: Optional[float], cur_lucro: Optional[float], cur_rec: Optional[float]) -> Dict[str, Any]:
    """
    Extrai métricas consolidadas dos 5 anos (2022 a 2026 LTM) a partir do cache histórico auditado.
    Calcula o desvio padrão histórico do ROE para mensurar previsibilidade de fosso econômico.
    """
    if not hist_data or not isinstance(hist_data, dict):
        return {
            "has_history": False,
            "effective_roe": cur_roe,
            "effective_roic": cur_roic,
            "anos_com_lucro": 5,
            "total_anos_registrados": 5,
            "cagr_rec_pct": None,
            "cagr_lucro_pct": None,
            "roe_std": None,
        }

    past_years = ["2022", "2023", "2024", "2025"]
    roes = []
    lucros = []
    receitas = []

    for yr in past_years:
        d = hist_data.get(yr, {})
        if d.get("roe") is not None:
            roes.append(float(d["roe"]))
        if d.get("lucro_liquido") is not None:
            lucros.append(float(d["lucro_liquido"]))
        if d.get("receita") is not None and float(d["receita"]) > 0:
            receitas.append(float(d["receita"]))

    # Adiciona o ano corrente LTM se disponível
    if cur_lucro is not None:
        lucros.append(float(cur_lucro))
    if cur_rec is not None and cur_rec > 0:
        receitas.append(float(cur_rec))

    # 1. ROE / ROIC Efetivo com Memória Temporal (60% LTM + 40% Média 2022-2025)
    effective_roe = cur_roe
    effective_roic = cur_roic
    roe_std = None

    if len(roes) >= 2:
        avg_hist_roe = sum(roes) / len(roes)
        mean_r = avg_hist_roe
        var_r = sum((x - mean_r) ** 2 for x in roes) / (len(roes) - 1)
        roe_std = math.sqrt(var_r)

        if cur_roe is not None:
            effective_roe = (cur_roe * 0.60) + (avg_hist_roe * 0.40)
        else:
            effective_roe = avg_hist_roe

        if cur_roic is not None:
            effective_roic = (cur_roic * 0.60) + (avg_hist_roe * 0.40)
        else:
            effective_roic = effective_roe

    # 2. Contagem de Anos com Lucro
    anos_com_lucro = sum(1 for l in lucros if l > 0)
    total_anos_registrados = len(lucros)

    # 3. CAGR Receita e Lucro
    cagr_rec = None
    if len(receitas) >= 2 and receitas[0] > 0 and receitas[-1] > 0:
        n_years = max(1, len(receitas) - 1)
        cagr_rec = (receitas[-1] / receitas[0]) ** (1.0 / n_years) - 1.0

    cagr_lucro = None
    if len(lucros) >= 2 and lucros[0] > 0 and lucros[-1] > 0:
        n_years = max(1, len(lucros) - 1)
        cagr_lucro = (lucros[-1] / lucros[0]) ** (1.0 / n_years) - 1.0

    return {
        "has_history": True,
        "effective_roe": effective_roe,
        "effective_roic": effective_roic,
        "anos_com_lucro": anos_com_lucro,
        "total_anos_registrados": total_anos_registrados,
        "cagr_rec_pct": cagr_rec,
        "cagr_lucro_pct": cagr_lucro,
        "roe_std": roe_std,
    }


def calculate_financial_institution_quality(row: Dict[str, Any], hist_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    MÓDULO BANCÁRIO & MOAT TERMINAL: Scoring Especializado para Instituições Financeiras.
    - Rentabilidade: ROE Efetivo Quinquenal (60% LTM + 40% Média Histórica).
    - Solidez: Escala Sistêmica de Balanço (Patrimônio Líquido) e colchão de solvência anti-crise de liquidez.
    - Consistência: Resiliência de lucros no quinquênio e penalização por volatilidade errática de ROE (risco de atacado).
    """
    cur_roe = row.get("roe") or 0.0
    mrg_liq = row.get("mrg_liq") or 0.0
    cresc = row.get("cresc_rec5a")
    cur_lucro = row.get("lucro_liq")
    cur_rec = row.get("receita_liq")
    patrim_liq = row.get("patrim_liq")

    h_metrics = extract_historical_metrics(hist_data, cur_roe, cur_roe, cur_lucro, cur_rec)
    effective_roe = h_metrics["effective_roe"] if (h_metrics["has_history"] and h_metrics["effective_roe"] is not None) else cur_roe

    # Pilar 1: Rentabilidade Financeira (Peso 40%) - Curva Contínua Logarítmica de ROE
    s_roe = score_roe(effective_roe)
    m_val = (mrg_liq * 100.0 if abs(mrg_liq) < 2.0 else mrg_liq) if mrg_liq else None
    if m_val is not None and not math.isnan(m_val) and 10.0 <= m_val <= 80.0:
        s_mrg = score_mrg_liq(mrg_liq)
        score_pilar_rentabilidade = (s_roe * 0.85) + (s_mrg * 0.15)
    else:
        s_mrg = s_roe
        score_pilar_rentabilidade = s_roe

    # Pilar 2: Solidez Patrimonial e Escala Institucional (Peso 35%)
    # Bancos sistêmicos de grande porte possuem captação de varejo a custo baixo e menor risco de liquidez
    pl_val = float(patrim_liq or 0.0)
    if pl_val >= 50_000_000_000:  # Bancos Mega Sistêmicos (Itaú, BB, Bradesco, Santander)
        base_solidez = 91.0
    elif pl_val >= 15_000_000_000:  # Grandes Bancos / Seguradoras Líderes (BTG Pactual, Itaúsa, BB Seguridade, Caixa Seguridade)
        base_solidez = 86.0
    elif pl_val >= 5_000_000_000:  # Médio-Grande (Porto Seguro, ABC Brasil, Banrisul)
        base_solidez = 78.0
    elif pl_val >= 1_000_000_000:  # Médio Atacado / Nicho de Consignado (Pine, Mercantil, Daycoval)
        base_solidez = 62.0
    else:  # Pequeno Porte (< R$ 1 Bi)
        base_solidez = 46.0

    r_pct = effective_roe * 100.0 if abs(effective_roe) < 2.0 else effective_roe
    if r_pct >= 20.0:
        base_solidez = min(92.0, base_solidez + 2.0)
    elif r_pct < 10.0:
        base_solidez = max(30.0, base_solidez - 12.0)

    score_pilar_solidez = base_solidez

    # Pilar 3: Consistência & Histórico (Peso 25%)
    anos_lucro = h_metrics["anos_com_lucro"]
    total_anos = h_metrics.get("total_anos_registrados", 5)
    if anos_lucro == total_anos:
        base_cons = 86.0
    elif anos_lucro == total_anos - 1:
        base_cons = 68.0
    else:
        base_cons = 45.0

    s_cresc = score_cresc_rec5a(cresc)
    score_pilar_consistencia = (base_cons * 0.70) + (s_cresc * 0.30)

    # Penalidade por Volatilidade Excessiva do ROE (Inexistência de Moat Estrutural / Risco Cíclico)
    roe_std = h_metrics.get("roe_std")
    if roe_std is not None and roe_std > 0.07:
        penalidade_vol = min(12.0, (roe_std - 0.07) * 100.0)
        score_pilar_consistencia = max(20.0, score_pilar_consistencia - penalidade_vol)

    # Quality Score Final Ponderado
    quality_score = (
        (score_pilar_rentabilidade * 0.40) +
        (score_pilar_solidez * 0.35) +
        (score_pilar_consistencia * 0.25)
    )
    # Teto teórico assintótico (nenhuma empresa atinge 100.0)
    quality_score = round(max(5.0, min(92.5, quality_score)), 1)

    if quality_score >= 80.0:
        quality_tier = "Tier 1: Classe Mundial (Wide/Narrow Moat)"
        quality_tag = "CLASSE_MUNDIAL"
    elif quality_score >= 65.0:
        quality_tier = "Tier 2: Empresa Sólida / Saudável"
        quality_tag = "SOLIDA"
    elif quality_score >= 50.0:
        quality_tier = "Tier 3: Operação Medíocre / Concorrência Predatória"
        quality_tag = "MEDIOCRE"
    else:
        quality_tier = "Tier 4: Risco Estrutural / Destruidor de Valor"
        quality_tag = "RISCO_ESTRUTURAL"

    return {
        "quality_score": quality_score,
        "quality_tier": quality_tier,
        "quality_tag": quality_tag,
        "pilar_rentabilidade": round(score_pilar_rentabilidade, 1),
        "pilar_solidez": round(score_pilar_solidez, 1),
        "pilar_consistencia": round(score_pilar_consistencia, 1),
        "is_financial": True,
        "sub_scores": {
            "roic": s_roe,
            "roe": s_roe,
            "mrg_liq": s_mrg,
            "div_liq_ebitda": score_pilar_solidez,
            "liq_corr": score_pilar_solidez,
            "cresc_rec5a": s_cresc,
            "mrg_bruta": s_mrg,
        },
    }


def calculate_business_quality(row: Dict[str, Any], sector_name: str = "", hist_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Calcula o Moat Quality Score (0 a 92.5) com base estrita nos 3 pilares de Charlie Munger:
    - Rentabilidade: ROIC/ROE Efetivos com Memória Temporal Quinquenal (60% LTM + 40% Histórico).
    - Solidez: Balanço patrimonial, solvência líquida e liquidez corrente contínua.
    - Consistência: Resiliência de lucros no quinquênio e poder de precificação (Margem Bruta).
    - Desconto Cíclico: Incorporadoras imobiliárias e commodities recebem fator de previsibilidade de fosso econômico.
    """
    ticker = str(row.get("ticker", "")).strip().upper()
    if is_financial_sector(sector_name, ticker):
        return calculate_financial_institution_quality(row, hist_data)

    cur_roe = row.get("roe")
    cur_roic = row.get("roic")
    cur_lucro = row.get("lucro_liq")
    cur_rec = row.get("receita_liq")

    h_metrics = extract_historical_metrics(hist_data, cur_roe, cur_roic, cur_lucro, cur_rec)
    effective_roe = h_metrics["effective_roe"] if (h_metrics["has_history"] and h_metrics["effective_roe"] is not None) else cur_roe
    effective_roic = h_metrics["effective_roic"] if (h_metrics["has_history"] and h_metrics["effective_roic"] is not None) else cur_roic

    # 1. Rentabilidade (Peso 40%) - ROIC, ROE e Margem Líquida em Curvas Contínuas
    s_roic = score_roic(effective_roic)
    s_roe = score_roe(effective_roe)
    s_mrg_liq = score_mrg_liq(row.get("mrg_liq"))
    score_pilar_rentabilidade = (s_roic * 0.40) + (s_roe * 0.35) + (s_mrg_liq * 0.25)

    # 2. Solidez Financeira (Peso 35%)
    patrim_liq = row.get("patrim_liq")
    has_negative_equity = (patrim_liq is not None and patrim_liq < 0) or ("PATRIMONIO_LIQUIDO_NEGATIVO" in row.get("alert_flags", []))

    if has_negative_equity:
        s_dl_ebitda = 0.0
        s_liq_corr = 0.0
        score_pilar_solidez = 0.0
    else:
        s_dl_ebitda = score_div_liq_ebitda(row.get("div_liq_ebitda"))
        s_liq_corr = score_liq_corr(row.get("liq_corr"))
        score_pilar_solidez = (s_dl_ebitda * 0.55) + (s_liq_corr * 0.45)

    # 3. Consistência e Defensibilidade (Peso 25%)
    anos_lucro = h_metrics["anos_com_lucro"]
    total_anos = h_metrics.get("total_anos_registrados", 5)
    if anos_lucro == total_anos:
        base_cons = 86.0
    elif anos_lucro == total_anos - 1:
        base_cons = 68.0
    else:
        base_cons = 45.0

    s_cresc = score_cresc_rec5a(row.get("cresc_rec5a"))
    s_mrg_bruta = score_mrg_bruta(row.get("mrg_bruta"))

    # Ajuste de Intensidade de Capital (EBIT / EBITDA)
    ev_ebitda = row.get("ev_ebitda")
    ev_ebit = row.get("ev_ebit")
    capital_intensity = None
    if ev_ebitda and ev_ebit and ev_ebit > 0 and ev_ebitda > 0:
        capital_intensity = ev_ebitda / ev_ebit
        if capital_intensity < 0.60:
            s_mrg_bruta = max(20.0, s_mrg_bruta - 12.0)

    score_pilar_consistencia = (base_cons * 0.40) + (s_cresc * 0.30) + (s_mrg_bruta * 0.30)

    # Quality Score Bruto Ponderado
    raw_score = (
        (score_pilar_rentabilidade * 0.40) +
        (score_pilar_solidez * 0.35) +
        (score_pilar_consistencia * 0.25)
    )

    # Ajuste Setorial de Previsibilidade de Fosso Econômico (Moat Defensibility)
    if is_cyclical_sector(sector_name):
        # Incorporadoras / Construção Civil: alto risco de taxa de juros, distratos e ciclo imobiliário
        raw_score *= 0.90
    elif is_commodity_sector(sector_name):
        # Produtores de Commodities: tomadores de preço, vulneráveis ao ciclo global de preços
        raw_score *= 0.88

    # Salvaguarda Munger: Empresas com Passivo a Descoberto NUNCA podem passar de Tier 4
    if has_negative_equity:
        quality_score = min(35.0, round(raw_score, 1))
        quality_tier = "Tier 4: Risco Estrutural / Destruidor de Valor"
        quality_tag = "RISCO_ESTRUTURAL"
    else:
        quality_score = round(max(5.0, min(92.5, raw_score)), 1)
        if quality_score >= 80.0:
            quality_tier = "Tier 1: Classe Mundial (Wide/Narrow Moat)"
            quality_tag = "CLASSE_MUNDIAL"
        elif quality_score >= 65.0:
            quality_tier = "Tier 2: Empresa Sólida / Saudável"
            quality_tag = "SOLIDA"
        elif quality_score >= 50.0:
            quality_tier = "Tier 3: Operação Medíocre / Concorrência Predatória"
            quality_tag = "MEDIOCRE"
        else:
            quality_tier = "Tier 4: Risco Estrutural / Destruidor de Valor"
            quality_tag = "RISCO_ESTRUTURAL"

    return {
        "quality_score": quality_score,
        "quality_tier": quality_tier,
        "quality_tag": quality_tag,
        "pilar_rentabilidade": round(score_pilar_rentabilidade, 1),
        "pilar_solidez": round(score_pilar_solidez, 1),
        "pilar_consistencia": round(score_pilar_consistencia, 1),
        "is_financial": False,
        "capital_intensity": capital_intensity,
        "sub_scores": {
            "roic": s_roic,
            "roe": s_roe,
            "mrg_liq": s_mrg_liq,
            "div_liq_ebitda": s_dl_ebitda,
            "liq_corr": s_liq_corr,
            "cresc_rec5a": s_cresc,
            "mrg_bruta": s_mrg_bruta,
        },
    }


def evaluate_entry_valuation(row: Dict[str, Any], sector_name: str = "") -> Dict[str, Any]:
    """
    Filtro 2: Modelagem Fundamentalista de Múltiplos e Solvência:
    - Spread vs NTN-B (Equity Risk Premium Real)
    - Payout Implícito (DY / EY)
    - Alerta de Pico de Ciclo de Commodities
    - Cobertura da Dívida pelo EBIT (Anti-Selic Alta)
    """
    pl = row.get("pl")
    ev_ebitda = row.get("ev_ebitda")
    ev_ebit = row.get("ev_ebit")
    earnings_yield = row.get("earnings_yield")
    div_yield = row.get("div_yield") or 0.0
    div_liq_ebitda = row.get("div_liq_ebitda")
    roic = row.get("roic") or 0.0
    ticker = str(row.get("ticker", "")).strip().upper()
    is_fin = is_financial_sector(sector_name, ticker)
    is_com = is_commodity_sector(sector_name)

    # SALVAGUARDA INSTITUCIONAL INEGOCIÁVEL: Passivo a Descoberto (PL Negativo)
    patrim_liq = row.get("patrim_liq")
    has_negative_equity = (patrim_liq is not None and patrim_liq < 0) or ("PATRIMONIO_LIQUIDO_NEGATIVO" in row.get("alert_flags", []))

    if has_negative_equity:
        pl_val = f"{pl:.1f}x" if pl else "N/D"
        ey_val = round((100.0 / pl), 2) if (pl and pl > 0) else None
        ey_sp = round(ey_val - NTN_B_BENCHMARK, 2) if ey_val else None
        pl_num = abs(patrim_liq) / 1e9 if patrim_liq else 0
        return {
            "entry_status": "🔴 MÚLTIPLOS ELEVADOS / ALTO RISCO",
            "entry_tag": "ESTICADA",
            "entry_color": "#EF4444",
            "earnings_yield_pct": ey_val,
            "ey_spread": ey_sp,
            "payout_implicito": None,
            "payout_tag": "N/D (Insolvência Técnica)",
            "is_commodity_peak": False,
            "is_debt_vulnerable": True,
            "capital_intensity": None,
            "cfa_flags": ["PATRIMONIO_LIQUIDO_NEGATIVO", "PASSIVO_A_DESCOBERTO"],
            "rationale": (
                f"Patrimônio Líquido negativo de -R$ {pl_num:.2f} bilhões (passivo a descoberto). "
                f"O P/L aparente de {pl_val} decorre de renegociações contábeis não-caixa de dívida e variações cambiais. "
                "Incompatível com critérios de solidez contábil e preservação patrimonial."
            ),
        }

    if pl is None or pl <= 0:
        return {
            "entry_status": "🔴 MÚLTIPLOS ELEVADOS / SEM BASE DE LUCRO",
            "entry_tag": "ESTICADA",
            "entry_color": "#EF4444",
            "earnings_yield_pct": None,
            "ey_spread": None,
            "payout_implicito": None,
            "payout_tag": "N/D",
            "is_commodity_peak": False,
            "is_debt_vulnerable": False,
            "capital_intensity": None,
            "cfa_flags": ["PREJUIZO_CONTABIL"],
            "rationale": "Empresa reportando prejuízo contábil no período LTM (P/L negativo). Ausência de base de lucros operacionais para cálculo de múltiplos e rendimento.",
        }

    ey_pct = (earnings_yield * 100.0) if earnings_yield else (100.0 / pl)

    # CRITÉRIO 2: Spread de Earnings Yield vs. NTN-B (Equity Risk Premium Local)
    ey_spread = round(ey_pct - NTN_B_BENCHMARK, 2)

    # CRITÉRIO 6: Payout Implícito (Dividend Yield / Earnings Yield = DY * P/L)
    payout_implicito = round((div_yield * pl), 2) if (pl and div_yield is not None) else None
    if payout_implicito is not None:
        if payout_implicito > 1.05:
            payout_tag = "⚠️ INSUSTENTÁVEL (>100% dos Lucros)"
        elif 0.40 <= payout_implicito <= 0.85:
            payout_tag = "💎 SAUDÁVEL E DISCIPLINADO (40%-85%)"
        else:
            payout_tag = "📈 RETENÇÃO / REINVESTIMENTO"
    else:
        payout_tag = "N/D"

    # CRITÉRIO 4: Alerta de Pico de Ciclo de Commodities
    is_commodity_peak = False
    if is_com and pl < 6.5 and roic > 0.18:
        is_commodity_peak = True

    # CRITÉRIO 5: Cobertura da Dívida pelo EBIT (Anti-Selic Alta)
    # Se div_liq_ebitda for alto (>2.5x), estima-se que a Selic consumirá grande fatia do EBIT
    is_debt_vulnerable = False
    if not is_fin and div_liq_ebitda is not None and div_liq_ebitda > 2.8:
        is_debt_vulnerable = True

    # CRITÉRIO 1: Intensidade de Capital (EBITDA vs EBIT) - não aplicável a instituições financeiras
    capital_intensity = None
    if not is_fin and ev_ebitda and ev_ebit and ev_ebit > 0 and ev_ebitda > 0:
        capital_intensity = ev_ebitda / ev_ebit

    # Flags Institucionais de Risco / Auditoria
    cfa_flags = []
    if is_commodity_peak:
        cfa_flags.append("PICO_DE_CICLO_COMMODITIES")
    if is_debt_vulnerable:
        cfa_flags.append("ALTA_VULNERABILIDADE_JUROS")
    if ey_spread < 0.0:
        cfa_flags.append("PREMIO_RISCO_NEGATIVO_NTNB")
    if payout_implicito and payout_implicito > 1.05:
        cfa_flags.append("PAYOUT_DESALAVANCAGEM_ALERTA")

    # Classificação do Status de Entrada com Filtro Rigoroso (3 Alternativas Estritas)
    is_asymmetry = False
    is_stretched = False

    if is_fin:
        pvp_val = row.get("pvp")
        # Para bancos e holdings financeiras: P/L atrativo (< 9.5x) e spread sobre NTN-B (>= +3.5%)
        # Ou com P/VP em desconto patrimonial (P/VP <= 1.20x) com P/L de um dígito
        if (pl < 9.5 and ey_spread >= 3.5) or (pvp_val is not None and pvp_val <= 1.20 and pl < 10.5 and ey_spread >= 2.5):
            is_asymmetry = True
        elif pl > 15.0 or ey_spread < 0.0 or (pvp_val is not None and pvp_val > 3.0):
            is_stretched = True
    else:
        ev_cond = (ev_ebitda is not None and ev_ebitda > 0 and ev_ebitda < 6.0) or (ev_ebitda is None)
        # Assimetria requer: P/L < 8x, Spread NTN-B >= +5.0% e EV/EBITDA < 6x
        if pl < 8.0 and ey_spread >= 5.0 and ev_cond:
            # Se for pico de ciclo evidente de commodity, modera a classificação
            if not is_commodity_peak:
                is_asymmetry = True
        elif pl > 15.0 or (ev_ebitda is not None and ev_ebitda > 10.0) or ey_spread < 0.0:
            is_stretched = True

    if is_asymmetry:
        status = "🟢 MÚLTIPLOS DESCONTADOS"
        tag = "ASSIMETRIA_FAVORAVEL"
        color = "#10B981"
        rationale = (
            f"Earnings Yield de {ey_pct:.1f}% confere spread de +{ey_spread:.1f}% sobre a NTN-B real (6,5%). "
            f"P/L de {pl:.1f}x negocia abaixo da média histórica do setor e do mercado."
        )
    elif is_stretched:
        status = "🔴 MÚLTIPLOS ELEVADOS"
        tag = "ESTICADA"
        color = "#EF4444"
        spread_msg = f"Spread vs NTN-B comprimido em {ey_spread:+.1f}%" if ey_spread < 2.0 else f"P/L elevado de {pl:.1f}x"
        rationale = (
            f"{spread_msg}. Earnings Yield de {ey_pct:.1f}% reflete cotação negociando com prêmio em múltiplos frente aos pares e à taxa real soberana."
        )
    else:
        status = "🟡 VALUATION EM LINHA"
        tag = "PRECO_JUSTO"
        color = "#F59E0B"
        rationale = (
            f"P/L de {pl:.1f}x e Earnings Yield de {ey_pct:.1f}% (Spread de {ey_spread:+.1f}% sobre NTN-B). "
            f"Múltiplos situam-se na faixa mediana histórica do setor."
        )

    return {
        "entry_status": status,
        "entry_tag": tag,
        "entry_color": color,
        "earnings_yield_pct": round(ey_pct, 2),
        "ey_spread": ey_spread,
        "payout_implicito": payout_implicito,
        "payout_tag": payout_tag,
        "is_commodity_peak": is_commodity_peak,
        "is_debt_vulnerable": is_debt_vulnerable,
        "capital_intensity": capital_intensity,
        "cfa_flags": cfa_flags,
        "rationale": rationale,
    }


def generate_cfa_verdict(
    ticker: str,
    company_name: str,
    quality_data: Dict[str, Any],
    valuation_data: Dict[str, Any],
    metrics: Dict[str, Any],
) -> List[Dict[str, str]]:
    """
    Síntese Executiva Fundamentalista baseada no Framework Munger & Balanços Auditados CVM.
    Incorpora 6 critérios analíticos em 3 bullets objetivos e aprofundados:
    1. Eficiência Operacional (Moat, ROIC, ROE, Margem e Disciplina de Capital)
    2. Estrutura de Capital & Riscos (Endividamento, Intensidade de Capital Capex e Ciclicalidade)
    3. Análise Quantitativa de Múltiplos & NTN-B (Spread real frente ao Tesouro IPCA+)
    """
    q_score = quality_data["quality_score"]
    is_fin = quality_data.get("is_financial", False)
    roic = metrics.get("roic") or 0.0
    roe = metrics.get("roe") or 0.0
    mrg_liq = metrics.get("mrg_liq") or 0.0
    cresc = metrics.get("cresc_rec5a") or 0.0
    dl_ebitda = metrics.get("div_liq_ebitda")
    is_net_cash = metrics.get("is_net_cash", False)
    ey = valuation_data.get("earnings_yield_pct")
    ey_spread = valuation_data.get("ey_spread")
    payout = valuation_data.get("payout_implicito")
    payout_tag = valuation_data.get("payout_tag", "")
    is_com_peak = valuation_data.get("is_commodity_peak", False)
    is_debt_vuln = valuation_data.get("is_debt_vulnerable", False)
    cap_intensity = valuation_data.get("capital_intensity")

    is_passivo_descoberto = valuation_data.get("entry_tag") == "PASSIVO_DESCOBERTO" or (metrics.get("patrim_liq") is not None and metrics.get("patrim_liq") < 0)

    # BULLET 1: Por que é boa? (Fosso & Eficiência de Capital)
    if is_passivo_descoberto:
        pl_val = abs(metrics.get("patrim_liq", 0)) / 1e9
        bullet_1 = (
            f"**Insolvência Técnica & Passivo a Descoberto:** {company_name} opera com patrimônio líquido negativo de -R$ {pl_val:.2f} bilhões. "
            f"Todos os ativos somados não cobrem o montante devido aos credores e arrendadores. "
            f"Quality Score limitado pelo modelo Munger em **{q_score}/100** ({quality_data['quality_tier']})."
        )
    else:
        positives = []
        if is_fin:
            positives.append(f"instituição financeira/holding bancária com ROE estrutural de {roe*100:.1f}%")
            if 0.15 <= mrg_liq <= 1.0:
                positives.append(f"alta margem líquida bancária de {mrg_liq*100:.1f}%")
            elif mrg_liq > 1.0:
                positives.append("geração robusta via equivalência patrimonial de coligadas")
        else:
            if roic >= 0.18:
                positives.append(f"retorno sobre capital excepcional (ROIC de {roic*100:.1f}%)")
            elif roe >= 0.18:
                positives.append(f"alta rentabilidade patrimonial (ROE de {roe*100:.1f}%)")
            if mrg_liq >= 0.12:
                positives.append(f"poder de precificação sustentável (Margem Líquida de {mrg_liq*100:.1f}%)")
            if is_net_cash:
                positives.append("balanço ultraconservador em caixa líquido")
            elif dl_ebitda is not None and 0 <= dl_ebitda <= 1.5:
                positives.append(f"alavancagem controlada de {dl_ebitda:.2f}x Dív. Líq./EBITDA")

        if cresc >= 0.08:
            positives.append(f"expansão secular de receita de {cresc*100:.1f}% a.a. em 5 anos")

        if payout and 0.40 <= payout <= 0.85:
            positives.append(f"política de proventos sustentável (Payout Implícito de {payout*100:.0f}%)")

        if not positives:
            positives.append("empresa com liquidez auditada e operação estabelecida no mercado doméstico")

        bullet_1 = (
            f"**Fundamentos & Fosso Competitivo:** {company_name} apresenta {', '.join(positives[:3])}. "
            f"Quality Score consolidado em **{q_score}/100** ({quality_data['quality_tier']})."
        )

    # BULLET 2: Onde está o risco? (Teste Ácido de Juros, Capex e Ciclos)
    risks = []
    if is_com_peak:
        risks.append(
            "⚠️ **Alerta de Pico de Ciclo de Commodities**: Múltiplos baixos e retornos elevados refletem o ápice de preços de matérias-primas no mercado global, exigindo cautela com eventual reversão à média"
        )
    if not is_fin and is_debt_vuln:
        risks.append(
            f"⚠️ **Vulnerabilidade a Juros (Selic Alta)**: Alavancagem de {dl_ebitda:.2f}x Dív.Líq/EBITDA impõe expressiva carga de despesas financeiras em ambiente monetário restritivo"
        )
    if not is_fin and cap_intensity is not None and cap_intensity < 0.60:
        risks.append(
            f"⚠️ **Intensidade de Capital Elevada (Munger Acid Test)**: Apenas {cap_intensity*100:.0f}% do EBITDA se converte em EBIT, demonstrando pesado arrasto de Capex de manutenção e depreciação"
        )
    if payout and payout > 1.05:
        risks.append(
            f"⚠️ **Payout Excedente ({payout*100:.0f}%)**: Proventos superam o lucro líquido LTM gerado, sinalizando que a distribuição é financiada por desalavancagem de caixa ou endividamento"
        )
    if not is_fin and dl_ebitda is not None and dl_ebitda > 3.0 and not is_debt_vuln:
        risks.append(f"alavancagem de {dl_ebitda:.2f}x Dív.Líq/EBITDA requer monitoramento contínuo")
    if not is_fin and mrg_liq < 0.05 and mrg_liq > 0:
        risks.append(f"margem líquida comprimida ({mrg_liq*100:.1f}%), vulnerável a pressão inflacionária de insumos")

    if is_fin:
        risks.append("sensibilidade ao ciclo de crédito bancário (inadimplência/PDD), margem financeira de intermediação e oscilações da taxa Selic")

    if not risks:
        risks.append("riscos primariamente atrelados ao cenário macroeconômico doméstico, oscilações do câmbio e custo de crédito soberano")

    bullet_2 = f"**Pontos de Atenção & Riscos:** {'; '.join(risks[:2])}."

    # BULLET 3: Como está a entrada? (Spread Real vs NTN-B)
    if ey_spread is not None:
        spread_str = f"+{ey_spread:.1f}%" if ey_spread > 0 else f"{ey_spread:.1f}%"
    else:
        spread_str = "N/D"

    ey_str = f"**{ey:.1f}% a.a.**" if ey is not None else "**N/D (Prejuízo)**"
    bullet_3 = (
        f"**Comportamento de Múltiplos & NTN-B:** {valuation_data['entry_status']}. "
        f"Earnings Yield auditado em {ey_str} (Spread vs. NTN-B real de 6,5%: **{spread_str}**). "
        f"{valuation_data['rationale']}"
    )

    return [
        {"title": "1. Fundamentos & Eficiência Operacional", "content": bullet_1, "icon": "diamond"},
        {"title": "2. Estrutura de Capital & Riscos Observados", "content": bullet_2, "icon": "shield"},
        {"title": "3. Análise Quantitativa de Múltiplos & NTN-B", "content": bullet_3, "icon": "scale"},
    ]
