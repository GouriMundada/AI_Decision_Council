import streamlit as st
import pandas as pd

from database import get_history, delete_decision
from reports.pdf_report import generate_pdf

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

st.image("assets/Logo1.png", width=90)

st.title("📜 Decision History")

history = get_history()

total = len(history)

high = len([r for r in history if r[2] >= 80])

medium = len([r for r in history if 50 <= r[2] < 80])

low = len([r for r in history if r[2] < 50])

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📄 Total", total)

with col2:
    st.metric("🔴 High Risk", high)

with col3:
    st.metric("🟡 Medium Risk", medium)

with col4:
    st.metric("🟢 Low Risk", low)

st.markdown("---")
df = pd.DataFrame(
    history,
    columns=[
        "id",
        "question",
        "risk",
        "experts",
        "confidence",
        "agreement",
        "result",
        "created_at"
    ]
)

st.markdown("### 🔍 Search")

csv = df.to_csv(index=False).encode("utf-8-sig")

st.download_button(
    label="📥 Download Decision History (CSV)",
    data=csv,
    file_name="decision_history.csv",
    mime="text/csv"
)

pdf = generate_pdf(history)

st.download_button(
    label="📄 Download Decision History (PDF)",
    data=pdf,
    file_name="decision_history.pdf",
    mime="application/pdf"
)

search = st.text_input(
    "Search by Question",
    placeholder="Type a question..."
)

risk_filter = st.selectbox(
    "Filter by Risk",
    ["All", "High", "Medium", "Low"]
)

expert_filter = st.selectbox(
    "Filter by Expert",
    [
        "All",
        "Legal Agent",
        "Finance Agent",
        "Technical Agent",
        "Education Agent",
        "Ethics Agent"
    ]
)

sort_option = st.selectbox(
    "Sort By",
    [
        "Latest First",
        "Oldest First",
        "Highest Risk",
        "Lowest Risk"
    ]
)

if risk_filter == "High":
    history = [row for row in history if row[2] >= 80]

elif risk_filter == "Medium":
    history = [row for row in history if 50 <= row[2] < 80]

elif risk_filter == "Low":
    history = [row for row in history if row[2] < 50]

if expert_filter != "All":
    history = [
        row for row in history
        if expert_filter.lower() in row[3].lower()
    ]

# Sorting
if sort_option == "Latest First":
    history = sorted(history, key=lambda x: x[7], reverse=True)

elif sort_option == "Oldest First":
    history = sorted(history, key=lambda x: x[7])

elif sort_option == "Highest Risk":
    history = sorted(history, key=lambda x: x[2], reverse=True)

elif sort_option == "Lowest Risk":
    history = sorted(history, key=lambda x: x[2])


if search:
    history = [
        row for row in history
        if search.lower() in row[1].lower()
    ]

for row in history:

    st.markdown("---")

    st.subheader(row[1])

    st.write("### 👥 Experts")

    experts = row[3].split(",")

    for expert in experts:
        st.markdown(f"✅ {expert.strip()}")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("⚠ Risk", row[2])

        if row[2] >= 80:
            st.error(f"🔴 High Risk ({row[2]})")
        elif row[2] >= 50:
            st.warning(f"🟡 Medium Risk ({row[2]})")
        else:
            st.success(f"🟢 Low Risk ({row[3]})")

    with col2:
        st.metric("🎯 Confidence", row[4])

    with col3:
        st.metric("🤝 Agreement", row[5])

    with st.expander("👁 View Full Decision"):

        st.markdown("### 🤖 AI Council Final Decision")
        st.success(row[6])

    st.caption(f"🗓 Decision Created: {row[7]}")
    if f"confirm_{row[0]}" not in st.session_state:
        st.session_state[f"confirm_{row[0]}"] = False

    if not st.session_state[f"confirm_{row[0]}"]:

        if st.button("🗑 Delete Decision", key=f"delete_{row[0]}"):
            st.session_state[f"confirm_{row[0]}"] = True
            st.rerun()

    else:

        st.warning("⚠️ Are you sure you want to delete this decision?")

        col_yes, col_no = st.columns(2)

        with col_yes:

            if st.button("✅ Yes", key=f"yes_{row[0]}"):

                delete_decision(row[0])

                st.success("Decision deleted successfully!")

                st.rerun()

        with col_no:

            if st.button("❌ No", key=f"no_{row[0]}"):

                st.session_state[f"confirm_{row[0]}"] = False

                st.rerun()
st.markdown("---")

st.caption(
    "🤖 AI Decision Council | Decision History Module | Version 1.0"
)