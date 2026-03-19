from pydantic import BaseModel, Field
from typing import List
from tools import llm, serper_tool
from state import State
import json

def report_agent_node(state: State) -> State:
    "Building a detailed report"
    ranked_list   = state.ranked_list
    fin_scores    = state.financial_scores
    risk_scores   = state.risk_scores
    ai_scores     = state.ai_scores
    financial_raw = state.financial_raw
    risk_raw      = state.risk_raw
    domain        = state.domain

    # Build a rich context block per ticker
    ticker_contexts = []

    for entry in ranked_list:
        ticker = entry["ticker"]

        context = f"""
        === {ticker} (Total score: {entry['total_score']}/10 — {entry['recommendation']}) ===

        FINANCIAL ANALYSIS (score: {entry['financial_score']}/10):
        - Summary:    {fin_scores.get(ticker, {}).get('summary', 'N/A')}
        - Strengths:  {fin_scores.get(ticker, {}).get('strengths', [])}
        - Weaknesses: {fin_scores.get(ticker, {}).get('weaknesses', [])}
        - PE Ratio:         {financial_raw.get(ticker, {}).get('pe_ratio', 'N/A')}
        - Profit Margin:    {financial_raw.get(ticker, {}).get('profit_margin', 'N/A')}%
        - Revenue Growth:   {financial_raw.get(ticker, {}).get('revenue_growth', 'N/A')}%
        - Debt/Equity:      {financial_raw.get(ticker, {}).get('debt_to_equity', 'N/A')}
        - Free Cash Flow:   {financial_raw.get(ticker, {}).get('free_cash_flow', 'N/A')}

        RISK ANALYSIS (score: {entry['risk_score']}/10):
        - Summary:          {risk_scores.get(ticker, {}).get('summary', 'N/A')}
        - Most resilient:   {risk_scores.get(ticker, {}).get('most_resilient_crash', 'N/A')}
        - Biggest risk:     {risk_scores.get(ticker, {}).get('biggest_risk', 'N/A')}
        - Beta:             {risk_raw.get(ticker, {}).get('beta', 'N/A')}
        - 5Y Volatility:    {risk_raw.get(ticker, {}).get('volatility', 'N/A')}%
        - Crash drawdowns:  {json.dumps(risk_raw.get(ticker, {}).get('crashes', {}))}

        AI RELEVANCE (score: {entry['ai_score']}/10):
        - Summary:          {ai_scores.get(ticker, {}).get('summary', 'N/A')}
        - AI Products:      {ai_scores.get(ticker, {}).get('ai_products', [])}
        - AI Revenue:       {ai_scores.get(ticker, {}).get('ai_revenue_exposure', 'N/A')}
        - Partnerships:     {ai_scores.get(ticker, {}).get('key_partnerships', [])}
        - Moat:             {ai_scores.get(ticker, {}).get('competitive_moat', 'N/A')}
        """
        ticker_contexts.append(context)

    full_context = "\n\n".join(ticker_contexts)

    prompt = f"""
    You are a senior investment analyst. Write a professional investment research
    report for the {domain} sector based on the analysis below.

    The report must include:
    1. Executive Summary — top pick and why in 3-4 sentences
    2. Sector Overview — brief note on {domain} in the AI era
    3. Stock-by-stock analysis — for each ticker cover:
       a. Financial health highlights
       b. Market crash resilience
       c. AI era positioning
       d. Final recommendation (BUY / HOLD / AVOID) with justification
    4. Comparison table — ticker | financial score | risk score | AI score | total | recommendation
    5. Disclaimer — this is AI-generated research, not financial advice

    ANALYSIS DATA:
    {full_context}

    Write in clear, professional markdown format.
    """

    response  = llm().invoke(prompt)
    report_md = response.content

    # Optional: save to file
    with open(f"{domain.replace(' ', '_')}_report.md", "w") as f:
        f.write(report_md)

    return {"final_report": report_md}