from pathlib import Path
import json
import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

RESULTS_FILE = (
    PROJECT_ROOT
    / "data"
    / "evaluation"
    / "benchmark_results.json"
)

st.title("Evaluation Results")

if not RESULTS_FILE.exists():

    st.error(
        "benchmark_results.json not found"
    )

    st.stop()

with open(
    RESULTS_FILE,
    "r",
    encoding="utf-8"
) as file:

    results = json.load(file)

df = pd.DataFrame(results)

st.metric(
    "Total Evaluations",
    len(df)
)

st.dataframe(
    df,
    use_container_width=True
)

st.subheader(
    "Latency Distribution"
)

st.bar_chart(
    df["latency"]
)