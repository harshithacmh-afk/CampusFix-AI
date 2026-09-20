import streamlit as st
import pandas as pd

from graph.workflow import app
from database.db import (
    save_complaint,
    save_feedback,
    get_latest_complaint_id,
    get_complaints,
    initialize_database
)
from retrieval.update_knowledge_base import add_feedback_case

st.set_page_config(
    page_title="CampusFix AI",
    page_icon=" ",
    layout="wide"
)


st.markdown(
    """
<style>

.main {
    background-color: #f7f9fc;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}


/* HERO */

.hero {
    background: linear-gradient(135deg, #0f172a, #1e3a8a);
    padding: 30px;
    border-radius: 20px;
    margin-bottom: 25px;
    color: white;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
}

.hero h1 {
    font-size: 42px;
    margin: 0 0 8px 0;
}

.hero p {
    font-size: 18px;
    margin: 5px 0;
    opacity: 0.92;
}


/* PIPELINE */

.pipeline {
    background: white;
    padding: 20px;
    border-radius: 16px;
    border: 1px solid #dbeafe;
    text-align: center;
    margin-top: 20px;
    margin-bottom: 25px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
}

.pipeline h3 {
    margin: 0 0 12px 0;
    color: #0f172a;
}

.pipeline p {
    font-size: 16px;
    color: #334155;
    margin: 0;
}


/* CARD */

.card {
    background: white;
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    margin-top: 15px;
}


/* DIAGNOSIS CARD */

.diagnosis-card {
    background: white;
    padding: 25px;
    border-radius: 18px;
    border: 1px solid #dbeafe;
    box-shadow: 0 5px 18px rgba(0, 0, 0, 0.06);
    margin-top: 15px;
    margin-bottom: 20px;
}

.label {
    font-size: 13px;
    color: #64748b;
    font-weight: 700;
    letter-spacing: 0.5px;
}

.value {
    font-size: 23px;
    font-weight: 700;
    color: #0f172a;
    margin-top: 5px;
}


/* FEEDBACK */

.feedback-card {
    background: white;
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #e5e7eb;
    margin-top: 20px;
}


/* FOOTER */

.footer {
    text-align: center;
    color: #64748b;
    font-size: 13px;
    padding: 25px 0 10px 0;
}

</style>
""",
    unsafe_allow_html=True
)

st.sidebar.title(" CampusFix AI")

st.sidebar.write(
    "Multi-Agent Facility Decision Support System"
)

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate",
    [
        "🔧 Diagnose Complaint",
        "📊 Dashboard"
    ]
)

st.sidebar.markdown("---")

st.sidebar.subheader("👤 User Role")

user_role = st.sidebar.selectbox(
    "Select your role",
    [
        "Facility Manager",
        "Technician"
    ]
)

if user_role == "Facility Manager":

    st.sidebar.success(
        "🏢 Facility Manager\n\n"
        "Access: Diagnosis, recommendations and dashboard"
    )

else:

    st.sidebar.info(
        "🔧 Technician\n\n"
        "Access: Diagnosis and technician feedback"
    )

st.sidebar.markdown("---")

st.sidebar.info(
    "💡 AI-powered maintenance diagnosis using "
    "historical maintenance knowledge."
)


st.markdown(
    """
<div class="hero">
<h1> CampusFix AI</h1>
<p>Multi-Agent Campus Facility Decision Support System</p>
<p>From maintenance complaints to explainable decisions.</p>
</div>
""",
    unsafe_allow_html=True
)


