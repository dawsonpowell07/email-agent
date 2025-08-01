from langgraph.graph import StateGraph, START, END
from state import State
from nodes.classifier import classifier_agent
from nodes.summarizer import summarizer_agent
from utils.print import pretty_print_messages

graph_builder = StateGraph(State)

graph_builder.add_node("summarizer", summarizer_agent)
graph_builder.add_node("classifier", classifier_agent)

graph_builder.add_edge(START, "summarizer")
graph_builder.add_edge("summarizer", "classifier")
graph_builder.add_edge("classifier", END)

graph = graph_builder.compile()

# user_email = "dawsonpowell07@gmail.com"

# for chunk in graph.stream(
#     {
#         "messages": [{"role": "user", "content": "classify my emails"}],
#         "user_email": user_email,
#     }
# ):
#     pretty_print_messages(chunk)
