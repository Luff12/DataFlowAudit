import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

from audit import run_audit
from anomaly_detection import detect_anomalies
from pipeline_monitor import run_pipeline
from quality_score import calculate_quality_score

# =====================================================
# 1. PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="DataFlow Audit",
    page_icon="🔷",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =====================================================
# 2. PROFESSIONAL DARK THEME
# =====================================================

st.markdown(
    """
<style>

.stApp {
    background-color: #0A0F1C;
    color: #E5E7EB;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}

section[data-testid="stSidebar"] {
    background-color: #101827;
    border-right: 1px solid #263247;
}

h1, h2, h3 {
    color: #F8FAFC !important;
}

p, label {
    color: #CBD5E1;
}

/* Native Streamlit metric cards */
div[data-testid="stMetric"] {
    background: linear-gradient(145deg, #19283E, #111B2D) !important;
    border: 1px solid #293B55 !important;
    border-radius: 14px !important;
    padding: 20px !important;
    min-height: 125px;
    box-shadow: 0 5px 18px rgba(0, 0, 0, 0.15);
}

div[data-testid="stMetricLabel"] {
    color: #94A3B8 !important;
    font-size: 13px !important;
    font-weight: 600 !important;
}

div[data-testid="stMetricValue"] {
    color: #38BDF8 !important;
    font-size: 30px !important;
    font-weight: 700 !important;
}

/* Match the Streamlit top toolbar to the dark theme */
header[data-testid="stHeader"] {
    background: #0A0F1C !important;
}

div[data-testid="stToolbar"] {
    background: #0A0F1C !important;
}

.stButton > button {
    background-color: #2563EB;
    color: white;
    border: 1px solid #3B82F6;
    border-radius: 9px;
    min-height: 42px;
    font-weight: 600;
}

.stButton > button:hover {
    background-color: #1D4ED8;
    color: white;
}

div[data-testid="stDataFrame"] {
    border: 1px solid #263247;
    border-radius: 12px;
}

/* Cleaner navigation and sidebar buttons */
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1 {
    font-size: 22px;
    letter-spacing: -0.7px;
}

section[data-testid="stSidebar"] .stRadio label {
    padding: 7px 9px;
    border-radius: 8px;
}

/* Consistent chart corners */
div[data-testid="stPlotlyChart"] {
    background: #121E30;
    border: 1px solid #263B56;
    border-radius: 14px;
    padding: 8px;
}

hr {
    border-color: #263247;
}

</style>
""",
    unsafe_allow_html=True,
)


# =====================================================
# 3. DATABASE FUNCTION
# =====================================================


def get_data(table_name):

    allowed_tables = ["audit_results", "pipeline_logs", "anomaly_results"]

    if table_name not in allowed_tables:
        return pd.DataFrame()

    connection = None

    try:
        connection = sqlite3.connect("audit_database.db")

        result = pd.read_sql_query(
            f"SELECT * FROM {table_name} ORDER BY id DESC", connection
        )

        return result

    except Exception as error:
        st.error(f"Database error: {error}")
        return pd.DataFrame()

    finally:
        if connection:
            connection.close()


# =====================================================
# 4. LOAD DATA
# =====================================================

try:
    data = pd.read_csv("data/sample_data.csv")

except Exception as error:
    st.error(f"Dataset could not be loaded: {error}")
    st.stop()


audit_data = get_data("audit_results")
pipeline_data = get_data("pipeline_logs")
anomaly_data = get_data("anomaly_results")

quality = calculate_quality_score(data)


# =====================================================
# 5. CALCULATE DATA QUALITY METRICS
# =====================================================

total_records = len(data)

missing_values = int(data.isnull().sum().sum())

duplicate_records = int(data.duplicated().sum())

negative_amounts = 0

if "amount" in data.columns:
    negative_amounts = int((data["amount"] < 0).sum())

invalid_ids = 0

if "order_id" in data.columns:
    invalid_ids = int((data["order_id"] <= 0).sum())


# =====================================================
# 6. CALCULATE AI METRICS
# =====================================================

total_anomalies = 0
normal_transactions = 0

if not anomaly_data.empty:

    if "status" in anomaly_data.columns:

        total_anomalies = int((anomaly_data["status"] == "Anomaly").sum())

        normal_transactions = int((anomaly_data["status"] == "Normal").sum())


# =====================================================
# 7. REUSABLE KPI CARD
# =====================================================


