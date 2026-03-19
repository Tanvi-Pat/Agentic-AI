from langgraph.graph import StateGraph
from state import State
from nodes.aggregator import aggregator_node
from nodes.ai_scorer import ai_scorer_node
from nodes.candidate_extractor import candidate_extractor_node
from nodes.financial_analyst import financial_analyst_node
from nodes.risk_accessor import risk_assessor_node
from nodes.report_agent import report_agent_node

def build_graph():
    graph = StateGraph(State)
    graph.add_node("candidate_extractor", candidate_extractor_node)
    graph.add_node("financial_analyst", financial_analyst_node)
    graph.add_node("risk_assessor", risk_assessor_node)
    graph.add_node("ai_scorer", ai_scorer_node)
    graph.add_node("aggregator", aggregator_node)
    graph.add_node("report_agent", report_agent_node)

    graph.set_entry_point("candidate_extractor")

    graph.add_edge("candidate_extractor", "financial_analyst")
    graph.add_edge("candidate_extractor", "risk_assessor")
    graph.add_edge("candidate_extractor", "ai_scorer")

    graph.add_edge("financial_analyst", "aggregator")
    graph.add_edge("risk_assessor", "aggregator")
    graph.add_edge("ai_scorer", "aggregator")

    graph.add_edge("aggregator", "report_agent")

    return graph.compile()