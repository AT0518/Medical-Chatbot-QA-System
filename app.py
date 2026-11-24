import os
import re

import streamlit as st
from src_code.utils import format_patient_response

# Bridge Streamlit secrets to environment variables (useful on Streamlit Cloud).
try:
    for _key, _value in st.secrets.items():
        if isinstance(_value, str) and _key and _key not in os.environ:
            os.environ[_key] = _value
except Exception:
    pass

st.set_page_config(
    page_title="Medical Chatbot QA System",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Sora:wght@600;700;800&display=swap');

        :root {
            --navy: #0b2a4a;
            --navy-soft: #123b63;
            --teal: #0f766e;
            --teal-bright: #14b8a6;
            --blue: #2563eb;
            --sky: #38bdf8;
            --ink: #10233d;
            --muted: #5b6f86;
            --line: rgba(148, 163, 184, 0.28);
            --surface: rgba(255, 255, 255, 0.82);
            --surface-strong: #ffffff;
            --soft: #f3f8ff;
            --success: #10b981;
            --shadow-sm: 0 10px 30px rgba(15, 23, 42, 0.08);
            --shadow-md: 0 18px 45px rgba(15, 23, 42, 0.12);
        }

        html, body, [class*="st-"], [data-testid="stAppViewContainer"], [data-testid="stSidebar"] {
            font-family: 'Manrope', sans-serif;
            color: var(--ink);
        }

        h1, h2, h3, .workspace-title, .brand-name, .welcome h1 {
            font-family: 'Sora', 'Manrope', sans-serif;
        }

        .stApp {
            background:
                radial-gradient(900px circle at 8% -10%, rgba(56, 189, 248, 0.18), transparent 45%),
                radial-gradient(700px circle at 92% 0%, rgba(20, 184, 166, 0.16), transparent 40%),
                radial-gradient(700px circle at 50% 110%, rgba(37, 99, 235, 0.12), transparent 45%),
                linear-gradient(180deg, #f8fbff 0%, #eef5fb 45%, #f7fbff 100%);
            background-attachment: fixed;
        }

        .stApp::before,
        .stApp::after {
            content: "";
            position: fixed;
            border-radius: 999px;
            filter: blur(40px);
            opacity: 0.35;
            z-index: 0;
            pointer-events: none;
            animation: floatOrb 14s ease-in-out infinite;
        }

        .stApp::before {
            width: 320px;
            height: 320px;
            top: 8%;
            right: 6%;
            background: rgba(20, 184, 166, 0.22);
        }

        .stApp::after {
            width: 260px;
            height: 260px;
            bottom: 10%;
            left: 4%;
            background: rgba(37, 99, 235, 0.18);
            animation-delay: -6s;
        }

        @keyframes floatOrb {
            0%, 100% { transform: translate3d(0, 0, 0) scale(1); }
            50% { transform: translate3d(0, -18px, 0) scale(1.04); }
        }

        [data-testid="stAppViewContainer"] > .main {
            position: relative;
            z-index: 1;
        }

        [data-testid="stHeader"] {
            background: transparent;
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(255,255,255,0.96) 0%, rgba(246,250,255,0.98) 100%);
            border-right: 1px solid var(--line);
            backdrop-filter: blur(10px);
        }

        [data-testid="stSidebar"] > div:first-child {
            padding-top: 1.1rem;
        }

        .block-container {
            max-width: 1240px;
            padding-top: 1.4rem;
            padding-bottom: 6rem;
        }

        .brand {
            display: flex;
            align-items: center;
            gap: 0.85rem;
            padding: 0.2rem 0.2rem 1.2rem;
            margin-bottom: 0.35rem;
            border-bottom: 1px solid var(--line);
        }

        .brand-mark {
            width: 48px;
            height: 48px;
            display: grid;
            place-items: center;
            border-radius: 16px;
            background: linear-gradient(135deg, var(--navy), var(--teal));
            color: white;
            font-size: 1.35rem;
            box-shadow: 0 12px 28px rgba(15, 118, 110, 0.28);
            animation: pulseSoft 3s ease-in-out infinite;
        }

        @keyframes pulseSoft {
            0%, 100% { transform: scale(1); box-shadow: 0 12px 28px rgba(15, 118, 110, 0.28); }
            50% { transform: scale(1.03); box-shadow: 0 16px 34px rgba(37, 99, 235, 0.22); }
        }

        .brand-name {
            color: var(--navy);
            font-size: 1.02rem;
            font-weight: 800;
            line-height: 1.2;
            letter-spacing: -0.02em;
        }

        .brand-subtitle {
            color: var(--muted);
            font-size: 0.76rem;
            margin-top: 0.18rem;
            font-weight: 600;
        }

        .workspace-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            margin-bottom: 1.35rem;
            padding: 1.3rem 1.45rem;
            border: 1px solid rgba(255,255,255,0.7);
            border-radius: 24px;
            background: linear-gradient(135deg, rgba(255,255,255,0.88), rgba(241,248,255,0.78));
            box-shadow: var(--shadow-sm);
            backdrop-filter: blur(14px);
            animation: fadeSlideDown 0.6s ease-out both;
            position: relative;
            overflow: hidden;
        }

        .workspace-header::after {
            content: "";
            position: absolute;
            inset: 0;
            background: linear-gradient(110deg, transparent 20%, rgba(255,255,255,0.35) 50%, transparent 80%);
            transform: translateX(-120%);
            animation: sheen 8s ease-in-out infinite;
            pointer-events: none;
        }

        @keyframes sheen {
            0%, 70%, 100% { transform: translateX(-120%); }
            35% { transform: translateX(120%); }
        }

        @keyframes fadeSlideDown {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .workspace-kicker {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            color: var(--teal);
            font-size: 0.72rem;
            font-weight: 800;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            margin-bottom: 0.35rem;
        }

        .workspace-title {
            color: var(--navy);
            font-size: clamp(1.45rem, 2.2vw, 2rem);
            font-weight: 800;
            letter-spacing: -0.04em;
            line-height: 1.1;
        }

        .workspace-caption {
            color: var(--muted);
            font-size: 0.95rem;
            margin-top: 0.4rem;
            line-height: 1.5;
        }

        .status-pill {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.55rem 0.9rem;
            border: 1px solid rgba(16, 185, 129, 0.2);
            border-radius: 999px;
            background: rgba(236, 253, 245, 0.9);
            color: #047857;
            font-size: 0.78rem;
            font-weight: 700;
            white-space: nowrap;
            box-shadow: 0 6px 18px rgba(16, 185, 129, 0.12);
        }

        .status-dot {
            width: 9px;
            height: 9px;
            border-radius: 50%;
            background: var(--success);
            box-shadow: 0 0 0 rgba(16, 185, 129, 0.5);
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.45); }
            70% { box-shadow: 0 0 0 8px rgba(16, 185, 129, 0); }
            100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
        }

        .welcome {
            max-width: 860px;
            margin: 2.2rem auto 2.1rem;
            text-align: center;
            animation: rise 0.7s ease-out both;
        }

        @keyframes rise {
            from { opacity: 0; transform: translateY(16px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .welcome-icon-wrap {
            position: relative;
            width: 84px;
            height: 84px;
            margin: 0 auto 1rem;
        }

        .welcome-icon-glow {
            position: absolute;
            inset: 0;
            border-radius: 28px;
            background: linear-gradient(135deg, rgba(56,189,248,0.35), rgba(20,184,166,0.35));
            filter: blur(14px);
            animation: glow 3.5s ease-in-out infinite;
        }

        @keyframes glow {
            0%, 100% { opacity: 0.55; transform: scale(0.95); }
            50% { opacity: 0.9; transform: scale(1.05); }
        }

        .welcome-icon {
            position: relative;
            width: 84px;
            height: 84px;
            display: grid;
            place-items: center;
            border-radius: 26px;
            background: linear-gradient(145deg, #ffffff, #e9f7f5);
            border: 1px solid rgba(20, 184, 166, 0.18);
            font-size: 2rem;
            box-shadow: 0 18px 40px rgba(15, 118, 110, 0.14);
        }

        .welcome-eyebrow {
            display: inline-flex;
            padding: 0.35rem 0.75rem;
            margin-bottom: 0.8rem;
            border-radius: 999px;
            background: rgba(37, 99, 235, 0.08);
            color: var(--blue);
            font-size: 0.73rem;
            font-weight: 800;
            letter-spacing: 0.12em;
            text-transform: uppercase;
        }

        .welcome h1 {
            color: var(--navy);
            font-size: clamp(2rem, 3.2vw, 2.8rem);
            line-height: 1.08;
            letter-spacing: -0.045em;
            margin: 0;
        }

        .welcome p {
            max-width: 640px;
            margin: 0.85rem auto 0;
            color: var(--muted);
            font-size: 1.02rem;
            line-height: 1.7;
        }

        .suggestions {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 1rem;
            max-width: 980px;
            margin: 0 auto;
        }

        .suggestion-card {
            min-height: 138px;
            padding: 1.2rem 1.2rem 1.15rem;
            border: 1px solid rgba(255,255,255,0.7);
            border-radius: 20px;
            background: linear-gradient(180deg, rgba(255,255,255,0.92), rgba(248,251,255,0.86));
            color: var(--ink);
            box-shadow: var(--shadow-sm);
            backdrop-filter: blur(10px);
            transition: transform 220ms ease, border-color 220ms ease, box-shadow 220ms ease;
            position: relative;
            overflow: hidden;
            animation: cardIn 0.6s ease-out both;
        }

        .suggestion-card:nth-child(1) { animation-delay: 0.05s; }
        .suggestion-card:nth-child(2) { animation-delay: 0.12s; }
        .suggestion-card:nth-child(3) { animation-delay: 0.19s; }

        @keyframes cardIn {
            from { opacity: 0; transform: translateY(14px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .suggestion-card::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--teal-bright), var(--blue), var(--sky));
            opacity: 0.85;
        }

        .suggestion-card:hover {
            transform: translateY(-5px);
            border-color: rgba(56, 189, 248, 0.35);
            box-shadow: var(--shadow-md);
        }

        .suggestion-label {
            color: var(--teal);
            font-size: 0.72rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.1em;
        }

        .suggestion-text {
            margin-top: 0.55rem;
            font-size: 0.92rem;
            line-height: 1.55;
            color: var(--navy-soft);
            font-weight: 600;
        }

        [data-testid="stChatMessage"] {
            border: 1px solid var(--line);
            border-radius: 20px;
            background: rgba(255, 255, 255, 0.88);
            color: var(--ink);
            margin: 0.85rem 0;
            padding: 1rem 1.15rem;
            box-shadow: var(--shadow-sm);
            backdrop-filter: blur(10px);
            animation: messageIn 0.35s ease-out both;
        }

        @keyframes messageIn {
            from { opacity: 0; transform: translateY(8px); }
            to { opacity: 1; transform: translateY(0); }
        }

        [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
            background: linear-gradient(135deg, rgba(239,246,255,0.95), rgba(255,255,255,0.95));
            border-left: 4px solid var(--blue);
        }

        [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
            background: linear-gradient(180deg, rgba(255,255,255,0.96), rgba(248,252,255,0.92));
            border-left: 4px solid var(--teal-bright);
        }

        [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] {
            color: var(--ink);
            font-size: 0.98rem;
            line-height: 1.7;
        }

        [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p {
            margin-bottom: 0.7rem;
        }

        [data-testid="stChatMessage"] h1,
        [data-testid="stChatMessage"] h2,
        [data-testid="stChatMessage"] h3 {
            color: var(--navy);
            font-weight: 800;
            letter-spacing: -0.02em;
            line-height: 1.25;
        }

        [data-testid="stChatMessage"] h2 {
            margin: 1.1rem 0 0.55rem;
            padding: 0.55rem 0.85rem;
            border-radius: 14px;
            background: linear-gradient(90deg, rgba(20,184,166,0.12), rgba(37,99,235,0.06));
            border: 1px solid rgba(20,184,166,0.18);
            font-size: 1.18rem;
        }

        [data-testid="stChatMessage"] h3 {
            margin: 1rem 0 0.45rem;
            padding: 0.45rem 0.75rem;
            border-left: 4px solid var(--teal-bright);
            border-radius: 0 12px 12px 0;
            background: rgba(240, 253, 250, 0.8);
            font-size: 1.08rem;
        }

        [data-testid="stChatMessage"] h2:first-child,
        [data-testid="stChatMessage"] h3:first-child {
            margin-top: 0.15rem;
        }

        [data-testid="stChatMessage"] ul {
            margin: 0.35rem 0 0.8rem;
            padding-left: 1.2rem;
        }

        [data-testid="stChatMessage"] li {
            margin: 0.45rem 0;
            padding: 0.2rem 0.1rem 0.2rem 0.15rem;
            line-height: 1.65;
            color: #1e3a5f;
        }

        [data-testid="stChatMessage"] li::marker {
            color: var(--teal-bright);
        }

        [data-testid="stChatMessage"] li strong {
            color: var(--navy);
            font-weight: 800;
        }

        [data-testid="stChatMessage"] hr {
            border: none;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(148,163,184,0.45), transparent);
            margin: 1rem 0;
        }

        [data-testid="stChatMessage"] code {
            background: rgba(15, 118, 110, 0.08);
            color: var(--teal);
            padding: 0.12rem 0.35rem;
            border-radius: 6px;
            font-size: 0.92em;
        }

        [data-testid="stChatInput"] {
            border: 1px solid rgba(148, 163, 184, 0.35);
            border-radius: 18px;
            background: rgba(255, 255, 255, 0.94);
            box-shadow: 0 12px 30px rgba(15, 23, 42, 0.1);
            backdrop-filter: blur(10px);
            transition: border-color 180ms ease, box-shadow 180ms ease, transform 180ms ease;
        }

        [data-testid="stChatInput"]:focus-within {
            border-color: rgba(20, 184, 166, 0.55);
            box-shadow: 0 0 0 4px rgba(20, 184, 166, 0.12), 0 14px 34px rgba(15, 23, 42, 0.12);
            transform: translateY(-1px);
        }

        [data-testid="stChatInput"] textarea {
            color: var(--ink);
            caret-color: var(--teal);
            font-size: 0.98rem;
        }

        [data-testid="stChatInput"] textarea::placeholder {
            color: #6b7f95;
            opacity: 1;
        }

        [data-testid="stBottom"] {
            background: linear-gradient(180deg, rgba(247,251,255,0.72), rgba(247,251,255,0.96));
            border-top: 1px solid var(--line);
            backdrop-filter: blur(8px);
        }

        [data-testid="stMetric"] {
            padding: 0.85rem 0.95rem;
            border: 1px solid var(--line);
            border-radius: 16px;
            background: rgba(255,255,255,0.9);
            box-shadow: 0 8px 20px rgba(15, 23, 42, 0.05);
            transition: transform 180ms ease, box-shadow 180ms ease;
        }

        [data-testid="stMetric"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 24px rgba(15, 23, 42, 0.08);
        }

        [data-testid="stMetricLabel"] p {
            color: var(--muted);
            font-weight: 700;
            font-size: 0.82rem;
        }

        [data-testid="stMetricValue"] {
            color: var(--navy);
            font-family: 'Sora', 'Manrope', sans-serif;
        }

        [data-testid="stCaptionContainer"], .stCaption {
            color: var(--muted);
        }

        .sidebar-section {
            color: var(--teal);
            font-size: 0.7rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            margin: 1.3rem 0 0.55rem;
        }

        .sidebar-note {
            padding: 0.9rem 0.95rem;
            border-radius: 14px;
            background: linear-gradient(180deg, rgba(240,249,255,0.95), rgba(236,253,245,0.85));
            border: 1px solid rgba(20, 184, 166, 0.18);
            color: #35546f;
            font-size: 0.78rem;
            line-height: 1.6;
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.6);
        }

        [data-testid="stButton"] button {
            border-radius: 12px;
            border: 1px solid rgba(148, 163, 184, 0.35);
            background: linear-gradient(180deg, #ffffff, #f8fbff);
            color: var(--navy);
            font-weight: 700;
            padding: 0.55rem 0.9rem;
            transition: all 180ms ease;
            box-shadow: 0 4px 12px rgba(15, 23, 42, 0.04);
        }

        [data-testid="stButton"] button:hover {
            border-color: rgba(20, 184, 166, 0.45);
            background: linear-gradient(180deg, #f0fdfa, #eff6ff);
            color: var(--teal);
            transform: translateY(-1px);
            box-shadow: 0 10px 20px rgba(15, 118, 110, 0.12);
        }

        [data-testid="stButton"] button:active {
            transform: translateY(0);
        }

        @media (max-width: 900px) {
            .suggestions { grid-template-columns: 1fr; }
        }

        @media (max-width: 780px) {
            .block-container { padding-left: 1rem; padding-right: 1rem; }
            .workspace-header { align-items: flex-start; flex-direction: column; padding: 1.1rem; }
            .status-pill { align-self: flex-start; }
            .welcome { margin-top: 1.6rem; }
            .welcome-icon-wrap, .welcome-icon { width: 72px; height: 72px; }
        }

        @media (prefers-reduced-motion: reduce) {
            *, *::before, *::after {
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown(
        """
        <div class="brand">
            <div class="brand-mark">?</div>
            <div>
                <div class="brand-name">Medical Chatbot QA System</div>
                <div class="brand-subtitle">Clinical RAG intelligence workspace</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="sidebar-section">Workspace</div>', unsafe_allow_html=True)
    st.caption("Retrieval-grounded medical document question answering")

    st.markdown('<div class="sidebar-section">Retrieval settings</div>', unsafe_allow_html=True)
    st.metric("Retrieved sources", "5")
    st.metric("Search mode", "Semantic")

    st.markdown('<div class="sidebar-section">Session</div>', unsafe_allow_html=True)
    exchanges = len(st.session_state.get("messages", [])) // 2
    st.metric("Completed exchanges", str(exchanges))

    if st.button("Clear conversation", width="stretch"):
        st.session_state.messages = []
        st.rerun()

    st.markdown(
        """
        <div class="sidebar-section">Clinical notice</div>
        <div class="sidebar-note">
            Responses are generated from retrieved medical documents. Verify important clinical
            details against the source records and consult a qualified healthcare professional
            before making decisions.
        </div>
        """,
        unsafe_allow_html=True,
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown(
    """
    <div class="workspace-header">
        <div>
            <div class="workspace-kicker">Clinical document intelligence</div>
            <div class="workspace-title">Medical Chatbot QA System</div>
            <div class="workspace-caption">Ask questions and receive clear, retrieval-grounded answers from medical records</div>
        </div>
        <div class="status-pill"><span class="status-dot"></span>Retrieval system online</div>
    </div>
    """,
    unsafe_allow_html=True,
)

if not st.session_state.messages:
    st.markdown(
        """
        <section class="welcome">
            <div class="welcome-icon-wrap">
                <div class="welcome-icon-glow"></div>
                <div class="welcome-icon">🩺</div>
            </div>
            <div class="welcome-eyebrow">AI-powered clinical Q&amp;A</div>
            <h1>How can I assist with your medical records today?</h1>
            <p>
                Explore diagnoses, hospital courses, medications, follow-up plans, and patient summaries
                with answers grounded in retrieved clinical documents.
            </p>
        </section>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="suggestions">
            <div class="suggestion-card">
                <div class="suggestion-label">Patient summary</div>
                <div class="suggestion-text">Summarize the retrieved patients, key diagnoses, and important clinical findings.</div>
            </div>
            <div class="suggestion-card">
                <div class="suggestion-label">Care &amp; follow-up</div>
                <div class="suggestion-text">What follow-up instructions, care plans, or recommendations are documented?</div>
            </div>
            <div class="suggestion-card">
                <div class="suggestion-label">Medication review</div>
                <div class="suggestion-text">List the medications, treatments, or discharge prescriptions mentioned in the records.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="🧑‍⚕️" if message["role"] == "user" else "🩺"):
        content = message["content"]
        if message["role"] == "assistant":
            content = format_patient_response(content)
        st.markdown(content)

prompt = st.chat_input("Ask about diagnoses, medications, follow-up plans, or patient summaries...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user", avatar="🧑‍⚕️"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🩺"):
        with st.spinner("Searching medical records and preparing a clear answer..."):
            raw_error = None
            try:
                from src_code.main import main

                response = main(user_query=prompt)
            except Exception as exc:
                raw_error = str(exc)
                response = f"Unable to complete the request: {raw_error}"
                is_quota_error = "429" in raw_error or "RESOURCE_EXHAUSTED" in raw_error or "Quota exceeded" in raw_error
                is_auth_error = "401" in raw_error or "UNAUTHENTICATED" in raw_error or "API key not valid" in raw_error
                if "Missing required environment variable" in raw_error:
                    env_status = {
                        "MONGODB_URI": bool(os.getenv("MONGODB_URI")),
                        "PINECONE_API_KEY": bool(os.getenv("PINECONE_API_KEY")),
                        "GEMINI_API_KEY": bool(os.getenv("GEMINI_API_KEY")),
                        "GOOGLE_API_KEY": bool(os.getenv("GOOGLE_API_KEY")),
                        "PINECONE_INDEX_NAME": bool(os.getenv("PINECONE_INDEX_NAME")),
                    }
                    response += "\n\nEnvironment variables detected (values hidden): " + ", ".join(
                        f"{name}={'set' if present else 'missing'}" for name, present in env_status.items()
                    )
                elif is_quota_error:
                    retry_hint = ""
                    match = re.search(r"Please retry in ([^.]+)", raw_error)
                    if match:
                        retry_hint = f"\n- **Retry after:** {match.group(1).strip()}"
                    response = (
                        "## Request limit reached\n"
                        "- **What happened:** The Gemini API request could not be completed because the current quota/rate limit was exceeded.\n"
                        "- **Likely cause:** Free-tier daily or per-minute request limits for the configured model/project have been reached."
                        f"{retry_hint}\n"
                        "- **What to do:** Wait for the quota to reset, check your plan/billing, or switch to a project/key with available quota.\n"
                        "- **Rate limits:** https://aistudio.google.com/docs/rate-limits\n"
                        "- **Usage:** https://ai.dev/rate-limit"
                    )
                elif is_auth_error:
                    env_status = {
                        "GEMINI_API_KEY": bool(os.getenv("GEMINI_API_KEY")),
                        "GOOGLE_API_KEY": bool(os.getenv("GOOGLE_API_KEY")),
                    }
                    env_status_text = ", ".join(
                        f"{name}={'set' if present else 'missing'}" for name, present in env_status.items()
                    )
                    response = (
                        "## Authentication failed\n"
                        "- **What happened:** The Gemini API rejected the request because the API credentials are missing, invalid, or unsupported.\n"
                        "- **Likely cause:** The configured key/token is not a valid Google AI Studio Gemini API key for this API (for example, an expired key or an unsupported access token type).\n"
                        f"- **Environment variables detected (values hidden):** {env_status_text}\n"
                        "- **What to do:** Verify the Gemini API key used by the app, replace it with a valid key from Google AI Studio, and ensure it is configured correctly for this environment.\n"
                        "- **API keys & setup:** https://aistudio.google.com/apikey"
                    )

        formatted_response = format_patient_response(response)
        st.markdown(formatted_response)
        if raw_error and (is_quota_error or is_auth_error):
            with st.expander("Technical error details"):
                st.code(raw_error)

    st.session_state.messages.append({"role": "assistant", "content": response})
