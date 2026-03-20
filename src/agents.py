from crewai import Agent
from langchain_community.llms import Ollama
from src.tools import summarize_text
from src.logger import logger

# Local LLM
llm = Ollama(model="llama3")

# -------- Research Agent --------
research_agent = Agent(
    role="Researcher",
    goal="Collect research papers and extract key content",
    backstory="Expert in research data collection",
    llm=llm,
    verbose=True,
)

# -------- Validator Agent --------
validator_agent = Agent(
    role="Validator",
    goal="Clean duplicate and irrelevant data",
    backstory="Ensures data quality",
    llm=llm,
    verbose=True,
)

# -------- Writer Agent --------
writer_agent = Agent(
    role="Writer",
    goal="Generate structured research report with citations",
    backstory="Expert in writing research summaries",
    llm=llm,
    verbose=True,
)


# -------- NLP Processor --------
def nlp_process(data):
    logger.info("Running NLP summarization")

    if isinstance(data, list):
        combined = " ".join([d["summary"] for d in data])
        return summarize_text(combined)

    return summarize_text(data)
