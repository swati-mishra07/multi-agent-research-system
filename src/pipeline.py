from crewai import Task, Crew
from src.agents import (
    research_agent,
    validator_agent,
    writer_agent,
    nlp_process,
)
from src.tools import search_arxiv, extract_text_from_pdf
from src.logger import logger


def research_pipeline(topic=None, pdf_path=None):

    logger.info("Hybrid Pipeline started")

    # Step 1: Data
    if pdf_path:
        raw_data = extract_text_from_pdf(pdf_path)
    else:
        raw_data = search_arxiv(topic)

    # Step 2: NLP Preprocessing
    processed_data = nlp_process(raw_data)

    # Step 3: CrewAI Tasks
    research_task = Task(
        description=f"Analyze this research:\n{processed_data}",
        agent=research_agent,
    )

    validation_task = Task(
        description="Validate and refine the research content",
        agent=validator_agent,
    )

    writing_task = Task(
        description="""
        Create a structured report:
        - Title
        - Introduction
        - Key Findings
        - Conclusion
        - References
        """,
        agent=writer_agent,
    )

    crew = Crew(
        agents=[research_agent, validator_agent, writer_agent],
        tasks=[research_task, validation_task, writing_task],
        verbose=True,
    )

    result = crew.kickoff()

    return result
