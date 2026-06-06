import streamlit as st
import pandas as pd
import json
from pathlib import Path

PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parent
    .parent
    .parent
)

GUARDRAILS_FILE = (
    PROJECT_ROOT
    / "data"
    / "logs"
    / "guardrails.json"
)

st.title("🛡️ Guardrails")

with open(
    GUARDRAILS_FILE,
    "r"
) as file:
    data = json.load(file)

col1, col2, col3 = st.columns(3)

df = pd.DataFrame(data)

st.metric(
    "Blocked Requests",
    len(df)
)

st.dataframe(
    df,
    use_container_width=True
)