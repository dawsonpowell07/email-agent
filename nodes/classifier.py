from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from tools.add_to_label import add_to_label
from prompts.classifier_prompt import classifier_prompt
load_dotenv()

llm = init_chat_model(model="gpt-4o-mini", temperature=0)

classifier_agent = create_react_agent(
    llm=llm,
    tools=[add_to_label],
    prompt=classifier_prompt,
)