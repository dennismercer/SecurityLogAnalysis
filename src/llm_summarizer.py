
import os
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv

# Load .env variables (optional)
load_dotenv()

# Initialize LLM (set OPENAI_API_KEY in environment or .env)
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.2)

# Define a prompt template for summarizing security event details
prompt = PromptTemplate.from_template(
    "You are a security analyst. Explain what the following event indicates:\n\n{event}\n\nKeep the summary short and behavior-focused."
)

summarizer = LLMChain(llm=llm, prompt=prompt)

def summarize_event(row):
    """
    Summarize a row from the unified event stream using an LLM.
    Expects a 'event_details' column in the input row.
    """
    try:
        return summarizer.invoke({"event": row["event_details"]})
    except Exception as e:
        return f"[LLM ERROR] {str(e)}"
