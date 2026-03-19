from pydantic import BaseModel, Field
from typing import List
from state import State

def aggregator_node(state: State) -> State:
    print("Aggregating the metrics together to determine the winner")
    candidates    = state.candidates
    fin_scores    = state.financial_scores
    risk_scores   = state.risk_scores
    ai_scores     = state.ai_scores
    ranked_list   = []

    for ticker in candidates:
        f_score = fin_scores.get(ticker,{}).get("score", 0)
        r_score = risk_scores.get(ticker,{}).get("score", 0)
        a_score = ai_scores.get(ticker,{}).get("score", 0)

        # Weighted total — configurable
        total = (f_score * 0.40) + (r_score * 0.30) + (a_score * 0.30)

        # Recommendation logic
        if total >= 7.5:
            recommendation = "BUY"
        elif total >= 5.0:
            recommendation = "HOLD"
        else:
            recommendation = "AVOID"

        ranked_list.append({
            "ticker":          ticker,
            "financial_score": round(f_score, 2),
            "risk_score":      round(r_score, 2),
            "ai_score":        round(a_score, 2),
            "total_score":     round(total, 2),
            "recommendation":  recommendation,
        })

    # Sort by total score descending
    ranked_list.sort(key=lambda x: x["total_score"], reverse=True)

    return {"ranked_list": ranked_list}