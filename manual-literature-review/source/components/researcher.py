from typing import Type
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from exa_py import Exa
import requests
import streamlit as st
import os
from pypdf import PdfReader
# ================================================
# PDF Analysis Tool
# ================================================
class PDFAnalysisTool(BaseTool):
    name: str = "Analyze Uploaded PDF"
    description: str = "Read and analyze research paper PDF files uploaded by the user"

    def _run(self, pdf_path: str):
        try:
            reader = PdfReader(pdf_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            return text[:12000]
        except Exception as e:
            return f"PDF reading error: {str(e)}"


class EXAAnswerToolSchema(BaseModel):
    query: str = Field(..., description="The question you want to ask Exa.")

class EXAAnswerTool(BaseTool):
    name: str = "Ask Exa a question"
    description: str = "A tool that asks Exa a question and returns the answer."
    args_schema: Type[BaseModel] = EXAAnswerToolSchema
    answer_url: str = "https://api.exa.ai/answer"
    
    def _run(self, query: str):
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "x-api-key": os.environ.get("EXA_API_KEY")
        }
        try:
            response = requests.post(self.answer_url, json={"query": query, "text": True}, headers=headers)
            response.raise_for_status()
        except Exception as err:
            print(f"Error: {err}")
            raise
        response_data = response.json()
        answer = response_data["answer"]
        citations = response_data.get("citations", [])
        output = f"Answer: {answer}\n\n"
        if citations:
            output += "Citations:\n"
            for citation in citations:
                output += f"- {citation['title']} ({citation['url']})\n"
        return output

#--------------------------------#
#         LLM & Research Agent   #
#--------------------------------#

def create_researcher(selection):
    """Create a research agent with the specified LLM configuration."""
    provider = selection["provider"]
    model = selection["model"]
    
    if provider == "GROQ":
        llm = LLM(api_key=os.environ.get("GROQ_API_KEY"), model=f"groq/{model}")
    elif provider == "Ollama":
        llm = LLM(base_url="http://localhost:11434", model=f"ollama/{model}")
    else:
        # OpenAI models
        if model == "GPT-3.5": model = "gpt-3.5-turbo"
        elif model == "GPT-4": model = "gpt-4"
        elif model == "o1": model = "o1"
        elif model == "o1-mini": model = "o1-mini"
        llm = LLM(api_key=os.environ.get("OPENAI_API_KEY"), model=f"openai/{model}")
    
    researcher = Agent(
        role='Senior Academic Research Analyst',
        goal='Produce extremely deep, critical, and insightful academic research reports for 2025',
        backstory='You are a PhD-level researcher with 15+ years experience. You always go beyond surface level, find hidden connections, critique methodologies, identify research gaps, and provide forward-looking analysis.',
        tools=[EXAAnswerTool(),PDFAnalysisTool()],
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )
    return researcher

def create_research_task(researcher, task_description):
    """Create a research task for the agent to execute."""
    return Task(
        description=task_description,
        expected_output="""You are writing a HIGH-QUALITY, IN-DEPTH academic research report for 2025.

Return ONLY clean, professional Markdown. No JSON, no thinking steps, no internal variables.

Use this exact structure and make every section rich and detailed:

# Executive Summary
(3-4 strong paragraphs with key takeaways and significance)

# Key Findings
- 6-10 detailed bullet points with supporting evidence, numbers, dates, and comparisons

# In-Depth Analysis
Provide deep critical analysis:
• Compare different approaches/methodologies
• Discuss strengths and limitations of existing work
• Highlight contradictions or debates in the field
• Explain underlying trends and why they matter
• Include real-world implications and applications

# Research Gaps & Future Directions
• Clearly identify 4-6 important gaps in current research
• Suggest specific future research questions
• Predict developments in the next 12-24 months

# Critique and Comparison of Research
• Strengths and weaknesses of each paper
• Comparison between different methodologies and results
• Contradictions or agreements between studies

# Conclusion
Strong concluding insights and recommendations

# Sources
Numbered list with full titles, authors (if available), and URLs

Be critical, insightful, and academic. Use formal language. Go deep — do not be superficial.""",
        agent=researcher,
        output_file="output/research_report.md"
    )

#--------------------------------#
#         Research Crew          #
#--------------------------------#
def run_research(researcher, task):
    """Execute the research task using the configured agent."""
    crew = Crew(
        agents=[researcher],
        tasks=[task],
        verbose=True,
        process=Process.sequential
    )
    return crew.kickoff()