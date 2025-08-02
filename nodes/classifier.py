from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from tools.add_to_label import add_to_label
from tools.gmail_authenticate import gmail_authenticate
from prompts.classifier_prompt import classifier_prompt
from utils.logging import get_logger

load_dotenv()

logger = get_logger(__name__)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

logger.info("Creating classifier agent")
classifier_agent = create_react_agent(
    model=llm,
    tools=[add_to_label, gmail_authenticate],
    message_modifier=classifier_prompt,
)
logger.info("Successfully created classifier agent")
