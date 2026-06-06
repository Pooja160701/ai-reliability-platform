import streamlit as st
import json
from pathlib import Path

PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parent
    .parent
    .parent
)

RETRIEVAL_FILE = (
    PROJECT_ROOT
    / "data"
    / "logs"
    / "retrieval.json"
)

st.title("🔍 Retrieval Analytics")

with open(
    RETRIEVAL_FILE,
    "r"
) as file:
    data = json.load(file)

for item in data:

    st.subheader(
        item["question"]
    )

    st.write(
        item["documents"]
    )