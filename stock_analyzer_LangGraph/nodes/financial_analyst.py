from pydantic import BaseModel, Field
from typing import List
from tools import llm, serper_tool
from state import State
import yfinance as yf

class Financial_Analyst_Output(BaseModel):
    score: int = Field(description="Financial health score between [0-10] - 10 having the most healthy financial metrics")
    summary: str = Field(description="Summary of the financial health")
    strengths: List[str] = Field(description = "Financial strengths")
    weaknesses: List[str] = Field(description = "Financial weaknesses")

def financial_analyst_node(state: State) -> State:
    print("Understanding the financial health of the top candidate companies")
    candidates = state.candidates
    financial_scores = {}
    financial_raw = {}

    for ticker in candidates:
        stock=yf.Ticker(ticker)
        
        income_stmt = stock.financials          
        quarterly    = stock.quarterly_financials

        revenue       = income_stmt.loc["Total Revenue"] if "Total Revenue" in income_stmt.index else None
        net_income    = income_stmt.loc["Net Income"] if "Net Income" in income_stmt.index else None
        operating_inc = income_stmt.loc["Operating Income"] if "Operating Income" in income_stmt.index else None

        balance_sheet = stock.balance_sheet
        total_debt    = balance_sheet.loc["Total Debt"] if "Total Debt" in balance_sheet.index else None
        equity        = balance_sheet.loc["Stockholders Equity"] if "Stockholders Equity" in balance_sheet.index else None

        cashflow      = stock.cashflow
        free_cf       = cashflow.loc["Free Cash Flow"] if "Free Cash Flow" in cashflow.index else None

        info          = stock.info
        pe_ratio      = info.get("trailingPE", None)
        profit_margin = info.get("profitMargins", None)
        revenue_growth= info.get("revenueGrowth", None)
        debt_to_equity= info.get("debtToEquity", None)

        prompt = f"""
        Analyze the financial health of {ticker} based on the following data:
        - Revenue (last 4 years): {revenue.to_dict() if revenue is not None else 'N/A'}
        - Net income: {net_income.to_dict() if net_income is not None else 'N/A'}
        - Free cash flow: {free_cf.to_dict() if free_cf is not None else 'N/A'}
        - Debt to equity: {debt_to_equity}
        - PE ratio: {pe_ratio}
        - Profit margin: {profit_margin}
        - Revenue growth: {revenue_growth}

        Return a JSON with:
        {{
          "score": <0-10>,
          "summary": "<2 sentence summary>",
          "strengths": ["...", "..."],
          "weaknesses": ["...", "..."],
        }}
        """

        llm_with_output = llm().with_structured_output(Financial_Analyst_Output)
        response = llm_with_output.invoke(prompt)
        financial_scores[ticker] = response.model_dump()

        financial_raw[ticker] = {
          "pe_ratio":       pe_ratio,
          "profit_margin":  round(profit_margin * 100, 2) if profit_margin else None,
          "revenue_growth": round(revenue_growth * 100, 2) if revenue_growth else None,
          "debt_to_equity": debt_to_equity,
          "free_cash_flow": {str(k): v for k, v in free_cf.to_dict().items()} if free_cf is not None else None,
          "net_income":     {str(k): v for k, v in net_income.to_dict().items()} if net_income is not None else None,
          "revenue":        {str(k): v for k, v in revenue.to_dict().items()} if revenue is not None else None,
        }

    return {"financial_scores":financial_scores, "financial_raw":financial_raw}
