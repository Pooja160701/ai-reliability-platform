import json
from pathlib import Path
import streamlit as st

PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parent
    .parent
    .parent
)

COST_FILE = (
    PROJECT_ROOT
    / "data"
    / "logs"
    / "costs.json"
)

st.title("💰 Cost Dashboard")

with open(
    COST_FILE,
    "r"
) as file:
    data = json.load(file)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Embedding Calls",
    data["embedding_calls"]
)

col2.metric(
    "Generation Calls",
    data["generation_calls"]
)

col3.metric(
    "Estimated Cost",
    f"${data['estimated_cost']}"
)