from langgraph.graph import StateGraph, START, END
from state import State
from nodes.classifier import classifier_agent
from nodes.summarizer import summarizer_agent


graph_builder = StateGraph(State)

graph_builder.add_node("summarizer", summarizer_agent)
graph_builder.add_node("classifier", classifier_agent)

graph_builder.add_edge(START, "summarizer")
graph_builder.add_edge("summarizer", "classifier")
graph_builder.add_edge("classifier", END)
