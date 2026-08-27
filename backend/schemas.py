from typing import List, Literal
from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="Message or SMS to analyze"
    )


class Signal(BaseModel):
    type: Literal[
        "URGENT_LANGUAGE",
        "SUSPICIOUS_DOMAIN",
        "UNREALISTIC_REWARD",
        "PAYMENT_REQUEST",
        "SENSITIVE_INFORMATION_REQUEST",
        "BRAND_DOMAIN_MISMATCH"
    ]

    score: int = Field(
        ...,
        ge=0,
        le=100,
        description="Risk score contributed by this signal"
    )

    evidence: str = Field(
        ...,
        min_length=1,
        description="Text or feature that triggered the signal"
    )


class AnalyzeResponse(BaseModel):
    risk_score: int = Field(
        ...,
        ge=0,
        le=100,
        description="Overall fraud risk score"
    )

    risk_level: Literal[
        "LOW",
        "SUSPICIOUS",
        "HIGH"
    ]

    signals: List[Signal] = Field(default_factory=list)

    urls: List[str] = Field(default_factory=list)

    brands: List[str] = Field(default_factory=list)

    explanation: List[str] = Field(default_factory=list)

    safe_action: str = Field(
        ...,
        description="Recommended safe action for the user"
    )