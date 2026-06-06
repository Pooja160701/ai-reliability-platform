# dashboard/pages/Overview.py

from pathlib import Path
import json

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

REPORT_FILE = (
    PROJECT_ROOT
    / "data"
    / "evaluation"
    / "evaluation_report.json"
)

st.set_page_config(
    page_title="Overview",
    layout="wide"
)

st.title("AI Reliability Overview")

if not REPORT_FILE.exists():

    st.error(
        "evaluation_report.json not found"
    )

    st.stop()

with open(
    REPORT_FILE,
    "r",
    encoding="utf-8"
) as file:

    report = json.load(file)

status = report["status"]

if status == "PASS":
    st.success("Evaluation Gate Passed")
else:
    st.error("Evaluation Gate Failed")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Accuracy",
        f"{report['accuracy']:.2%}"
    )

with col2:

    st.metric(
        "Groundedness",
        f"{report['groundedness']:.2%}"
    )

with col3:

    st.metric(
        "Approval Rate",
        f"{report['approval_rate']:.2%}"
    )

col4, col5, col6 = st.columns(3)

with col4:

    st.metric(
        "Failure Rate",
        f"{report['failure_rate']:.2%}"
    )

with col5:

    st.metric(
        "Average Retries",
        round(
            report["average_retries"],
            2
        )
    )

with col6:

    st.metric(
        "Status",
        report["status"]
    )

st.divider()

st.subheader(
    "Evaluation Summary"
)

st.json(report)