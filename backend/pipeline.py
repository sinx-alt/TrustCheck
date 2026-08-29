from backend.schemas import AnalyzeRequest, AnalyzeResponse, Signal
from backend.config import get_settings
from backend.scoring import build_explanation, recommend_safe_action
from detector import analyze_message as detect  # confirm this path matches your actual folder name

settings = get_settings()


def _to_signal_objects(raw_signals: list[dict]) -> list[Signal]:
    return [
        Signal(
            type=s["type"],
            score=settings.signal_weights.get(s["type"], 0),
            evidence=s["evidence"],
        )
        for s in raw_signals
    ]


def analyze_message(request: AnalyzeRequest) -> AnalyzeResponse:
    raw_signals, risk_score, risk_level, urls, brand = detect(request.message)
    signals = _to_signal_objects(raw_signals)
    brands = [brand] if brand else []

    return AnalyzeResponse(
        risk_score=risk_score,
        risk_level=risk_level,
        signals=signals,
        urls=urls,
        brands=brands,
        explanation=build_explanation(signals),
        safe_action=recommend_safe_action(signals),
    )