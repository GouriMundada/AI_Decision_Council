import streamlit as st
import google.generativeai as genai

genai.configure(
    api_key=st.secrets["GEMINI_API_KEY"]
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


def ask_gemini(question):

    response = model.generate_content(
        question
    )

    return response.text

def get_agent_opinion(agent, question):

    prompt = f"""
You are {agent}.

Analyze the following question ONLY from your area of expertise.

Question:
{question}

Give:
1. Key concern
2. Recommendation

Keep answer under 100 words.
"""

    response = model.generate_content(prompt)

    return response.text

def detect_agents(question):

    question = question.lower()

    agents = []

    if any(word in question for word in [
        "hospital",
        "doctor",
        "patient",
        "medical",
        "health",
        "diagnosis"
    ]):
        agents.extend([
            "🏥 Healthcare Agent",
            "⚖️ Legal Agent",
            "🧠 Ethics Agent",
            "⚙️ Technical Agent"
        ])

    elif any(word in question for word in [
        "school",
        "college",
        "student",
        "education",
        "teacher"
    ]):
        agents.extend([
            "🎓 Education Agent",
            "🧠 Ethics Agent",
            "⚖️ Legal Agent"
        ])

    elif any(word in question for word in [
        "business",
        "company",
        "startup",
        "investment",
        "finance"
    ]):
        agents.extend([
            "💰 Finance Agent",
            "📈 Marketing Agent",
            "⚙️ Operations Agent",
            "⚖️ Legal Agent"
        ])

    elif any(word in question for word in [
        "government",
        "policy",
        "law",
        "india"
    ]):
        agents.extend([
            "🏛️ Policy Agent",
            "⚖️ Legal Agent",
            "🧠 Ethics Agent"
        ])

    else:
        agents.extend([
            "💰 Finance Agent",
            "⚖️ Legal Agent",
            "⚙️ Technical Agent"
        ])

    return agents