# Triad Agent Orchestrator 

A powerful multi-agent AI research system that combines web search, intelligent analysis, and adaptive formatting to deliver comprehensive, well-structured reports on any topic.

## Overview

The Triad Agent Orchestrator implements a three-stage pipeline where specialized AI agents collaborate to research, analyze, and present information:

1. **Searcher Agent** (Tavily) - Retrieves factual information from the web
2. **Analyst Agent** (Google Gemini) - Synthesizes data and adds expert context
3. **Structurer Agent** (Groq/Llama) - Formats content with intelligent, adaptive layouts

## Features

- **Intelligent Web Search**: Uses Tavily API for fast, relevant search results
- **Deep Analysis**: Gemini AI synthesizes information and adds contextual knowledge
- **Adaptive Formatting**: Automatically adjusts report structure based on content type
- **Auto-Save Reports**: Generates clean Markdown files for every query
- **Colorful CLI**: Beautiful terminal interface with status indicators
- **Error Handling**: Robust retry logic and graceful failure management

## Getting Started

### Prerequisites

- Python 3.8 or higher
- API keys for:
  - [Tavily API](https://tavily.com/) (web search)
  - [Google Gemini API](https://ai.google.dev/) (analysis)
  - [Groq API](https://groq.com/) (formatting)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/kunal51107/Triad-Agent-Orchestrator
   cd triad-agent-orchestrator
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   TAVILY_API_KEY=your_tavily_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   GROQ_API_KEY=your_groq_api_key_here
   ```

### Usage

Run the main orchestrator:

```bash
python main.py
```

Enter your research query when prompted:
```
Enter your research topic (or 'q' to quit): Compare iPhone 16 Pro vs Samsung S25 Ultra
```

The system will:
1. Search the web for relevant information
2. Analyze and synthesize the findings
3. Generate a formatted report
4. Save it as `Report_<your_query>.md`

## Project Structure

```
.
├── agents.py              # Core agent implementations
├── main.py                # Main orchestrator and CLI
├── requirements.txt       # Python dependencies
├── .env                   # API keys (create this)
├── .gitignore            # Git ignore rules
├── check_models_gemini.py # Utility to list Gemini models
├── check_models_grok.py   # Utility to list Groq models
└── Report_*.md           # Generated reports (auto-saved)
```

## Agent Architecture

### SearcherAgent
- **Role**: Web Research Specialist
- **Technology**: Tavily API
- **Output**: JSON with search results, direct answers, and sources

### AnalystAgent
- **Role**: Knowledge Synthesizer
- **Technology**: Google Gemini Flash
- **Output**: Structured JSON with analysis, context, and expert insights
- **Features**: Automatic topic classification, conflict detection, knowledge enrichment

### StructurerAgent
- **Role**: Content Strategist
- **Technology**: Groq (Llama 3.3 70B)
- **Output**: Professional Markdown reports
- **Features**: Adaptive formatting based on content type (comparisons, news, technical guides, etc.)

## Utility Scripts

### Check Available Models

**Gemini Models:**
```bash
python check_models_gemini.py
```

**Groq Models:**
```bash
python check_models_grok.py
```

## Example Use Cases

- **Product Comparisons**: "iPhone 16 Pro vs Samsung S25 Ultra specs"
- **Technical Research**: "How does quantum computing work?"
- **Current Events**: "Latest developments in AI regulation 2025"
- **Historical Analysis**: "Impact of the Renaissance on modern art"
- **How-To Guides**: "Best practices for machine learning deployment"

## Configuration

### Customize Search Depth

In `agents.py`, modify the `SearcherAgent.search()` method:

```python
response = self.client.search(
    query=query, 
    search_depth="advanced",  # Change to "advanced" for deeper research
    max_results=5,            # Increase for more sources
    include_answer=True
)
```

### Adjust AI Temperature

In `agents.py`, modify the `StructurerAgent.structure()` method:

```python
temperature=0.6,  # Lower for more focused, higher for more creative
```

## Error Handling

The system includes:
- Automatic retry logic for API rate limits
- Graceful degradation on search failures
- JSON parsing error recovery
- Network connectivity checks

## Output Format

Reports are saved as Markdown files with:
- Descriptive titles
- Professional formatting
- Tables for comparisons
- Blockquotes for key insights
- Proper citations and references

## Acknowledgments

- [Tavily](https://tavily.com/) for search API
- [Google](https://ai.google.dev/) for Gemini AI
- [Groq](https://groq.com/) for lightning-fast inference

**Made with 🤖 by combining the power of multiple AI agents**