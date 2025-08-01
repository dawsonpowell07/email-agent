from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from tools.add_to_label import add_to_label
from prompts.classifier_prompt import classifier_prompt
load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

classifier_agent = create_react_agent(
    model=llm,
    tools=[add_to_label],
    prompt=classifier_prompt,
)