def show_kpi(icon, label, value, note):
    """
    Display one professional KPI card.

    Streamlit's native metric component keeps the label and value
    together inside the card. The note is kept as a tooltip.
    """

    st.metric(label=f"{icon}  {label}", value=value, help=note, border=True)


# =====================================================
# 8. CHART DESIGN
# =====================================================


def style_chart(fig, height=350):

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#121E30",
        plot_bgcolor="#121E30",
        font=dict(family="Arial", color="#CBD5E1", size=12),
        title_font=dict(size=17, color="#F8FAFC"),
        margin=dict(l=20, r=20, t=55, b=25),
        height=height,
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#CBD5E1")),
    )

    return fig


# =====================================================
# 9. SIDEBAR
# =====================================================

with st.sidebar:

    # Professional brand identity (native Streamlit elements)

    st.markdown("# ◈ DataFlow Audit")
    st.caption("AI-POWERED DATA OBSERVABILITY")

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "Overview",
            "Data Quality",
            "AI Anomalies",
            "Pipeline Monitoring",
            "Audit History",
        ],
        label_visibility="collapsed",
    )

    st.divider()

    st.caption("QUICK ACTIONS")

    # Run data audit

    if st.button("🔍 Run Data Audit", use_container_width=True):

        with st.spinner("Analyzing dataset..."):

            run_audit()

        st.success("Data audit completed!")

        st.rerun()

    # Run AI detection

    if st.button("🤖 Run AI Detection", use_container_width=True):

        with st.spinner("Detecting unusual transactions..."):

            detect_anomalies()

        st.success("AI detection completed!")

        st.rerun()

    # Run pipeline

    if st.button("🚀 Run Pipeline", use_container_width=True):

        with st.spinner("Executing pipeline..."):

            run_pipeline()

        st.success("Pipeline completed!")

        st.rerun()

    # Refresh dashboard

    if st.button("🔄 Refresh Dashboard", use_container_width=True):

        st.rerun()

    st.divider()

    st.caption("DATAFLOW AUDIT")
    st.caption("AI DATA QUALITY PLATFORM")
    st.caption("PROJECT VERSION 1.0")


# =====================================================
# 10. MAIN HEADER
# =====================================================

header_col1, header_col2 = st.columns([4, 1])

with header_col1:

    st.title(page)

    st.caption("Data quality intelligence | Anomaly detection | Pipeline monitoring")

with header_col2:

    if total_records > 0:
        st.success("DATASET LOADED")
    else:
        st.warning("DATASET EMPTY")

# Compact operational status row. These are based on current data,
# not a claim that a scheduled production monitor is running.
status_col1, status_col2, status_col3 = st.columns(3)

with status_col1:
    if (
        missing_values == 0
        and duplicate_records == 0
        and negative_amounts == 0
        and invalid_ids == 0
    ):
        st.success("Data checks: no basic issues")
    else:
        st.warning("Data checks: issues detected")

with status_col2:
    if not pipeline_data.empty and "status" in pipeline_data.columns:
        latest_status = str(pipeline_data.iloc[0]["status"])
        if latest_status == "SUCCESS":
            st.success("Latest pipeline: SUCCESS")
        else:
            st.error("Latest pipeline: FAILED")
    else:
        st.info("Pipeline: no run recorded")

with status_col3:
    if total_anomalies > 0:
        st.warning(f"AI findings: {total_anomalies} anomalies")
    elif not anomaly_data.empty:
        st.success("AI findings: no anomalies")
    else:
        st.info("AI detection: not run yet")

st.divider()


# =====================================================
# 11. OVERVIEW PAGE
# =====================================================

