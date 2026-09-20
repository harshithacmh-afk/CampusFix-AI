# CampusFix AI

## Multi-Agent Campus Facility Decision Support System

**CampusFix AI** is an Agentic AI-powered facility maintenance system that helps facility managers diagnose equipment problems using historical maintenance cases.

Instead of relying only on manual diagnosis, the system retrieves similar past maintenance cases and uses them to provide an explainable recommendation for the likely cause, repair action, estimated cost, repair time, and urgency.

---

## Problem Statement

Facility managers often diagnose equipment failures based on memory and experience. This can make diagnosis slower and inconsistent, especially when multiple maintenance complaints occur.

CampusFix AI addresses this problem by using historical maintenance records as a searchable knowledge base.

---

##  Solution

The system follows an agentic workflow:

```text
Maintenance Complaint
        ↓
Complaint Retrieval
        ↓
Similar Historical Cases
        ↓
Diagnosis Agent
        ↓
Recommendation Agent
        ↓
Urgency Analysis
        ↓
Explainable Reasoning
        ↓
Technician Feedback
        ↓
Knowledge Base Improvement
```

---

##  Key Features

*  Semantic search over historical maintenance records
*  Similar-case retrieval using Sentence Transformers
*  FAISS vector similarity search
*  Multi-agent workflow using LangGraph
*  Likely root-cause diagnosis
*  Recommended repair action
*  Estimated repair cost
*  Estimated repair time
*  Urgency classification
*  Plain-language reasoning explanation
*  Streamlit dashboard
*  SQLite complaint logging
*  Technician feedback loop
*  Feedback-based knowledge-base improvement

---

##  Multi-Agent Architecture

CampusFix AI uses multiple specialized agents:

### 1. Retrieval Agent

Searches historical maintenance records and retrieves the most relevant cases using semantic similarity.

### 2. Diagnosis Agent

Analyzes the retrieved cases and identifies the most likely root cause.

### 3. Recommendation Agent

Determines the most common historical resolution and estimates cost and repair time.

### 4. Urgency Agent

Determines the urgency level based on historical maintenance cases.

### 5. Explanation Agent

Generates a plain-language explanation showing how historical evidence supports the diagnosis and recommendation.

---

##  Technician Feedback Loop

CampusFix AI includes a continuous improvement mechanism.

After receiving a diagnosis, a technician can mark it as:

* ✅ Correct
* ❌ Incorrect

For an incorrect diagnosis, the technician can provide:

* Actual cause
* Actual resolution
* Actual cost
* Actual repair time

The confirmed feedback is then added to the maintenance knowledge base and the FAISS index is rebuilt.

```text
AI Diagnosis
     ↓
Technician Feedback
     ↓
Correct / Incorrect
     ↓
Actual Maintenance Details
     ↓
Knowledge Base
     ↓
FAISS Re-indexing
     ↓
Improved Future Retrieval
```

---

##  Technology Stack

| Technology            | Purpose                        |
| --------------------- | ------------------------------ |
| Python                | Core development               |
| Streamlit             | Web dashboard                  |
| LangGraph             | Agent workflow orchestration   |
| Sentence Transformers | Text embeddings                |
| FAISS                 | Similarity search              |
| Pandas                | Data processing                |
| SQLite                | Complaint and feedback logging |
| Plotly                | Data visualization             |

---

##  Project Structure

```text
CampusFix-AI/
│
├── agents/
│   ├── diagnosis_agent.py
│   ├── explanation_agent.py
│   ├── recommendation_agent.py
│   └── urgency_agent.py
│
├── data/
│   ├── generate_data.py
│   └── maintenance_records.csv
│
├── database/
│   └── db.py
│
├── graph/
│   └── workflow.py
│
├── retrieval/
│   ├── embeddings.py
│   ├── vector_store.py
│   └── update_knowledge_base.py
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

##  How to Run

### 1. Clone the repository

```bash
git clone https://github.com/harshithacmh-afk/CampusFix-AI.git
cd CampusFix-AI
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
streamlit run app.py
```

The application will open in the browser.

---

##  Example Use Cases

### AC Failure

**Complaint:**

> The AC is running but the classroom is still very warm.

The system retrieves similar historical AC cases and can identify a likely issue such as a clogged air filter, along with a recommended repair, estimated cost, repair time, and urgency.

### Generator Failure

**Complaint:**

> The generator is not starting.

The system searches historical generator cases and provides a diagnosis based on the retrieved maintenance evidence.

### Elevator Failure

**Complaint:**

> The elevator stops between floors.

The system retrieves similar elevator maintenance cases and provides an explainable recommendation.

---

##  Dashboard

The Streamlit dashboard provides:

* Total complaints
* High/Critical cases
* Knowledge-base record count
* Recent complaint history
* Diagnosis information
* Technician feedback

---

##  Evaluation Areas

The system can be evaluated based on:

* Retrieval relevance
* Diagnosis consistency
* Recommendation usefulness
* Explainability
* Dashboard usability
* Technician feedback integration
* Knowledge-base improvement

---

##  Future Enhancements

Potential future improvements include:

* LLM-powered diagnosis reasoning
* Real-time maintenance alerts
* Multiple simultaneous complaint processing
* Advanced analytics
* Technician authentication
* Equipment-specific knowledge bases
* Predictive maintenance
* Cloud deployment
* Role-based dashboards

---

##  Project

**CampusFix AI — Multi-Agent Campus Facility Decision Support System**

Built for an Agentic AI Hackathon.