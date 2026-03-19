from pydantic import BaseModel, Field
from typing import List
from tools import llm, serper_tool
from state import State
import yfinance as yf
import json

class Risk_Assessor_Output(BaseModel):
    score: int = Field(description="Market crash resilience score between [0-10] - 10 being the most resilent. Crash resilience meaning its robustness to recover")
    summary: str = Field(description="Summary of the risk assessment")
    most_resilient_crash: str = Field(description = "Crash name")
    biggest_risk: str = Field(description = "Key risks") 

def risk_assessor_node(state: State) -> State:
    print("Examining the risk assessment of the top candidate companies")
    candidates = state.candidates
    risk_scores = {}
    risk_raw = {}

    # Define crash windows to test resilience
    crash_windows = {
        "2008_crisis":    ("2008-01-01", "2009-03-31"),
        "2020_covid":     ("2020-02-01", "2020-04-30"),
        "2022_correction":("2022-01-01", "2022-12-31"),
    }

    for ticker in candidates:
        stock     = yf.Ticker(ticker)
        crash_data = {}

        for crash_name, (start, end) in crash_windows.items():
            try:
                hist = stock.history(start=start, end=end)
                if hist.empty:
                    crash_data[crash_name] = "No data"
                    continue

                peak     = hist["Close"].max()
                trough   = hist["Close"].min()
                drawdown = ((trough - peak) / peak) * 100  # negative = drop %

                # Recovery: how long to get back to pre-crash price
                pre_crash_price = hist["Close"].iloc[0]
                recovery_hist   = stock.history(start=end, end="2023-12-31")
                recovered       = recovery_hist[recovery_hist["Close"] >= pre_crash_price]
                recovery_days   = (recovered.index[0] - hist.index[-1]).days if not recovered.empty else None

                crash_data[crash_name] = {
                    "max_drawdown_pct": round(drawdown, 2),
                    "recovery_days":    recovery_days,
                }
            except Exception as e:
                crash_data[crash_name] = f"Error: {str(e)}"

        # Beta and volatility
        info    = stock.info
        beta    = info.get("beta", None)
        hist_5y = stock.history(period="5y")
        volatility = round(hist_5y["Close"].pct_change().std() * 100, 4) if not hist_5y.empty else None

        prompt = f"""
        Assess the market crash resilience of {ticker}:
        - Crash drawdowns and recovery: {json.dumps(crash_data)}
        - Beta (market sensitivity): {beta}
        - 5-year daily volatility: {volatility}%

        Return JSON:
        {{
          "score": <0-10>,
          "summary": "<2 sentence summary>",
          "most_resilient_crash": "<crash name>",
          "biggest_risk": "<key risk>"
        }}
        """
        llm_with_output = llm().with_structured_output(Risk_Assessor_Output)
        response = llm_with_output.invoke(prompt)
        risk_scores[ticker] = response.model_dump()

        risk_raw[ticker] = {
            "beta":       beta,
            "volatility": volatility,
            "crashes":    crash_data,   # full drawdown + recovery dict per crash window
        }

    return {"risk_scores": risk_scores, "risk_raw": risk_raw}