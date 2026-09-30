"""
app.py
======
JP Morgan & Charlie Munger B3 Screener & Terminal de Diagnóstico.
Aplicação analítica institucional de alta performance para triagem de ações da B3,
alimentada 100% pelo Fundamentus sob o rigoroso princípio de Charlie Munger:
"Compre empresas excepcionais a preços razoáveis."
Inclui os 6 Módulos Avançados CFA:
- Teste Ácido de Munger (Intensidade de Capital EBIT / EBITDA)
- Spread de Juro Real vs. NTN-B (Equity Risk Premium)
- Scoring Especializado para Bancos e Seguradoras
- Alerta de Pico de Ciclo de Commodities
- Cobertura da Dívida Anti-Selic Alta
- Payout Implícito e Sustentabilidade de Dividendos
"""

from __future__ import annotations
import os
import io
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

from data_pipeline import (
    get_cached_universe,
    fetch_fundamentus_ticker_details,
    get_current_timestamp_brt,
)
from scoring_engine import (
    calculate_business_quality,
    evaluate_entry_valuation,
    generate_cfa_verdict,
    NTN_B_BENCHMARK,
)

# Configuração de Página Streamlit (Modo Wide Institucional)
st.set_page_config(
    page_title="JP Morgan | Munger B3 Terminal",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Injeção de CSS Institucional
CSS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "styles.css")
if os.path.exists(CSS_FILE):
    with open(CSS_FILE, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def format_currency(val: float | None) -> str:
    if val is None or pd.isna(val):
        return "N/D"
    return f"R$ {val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def format_billions(val: float | None) -> str:
    if val is None or pd.isna(val):
        return "N/D"
    if abs(val) >= 1_000_000_000:
        return f"R$ {val / 1_000_000_000:,.2f} B".replace(",", "X").replace(".", ",").replace("X", ".")
    elif abs(val) >= 1_000_000:
        return f"R$ {val / 1_000_000:,.2f} M".replace(",", "X").replace(".", ",").replace("X", ".")
    return format_currency(val)


def format_percent(val: float | None) -> str:
    if val is None or pd.isna(val):
        return "N/D"
    num = val * 100.0 if abs(val) < 2.0 else val
    return f"{num:,.2f}%".replace(",", "X").replace(".", ",").replace("X", ".")


def format_multiple(val: float | None) -> str:
    if val is None or pd.isna(val):
        return "N/D"
    return f"{val:,.2f}x".replace(",", "X").replace(".", ",").replace("X", ".")


@st.cache_data(ttl=900, show_spinner=False)
def load_and_score_universe(force_refresh: bool = False):
    """Carrega o universo do Fundamentus e calcula Quality Score e Entry Valuation."""
    df, audit_timestamp = get_cached_universe(force_refresh=force_refresh)

    scored_records = []
    for _, row in df.iterrows():
        row_dict = row.to_dict()
        sector = str(row_dict.get("setor", "Indústria / Geral"))
        q = calculate_business_quality(row_dict, sector)
        v = evaluate_entry_valuation(row_dict, sector)

        record = {
            **row_dict,
            "quality_score": q["quality_score"],
            "quality_tier": q["quality_tier"],
            "quality_tag": q["quality_tag"],
            "pilar_rentabilidade": q["pilar_rentabilidade"],
            "pilar_solidez": q["pilar_solidez"],
            "pilar_consistencia": q["pilar_consistencia"],
            "is_financial": q.get("is_financial", False),
            "entry_status": v["entry_status"],
            "entry_tag": v["entry_tag"],
            "entry_color": v["entry_color"],
            "earnings_yield_pct": v.get("earnings_yield_pct"),
            "ey_spread": v.get("ey_spread"),
            "payout_implicito": (v.get("payout_implicito") * 100.0) if v.get("payout_implicito") is not None else None,
            "payout_tag": v.get("payout_tag", "N/D"),
            "is_commodity_peak": v.get("is_commodity_peak", False),
            "is_debt_vulnerable": v.get("is_debt_vulnerable", False),
            "capital_intensity": v.get("capital_intensity"),
            "cfa_flags": v.get("cfa_flags", []),
            "sub_scores": q["sub_scores"],
            "rationale": v.get("rationale", ""),
        }
        scored_records.append(record)

    scored_df = pd.DataFrame(scored_records)
    return scored_df, audit_timestamp


def render_radar_chart(q_data: dict) -> go.Figure:
    """Gera gráfico radar Dark Theme institucional para os 3 pilares de qualidade."""
    categories = ["Rentabilidade (40%)", "Solidez Balanço (35%)", "Consistência (25%)"]
    values = [
        q_data.get("pilar_rentabilidade", 50),
        q_data.get("pilar_solidez", 50),
        q_data.get("pilar_consistencia", 50),
    ]
    categories_closed = categories + [categories[0]]
    values_closed = values + [values[0]]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values_closed,
        theta=categories_closed,
        fill="toself",
        fillcolor="rgba(0, 208, 132, 0.20)",
        line=dict(color="#00D084", width=2.5),
        name="Score da Empresa",
        hoverinfo="r+theta",
    ))

    fig.add_trace(go.Scatterpolar(
        r=[80, 80, 80, 80],
        theta=categories_closed,
        mode="lines",
        line=dict(color="rgba(100, 181, 246, 0.45)", width=1.5, dash="dash"),
        name="Benchmark Tier 1 (80 pts)",
        hoverinfo="none",
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                showline=False,
                gridcolor="#232B3B",
                tickfont=dict(color="#64748B", size=9, family="JetBrains Mono"),
            ),
            angularaxis=dict(
                gridcolor="#232B3B",
                linecolor="#232B3B",
                tickfont=dict(color="#CBD5E1", size=11, family="Inter", weight=600),
            ),
            bgcolor="#151A23",
        ),
        paper_bgcolor="#151A23",
        margin=dict(l=40, r=40, t=30, b=30),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.22,
            xanchor="center",
            x=0.5,
            font=dict(color="#94A3B8", size=10),
        ),
        height=320,
    )
    return fig


