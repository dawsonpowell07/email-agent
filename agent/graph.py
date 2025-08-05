from langgraph.graph import StateGraph, START, END
from agent.state import State
from agent.nodes.classifier import classifier_agent
from agent.nodes.summarizer import summarizer_agent
from agent.nodes.authenticator import load_auth

graph_builder = StateGraph(State)

async def call_summarizer_agent(state: State) -> dict[str, any]:
    messages = state["messages"]
    user_email = state["user_email"]

    response = await summarizer_agent.ainvoke({
        state
    })

    return {
        "messages": state["messages"] + [response],  # preserve chat history
    }


async def call_classifier_agent(state: State) -> dict[str, any]:
    messages = state["messages"]
    user_email = state["user_email"]
    summaries = state.get("summaries", {})

    response = await classifier_agent.ainvoke({
        state
    })

    return {
        "messages": state["messages"] + [response],  # preserve chat history
    }

# Nodes
graph_builder.add_node("auth", load_auth)
graph_builder.add_node("summarizer", call_summarizer_agent)
graph_builder.add_node("classifier", call_classifier_agent)

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
