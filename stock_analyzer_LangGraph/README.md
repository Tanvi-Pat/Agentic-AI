# Stock Analyzer — AI-Powered Investment Research Agent

Stock Analyzer is an agentic AI system built with LangGraph that generates 
detailed, data-driven investment research reports on publicly traded companies 
within a given sector — in real time.

## How It Works

The system evaluates each stock across three core dimensions:

### 1. Financial Health
Extracts 4 years of historical data from Yahoo Finance and analyzes:
- Revenue growth
- Profit margins
- PE ratio
- Debt-to-equity ratio
- Net income
- Free cash flow

### 2. Market Crash Resilience
Examines stock performance during major historical market downturns by measuring:
- Maximum % drawdown during each crash
- Time taken to fully recover

### 3. AI Adoption & Investment
Uses real-time web search (Serper API) to evaluate:
- AI revenue strategy
- Competitive positioning in the AI landscape
- AI partnership investments

## Recommendation Engine
Each dimension is independently scored and combined via a configurable 
weighted aggregation model to produce a final composite score — issuing 
a clear **Buy / Hold / Avoid** recommendation per stock.

## Tech Stack
- **LangGraph** — agent orchestration
- **LangChain + OpenAI** — LLM reasoning and structured outputs
- **Yahoo Finance (yfinance)** — financial data extraction
- **Serper API** — real-time web search
- **Python / Pydantic** — data validation and modeling

## Project Structure
```
stock_agent/
├── main.py                  # entry point
├── graph.py                 # LangGraph graph definition
├── state.py                 # AgentState and Pydantic models
├── nodes/
│   ├── candidate_extractor.py
│   ├── financial_analyst.py
│   ├── risk_assessor.py
│   ├── ai_scorer.py
│   ├── aggregator.py
│   └── report_agent.py
├── tools/
│   ├── yahoo_finance.py
│   └── web_search.py
├── .env                     # API keys (never commit)
└── requirements.txt
```

## Setup

1. Clone the repository
```bash
git clone https://github.com/Tanvi-Pat/Agentic-AI.git
cd stock-analyzer
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Add your API keys to `.env`
```
OPENAI_API_KEY=your_key_here
SERPER_API_KEY=your_key_here
```

4. Run
```bash
python main.py "audience measurement"
```

## Disclaimer
This tool is for research and educational purposes only. 
It does not constitute financial advice.