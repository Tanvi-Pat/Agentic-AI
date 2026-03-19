from pydantic import BaseModel
from typing import List

class State(BaseModel):
    domain: str
    candidates: List[str]

    financial_scores: dict
    risk_scores: dict
    ai_scores: dict
    
    financial_raw: dict
    risk_raw: dict
    ai_raw: dict

    ranked_list: list
    final_report: str