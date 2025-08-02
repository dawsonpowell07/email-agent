from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from tools.get_emails import get_emails
from tools.gmail_authenticate import gmail_authenticate
from prompts.summarizer_prompt import summarizer_prompt
from utils.logging import get_logger

load_dotenv()

logger = get_logger(__name__)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

logger.info("Creating summarizer agent")
summarizer_agent = create_react_agent(
    model=llm,
    tools=[get_emails, gmail_authenticate],
    message_modifier=summarizer_prompt,
)
logger.info("Successfully created summarizer agent")
