from schemas import AnalyzeRequest, AnalyzeResponse, Signal
from config import get_settings
from scoring import build_explanation, recommend_safe_action
from detection.detector import analyze_message as detect  # aliased — avoids name collision

settings = get_settings()


def _to_signal_objects(raw_signals: list[dict]) -> list[Signal]:
    """Attach an illustrative per-signal score from config.py weights.
    Won't sum exactly to risk_score — detector.py's combo bonuses account
    for the gap, and that's expected, not a bug."""
    return [
        Signal(
            type=s["type"],
            score=settings.signal_weights.get(s["type"], 0),
            evidence=s["evidence"],
        )
        for s in raw_signals
    ]


def analyze_message(request: AnalyzeRequest) -> AnalyzeResponse:
    raw_signals, risk_score, risk_level = detect(request.message)
    signals = _to_signal_objects(raw_signals)

    # Stopgap until Member 4 exposes urls/brands directly — remove once they do
    import re
    urls = re.findall(r"https?://\S+", request.message)
    brands = [
        b for b in ("flipkart", "amazon", "google", "microsoft", "apple", "paytm", "sbi")
        if b in request.message.lower()
    ]

    return AnalyzeResponse(
        risk_score=risk_score,
        risk_level=risk_level,
        signals=signals,
        urls=urls,
        brands=brands,
        explanation=build_explanation(signals),
        safe_action=recommend_safe_action(signals),
    )