def render_munger_2x2_matrix(
    df: pd.DataFrame,
    x_metric: str = "pl",
    selected_ticker: str | None = None,
) -> go.Figure:
    """
    Renderiza a Matriz 2x2 de Charlie Munger (Qualidade vs. Preço).
    Eixo Y: Business Quality Score (0 a 100) com limiar de qualidade em 75 pontos.
    Eixo X: Preço / Valuation (P/L ou Earnings Yield %).
    """
    plot_df = df[(df["pl"].notna()) & (df["pl"] > 0) & (df["pl"] <= 40.0)].copy()
    quality_threshold = 75.0

    if x_metric == "pl":
        x_col = "pl"
        x_threshold = 12.0
        x_min, x_max = 0.0, 32.0
        x_title = "Preço sobre Lucro (P/L) [← Mais Barato | Mais Caro →]"
        
        q1_x0, q1_x1, q1_y0, q1_y1 = x_min, x_threshold, quality_threshold, 105.0
        q2_x0, q2_x1, q2_y0, q2_y1 = x_threshold, x_max, quality_threshold, 105.0
        q3_x0, q3_x1, q3_y0, q3_y1 = x_min, x_threshold, 20.0, quality_threshold
        q4_x0, q4_x1, q4_y0, q4_y1 = x_threshold, x_max, 20.0, quality_threshold

        q1_label = "🟢 EXCELENTE & BARATA<br><sup>Máxima Oportunidade (Munger Sweet Spot)</sup>"
        q2_label = "🌱 EXCELENTE PORÉM CARA<br><sup>Franquia Premium (Múltiplo Exigente)</sup>"
        q3_label = "🍑 MEDIANA PORÉM BARATA<br><sup>Barganhas & Dividendos (Proteção de Preço)</sup>"
        q4_label = "🛑 FRÁGIL & CARA<br><sup>Sem Margem de Segurança</sup>"
    else:
        x_col = "earnings_yield_pct"
        x_threshold = 10.0
        x_min, x_max = 0.0, 30.0
        x_title = f"Earnings Yield (% a.a.) [NTN-B Ref: {NTN_B_BENCHMARK}% | ← Mais Caro | Mais Retorno/Barato →]"

        q2_x0, q2_x1, q2_y0, q2_y1 = x_min, x_threshold, quality_threshold, 105.0
        q1_x0, q1_x1, q1_y0, q1_y1 = x_threshold, x_max, quality_threshold, 105.0
        q4_x0, q4_x1, q4_y0, q4_y1 = x_min, x_threshold, 20.0, quality_threshold
        q3_x0, q3_x1, q3_y0, q3_y1 = x_threshold, x_max, 20.0, quality_threshold

        q1_label = "🟢 EXCELENTE & BARATA<br><sup>Máxima Oportunidade (Alto EY ≥ 10%)</sup>"
        q2_label = "🌱 EXCELENTE PORÉM CARA<br><sup>Franquia Premium (Retorno Comprimido)</sup>"
        q3_label = "🍑 MEDIANA PORÉM BARATA<br><sup>Barganhas & Dividendos (Alto EY)</sup>"
        q4_label = "🛑 FRÁGIL & CARA<br><sup>Sem Margem de Segurança</sup>"

    fig = go.Figure()

    # 1. Fundo sombreado institucional dos 4 Polos Estratégicos
    fig.add_shape(type="rect", x0=q1_x0, x1=q1_x1, y0=q1_y0, y1=q1_y1, fillcolor="rgba(0, 208, 132, 0.12)", line=dict(width=0), layer="below")
    fig.add_shape(type="rect", x0=q2_x0, x1=q2_x1, y0=q2_y0, y1=q2_y1, fillcolor="rgba(134, 239, 172, 0.09)", line=dict(width=0), layer="below")
    fig.add_shape(type="rect", x0=q3_x0, x1=q3_x1, y0=q3_y0, y1=q3_y1, fillcolor="rgba(253, 186, 116, 0.10)", line=dict(width=0), layer="below")
    fig.add_shape(type="rect", x0=q4_x0, x1=q4_x1, y0=q4_y0, y1=q4_y1, fillcolor="rgba(220, 38, 38, 0.11)", line=dict(width=0), layer="below")

    # 2. Linhas divisorias dos eixos
    fig.add_shape(type="line", x0=x_threshold, x1=x_threshold, y0=20.0, y1=105.0, line=dict(color="#3B82F6", width=1.5, dash="dash"))
    fig.add_shape(type="line", x0=x_min, x1=x_max, y0=quality_threshold, y1=quality_threshold, line=dict(color="#3B82F6", width=1.5, dash="dash"))

    # 3. Anotações dos Quadrantes
    fig.add_annotation(x=(q1_x0 + q1_x1) / 2, y=q1_y1 - 3, text=q1_label, showarrow=False, font=dict(size=10, color="#00D084", family="Inter"), align="center")
    fig.add_annotation(x=(q2_x0 + q2_x1) / 2, y=q2_y1 - 3, text=q2_label, showarrow=False, font=dict(size=10, color="#F2C94C", family="Inter"), align="center")
    fig.add_annotation(x=(q3_x0 + q3_x1) / 2, y=q3_y1 - 3, text=q3_label, showarrow=False, font=dict(size=10, color="#FB923C", family="Inter"), align="center")
    fig.add_annotation(x=(q4_x0 + q4_x1) / 2, y=q4_y1 - 3, text=q4_label, showarrow=False, font=dict(size=10, color="#F87171", family="Inter"), align="center")

    # 4. Plotar os ativos (Scatter Points)
    status_groups = [
        ("🟢 ZONA DE ASSIMETRIA FAVORÁVEL", "#00D084"),
        ("🟡 PREÇO JUSTO / CARREGO", "#F2C94C"),
        ("🔴 ENTRADA ESTICADA / CARA", "#EB5757"),
    ]

    for status_label, color in status_groups:
        sub_df = plot_df[plot_df["entry_status"].str.contains(status_label.split()[1], na=False)]
        if sub_df.empty:
            continue

        hover_texts = []
        for _, r in sub_df.iterrows():
            roic_str = f"{r['roic']*100:.1f}%" if pd.notna(r.get("roic")) else "N/D"
            ev_str = f"{r['ev_ebitda']:.1f}x" if pd.notna(r.get("ev_ebitda")) else "N/D"
            pl_str = f"{r['pl']:.1f}x" if pd.notna(r.get("pl")) else "N/D"
            ey_str = f"{r.get('earnings_yield_pct', 0):.1f}%"
            spread_str = f"{r.get('ey_spread', 0):+.1f}%"
            dy_str = f"{r['div_yield']*100:.1f}%" if pd.notna(r.get("div_yield")) else "N/D"
            payout_str = f"{r['payout_implicito']:.0f}%" if pd.notna(r.get("payout_implicito")) else "N/D"
            
            flag_notice = ""
            if r.get("is_commodity_peak"):
                flag_notice += "<br>⚠️ <i>Alerta: Possível Pico de Ciclo Commodities</i>"
            if r.get("is_debt_vulnerable"):
                flag_notice += "<br>⚠️ <i>Alerta: Alta Vulnerabilidade a Juros</i>"

            ht = (
                f"<b>{r['ticker']}</b> ({r.get('setor', 'Geral')})<br>"
                f"• Quality Score: <b>{r['quality_score']}</b>/100<br>"
                f"• P/L: <b>{pl_str}</b> | EV/EBITDA: <b>{ev_str}</b><br>"
                f"• Earnings Yield: <b>{ey_str}</b> (Spread NTN-B: <b>{spread_str}</b>)<br>"
                f"• ROIC: <b>{roic_str}</b> | DY: <b>{dy_str}</b> | Payout: <b>{payout_str}</b><br>"
                f"• Status: {r['entry_status']}{flag_notice}"
            )
            hover_texts.append(ht)

        fig.add_trace(go.Scatter(
            x=sub_df[x_col],
            y=sub_df["quality_score"],
            mode="markers+text",
            marker=dict(
                size=10,
                color=color,
                line=dict(width=1, color="#151A23"),
                opacity=0.88,
            ),
            text=sub_df["ticker"],
            textposition="top center",
            textfont=dict(size=9, color="#E2E8F0", family="JetBrains Mono"),
            hovertext=hover_texts,
            hoverinfo="text",
            name=status_label.split()[1] + " (" + str(len(sub_df)) + ")",
            customdata=sub_df["ticker"],
        ))

    # 5. Destaque para o ativo selecionado
    if selected_ticker and selected_ticker in plot_df["ticker"].values:
        sel_row = plot_df[plot_df["ticker"] == selected_ticker].iloc[0]
        sel_x = sel_row[x_col]
        sel_y = sel_row["quality_score"]

        fig.add_trace(go.Scatter(
            x=[sel_x],
            y=[sel_y],
            mode="markers",
            marker=dict(size=20, color="rgba(255, 255, 255, 0.0)", line=dict(color="#FFFFFF", width=3), symbol="circle"),
            showlegend=False,
            hoverinfo="none",
        ))

        fig.add_annotation(
            x=sel_x,
            y=sel_y + 4.5,
            text=f"📍 <b>{selected_ticker}</b> (Ativo Selecionado)",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowcolor="#FFFFFF",
            font=dict(size=11, color="#FFFFFF", family="JetBrains Mono"),
            bgcolor="#0B0E14",
            bordercolor="#3B82F6",
            borderwidth=1,
            borderpad=4,
        )

    # 6. Layout Institucional Dark
    fig.update_layout(
        title=dict(
            text="<b>MATRIZ MUNGER 2x2: QUALIDADE DO NEGÓCIO vs. PREÇO DE ENTRADA</b>",
            font=dict(family="Inter", size=13, color="#F8FAFC"),
            x=0.01, y=0.98,
        ),
        xaxis=dict(
            title=dict(text=x_title, font=dict(family="Inter", size=11, color="#94A3B8")),
            range=[x_min, x_max],
            gridcolor="#1E2535",
            zerolinecolor="#232B3B",
            tickfont=dict(family="JetBrains Mono", size=10, color="#64748B"),
        ),
        yaxis=dict(
            title=dict(text="Business Quality Score (0 a 100) [↑ Maior Excelência Operacional]", font=dict(family="Inter", size=11, color="#94A3B8")),
            range=[20, 105],
            gridcolor="#1E2535",
            zerolinecolor="#232B3B",
            tickfont=dict(family="JetBrains Mono", size=10, color="#64748B"),
        ),
        paper_bgcolor="#151A23",
        plot_bgcolor="#11151F",
        margin=dict(l=55, r=25, t=50, b=45),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1.0,
            font=dict(color="#CBD5E1", size=10, family="Inter"),
            bgcolor="rgba(15, 19, 28, 0.7)",
            bordercolor="#232B3B",
            borderwidth=1,
        ),
        height=580,
    )

    return fig