if page == "Overview":

    st.subheader("Platform Overview")

    st.caption("A quick overview of your dataset health and monitoring results.")

    # First KPI row

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        show_kpi(
            "📁", "TOTAL RECORDS", f"{total_records:,}", "Records in current dataset"
        )

    with col2:
        show_kpi(
            "🎯",
            "QUALITY SCORE",
            f"{quality['overall_score']:.1f}%",
            "Overall estimated quality",
        )

    with col3:
        show_kpi("⚠️", "MISSING VALUES", f"{missing_values:,}", "Empty dataset cells")

    with col4:
        show_kpi(
            "🤖",
            "AI ANOMALIES",
            f"{total_anomalies:,}",
            "Unusual transactions detected",
        )

    st.write("")

    # Second KPI row

    col5, col6, col7 = st.columns(3)

    with col5:
        show_kpi("📑", "DUPLICATE ROWS", duplicate_records, "Repeated records")

    with col6:
        show_kpi(
            "💸", "NEGATIVE AMOUNTS", negative_amounts, "Invalid transaction amounts"
        )

    with col7:
        show_kpi("🆔", "INVALID ORDER IDs", invalid_ids, "Invalid order identifiers")

    st.divider()

    # Quality chart and AI chart

    left, right = st.columns([1.5, 1])

    with left:

        st.subheader("Data Quality Scorecard")

        score_data = pd.DataFrame(
            {
                "Dimension": [
                    "Completeness",
                    "Uniqueness",
                    "Validity",
                    "Consistency",
                    "Accuracy",
                ],
                "Score": [
                    quality["completeness"],
                    quality["uniqueness"],
                    quality["validity"],
                    quality["consistency"],
                    quality["accuracy"],
                ],
            }
        )

        fig = px.bar(
            score_data,
            x="Score",
            y="Dimension",
            orientation="h",
            text="Score",
            range_x=[0, 110],
        )

        fig.update_traces(
            marker_color="#38BDF8", texttemplate="%{text:.1f}%", textposition="outside"
        )

        fig.update_layout(
            xaxis_title="Quality Score (%)", yaxis_title="", showlegend=False
        )

        fig.update_xaxes(gridcolor="#263B56")

        fig.update_yaxes(categoryorder="total ascending")

        st.plotly_chart(style_chart(fig, 340), use_container_width=True)

    with right:

        st.subheader("AI Detection Summary")

        chart_data = pd.DataFrame(
            {
                "Type": ["Normal", "Anomaly"],
                "Count": [normal_transactions, total_anomalies],
            }
        )

        fig = px.pie(
            chart_data,
            names="Type",
            values="Count",
            hole=0.65,
            color="Type",
            color_discrete_map={"Normal": "#10B981", "Anomaly": "#F97316"},
        )

        st.plotly_chart(style_chart(fig, 340), use_container_width=True)

    st.divider()

    st.subheader("Recent Dataset Records")

    st.dataframe(data.head(10), use_container_width=True, hide_index=True)


# =====================================================
# 12. DATA QUALITY PAGE
# =====================================================

elif page == "Data Quality":

    st.title("🔍 Data Quality Analysis")

    st.caption("Measure the reliability and condition of your dataset.")

    col1, col2 = st.columns(2)

    with col1:
        show_kpi(
            "🎯",
            "OVERALL QUALITY",
            f"{quality['overall_score']:.1f}%",
            "Average of five quality dimensions",
        )

    with col2:
        show_kpi("⚠️", "MISSING VALUES", missing_values, "Total empty cells")

    st.divider()

    st.subheader("Quality Dimensions")

    dimensions = [
        ("Completeness", quality["completeness"]),
        ("Uniqueness", quality["uniqueness"]),
        ("Validity", quality["validity"]),
        ("Consistency", quality["consistency"]),
        ("Accuracy", quality["accuracy"]),
    ]

    for name, score in dimensions:

        st.write(f"**{name} — {score:.1f}%**")

        st.progress(min(max(float(score) / 100, 0), 1))

    st.divider()

    st.subheader("Missing Values by Column")

    missing_data = pd.DataFrame(
        {"Column": data.columns, "Missing Values": data.isnull().sum().values}
    )

    fig = px.bar(missing_data, x="Column", y="Missing Values", text="Missing Values")

    fig.update_traces(marker_color="#38BDF8")

    st.plotly_chart(style_chart(fig), use_container_width=True)

    st.subheader("Full Dataset")

    st.dataframe(data, use_container_width=True, hide_index=True)


# =====================================================
# 13. AI ANOMALY PAGE
# =====================================================

