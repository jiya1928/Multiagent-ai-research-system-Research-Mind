from crewai import Agent
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from langchain_ollama import ChatOllama

# PHI3 MINI - Fastest, no limit, personal best quality
llm = ChatOllama(model="phi3:mini", temperature=0.2, num_ctx=4096)

web_search = SerperDevTool()
scrape = ScrapeWebsiteTool()

search_agent = Agent(
    role='Elite Search Specialist',
    goal='Find 7 high-quality URLs for {topic}',
    backstory='MIT researcher, finds authentic sources',
    tools=[web_search],
    llm=llm, verbose=True
)

reader_agent = Agent(
    role='Senior Research Analyst',
    goal='Deep read for {topic}',
    backstory='PhD level analyst',
    tools=[scrape],
    llm=llm, verbose=True
)

writer_agent = Agent(
    role='Principal Research Writer',
    goal='Write publication-quality draft on {topic}',
    backstory='Nature journal writer',
    llm=llm, verbose=True
)

critic_agent = Agent(
    role='Chief Editor & Fact-Checker',
    goal='CRITICAL REVIEW + MISSING SOURCES + FINAL REPORT for {topic} with URLs',
    backstory='Harsh peer reviewer, always outputs Critical Review section',
    llm=llm, verbose=True
)