if page == "📊 Dashboard":

    st.title("📊 CampusFix Dashboard")

    st.caption(
        "Monitor maintenance complaints, priorities, and knowledge-base growth."
    )

    complaints = get_complaints()

    total_complaints = len(complaints)

    high_priority = sum(
        1
        for complaint in complaints
        if complaint[7] in ["High", "Critical"]
    )

    knowledge_base = pd.read_csv(
        "data/maintenance_records.csv"
    )

    knowledge_base_count = len(knowledge_base)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "📋 Total Complaints",
            total_complaints
        )

    with col2:
        st.metric(
            "🚨 High/Critical Cases",
            high_priority
        )

    with col3:
        st.metric(
            "📚 Knowledge Base Records",
            knowledge_base_count
        )

    st.markdown("---")

    st.subheader("📊 Maintenance Cases by Equipment")

    equipment_counts = (
        knowledge_base["equipment_type"]
        .value_counts()
        .reset_index()
    )

    equipment_counts.columns = [
        "Equipment",
        "Cases"
    ]

    st.bar_chart(
        equipment_counts.set_index("Equipment")
    )
   

    st.markdown("---")

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
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No complaints have been recorded yet."
        )


    st.markdown(
        """
<div class="footer">
CampusFix AI • Multi-Agent Facility Decision Support
</div>
""",
        unsafe_allow_html=True
    )

    st.stop()


if "processing_trace" not in st.session_state:
    st.session_state.processing_trace = []

if "diagnosis_result" not in st.session_state:
    st.session_state.diagnosis_result = None


if "example_complaint" not in st.session_state:
    st.session_state.example_complaint = ""


knowledge_base_status = pd.read_csv(
    "data/maintenance_records.csv"
)

status_col1, status_col2, status_col3 = st.columns(3)

with status_col1:
    st.success("🟢 AI Engine\n\nReady")

with status_col2:
    st.success(
        f"🟢 Knowledge Base\n\n{len(knowledge_base_status)} cases"
    )

with status_col3:
    st.success("🟢 Feedback Loop\n\nEnabled")

st.markdown(
    """
<div class="pipeline">
<h3>🤖 AI Decision Pipeline</h3>
<p>
📝 Complaint Intake
&nbsp; → &nbsp;
🔎 Semantic Retrieval
&nbsp; → &nbsp;
🧠 Diagnosis
&nbsp; → &nbsp;
🛠️ Recommendation
&nbsp; → &nbsp;
🚨 Urgency
&nbsp; → &nbsp;
💡 Explanation
</p>
</div>
""",
    unsafe_allow_html=True
)



st.subheader("💬 Maintenance Complaint")

st.caption(
    "Describe the equipment problem and let CampusFix AI "
    "search historical maintenance cases."
)



example_col1, example_col2, example_col3 = st.columns(3)

with example_col1:

    if st.button(
        "❄️ AC Example",
        use_container_width=True
    ):

        st.session_state.example_complaint = (
            "The AC is running but the classroom is still very warm"
        )


with example_col2:

    if st.button(
        "⚡ Generator Example",
        use_container_width=True
    ):

        st.session_state.example_complaint = (
            "The generator is not starting"
        )


with example_col3:

    if st.button(
        "🛗 Elevator Example",
        use_container_width=True
    ):

        st.session_state.example_complaint = (
            "The elevator stops between floors"
        )



complaint = st.text_area(
    "Enter the maintenance complaint",
    value=st.session_state.example_complaint,
    height=120,
    placeholder=(
        "Example: The AC is running but the classroom "
        "is still very warm"
    )
)




if st.button(
    "🔍 Diagnose Complaint",
    use_container_width=True
):

    if complaint.strip():
        st.session_state.processing_trace = [
            "✓ Complaint received",
            "✓ Searching historical maintenance cases",
            "✓ Running diagnosis agent",
            "✓ Generating repair recommendation",
            "✓ Determining urgency",
            "✓ Generating explainable reasoning"
        ]
        with st.spinner(
            "🤖 CampusFix AI is analyzing historical cases..."
        ):

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

        st.success(
            "✅ Diagnosis completed successfully!"
        )

    else:

        st.warning(
            "Please enter a maintenance complaint first."
        )


if st.session_state.processing_trace:

    with st.expander("🤖 View AI Processing Trace", expanded=True):

        for step in st.session_state.processing_trace:

            st.success(step)

