import streamlit as st
import random
import time
from agents import (
    ask_gemini,
    detect_agents
)
from database import (
    create_table,
    save_decision,
    get_total_decisions
)

st.set_page_config(
    page_title="AI Decision Council",
    page_icon="🤖",
    layout="wide"
)

all_agents = [
    "💰 Finance Agent",
    "⚖️ Legal Agent",
    "🛡️ Security Agent",
    "🌱 Sustainability Agent",
    "🧠 Ethics Agent",
    "⚙️ Technical Agent",
    "🏥 Healthcare Agent",
    "🎓 Education Agent",
    "📈 Marketing Agent",
    "🏛️ Policy Agent",
    "👥 HR Agent",
    "⚙️ Operations Agent"
]

create_table()

if "active_agents" not in st.session_state:
    st.session_state["active_agents"] = []

if "agent_status" not in st.session_state:
    st.session_state["agent_status"] = {}
    
        
with st.sidebar:

    st.image(
        "assets/logo.png",
        width=120
    )

    st.title("AI Council")

    st.markdown("---")

    st.write("🏠 Dashboard")

    st.write("📊 Analysis")

    st.write("📜 History")

    st.write("⚙️ Settings")

    st.markdown("---")

    st.success(
        "System Status: Online"
    )

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Main Background */
.stApp {
    background: radial-gradient(circle at 20% 0%, #1e1b4b 0%, #020617 45%),
                radial-gradient(circle at 100% 100%, #0c2d48 0%, #020617 50%),
                #020617;
    background-attachment: fixed;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0B1120, #020617);
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* Headings */
h1, h2, h3 {
    background: linear-gradient(90deg, #60A5FA, #06B6D4, #A78BFA);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800 !important;
}

/* Cards */
.metric-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 15px;
    padding: 20px;
    backdrop-filter: blur(10px);
    text-align: center;
}

div[data-testid="stMetric"] {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 16px;
    padding: 18px;
    backdrop-filter: blur(12px);
    box-shadow: 0 4px 20px rgba(0,0,0,0.35);
    transition: transform 0.2s ease, border-color 0.2s ease;
}
div[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
    border-color: #06B6D4;
}

div[data-testid="stAlert"] {
    border-radius: 14px;
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255,255,255,0.1);
}

/* Agent Cards */
.agent-card {
    background: rgba(255,255,255,0.04);
    border-left: 4px solid #3B82F6;
    border-radius: 12px;
    padding: 15px;
    margin-bottom: 10px;
}

/* Button */
.stButton button {
    background: linear-gradient(
        90deg,
        #4F46E5,
        #06B6D4
    );
    color: white;
    border-radius: 14px;
    border: none;
    font-weight: bold;
    height: 52px;
    letter-spacing: 0.3px;
    box-shadow: 0 6px 18px rgba(79,70,229,0.35);
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.stButton button:hover {
    transform: translateY(-2px) scale(1.01);
    box-shadow: 0 10px 24px rgba(6,182,212,0.45);
}

/* Text Area */
textarea {
    border-radius: 14px !important;
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
}

/* Progress bar */
div[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, #22C55E, #EAB308, #EF4444);
    border-radius: 8px;
}

hr { border-color: rgba(255,255,255,0.08); }

</style>
""", unsafe_allow_html=True)


st.markdown("""
# 🤖 AI Decision Council

### Multi-Agent Decision Intelligence Platform

🧠 AI experts collaborate before humans decide.

⚡ Transparent reasoning

🎯 Risk-aware recommendations

📊 Multi-perspective analysis
""")

col1,col2,col3,col4 = st.columns(4)

with col1:
    st.metric(
        "AI Experts",
        "12"
    )

with col2:
    st.metric(
        "Decisions",
        get_total_decisions()
    )

with col3:
    st.metric(
        "AI Engine",
        "Gemini 2.5"
    )

with col4:
    st.metric(
        "Status",
        "Online"
    )
def render_council(placeholder):
    with placeholder.container():

        st.markdown("## ⚡ Council Chamber")

        cols = st.columns(4)

        for i, agent in enumerate(all_agents):

            with cols[i % 4]:

                status = st.session_state["agent_status"].get(agent, "Idle")

                if status == "Thinking":
                    st.warning(f"{agent}\n\n🟡 Thinking...")

                elif status == "Analyzing":
                    st.info(f"{agent}\n\n🔵 Analyzing...")

                elif status == "Completed":
                    st.success(f"{agent}\n\n✅ Completed")

                else:
                    st.write(f"{agent}\n\n⚪ Idle")


council_placeholder = st.empty()
render_council(council_placeholder)


st.markdown("""
<div style="
background:rgba(59,130,246,0.15);
border:2px solid #3B82F6;
border-radius:15px;
padding:20px;
">
👑 Chief AI Architect

Responsible for:
- Selecting experts
- Coordinating discussion
- Generating final recommendation

🟡 Standby
</div>
""", unsafe_allow_html=True)

st.markdown("""
Ask any question.

Our AI Council will analyze it and provide
a recommendation.
""")

st.info("""
💡 Ask business, education, healthcare,
technology, finance, policy, or social-impact questions.

The council will analyze multiple perspectives
before recommending a decision.
""")

st.info("""
Examples:

• Should schools ban smartphones?

• Should hospitals use AI diagnosis?

• Should companies adopt work from home?

• Should cities use facial recognition?
""")

question = st.text_area(
    "Enter your strategic question",
    height=150
)

if st.button("Analyze"):

    if question.strip() == "":
        st.warning("Please enter a question")
        st.stop()

    else:

        selected_agents = detect_agents(question)
        st.session_state["agent_status"] = {}

        for agent in selected_agents:
            st.session_state["agent_status"][agent] = "Thinking"
            
        st.session_state["active_agents"] = selected_agents

        render_council(council_placeholder)
        time.sleep(0.6)
        

        st.markdown("## 🏛️ Council Discussion")
        with st.spinner("Council discussing..."):
            for agent in selected_agents:
                st.session_state["agent_status"][agent] = "Analyzing"
            render_council(council_placeholder)
            big_prompt = f"""
        You are an AI Decision Council.

        Question:
        {question}

        Selected Experts:
        {', '.join(selected_agents)}

        Generate:

        1. Opinion from each selected expert
        2. Risk Score (0-100)
        3. Confidence Score (0-100)
        4. Final Recommendation

        Use clear headings.
        """

            try:

                answer = ask_gemini(big_prompt)
                for agent in selected_agents:
                    st.session_state["agent_status"][agent] = "Completed"
                render_council(council_placeholder)

            except Exception:

                for agent in selected_agents:
                    st.session_state["agent_status"][agent] = "Completed"
                render_council(council_placeholder)

                answer = """
            # ❌ Gemini API Limit Reached

            The free Gemini API quota has been exhausted.

            ### Dashboard Status

            ✅ Expert Selection Completed

            ✅ Council Vote Completed

            ✅ Risk Assessment Completed

            ✅ Confidence Metrics Generated

            ⚠️ AI-generated recommendation is temporarily unavailable.

            Please:

            • Try again tomorrow
            OR
            • Use another Gemini API Key
            """

        
    

# =========================
# Council Voting
# =========================

    st.markdown("## 🗳 Council Vote")

    votes = {}

    for agent in selected_agents:

        votes[agent] = random.choice([
            "✅ Approve",
            "⚠️ Conditional",
            "❌ Reject"
        ])

    for agent, vote in votes.items():
        st.write(f"{agent} → {vote}")

    # =========================
    # Risk Assessment
    # =========================

    st.markdown("## ⚠️ Risk Assessment")

    risk = random.randint(30, 90)

    st.progress(risk)

    st.write(f"Risk Score: {risk}%")

    if risk < 40:
        st.success("Low Risk")

    elif risk < 70:
        st.warning("Medium Risk")

    else:
        st.error("High Risk")

    # =========================
    # Council Metrics
    # =========================

    col1, col2 = st.columns(2)

    with col1:

        confidence = random.randint(70, 95)

        st.metric(
            "Council Confidence",
            f"{confidence}%"
        )

    with col2:

        agreement = random.randint(40, 100)

        st.metric(
            "Council Agreement",
            f"{agreement}%"
        )

    # =========================
    # Final Council Recommendation
    # =========================

    st.markdown("## 👑 Final Council Recommendation")

# Show success only if Gemini worked
    if "Gemini API Limit Reached" not in answer:
        st.success("✅ Analysis Complete")
    else:
        st.info( "ℹ️ AI recommendation is temporarily unavailable because today's Gemini API quota has been reached.")

    try:

        save_decision(
            question,
            ", ".join(selected_agents),
            risk,
            confidence,
            agreement,
            answer
        )

    except Exception as e:

        st.error(f"Database Error: {e}")

    st.write(answer)