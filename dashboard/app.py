# dashboard/app.py

import streamlit as st

st.set_page_config(
    page_title="AI Reliability Platform",
    page_icon="🛡️",
    layout="wide"
)

st.title(
    "🛡️ AI Reliability Platform"
)

st.markdown(
    """
    Enterprise platform for:

    - Self-Healing RAG
    - Guardrails Gateway
    - LLM Evaluation
    - Observability
    """
)