if st.session_state.diagnosis_result is not None:

    result = st.session_state.diagnosis_result

    st.markdown("---")

    st.subheader("🔎 AI Diagnosis")


    

    st.markdown(
        f"""
<div class="diagnosis-card">
<div class="label">LIKELY ROOT CAUSE</div>
<div class="value">🔧 {result["likely_cause"]}</div>
<br>
<div class="label">CONFIDENCE</div>
<div class="value">🧠 {result["confidence"]}</div>
</div>
""",
        unsafe_allow_html=True
    )


    st.subheader("🔎 Historical Evidence")

    evidence_cases = result["cases"]

    if evidence_cases is not None and not evidence_cases.empty:

        matching_evidence = evidence_cases[
            evidence_cases["root_cause"]
            == result["likely_cause"]
        ]

        st.info(
            f"📚 {len(matching_evidence)} of "
            f"{len(evidence_cases)} retrieved historical cases "
            f"had the same root cause: "
            f"**{result['likely_cause']}**."
        )

        with st.expander("View Retrieved Historical Cases"):

            evidence_display = matching_evidence[
                [
                    "case_id",
                    "equipment_type",
                    "complaint",
                    "root_cause",
                    "resolution"
                ]
            ].copy()

            st.dataframe(
                evidence_display,
                use_container_width=True,
                hide_index=True
            )

    else:

        st.warning(
            "No historical evidence was retrieved."
        )

    

    st.subheader("🛠️ Recommended Action")

    rec_col1, rec_col2, rec_col3 = st.columns(3)

    with rec_col1:

        st.metric(
            "🔧 Recommended Fix",
            result["recommendation"]["recommended_fix"]
        )

    with rec_col2:

        st.metric(
            "💰 Estimated Cost",
            result["recommendation"]["estimated_cost"]
        )

    with rec_col3:

        st.metric(
            "⏱️ Repair Time",
            result["recommendation"]["estimated_time"]
        )


    

    st.subheader("🚨 Urgency")

    urgency = result["urgency"]

    if urgency == "Critical":

        st.error(
            "🔴 CRITICAL — Immediate attention required"
        )

    elif urgency == "High":

        st.warning(
            "🟠 HIGH — Priority maintenance recommended"
        )

    elif urgency == "Medium":

        st.info(
            "🟡 MEDIUM — Maintenance should be scheduled"
        )

    else:

        st.success(
            "🟢 LOW — Routine maintenance recommended"
        )



    st.subheader("🧠 Explainable Reasoning")

    st.markdown(
        f"""
<div class="card">
{result["explanation"]}
</div>
""",
        unsafe_allow_html=True
    )



st.markdown("---")

st.subheader("👨‍🔧 Technician Feedback")

st.caption(
    "Technician feedback helps CampusFix AI improve its "
    "maintenance knowledge base."
)


feedback = st.radio(
    "Was this diagnosis correct?",
    [
        "Correct",
        "Incorrect"
    ],
    horizontal=True
)


actual_cause = ""
actual_resolution = ""
actual_cost = ""
actual_time = ""



if feedback == "Incorrect":

    st.warning(
        "Please provide the actual maintenance details."
    )

    feedback_col1, feedback_col2 = st.columns(2)

    with feedback_col1:

        actual_cause = st.text_input(
            "Actual Cause"
        )

        actual_cost = st.text_input(
            "Actual Cost"
        )

    with feedback_col2:

        actual_resolution = st.text_input(
            "Actual Resolution"
        )

        actual_time = st.text_input(
            "Actual Repair Time"
        )




if st.button(
    "📥 Submit Technician Feedback",
    use_container_width=True
):

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




st.markdown(
    """
<div class="footer">
🏫 CampusFix AI &nbsp; | &nbsp;
Powered by LangGraph + FAISS + Sentence Transformers
</div>
""",
    unsafe_allow_html=True
)