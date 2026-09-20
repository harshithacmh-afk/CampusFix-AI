import streamlit as st
import pandas as pd

from graph.workflow import app
from database.db import (
    save_complaint,
    save_feedback,
    get_latest_complaint_id,
    get_complaints
)
from retrieval.update_knowledge_base import add_feedback_case


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="CampusFix AI",
    page_icon="🏫",
    layout="wide"
)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("🏫 CampusFix AI")
st.sidebar.write("Facility Decision Support System")

page = st.sidebar.radio(
    "Navigate",
    ["🔧 Diagnose Complaint", "📊 Dashboard"]
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🏫 CampusFix AI")

st.subheader(
    "Multi-Agent Campus Facility Decision Support System"
)


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

if page == "📊 Dashboard":

    st.title("📊 CampusFix Dashboard")

    complaints = get_complaints()

    total_complaints = len(complaints)

    high_priority = sum(
        1 for complaint in complaints
        if complaint[7] in ["High", "Critical"]
    )

    knowledge_base = pd.read_csv(
        "data/maintenance_records.csv"
    )

    st.metric(
        "Total Complaints",
        total_complaints
    )

    st.metric(
        "High/Critical Cases",
        high_priority
    )

    st.metric(
        "Knowledge Base Records",
        len(knowledge_base)
    )

    st.subheader("📋 Recent Complaints")

    if complaints:

        history = pd.DataFrame(
            complaints,
            columns=[
                "ID",
                "Complaint",
                "Likely Cause",
                "Confidence",
                "Recommended Fix",
                "Estimated Cost",
                "Estimated Time",
                "Urgency",
                "Explanation",
                "Created At"
            ]
        )

        st.dataframe(
            history[
                [
                    "ID",
                    "Complaint",
                    "Likely Cause",
                    "Urgency",
                    "Estimated Cost",
                    "Created At"
                ]
            ],
            use_container_width=True
        )

    else:

        st.info(
            "No complaints have been recorded yet."
        )

    st.stop()


# --------------------------------------------------
# DIAGNOSIS SESSION STATE
# --------------------------------------------------

if "diagnosis_result" not in st.session_state:
    st.session_state.diagnosis_result = None


# --------------------------------------------------
# COMPLAINT INPUT
# --------------------------------------------------

complaint = st.text_area(
    "Enter the maintenance complaint",
    placeholder=(
        "Example: The AC is running but the classroom "
        "is still very warm"
    )
)


# --------------------------------------------------
# DIAGNOSE BUTTON
# --------------------------------------------------

if st.button("🔍 Diagnose Complaint"):

    if complaint.strip():

        result = app.invoke(
            {
                "complaint": complaint
            }
        )

        st.session_state.diagnosis_result = result

        save_complaint(
            complaint,
            result["likely_cause"],
            result["confidence"],
            result["recommendation"]["recommended_fix"],
            result["recommendation"]["estimated_cost"],
            result["recommendation"]["estimated_time"],
            result["urgency"],
            result["explanation"]
        )

    else:

        st.warning(
            "Please enter a complaint first."
        )


# --------------------------------------------------
# DISPLAY DIAGNOSIS
# --------------------------------------------------

if st.session_state.diagnosis_result is not None:

    result = st.session_state.diagnosis_result

    st.subheader("🔎 Diagnosis")

    st.write(
        "**Likely Cause:**",
        result["likely_cause"]
    )

    st.write(
        "**Confidence:**",
        result["confidence"]
    )

    st.subheader("🛠️ Recommended Action")

    st.write(
        "**Fix:**",
        result["recommendation"]["recommended_fix"]
    )

    st.write(
        "**Estimated Cost:**",
        result["recommendation"]["estimated_cost"]
    )

    st.write(
        "**Estimated Repair Time:**",
        result["recommendation"]["estimated_time"]
    )

    st.write(
        "**Urgency:**",
        result["urgency"]
    )

    st.subheader("🧠 Reasoning")

    st.write(
        result["explanation"]
    )


# --------------------------------------------------
# TECHNICIAN FEEDBACK
# --------------------------------------------------

st.subheader("👨‍🔧 Technician Feedback")

feedback = st.radio(
    "Was this diagnosis correct?",
    ["Correct", "Incorrect"]
)


actual_cause = ""
actual_resolution = ""
actual_cost = ""
actual_time = ""


# --------------------------------------------------
# INCORRECT FEEDBACK DETAILS
# --------------------------------------------------

if feedback == "Incorrect":

    st.warning(
        "Please provide the actual maintenance details."
    )

    actual_cause = st.text_input(
        "Actual Cause"
    )

    actual_resolution = st.text_input(
        "Actual Resolution"
    )

    actual_cost = st.text_input(
        "Actual Cost"
    )

    actual_time = st.text_input(
        "Actual Repair Time"
    )


# --------------------------------------------------
# SUBMIT FEEDBACK
# --------------------------------------------------

if st.button("Submit Feedback"):

    complaint_id = get_latest_complaint_id()

    if complaint_id is not None:

        save_feedback(
            complaint_id,
            feedback,
            actual_cause,
            actual_resolution,
            actual_cost,
            actual_time
        )

        if feedback == "Incorrect":

            add_feedback_case(
                complaint,
                "Unknown",
                "Unknown",
                "Unknown",
                actual_cause,
                actual_resolution,
                actual_cost,
                actual_time
            )

        st.success(
            "✅ Technician feedback recorded successfully!"
        )

    else:

        st.warning(
            "Please diagnose a complaint before submitting feedback."
        )