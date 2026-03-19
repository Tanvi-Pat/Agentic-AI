from pydantic import BaseModel, Field
from typing import List
from tools import llm, serper_tool
from state import State
import yfinance as yf
import json

class AI_Scorer_Output(BaseModel):
    score: int = Field(description="AI adoption health score between [0-10] - 10 having very high AI adoption and investments in AI")
    summary: str = Field(description="Summary of the AI scorer")
    ai_revenue_exposure: str = Field(description = "Choose between low, medium or high depending upon their revenue exposure towards AI") 

def ai_scorer_node(state: State) -> State:
    print("Studying the AI adoption of the top candidate companies")
    candidates = state.candidates
    ai_scores  = {}
    ai_raw = {}
    combined_results = ""

    for ticker in candidates:
        queries = [
            f"{ticker} artificial intelligence revenue strategy 2025",
            f"{ticker} AI products partnerships investment 2025",
            f"{ticker} AI competitive advantage large language models",
        ]

        for q in queries:
            results = serper_tool().invoke(q)
            response = llm().invoke(results)
            combined_results += response.content + "\n\n"

        prompt = f"""
        Based on the following web search results about {ticker},
        evaluate how well positioned this company is in the AI era.

        Search results:
        {combined_results}

        Return JSON:
        {{
          "score": <0-10>,
          "summary": "<2 sentence summary>",
          "ai_revenue_exposure": "<low|medium|high>"
        }}
        """
        llm_with_output = llm().with_structured_output(AI_Scorer_Output)
        response = llm_with_output.invoke(prompt)
        ai_scores[ticker] = response.model_dump()

        ai_raw[ticker] = {
            "search_snippets": combined_results[:2000] 
        }

    return {"ai_scores": ai_scores, "ai_raw": ai_raw}