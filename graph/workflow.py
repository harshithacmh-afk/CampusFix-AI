from typing import TypedDict


class CampusFixState(TypedDict):
    complaint: str
    cases: object
    likely_cause: str
    confidence: str
    recommendation: dict
    urgency: str
    explanation: str
from retrieval.vector_store import retrieve_cases


def retrieval_node(state: CampusFixState):
    cases = retrieve_cases(state["complaint"])

    return {
        "cases": cases
    }
from agents.diagnosis_agent import diagnose_cases


def diagnosis_node(state: CampusFixState):
    diagnosis = diagnose_cases(state["cases"])

    return {
        "likely_cause": diagnosis["likely_cause"],
        "confidence": diagnosis["confidence"]
    }
from agents.recommendation_agent import recommend_fix


def recommendation_node(state: CampusFixState):
    recommendation = recommend_fix(
        state["cases"],
        state["likely_cause"]
    )

    return {
        "recommendation": recommendation
    }
from agents.urgency_agent import determine_urgency


def urgency_node(state: CampusFixState):
    urgency = determine_urgency(
        state["cases"],
        state["likely_cause"]
    )

    return {
        "urgency": urgency
    }
from agents.explanation_agent import explain_diagnosis


def explanation_node(state: CampusFixState):
    explanation = explain_diagnosis(
        state["complaint"],
        state["cases"],
        state["likely_cause"],
        state["confidence"],
        state["recommendation"],
        state["urgency"]
    )

    return {
        "explanation": explanation
    }
from langgraph.graph import StateGraph


workflow = StateGraph(CampusFixState)
workflow.add_node("retrieval", retrieval_node)
workflow.add_node("diagnosis", diagnosis_node)
workflow.add_node("recommendation", recommendation_node)
workflow.add_node("urgency", urgency_node)
workflow.add_node("explanation", explanation_node)
workflow.add_edge("retrieval", "diagnosis")
workflow.add_edge("diagnosis", "recommendation")
workflow.add_edge("recommendation", "urgency")
workflow.add_edge("urgency", "explanation")
from langgraph.graph import START

workflow.add_edge(START, "retrieval")
from langgraph.graph import END

workflow.add_edge("explanation", END)
app = workflow.compile()