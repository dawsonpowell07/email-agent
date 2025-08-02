from langgraph.graph import StateGraph, START, END
from state import State
from nodes.classifier import classifier_agent
from nodes.summarizer import summarizer_agent
from nodes.authenticator import load_auth
from utils.print import pretty_print_messages

graph_builder = StateGraph(State)

# Nodes
graph_builder.add_node("auth", load_auth)
graph_builder.add_node("summarizer", summarizer_agent)
graph_builder.add_node("classifier", classifier_agent)

# Edges
graph_builder.add_edge(START, "auth")
graph_builder.add_edge("auth", "summarizer")
graph_builder.add_edge("summarizer", "classifier")
graph_builder.add_edge("classifier", END)

graph = graph_builder.compile()


user_email = "dawsonpowell07@gmail.com"

for chunk in graph.stream(
    {
        "messages": [{"role": "user", "content": "classify my emails"}],
        "user_email": user_email,
    }
):
    print(chunk)