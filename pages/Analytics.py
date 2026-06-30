import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Analytics",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp {
    background: radial-gradient(circle at 20% 0%, #1e1b4b 0%, #020617 45%),
                radial-gradient(circle at 100% 100%, #0c2d48 0%, #020617 50%),
                #020617;
    background-attachment: fixed;
}
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0B1120, #020617);
    border-right: 1px solid rgba(255,255,255,0.08);
}
h1, h2, h3 {
    background: linear-gradient(90deg, #60A5FA, #06B6D4, #A78BFA);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800 !important;
}
div[data-testid="stMetric"], div[data-testid="metric-container"] {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 16px;
    padding: 18px;
    backdrop-filter: blur(12px);
    box-shadow: 0 4px 20px rgba(0,0,0,0.35);
}
div[data-testid="stAlert"] {
    border-radius: 14px;
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255,255,255,0.1);
}
</style>
""", unsafe_allow_html=True)

def get_statistics():

    conn = sqlite3.connect("data/council.db")

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            AVG(risk),
            AVG(confidence),
            AVG(agreement)
        FROM decisions
    """)

    data = cursor.fetchone()

    conn.close()

    return (
        round(data[0], 1) if data[0] else 0,
        round(data[1], 1) if data[1] else 0,
        round(data[2], 1) if data[2] else 0
    )

def load_data():

    conn = sqlite3.connect("data/council.db")

    df = pd.read_sql_query(
        "SELECT * FROM decisions",
        conn
    )

    conn.close()

    return df

def get_total_decisions():

    conn = sqlite3.connect("data/council.db")

    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM decisions"
    )

    total = cursor.fetchone()[0]

    conn.close()

    return total

st.markdown("---")
st.image("assets/Logo1.png", width=90)
st.title("📊 Decision Analytics")

st.markdown("---")

st.info("Analytics Dashboard - Real-time Decision Intelligence Dashboard")

avg_risk, avg_confidence, avg_agreement = get_statistics()
df = load_data()
col1, col2, col3, col4 = st.columns(4)

with col1:

    total = get_total_decisions()

    st.metric(
        "Total Decisions",
        total
    )
with col2:
    st.metric(
        "Average Risk",
        f"{avg_risk}%"
    )

with col3:
    st.metric(
        "Average Confidence",
        f"{avg_confidence}%"
    )

with col4:
    st.metric(
        "Average Agreement",
        f"{avg_agreement}%"
    )

st.markdown("---")

st.markdown("---")
st.subheader("📊 Decision Insights")

if not df.empty:

    col1, col2 = st.columns(2)

    with col1:

        import plotly.graph_objects as go

        gauge1, gauge2, gauge3 = st.columns(3)

        with gauge1:

            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=avg_risk,
                title={"text": "Risk"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": "red"}
                }
            ))

            st.plotly_chart(fig, use_container_width=True)

        with gauge2:

            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=avg_confidence,
                title={"text": "Confidence"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": "green"}
                }
            ))

            st.plotly_chart(fig, use_container_width=True)

        with gauge3:

            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=avg_agreement,
                title={"text": "Agreement"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": "blue"}
                }
            ))

            st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Count each expert individually

        expert_list = []

        for experts in df["experts"]:

            names = experts.split(",")

            for name in names:
                expert_list.append(name.strip())

        expert_df = pd.DataFrame(
            expert_list,
            columns=["Expert"]
        )

        expert_count = (
            expert_df["Expert"]
            .value_counts()
            .reset_index()
        )

        expert_count.columns = [
            "Expert",
            "Count"
        ]

        fig2 = px.pie(
            expert_count,
            names="Expert",
            values="Count",
            hole=0.45,
            title="Most Selected AI Experts"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

        
    st.markdown("---")

    # ===============================
    # 📈 Decision Timeline
    # ===============================

    timeline = df.copy()

    timeline["created_at"] = pd.to_datetime(
        timeline["created_at"]
    )

    timeline["Date"] = timeline["created_at"].dt.date

    timeline = (
        timeline
        .groupby("Date")
        .size()
        .reset_index(name="Total Decisions")
    )

    st.subheader("📊 Decision Summary")
     
    col1, col2, col3, col4 = st.columns(4)

    high_risk = len(df[df["risk"] >= 80])

    low_risk = len(df[df["risk"] < 80])

    most_expert = (
        df["experts"]
        .str.split(",")
        .explode()
        .str.strip()
        .mode()[0]
    )

    with col1:
        st.metric(
            "🔴 High Risk Decisions",
            high_risk
        )

    with col2:
        st.metric(
            "🟢 Low Risk Decisions",
            low_risk
        )

    with col3:
        st.metric(
            "⭐ Avg Confidence",
            f"{avg_confidence:.1f}%"
        )

    with col4:
        st.metric(
            "🏆 Most Active Expert",
            most_expert
        )



    st.markdown("---")

    st.subheader("📋 Recent Decisions")
    
    st.dataframe(
        df[
            [
                "question",
                "experts",
                "risk",
                "confidence",
                "agreement",
                "created_at"
            ]
        ],
        use_container_width=True
    )

else:

    st.info("No decisions available yet.")


st.markdown("---")

st.caption(
    "🤖 AI Decision Council | Analytics Dashboard | Version 1.0"
)