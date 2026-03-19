from pydantic import BaseModel, Field
from typing import List
from tools import llm, serper_tool
from state import State

class Candidate_Output(BaseModel):
    candidates: List[str] = Field(description="list of companies")

def candidate_extractor_node(state: State) -> State:
    print("Extracting top companies in the given domain")
    domain = state.domain

    results = serper_tool().invoke(f"top 5 publicly traded stocks in {domain} sector 2026")

    prompt =  f"""
    From the following search results, extract the top 5 stock ticker symbols
    in the {domain} sector. Return ONLY a JSON list of tickers.
    Example: ["NVDA", "AMD", "MSFT"]
    
    Search results:
    {results}
    """
    
    llm_with_output = llm().with_structured_output(Candidate_Output)
    response = llm_with_output.invoke(prompt)
    print(response.candidates)
    candidates = response.candidates

    return {"candidates": candidates}