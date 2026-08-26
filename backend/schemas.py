from pydantic import BaseModel, Field
from typing import List

class AnalyzeRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=5000)

class Signal(BaseModel):
    type: str        # e.g. "URGENT_LANGUAGE"
    score: int
    evidence: str

class AnalyzeResponse(BaseModel):
    risk_score: int
    risk_level: str          # "LOW" | "SUSPICIOUS" | "HIGH"
    signals: List[Signal]
    urls: List[str]
    brands: List[str]
    explanation: List[str]
    safe_action: str