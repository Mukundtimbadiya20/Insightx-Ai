import streamlit as st
import pandas as pd
import plotly.express as px

from analytics.data_loader import load_data, INDICATORS
from analytics.trend_detector import detect_trends
from analytics.outlier_detector import detect_outliers
from analytics.correlation_analyzer import detect_correlations
from services.insight_engine import generate_insights


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="InsightX AI",
    page_icon="📊",
    layout="wide",
)


# --------------------------------------------------
# DESIGN SYSTEM (styling only - no logic)
# --------------------------------------------------

INK = "#F4F7F7"
TEAL = "#0E7C86"
SEA = "#5FB3B3"
SAND = "#12303A"
SURFACE = "#1D4650"
MUTED = "#B8CDD1"
CHART_INK = "#12303A"
CORAL = "#E4572E"
AMBER = "#F0A202"
SAGE = "#3F9E7E"

SEVERITY_COLORS = {"Low": SAGE, "Medium": AMBER, "High": CORAL}
PALETTE = [TEAL, CORAL, AMBER, "#6C5B9E", SAGE, "#2F6690", "#B5446E", "#7A8B99"]

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"], .stApp {{
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: {INK};
    }}
    .stApp {{
        background: {SAND};
    }}
    .block-container {{
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1280px;
    }}

    /* Headings */
    h1 {{
        font-weight: 800 !important;
        letter-spacing: -0.03em;
        color: {INK};
        padding-bottom: 0 !important;
    }}
    h2, h3 {{
        font-weight: 700 !important;
        letter-spacing: -0.015em;
        color: {INK};
    }}
    [data-testid="stCaptionContainer"] {{
        color: {MUTED};
    }}

    /* Title accent */
    h1 {{
        font-size: 2.8rem !important;
        border-left: 8px solid {TEAL};
        padding-left: 0.9rem !important;
        line-height: 1.1 !important;
    }}

    /* Metric cards */
    [data-testid="stMetric"] {{
        background: {SURFACE};
        border: 1px solid #3C6971;
        border-left: 5px solid {TEAL};
        border-radius: 14px;
        padding: 0.9rem 1.1rem;
        box-shadow: 0 1px 2px rgba(18,48,58,0.04);
    }}
    [data-testid="stMetricLabel"] p {{
        font-weight: 600;
        color: {MUTED};
        font-size: 0.85rem;
    }}
    [data-testid="stMetricValue"] {{
        font-weight: 800;
        color: {INK};
    }}

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 0.4rem;
        border-bottom: 2px solid #3C6971;
    }}
    .stTabs [data-baseweb="tab"] {{
        border-radius: 10px 10px 0 0;
        padding: 0.6rem 1.1rem;
        font-weight: 600;
        color: {MUTED};
    }}
    .stTabs [aria-selected="true"] {{
        color: {TEAL} !important;
        background: {SURFACE};
    }}
    .stTabs [data-baseweb="tab-highlight"] {{
        background-color: {TEAL};
        height: 3px;
    }}

    /* Sidebar */
    [data-testid="stSidebar"] {{
        background: #0D2730;
        border-right: 1px solid #3C6971;
    }}
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {{
        font-size: 1.05rem;
        color: {INK};
    }}

    /* Containers, expanders, tables */
    [data-testid="stExpander"] {{
        background: {SURFACE};
        border: 1px solid #3C6971;
        border-radius: 14px;
    }}
    [data-testid="stDataFrame"] {{
        border: 1px solid #3C6971;
        border-radius: 12px;
        overflow: hidden;
    }}
    div[data-testid="stVerticalBlockBorderWrapper"] {{
        background: {SURFACE};
        border-radius: 14px;
    }}

    /* Form controls */
    [data-baseweb="input"],
    [data-baseweb="select"],
    [data-baseweb="popover"] > div,
    [data-testid="stSlider"] {{
        color: {INK};
    }}
    [data-baseweb="input"] > div,
    [data-baseweb="select"] > div {{
        background: {SURFACE};
        border-color: #3C6971;
    }}
    [data-baseweb="input"] input,
    [data-baseweb="select"] * {{
        color: {INK} !important;
    }}

    /* Buttons */
    .stDownloadButton button {{
        background: {TEAL};
        color: #FFFFFF;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        padding: 0.55rem 1.2rem;
    }}
    .stDownloadButton button:hover {{
        background: {INK};
        color: #FFFFFF;
    }}

    /* Severity badges */
    .badge {{
        display: inline-block;
        padding: 0.15rem 0.7rem;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 700;
        color: #FFFFFF;
        margin-left: 0.5rem;
        vertical-align: middle;
    }}
    .badge-Low {{ background: {SAGE}; }}
    .badge-Medium {{ background: {AMBER}; color: {INK}; }}
    .badge-High {{ background: {CORAL}; }}

    .footer {{
        text-align: center;
        color: {MUTED};
        font-size: 0.85rem;
        padding-top: 0.4rem;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


def style_fig(fig):
    """Apply the shared chart look (presentation only)."""
    fig.update_layout(
        template="plotly_white",
        font=dict(family="Plus Jakarta Sans, sans-serif", color=CHART_INK),
        title=dict(font=dict(size=18, color=CHART_INK)),
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        margin=dict(l=20, r=20, t=60, b=20),
        legend=dict(
            bgcolor="rgba(255,255,255,0)",
            title_font=dict(size=12),
        ),
        colorway=PALETTE,
    )
    fig.update_xaxes(gridcolor="#E8EFF0", zerolinecolor="#D2E0E2")
    fig.update_yaxes(gridcolor="#E8EFF0", zerolinecolor="#D2E0E2")
    return fig


st.title("InsightX AI")
st.caption(
    "Automated Healthcare Analytics & Insight Generation Engine"
)

st.markdown(
    """
    Analyze healthcare indicators, identify significant changes,
    detect statistical outliers, and generate structured insights.
    """
)


# --------------------------------------------------
# DATA LOADING
# --------------------------------------------------

st.sidebar.header("Data Configuration")

uploaded_file = st.sidebar.file_uploader(
    "Upload healthcare CSV",
    type=["csv"],
)

try:
    if uploaded_file is not None:
        df, quality_report = load_data(uploaded_file)
    else:
        df, quality_report = load_data(
            "data/healthcare_data.csv"
        )

except (ValueError, pd.errors.ParserError, OSError) as exc:
    st.error(f"Unable to load the dataset: {exc}")
    st.stop()


# --------------------------------------------------
# DATA QUALITY
# --------------------------------------------------

st.sidebar.subheader("Data Filters")

district_options = sorted(
    df["district"].dropna().unique().tolist()
)

selected_districts = st.sidebar.multiselect(
    "Districts",
    district_options,
    default=district_options,
)

valid_months = sorted(
    df["month"].dropna().unique().tolist()
)

selected_months = st.sidebar.multiselect(
    "Months",
    valid_months,
    default=valid_months,
    format_func=lambda value: value.strftime("%Y-%m"),
)

selected_indicators = st.sidebar.multiselect(
    "Indicators",
    INDICATORS,
    default=INDICATORS,
)

st.sidebar.subheader("Detection Thresholds")

trend_threshold = st.sidebar.slider(
    "Trend change threshold (%)",
    min_value=1,
    max_value=50,
    value=10,
)

correlation_threshold = st.sidebar.slider(
    "Correlation threshold",
    min_value=0.50,
    max_value=1.00,
    value=0.70,
    step=0.05,
)


# --------------------------------------------------
# FILTER DATA
# --------------------------------------------------

filtered_df = df[
    df["district"].isin(selected_districts)
    & df["month"].isin(selected_months)
].copy()

# Keep only the selected indicators for analysis.
analysis_indicators = selected_indicators

st.subheader("Data Overview")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Observations",
    len(df),
)

col2.metric(
    "Districts",
    df["district"].nunique(),
)

col3.metric(
    "Filtered Observations",
    len(filtered_df),
)

st.dataframe(
    filtered_df[
        ["month", "district"] + analysis_indicators
    ] if analysis_indicators
    else filtered_df[["month", "district"]],
    use_container_width=True,
)


# --------------------------------------------------
# DATA QUALITY REPORT
# --------------------------------------------------

with st.expander("View Data Quality Report"):
    quality_col1, quality_col2, quality_col3 = st.columns(3)

    quality_col1.metric(
        "Duplicate Records",
        quality_report["duplicate_records"],
    )

    quality_col2.metric(
        "Invalid Months",
        quality_report["invalid_months"],
    )

    quality_col3.metric(
        "Invalid Coverage Records",
        quality_report["invalid_coverage_records"],
    )

    missing_df = pd.DataFrame(
        quality_report["missing_values"].items(),
        columns=["Column", "Missing Values"],
    )

    st.dataframe(
        missing_df,
        use_container_width=True,
    )


# --------------------------------------------------
# HANDLE EMPTY SELECTIONS
# --------------------------------------------------

if filtered_df.empty:
    st.warning("No data matches the selected filters.")
    st.stop()

if not analysis_indicators:
    st.warning("Select at least one indicator.")
    st.stop()


# --------------------------------------------------
# ANALYTICS ENGINE
# --------------------------------------------------

trends = detect_trends(
    filtered_df,
    analysis_indicators,
    threshold=trend_threshold,
)

outliers = detect_outliers(
    filtered_df,
    analysis_indicators,
)

correlation_matrix, correlations = detect_correlations(
    filtered_df,
    analysis_indicators,
    threshold=correlation_threshold,
)

insights = generate_insights(
    df=filtered_df,
    trends=trends,
    outliers=outliers,
    correlations=correlations,
    trend_threshold=trend_threshold,
)


# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------

st.subheader("Analytics Summary")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

kpi1.metric(
    "Significant Trends",
    len(trends),
)

kpi2.metric(
    "Outliers Detected",
    len(outliers),
)

kpi3.metric(
    "Strong Correlations",
    len(correlations),
)

kpi4.metric(
    "Generated Insights",
    len(insights),
)


# --------------------------------------------------
# DASHBOARD TABS
# --------------------------------------------------

overview_tab, trends_tab, outliers_tab, correlations_tab, insights_tab = (
    st.tabs(
        [
            "Overview",
            "Trend Analysis",
            "Outlier Detection",
            "Correlation Analysis",
            "Automated Insights",
        ]
    )
)


# --------------------------------------------------
# OVERVIEW
# --------------------------------------------------

with overview_tab:
    st.subheader("Healthcare Indicator Overview")

    selected_overview_indicator = st.selectbox(
        "Select indicator for overview",
        analysis_indicators,
        key="overview_indicator",
    )

    overview_fig = px.line(
        filtered_df.sort_values("month"),
        x="month",
        y=selected_overview_indicator,
        color="district",
        markers=True,
        title=f"{selected_overview_indicator} Over Time",
    )
    overview_fig.update_traces(line=dict(width=3), marker=dict(size=8))
    style_fig(overview_fig)

    st.plotly_chart(
        overview_fig,
        use_container_width=True,
    )

    st.subheader("Insight Severity Distribution")

    if not insights.empty:
        severity_counts = (
            insights["severity"]
            .value_counts()
            .reindex(
                ["Low", "Medium", "High"],
                fill_value=0,
            )
            .rename_axis("Severity")
            .reset_index(name="Count")
        )

        severity_fig = px.bar(
            severity_counts,
            x="Severity",
            y="Count",
            color="Severity",
            color_discrete_map=SEVERITY_COLORS,
            text="Count",
            title="Insights by Severity",
        )
        severity_fig.update_traces(textposition="outside")
        severity_fig.update_layout(showlegend=False)
        style_fig(severity_fig)

        st.plotly_chart(
            severity_fig,
            use_container_width=True,
        )
    else:
        st.info("No insights were generated for the selected data.")


# --------------------------------------------------
# TREND ANALYSIS
# --------------------------------------------------

with trends_tab:
    st.subheader("Significant Trend Detection")

    if trends.empty:
        st.info("No significant trends detected.")
    else:
        st.dataframe(
            trends.sort_values(
                "change_pct",
                key=lambda values: values.abs(),
                ascending=False,
            ),
            use_container_width=True,
        )

        trend_fig = px.bar(
            trends,
            x="district",
            y="change_pct",
            color="indicator",
            title="Significant Percentage Changes",
            barmode="group",
        )
        style_fig(trend_fig)

        st.plotly_chart(
            trend_fig,
            use_container_width=True,
        )


# --------------------------------------------------
# OUTLIER DETECTION
# --------------------------------------------------

with outliers_tab:
    st.subheader("IQR-Based Outlier Detection")

    if outliers.empty:
        st.info("No statistical outliers detected.")
    else:
        st.dataframe(
            outliers,
            use_container_width=True,
        )

        outlier_fig = px.scatter(
            outliers,
            x="district",
            y="value",
            color="indicator",
            hover_data=["month", "lower_bound", "upper_bound"],
            title="Detected Outlier Values",
        )
        outlier_fig.update_traces(
            marker=dict(size=14, line=dict(width=1.5, color="#FFFFFF"))
        )
        style_fig(outlier_fig)

        st.plotly_chart(
            outlier_fig,
            use_container_width=True,
        )


# --------------------------------------------------
# CORRELATION ANALYSIS
# --------------------------------------------------

with correlations_tab:
    st.subheader("Pearson Correlation Matrix")

    corr_fig = px.imshow(
        correlation_matrix,
        text_auto=".2f",
        zmin=-1,
        zmax=1,
        color_continuous_scale=[
            [0.0, CORAL],
            [0.5, "#F7F9F9"],
            [1.0, TEAL],
        ],
        title="Healthcare Indicator Correlations",
    )
    style_fig(corr_fig)

    st.plotly_chart(
        corr_fig,
        use_container_width=True,
    )

    st.caption(
        "Correlation does not imply causation. "
        "Results from small datasets may be unstable."
    )

    st.subheader("Flagged Correlations")

    if correlations.empty:
        st.info(
            "No indicator pairs meet the selected threshold."
        )
    else:
        st.dataframe(
            correlations,
            use_container_width=True,
        )


# --------------------------------------------------
# AUTOMATED INSIGHTS
# --------------------------------------------------

with insights_tab:
    st.subheader("Generated Insights")

    if insights.empty:
        st.info("No insights available.")
    else:
        selected_severities = st.multiselect(
            "Filter by severity",
            ["Low", "Medium", "High"],
            default=["Low", "Medium", "High"],
        )

        visible_insights = insights[
            insights["severity"].isin(selected_severities)
        ]

        st.dataframe(
            visible_insights,
            use_container_width=True,
        )

        st.subheader("Insight Details")

        for _, row in visible_insights.iterrows():
            with st.container(border=True):
                st.markdown(
                    f"**{row['insight_id']} — "
                    f"{row['type'].title()}**"
                    f"<span class='badge badge-{row['severity']}'>"
                    f"{row['severity']}</span>",
                    unsafe_allow_html=True,
                )

                st.write(row["explanation"])

                st.caption(
                    f"Severity: {row['severity']} | "
                    f"District: {row['district']}"
                )

        st.download_button(
            "Download Insights CSV",
            data=insights.to_csv(index=False),
            file_name="insights.csv",
            mime="text/csv",
        )


# --------------------------------------------------
# EXPORT CORRELATION MATRIX
# --------------------------------------------------

st.sidebar.subheader("Export Results")

st.sidebar.download_button(
    "Download Correlation Matrix",
    data=correlation_matrix.to_csv(),
    file_name="correlation_matrix.csv",
    mime="text/csv",
)


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.markdown(
    "<div class='footer'>InsightX AI | Statistical analytics and "
    "automated insight generation</div>",
    unsafe_allow_html=True,
)