elif page == "AI Anomalies":

    st.title("🤖 AI Anomaly Intelligence")

    st.caption("Identify unusual transaction patterns using Isolation Forest.")

    if anomaly_data.empty:

        st.info(
            "No anomaly results are available yet. "
            "Use Run AI Detection in the sidebar."
        )

    else:

        col1, col2, col3 = st.columns(3)

        with col1:
            show_kpi(
                "📊",
                "TOTAL ANALYZED",
                len(anomaly_data),
                "Transactions in latest model results",
            )

        with col2:
            show_kpi(
                "🚨", "ANOMALIES", total_anomalies, "Transactions flagged as unusual"
            )

        with col3:
            show_kpi(
                "✅", "NORMAL", normal_transactions, "Transactions classified as normal"
            )

        st.divider()

        st.subheader("Transaction Distribution")

        chart_data = pd.DataFrame(
            {
                "Transaction": ["Normal", "Anomaly"],
                "Count": [normal_transactions, total_anomalies],
            }
        )

        fig = px.pie(
            chart_data,
            names="Transaction",
            values="Count",
            hole=0.6,
            color="Transaction",
            color_discrete_map={"Normal": "#10B981", "Anomaly": "#F97316"},
        )

        st.plotly_chart(style_chart(fig), use_container_width=True)

        st.divider()

        st.subheader("🚨 Unusual Transactions")

        if "status" in anomaly_data.columns:

            unusual_data = anomaly_data[anomaly_data["status"] == "Anomaly"]

            if unusual_data.empty:

                st.success("No unusual transactions were found.")

            else:

                st.dataframe(unusual_data, use_container_width=True, hide_index=True)

        st.subheader("Complete AI Results")

        st.dataframe(anomaly_data, use_container_width=True, hide_index=True)


# =====================================================
# 14. PIPELINE MONITORING PAGE
# =====================================================

elif page == "Pipeline Monitoring":

    st.title("🚀 Pipeline Monitoring")

    st.caption("Track pipeline executions, processing time, and failures.")

    if pipeline_data.empty:

        st.info("No pipeline logs available. " "Run the pipeline using the sidebar.")

    else:

        total_runs = len(pipeline_data)

        successful_runs = int((pipeline_data["status"] == "SUCCESS").sum())

        failed_runs = int((pipeline_data["status"] == "FAILED").sum())

        col1, col2, col3 = st.columns(3)

        with col1:
            show_kpi("🔄", "TOTAL RUNS", total_runs, "Recorded executions")

        with col2:
            show_kpi("✅", "SUCCESSFUL RUNS", successful_runs, "Completed successfully")

        with col3:
            show_kpi("❌", "FAILED RUNS", failed_runs, "Failed executions")

        st.divider()

        left, right = st.columns(2)

        with left:

            st.subheader("Execution Status")

            status_data = pipeline_data["status"].value_counts().reset_index()

            status_data.columns = ["Status", "Count"]

            fig = px.pie(
                status_data,
                names="Status",
                values="Count",
                hole=0.55,
                color="Status",
                color_discrete_map={"SUCCESS": "#10B981", "FAILED": "#EF4444"},
            )

            st.plotly_chart(style_chart(fig), use_container_width=True)

        with right:

            st.subheader("Execution Time")

            if "execution_time" in pipeline_data.columns:

                fig = px.line(pipeline_data, y="execution_time", markers=True)

                fig.update_traces(line_color="#38BDF8", marker_color="#38BDF8")

                fig.update_layout(
                    xaxis_title="Execution Number", yaxis_title="Time (seconds)"
                )

                st.plotly_chart(style_chart(fig), use_container_width=True)

        st.divider()

        st.subheader("Pipeline Execution Logs")

        st.dataframe(pipeline_data, use_container_width=True, hide_index=True)


# =====================================================
# 15. AUDIT HISTORY PAGE
# =====================================================

elif page == "Audit History":

    st.title("📋 Audit History")

    st.caption("Review data quality issues detected during previous audits.")

    if audit_data.empty:

        st.info("No audit history found. " "Run Data Audit from the sidebar.")

    else:

        col1, col2 = st.columns(2)

        with col1:
            show_kpi("📋", "AUDIT ENTRIES", len(audit_data), "Stored audit findings")

        with col2:

            issue_types = (
                audit_data["issue"].nunique() if "issue" in audit_data.columns else 0
            )

            show_kpi("🔎", "ISSUE TYPES", issue_types, "Different types of findings")

        st.divider()

        st.subheader("Audit History Table")

        st.dataframe(audit_data, use_container_width=True, hide_index=True)

        if "issue" in audit_data.columns and "count" in audit_data.columns:

            st.subheader("Issues by Category")

            issue_counts = audit_data.groupby("issue")["count"].sum().reset_index()

            fig = px.bar(issue_counts, x="issue", y="count", text="count")

            fig.update_traces(marker_color="#A78BFA")

            fig.update_layout(xaxis_title="Issue Type", yaxis_title="Number of Issues")

            st.plotly_chart(style_chart(fig), use_container_width=True)


# =====================================================
# 16. FOOTER
# =====================================================

st.divider()

st.caption("🔷 DATAFLOW AUDIT | Intelligent Data Quality & Pipeline Monitoring")

st.caption("Built with Python | Streamlit | Machine Learning | SQLite")