def main():
    if "selected_ticker" not in st.session_state:
        st.session_state.selected_ticker = None
    if "filter_mode" not in st.session_state:
        st.session_state.filter_mode = "ALL"
    if "matrix_x_metric" not in st.session_state:
        st.session_state.matrix_x_metric = "pl"

    # Top Bar Institucional
    col_hdr_left, col_hdr_right = st.columns([0.72, 0.28])

    with col_hdr_left:
        st.markdown(
            """
            <div class="jpm-title-section">
                <h1>
                    <span>🏛️ JP MORGAN</span>
                    <span style="color: #64748B; font-weight: 300;">|</span>
                    <span>MUNGER B3 TERMINAL</span>
                    <span class="jpm-badge-cfa">CFA CHARTERHOLDER RESEARCH</span>
                </h1>
                <div class="jpm-quote">
                    "É muito melhor comprar uma empresa maravilhosa a um preço justo do que uma empresa justa a um preço maravilhoso." — Charlie Munger
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    force_refresh = False
    with col_hdr_right:
        audit_placeholder = st.empty()
        btn_refresh = st.button("🔄 Atualizar Base Fundamentus", use_container_width=True)
        if btn_refresh:
            force_refresh = True
            st.cache_data.clear()

    with st.spinner("Conectando ao Fundamentus e auditando indicadores com filtros CFA..."):
        df_scored, audit_timestamp = load_and_score_universe(force_refresh=force_refresh)

    with col_hdr_right:
        audit_placeholder.markdown(
            f"""
            <div class="jpm-audit-badge">
                <div><span class="status-dot"></span><span class="label">Auditoria Ativa Fundamentus</span></div>
                <div class="timestamp">Auditado em: {audit_timestamp}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    # Barra de Filtros e Busca Rápida (5 Filtros Institucionais)
    col_filters, col_search = st.columns([0.72, 0.28])

    with col_filters:
        st.markdown("<div style='font-size: 0.75rem; color: #64748B; text-transform: uppercase; margin-bottom: 4px;'>Filtros Rápidos Institucionais CFA</div>", unsafe_allow_html=True)
        fcol1, fcol2, fcol3, fcol4, fcol5 = st.columns(5)
        with fcol1:
            if st.button("🌐 Todos", use_container_width=True):
                st.session_state.filter_mode = "ALL"
        with fcol2:
            if st.button("⭐ Tier 1 (>80)", use_container_width=True):
                st.session_state.filter_mode = "TIER1"
        with fcol3:
            if st.button("🎯 Assimetria (Score>75)", use_container_width=True):
                st.session_state.filter_mode = "ASYMMETRY"
        with fcol4:
            if st.button("📈 Spread NTN-B (>5%)", use_container_width=True):
                st.session_state.filter_mode = "NTNB_SPREAD"
        with fcol5:
            if st.button("🛡️ Caixa Líquido", use_container_width=True):
                st.session_state.filter_mode = "NET_CASH"

    with col_search:
        st.markdown("<div style='font-size: 0.75rem; color: #64748B; text-transform: uppercase; margin-bottom: 4px;'>Busca por Ticker</div>", unsafe_allow_html=True)
        search_query = st.text_input("Buscar Ticker", placeholder="Ex: WEGE3, PETR4, ITUB4...", label_visibility="collapsed").strip().upper()

    # Aplicação de Filtros
    filtered_df = df_scored.copy()

    if st.session_state.filter_mode == "TIER1":
        filtered_df = filtered_df[filtered_df["quality_score"] >= 80.0]
    elif st.session_state.filter_mode == "ASYMMETRY":
        filtered_df = filtered_df[(filtered_df["quality_score"] >= 75.0) & (filtered_df["pl"] > 0) & (filtered_df["pl"] < 8.0)]
    elif st.session_state.filter_mode == "NTNB_SPREAD":
        filtered_df = filtered_df[(filtered_df["ey_spread"].notna()) & (filtered_df["ey_spread"] >= 5.0)]
    elif st.session_state.filter_mode == "NET_CASH":
        filtered_df = filtered_df[filtered_df["is_net_cash"] == True]

    if search_query:
        filtered_df = filtered_df[filtered_df["ticker"].str.contains(search_query, na=False)]

    filtered_df = filtered_df.sort_values(by=["quality_score", "roic"], ascending=[False, False])

    # Barra de Resumo de Triagem
    st.markdown(
        f"""
        <div style="display: flex; gap: 1.5rem; align-items: center; padding: 0.5rem 0; border-bottom: 1px solid #232B3B; margin-bottom: 0.75rem; font-size: 0.8rem; color: #94A3B8;">
            <div>Ativos Qualificados: <b style="color: #F8FAFC; font-family: 'JetBrains Mono';">{len(filtered_df)}</b> / {len(df_scored)}</div>
            <div>• Filtro Ativo: <b style="color: #38BDF8;">{st.session_state.filter_mode}</b></div>
            <div>• NTN-B Benchmark: <span style="color: #F2C94C; font-family: 'JetBrains Mono';">{NTN_B_BENCHMARK}% a.a. real</span></div>
            <div>• Corte de Liquidez: <span style="color: #00D084; font-family: 'JetBrains Mono';">≥ R$ 1.000.000/dia</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Preparação da Tabela Principal para Exibição
    display_cols = [
        "ticker", "setor", "cotacao", "quality_score", "entry_status",
        "ey_spread", "pl", "ev_ebitda", "roic", "div_liq_ebitda", "div_yield", "payout_implicito"
    ]
    df_table = filtered_df[display_cols].copy()
    all_tickers = filtered_df["ticker"].tolist()

    # Layout Principal em 2 Colunas
    col_main, col_diag = st.columns([0.62, 0.38])

    with col_main:
        view_tabs = st.tabs(["📊 Matriz Munger 2x2 (Qualidade vs. Preço)", "📋 Tabela de Triagem B3 (Auditada)"])

        # ABA 1: MATRIZ 2X2 DE CHARLIE MUNGER
        with view_tabs[0]:
            mcol_ctrl1, mcol_ctrl2 = st.columns([0.60, 0.40])
            with mcol_ctrl1:
                metric_choice = st.radio(
                    "Métrica do Eixo Preço (X):",
                    options=["Preço sobre Lucro (P/L)", "Earnings Yield (1/[P/L] %)"],
                    horizontal=True,
                    label_visibility="collapsed",
                )
                x_metric_param = "pl" if "P/L" in metric_choice else "ey"
            with mcol_ctrl2:
                selected_from_dropdown = st.selectbox(
                    "Focar Ticker na Matriz:",
                    options=["-- Nenhum --"] + all_tickers,
                    index=(all_tickers.index(st.session_state.selected_ticker) + 1) if (st.session_state.selected_ticker in all_tickers) else 0,
                    label_visibility="collapsed",
                )
                if selected_from_dropdown != "-- Nenhum --" and selected_from_dropdown != st.session_state.selected_ticker:
                    st.session_state.selected_ticker = selected_from_dropdown

            fig_matrix = render_munger_2x2_matrix(
                filtered_df,
                x_metric=x_metric_param,
                selected_ticker=st.session_state.selected_ticker,
            )

            plotly_event = st.plotly_chart(
                fig_matrix,
                use_container_width=True,
                config={"displayModeBar": False},
                on_select="rerun",
                selection_mode="points",
            )

            if plotly_event and "selection" in plotly_event and plotly_event["selection"].get("points"):
                clicked_pt = plotly_event["selection"]["points"][0]
                clicked_ticker = clicked_pt.get("customdata")
                if clicked_ticker and clicked_ticker != st.session_state.selected_ticker:
                    st.session_state.selected_ticker = clicked_ticker
                    st.rerun()

            # Resumo Estatístico dos 4 Quadrantes
            q_thresh = 75.0
            p_thresh = 12.0
            valid_p = filtered_df[(filtered_df["pl"].notna()) & (filtered_df["pl"] > 0)]
            
            n_graal = len(valid_p[(valid_p["quality_score"] >= q_thresh) & (valid_p["pl"] < p_thresh)])
            n_marav = len(valid_p[(valid_p["quality_score"] >= q_thresh) & (valid_p["pl"] >= p_thresh)])
            n_traps = len(valid_p[(valid_p["quality_score"] < q_thresh) & (valid_p["pl"] < p_thresh)])
            n_perigo = len(valid_p[(valid_p["quality_score"] < q_thresh) & (valid_p["pl"] >= p_thresh)])

            st.markdown(
                f"""
                <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.5rem; margin-top: 0.75rem;">
                    <div style="background: rgba(0, 208, 132, 0.1); border: 1px solid rgba(0, 208, 132, 0.3); border-radius: 6px; padding: 0.6rem; text-align: center;">
                        <div style="font-size: 0.68rem; color: #00D084; font-weight: 600;">EXCELENTE &amp; BARATA</div>
                        <div style="font-size: 1.2rem; font-family: 'JetBrains Mono'; font-weight: 700; color: #FFFFFF;">{n_graal}</div>
                        <div style="font-size: 0.62rem; color: #94A3B8;">Alta Qualidade + Desconto</div>
                    </div>
                    <div style="background: rgba(134, 239, 172, 0.1); border: 1px solid rgba(134, 239, 172, 0.3); border-radius: 6px; padding: 0.6rem; text-align: center;">
                        <div style="font-size: 0.68rem; color: #86EFAC; font-weight: 600;">EXCELENTE / CARA</div>
                        <div style="font-size: 1.2rem; font-family: 'JetBrains Mono'; font-weight: 700; color: #FFFFFF;">{n_marav}</div>
                        <div style="font-size: 0.62rem; color: #94A3B8;">Franquia + Múltiplo Alto</div>
                    </div>
                    <div style="background: rgba(253, 186, 116, 0.1); border: 1px solid rgba(253, 186, 116, 0.3); border-radius: 6px; padding: 0.6rem; text-align: center;">
                        <div style="font-size: 0.68rem; color: #FDBA74; font-weight: 600;">MEDIANA / BARATA</div>
                        <div style="font-size: 1.2rem; font-family: 'JetBrains Mono'; font-weight: 700; color: #FFFFFF;">{n_traps}</div>
                        <div style="font-size: 0.62rem; color: #94A3B8;">Barganhas &amp; Dividendos</div>
                    </div>
                    <div style="background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.3); border-radius: 6px; padding: 0.6rem; text-align: center;">
                        <div style="font-size: 0.68rem; color: #F87171; font-weight: 600;">FRÁGIL &amp; CARA</div>
                        <div style="font-size: 1.2rem; font-family: 'JetBrains Mono'; font-weight: 700; color: #FFFFFF;">{n_perigo}</div>
                        <div style="font-size: 0.62rem; color: #94A3B8;">Sem Margem de Segurança</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # ABA 2: TABELA DE TRIAGEM B3
        with view_tabs[1]:
            st.markdown("<div style='font-size: 0.85rem; font-weight: 600; color: #F1F5F9; margin-bottom: 0.5rem;'>Tabela de Triagem B3 (Auditada & Enriquecida com Métricas CFA)</div>", unsafe_allow_html=True)

            tbl_event = st.dataframe(
                df_table,
                column_config={
                    "ticker": st.column_config.TextColumn("Ticker", width="small"),
                    "setor": st.column_config.TextColumn("Setor", width="medium"),
                    "cotacao": st.column_config.NumberColumn("Cotação", format="R$ %.2f", width="small"),
                    "quality_score": st.column_config.ProgressColumn("Quality Score", min_value=0, max_value=100, format="%.1f", width="medium"),
                    "entry_status": st.column_config.TextColumn("Status Entrada", width="medium"),
                    "ey_spread": st.column_config.NumberColumn("Spread NTN-B", format="%+.1f%%", width="small"),
                    "pl": st.column_config.NumberColumn("P/L", format="%.1f", width="small"),
                    "ev_ebitda": st.column_config.NumberColumn("EV/EBITDA", format="%.1f", width="small"),
                    "roic": st.column_config.NumberColumn("ROIC", format="%.1f%%", width="small"),
                    "div_liq_ebitda": st.column_config.NumberColumn("Dív.Líq/EBITDA", format="%.2fx", width="small"),
                    "div_yield": st.column_config.NumberColumn("DY", format="%.1f%%", width="small"),
                    "payout_implicito": st.column_config.NumberColumn("Payout", format="%.0f%%", width="small"),
                },
                hide_index=True,
                use_container_width=True,
                height=580,
                selection_mode="single-row",
                on_select="rerun",
            )

            selected_rows = tbl_event.selection.get("rows", [])
            if selected_rows:
                selected_idx = selected_rows[0]
                if selected_idx < len(df_table):
                    st.session_state.selected_ticker = df_table.iloc[selected_idx]["ticker"]

    if not st.session_state.selected_ticker and all_tickers:
        st.session_state.selected_ticker = all_tickers[0]

    current_ticker = st.session_state.selected_ticker

    # Painel de Diagnóstico Aprofundado (Coluna da Direita)
    with col_diag:
        if not current_ticker or current_ticker not in df_scored["ticker"].values:
            st.info("Selecione um ativo na tabela ou matriz para visualizar o diagnóstico institucional.")
            return

        active_stock_row = df_scored[df_scored["ticker"] == current_ticker].iloc[0].to_dict()

        with st.spinner(f"Coletando balanço completo de {current_ticker}..."):
            details = fetch_fundamentus_ticker_details(current_ticker)

        company_name = details.get("empresa") or current_ticker
        sector_name = details.get("setor") or active_stock_row.get("setor", "N/D")
        subsetor_name = details.get("subsetor") or "N/D"

        q_score_data = {
            "quality_score": active_stock_row["quality_score"],
            "quality_tier": active_stock_row["quality_tier"],
            "quality_tag": active_stock_row["quality_tag"],
            "pilar_rentabilidade": active_stock_row["pilar_rentabilidade"],
            "pilar_solidez": active_stock_row["pilar_solidez"],
            "pilar_consistencia": active_stock_row["pilar_consistencia"],
            "is_financial": active_stock_row.get("is_financial", False),
            "sub_scores": active_stock_row["sub_scores"],
        }
        valuation_data = {
            "entry_status": active_stock_row["entry_status"],
            "entry_tag": active_stock_row["entry_tag"],
            "entry_color": active_stock_row["entry_color"],
            "earnings_yield_pct": active_stock_row.get("earnings_yield_pct"),
            "ey_spread": active_stock_row.get("ey_spread"),
            "payout_implicito": (active_stock_row.get("payout_implicito") / 100.0) if active_stock_row.get("payout_implicito") is not None else None,
            "payout_tag": active_stock_row.get("payout_tag", ""),
            "is_commodity_peak": active_stock_row.get("is_commodity_peak", False),
            "is_debt_vulnerable": active_stock_row.get("is_debt_vulnerable", False),
            "capital_intensity": active_stock_row.get("capital_intensity"),
            "rationale": active_stock_row.get("rationale", ""),
        }
        cfa_bullets = generate_cfa_verdict(current_ticker, company_name, q_score_data, valuation_data, active_stock_row)

        # Header do Painel de Diagnóstico
        sector_badge = "🏦 Setor Financeiro (Modelo Bancário)" if active_stock_row.get("is_financial") else f"{sector_name} • {subsetor_name}"
        st.markdown(
            f"""
            <div class="jpm-card" style="padding: 1rem; margin-bottom: 0.75rem;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <div>
                        <div style="font-size: 1.35rem; font-weight: 700; color: #FFFFFF; font-family: 'JetBrains Mono';">{current_ticker}</div>
                        <div style="font-size: 0.85rem; color: #CBD5E1; font-weight: 500;">{company_name}</div>
                        <div style="font-size: 0.72rem; color: #64748B;">{sector_badge}</div>
                    </div>
                    <div style="text-align: right;">
                        <div class="quality-pill quality-tier1" style="font-size: 1.1rem; padding: 4px 12px;">
                            SCORE {active_stock_row['quality_score']}
                        </div>
                        <div style="font-size: 0.7rem; color: #94A3B8; margin-top: 4px;">{active_stock_row['quality_tier']}</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        diag_tabs = st.tabs(["💎 Radar & Métricas CFA", "📋 Espelho Balanço", "🏛️ Veredito CFA"])

        # BLOCO 1: RADAR DE QUALIDADE E MÉTRICAS CFA
        with diag_tabs[0]:
            st.markdown("<div class='jpm-card-title'>Pilares de Excelência Operacional (Charlie Munger)</div>", unsafe_allow_html=True)
            
            fig_radar = render_radar_chart(q_score_data)
            st.plotly_chart(fig_radar, use_container_width=True, config={"displayModeBar": False})

            # Grid de Métricas Expandido com Módulos CFA
            spread_str = f"{active_stock_row.get('ey_spread'):+.1f}%" if active_stock_row.get('ey_spread') is not None else "N/D"
            payout_str = f"{active_stock_row.get('payout_implicito'):.0f}%" if active_stock_row.get('payout_implicito') is not None else "N/D"
            cap_int = active_stock_row.get('capital_intensity')
            cap_str = f"{cap_int*100:.0f}%" if cap_int is not None else "N/D"

            st.markdown(
                f"""
                <div class="jpm-kpi-grid">
                    <div class="jpm-kpi-box">
                        <div class="jpm-kpi-label">ROIC / ROE</div>
                        <div class="jpm-kpi-value">{format_percent(active_stock_row.get('roic') or active_stock_row.get('roe'))}</div>
                        <div style="font-size: 0.65rem; color: #64748B;">Score: {q_score_data['sub_scores']['roic']:.0f}/100</div>
                    </div>
                    <div class="jpm-kpi-box">
                        <div class="jpm-kpi-label">Spread vs NTN-B</div>
                        <div class="jpm-kpi-value" style="color: {'#00D084' if (active_stock_row.get('ey_spread') or 0) >= 5.0 else ('#EB5757' if (active_stock_row.get('ey_spread') or 0) < 0 else '#F2C94C')};">{spread_str}</div>
                        <div style="font-size: 0.65rem; color: #64748B;">Ref. NTN-B: {NTN_B_BENCHMARK}%</div>
                    </div>
                    <div class="jpm-kpi-box">
                        <div class="jpm-kpi-label">Payout Implícito</div>
                        <div class="jpm-kpi-value">{payout_str}</div>
                        <div style="font-size: 0.65rem; color: #64748B;">{active_stock_row.get('payout_tag')}</div>
                    </div>
                    <div class="jpm-kpi-box">
                        <div class="jpm-kpi-label">Dív.Líq / EBITDA</div>
                        <div class="jpm-kpi-value">{format_multiple(active_stock_row.get('div_liq_ebitda')) if not active_stock_row.get('is_financial') else 'N/A (Banco)'}</div>
                        <div style="font-size: 0.65rem; color: #64748B;">Score: {q_score_data['sub_scores']['div_liq_ebitda']:.0f}/100</div>
                    </div>
                    <div class="jpm-kpi-box">
                        <div class="jpm-kpi-label">EBIT / EBITDA</div>
                        <div class="jpm-kpi-value">{cap_str}</div>
                        <div style="font-size: 0.65rem; color: #64748B;">Munger Acid Test</div>
                    </div>
                    <div class="jpm-kpi-box">
                        <div class="jpm-kpi-label">Margem Líquida</div>
                        <div class="jpm-kpi-value">{format_percent(active_stock_row.get('mrg_liq'))}</div>
                        <div style="font-size: 0.65rem; color: #64748B;">Score: {q_score_data['sub_scores']['mrg_liq']:.0f}/100</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # BLOCO 2: AUDITORIA DOS INDICADORES BRUTOS (ESPELHO FUNDAMENTUS)
        with diag_tabs[1]:
            st.markdown("<div class='jpm-card-title'>Espelho Fiel Fundamentus (Balanço & DRE)</div>", unsafe_allow_html=True)
            st.caption(f"Fonte Oficial: {details.get('audit_source')} • Balanço Processado: {details.get('ult_balanco')}")

            col_b1, col_b2 = st.columns(2)
            with col_b1:
                st.markdown("**Valuation & Múltiplos**")
                st.markdown(
                    f"""
                    - **Cotação Atual:** `{format_currency(active_stock_row.get('cotacao'))}`
                    - **Mín / Máx 52 sem:** `{format_currency(details.get('min_52sem'))}` / `{format_currency(details.get('max_52sem'))}`
                    - **Valor de Mercado:** `{format_billions(details.get('valor_mercado'))}`
                    - **Valor da Firma (EV):** `{format_billions(details.get('valor_firma'))}`
                    - **P/L Auditado:** `{format_multiple(active_stock_row.get('pl'))}`
                    - **Earnings Yield (1/[P/L]):** `{format_percent(active_stock_row.get('earnings_yield'))}`
                    - **Spread vs NTN-B:** `{spread_str}`
                    - **P/VP:** `{format_multiple(active_stock_row.get('pvp'))}`
                    - **EV/EBITDA:** `{format_multiple(active_stock_row.get('ev_ebitda'))}`
                    - **EV/EBIT:** `{format_multiple(active_stock_row.get('ev_ebit'))}`
                    - **Dividend Yield LTM:** `{format_percent(active_stock_row.get('div_yield'))}`
                    - **Payout Implícito:** `{payout_str}`
                    """
                )

            with col_b2:
                st.markdown("**Balanço Patrimonial & DRE**")
                st.markdown(
                    f"""
                    - **Ativo Total:** `{format_billions(details.get('ativo_total'))}`
                    - **Ativo Circulante:** `{format_billions(details.get('ativo_circulante'))}`
                    - **Disponibilidades (Caixa):** `{format_billions(details.get('disponibilidades'))}`
                    - **Dívida Bruta:** `{format_billions(details.get('divida_bruta'))}`
                    - **Dívida Líquida:** `{format_billions(details.get('divida_liquida'))}`
                    - **Patrimônio Líquido:** `{format_billions(details.get('patrimonio_liquido'))}`
                    - **Receita Líquida (12m):** `{format_billions(details.get('receita_liq_12m'))}`
                    - **EBIT (12m):** `{format_billions(details.get('ebit_12m'))}`
                    - **Lucro Líquido (12m):** `{format_billions(details.get('lucro_liq_12m'))}`
                    - **Margem Líquida:** `{format_percent(active_stock_row.get('mrg_liq'))}`
                    - **LPA / VPA:** `R$ {details.get('lpa') or 'N/D'}` / `R$ {details.get('vpa') or 'N/D'}`
                    """
                )

        # BLOCO 3: VEREDITO DO ANALISTA CFA
        with diag_tabs[2]:
            st.markdown("<div class='jpm-card-title'>Síntese Executiva Institucional (JP Morgan Research)</div>", unsafe_allow_html=True)
            
            st.markdown(
                f"""
                <div style="background: {active_stock_row['entry_color']}1A; border: 1px solid {active_stock_row['entry_color']}55; padding: 0.75rem 1rem; border-radius: 6px; margin-bottom: 0.75rem;">
                    <div style="font-size: 0.95rem; font-weight: 700; color: {active_stock_row['entry_color']}; font-family: 'JetBrains Mono';">
                        {active_stock_row['entry_status']}
                    </div>
                    <div style="font-size: 0.8rem; color: #CBD5E1; margin-top: 2px;">
                        {active_stock_row.get('rationale')}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Badges de Alertas Institucionais Especiais
            flags_html = ""
            if active_stock_row.get("is_commodity_peak"):
                flags_html += "<span style='background: rgba(245, 158, 11, 0.2); border: 1px solid #F59E0B; color: #FBBF24; padding: 3px 8px; border-radius: 4px; font-size: 0.72rem; font-weight: 600; margin-right: 6px;'>⚠️ ALERTA: Pico de Ciclo de Commodities</span>"
            if active_stock_row.get("is_debt_vulnerable"):
                flags_html += "<span style='background: rgba(235, 87, 87, 0.2); border: 1px solid #EB5757; color: #F87171; padding: 3px 8px; border-radius: 4px; font-size: 0.72rem; font-weight: 600; margin-right: 6px;'>⚠️ ALERTA: Vulnerabilidade a Juros Domésticos</span>"
            if (active_stock_row.get("payout_implicito") or 0) > 100:
                flags_html += "<span style='background: rgba(235, 87, 87, 0.2); border: 1px solid #EB5757; color: #F87171; padding: 3px 8px; border-radius: 4px; font-size: 0.72rem; font-weight: 600; margin-right: 6px;'>⚠️ ALERTA: Payout Insustentável (>100%)</span>"
            elif 40 <= (active_stock_row.get("payout_implicito") or 0) <= 85:
                flags_html += "<span style='background: rgba(0, 208, 132, 0.15); border: 1px solid #00D084; color: #00E699; padding: 3px 8px; border-radius: 4px; font-size: 0.72rem; font-weight: 600; margin-right: 6px;'>💎 Proventos Disciplinados</span>"

            if flags_html:
                st.markdown(f"<div style='margin-bottom: 0.85rem;'>{flags_html}</div>", unsafe_allow_html=True)

            for idx, bullet in enumerate(cfa_bullets):
                css_class = "risk" if idx == 1 else ("entry" if idx == 2 else "")
                st.markdown(
                    f"""
                    <div class="cfa-bullet-card {css_class}">
                        <div class="cfa-bullet-header">{bullet['icon']} {bullet['title']}</div>
                        <div class="cfa-bullet-body">{bullet['content']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            st.markdown(
                f"""
                <div style="font-size: 0.72rem; color: #64748B; margin-top: 1rem; border-top: 1px dashed #232B3B; padding-top: 0.5rem;">
                    <b>Metodologia CFA Institucional:</b> Referência de custo de oportunidade ancorada no Tesouro IPCA+ longo (NTN-B a {NTN_B_BENCHMARK}% a.a. de retorno real). Módulo bancário especializado com Golden Ratio P/VP x ROE. Livre de fluxos de caixa descontados perpétuos especulativos.
                </div>
                """,
                unsafe_allow_html=True,
            )


if __name__ == "__main__":
    main()
