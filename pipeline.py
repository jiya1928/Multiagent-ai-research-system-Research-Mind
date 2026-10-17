from crewai import Agent, Task, LLM, Crew, Process
from tools import web_search, wikipedia_search, scrape_webpage, summarize_text, extract_links

llm = LLM(
    model="ollama/llama3.2:latest",
    base_url="http://localhost:11434"
)

search_agent = Agent(
    role='Search Specialist',
    goal='Search web and Wikipedia for topic {topic} and find URLs',
    backstory='Expert in finding relevant sources. You always return URLs.',
    tools=[web_search, wikipedia_search],
    llm=llm,
    verbose=True,
    allow_delegation=False
)

reader_agent = Agent(
    role='Research Analyst',
    goal='Read content from search results',
    backstory='You read webpages and summarize key facts with sources.',
    tools=[scrape_webpage, summarize_text],
    llm=llm,
    verbose=True,
    allow_delegation=False
)

writer_agent = Agent(
    role='Report Writer',
    goal='Write draft report on {topic}',
    backstory='You write clear structured reports with Introduction, Findings with URLs, Conclusion.',
    llm=llm,
    verbose=True,
    allow_delegation=False
)

critic_agent = Agent(
    role='Critic and Fact-Checker',
    goal='Critically review draft and give final report',
    backstory='You are harsh critic. You find flaws like missing citations, bias, weak conclusion, then fix it.',
    tools=[extract_links],
    llm=llm,
    verbose=True,
    allow_delegation=False
)

def create_tasks(topic):
    search_task = Task(
        description='Search for topic: {topic}. Use web_search tool and wikipedia_search tool. Return at least 5 URLs and summary.',
        expected_output='List of URLs and search summary with sources',
        agent=search_agent
    )
    reader_task = Task(
        description='Read and summarize content. Use scrape_webpage and summarize_text on search results. Topic is {topic}',
        expected_output='Detailed research data with key points and URLs',
        agent=reader_agent
    )
    writer_task = Task(
        description='Write draft report on {topic} using research data. Structure: Introduction, 3-4 Key Findings with Source URLs, Conclusion.',
        expected_output='Draft report with source URLs',
        agent=writer_agent
    )
    critic_task = Task(
        description="Review draft report on {topic}. Check sources using extract_links. Then output FINAL IMPROVED REPORT with Introduction, Key Findings with URLs, Conclusion, and Sources.",
        expected_output='Critical review + Final improved report with sources',
        agent=critic_agent
    )
    return [search_task, reader_task, writer_task, critic_task]

def run_full_pipeline(topic: str, log_callback=None):
    def log(msg):
        if log_callback:
            try:
                log_callback(str(msg))
            except:
                pass

    tasks = create_tasks(topic)
    crew = Crew(
        agents=[search_agent, reader_agent, writer_agent, critic_agent],
        tasks=tasks,
        process=Process.sequential,
        verbose=True
    )
    log(f"Starting: {topic}")
    result = crew.kickoff(inputs={"topic": topic})
    log("Complete!")
    return result