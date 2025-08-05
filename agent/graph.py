from langgraph.graph import StateGraph, START, END
from agent.state import State
from agent.nodes.classifier import classifier_agent
from agent.nodes.summarizer import summarizer_agent
from agent.nodes.authenticator import load_auth

graph_builder = StateGraph(State)

async def call_summarizer_agent(state: State) -> dict[str, any]:
    response = await summarizer_agent.ainvoke(
        state
    )
    
    return {
        "messages": response
    }


async def call_classifier_agent(state: State) -> dict[str, any]:
    response = await classifier_agent.ainvoke(
        state
    )

    return {
        "messages": response
    }

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


# user_email = "dqpowel@clemson.edu"

# for chunk in graph.stream(
#     {
#         "messages": [{"role": "user", "content": "classify my emails"}],
#         "user_email": user_email,
#     }
# ):
#     print(chunk)
