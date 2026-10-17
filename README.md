# ResearchMind — Multi-Agent AI Research Assistant

ResearchMind is an AI-powered research assistant that automates the research process using specialized agents. It searches for relevant information, reads and summarizes sources, drafts a structured report, and reviews the output to improve its quality.

The project combines a multi-agent research pipeline with an interactive Streamlit interface, making it easier to explore topics and generate research reports.

## Features

- **Automated Web Search:** Discovers relevant information and source URLs using search tools.
- **Source Reading & Summarization:** Retrieves and summarizes information from web pages.
- **AI Report Generation:** Produces structured research reports with key findings and conclusions.
- **Critic & Review Pipeline:** Reviews the draft, identifies gaps, and refines the final report.
- **Interactive Web Interface:** Provides a dark-themed Streamlit UI to enter research topics and monitor pipeline progress.
- **Agent-Level Outputs:** Displays the work produced by individual stages of the research pipeline.
- **Report Export:** Allows users to download the final report in Markdown format.
- **Environment Variable Support:** Keeps API credentials in a local `.env` file rather than hardcoding them in the source code.

## Architecture

ResearchMind follows a four-stage research workflow:

1. **Search Agent** — Finds relevant web pages and discovers source URLs.
2. **Reader Agent** — Reads, extracts, and summarizes information from sources.
3. **Writer Chain** — Organizes research findings into a structured report.
4. **Critic Chain** — Reviews and refines the draft to produce the final report.

The workflow is orchestrated through a Python pipeline and presented through a Streamlit application.

## Tech Stack

- Python
- Streamlit
- LangChain
- LangChain-Groq
- LangChain-Google-GenAI
- DuckDuckGo Search
- BeautifulSoup
- Requests
- Python Dotenv
- LXML

## Project Structure

```text
Multiagent-ai-research-system-Research-Mind/
├── agents.py             # Agent definitions and behavior
├── app.py                # Streamlit application
├── pipeline.py           # Research workflow orchestration
├── tools.py              # Search and web research tools
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variable template
├── .gitignore            # Ignored files and secrets
└── research_report.txt   # Sample research output
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/jiya1928/Multiagent-ai-research-system-Research-Mind.git
cd Multiagent-ai-research-system-Research-Mind
```

### 2. Create a virtual environment

**Windows (PowerShell)**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS/Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a local `.env` file from the provided template.

**Windows (PowerShell):**

```powershell
Copy-Item .env.example .env
```

**macOS/Linux:**

```bash
cp .env.example .env
```

Open `.env` and add the credentials required by the project. Use `.env.example` to identify the required variable names.

**Security note:** Never commit your actual `.env` file or expose API keys in source code, screenshots, logs, or public documentation.

### 5. Run the application

Start the Streamlit application:

```bash
streamlit run app.py
```

Open the local URL displayed in the terminal, typically `http://localhost:8501`.

### 6. Generate a research report

1. Enter a research topic in the application.
2. Select **Run Research Pipeline**.
3. Monitor the pipeline's progress and agent logs.
4. Review the generated research report and individual agent outputs.
5. Download the final report in Markdown format.

## Security

This project uses a `.env` file for local configuration.

- `.env` contains local credentials and should not be committed.
- `.env.example` documents the required environment variable names without exposing secrets.
- `.venv/` and generated files should be excluded from version control where appropriate.

## Future Improvements

- Add persistent research history and report management.
- Improve source verification and citation quality.
- Add configurable research depth and output formats.
- Introduce automated tests and error handling.
- Support deployment for wider access.

## Author

**Jiya Bhardwaj**

- GitHub: [@jiya1928](https://github.com/jiya1928)
- LinkedIn: [Jiya Bhardwaj](https://www.linkedin.com/in/jiya-bhardwaj-90b04841a/)

---

If you find this project useful, consider giving the repository a ⭐ on GitHub.
