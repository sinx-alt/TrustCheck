from backend.schemas import Signal, RiskLevel


def build_explanation(signals: list[Signal]) -> list[str]:
    """Turn each triggered signal into a plain-language sentence for the user."""
    phrasing: dict[str, str] = {
        "URGENT_LANGUAGE": "The message uses urgent or threatening language to pressure a quick response.",
        "UNREALISTIC_REWARD": "The message promises an unusually large or unrealistic reward.",
        "SENSITIVE_INFORMATION_REQUEST": "The message asks you to share sensitive information such as an OTP or password.",
        "PAYMENT_REQUEST": "The message asks for a payment or fee before you can receive something.",
        "SUSPICIOUS_DOMAIN": "The link in the message points to a domain that could not be verified.",
        "BRAND_DOMAIN_MISMATCH": "The message claims to be from a brand whose verified domain does not match the link.",
    }
    return [phrasing[s.type] for s in signals if s.type in phrasing]


def recommend_safe_action(signals: list[Signal]) -> str:
    """Pick the most relevant safe-action guidance based on which signals fired."""
    if any(s.type == "BRAND_DOMAIN_MISMATCH" for s in signals):
        return "Do not use this link. Go to the brand's official app or type their website address manually."
    if not signals:
        return "No risk signals detected, but always verify unexpected requests through an official channel."
    return "Do not click the link or share information. Verify this claim through the organization's official app or support line."


# --- Kept for local testing/comparison only — NOT used in the live pipeline ---
# Member 4's detector.py computes the authoritative risk_score/risk_level via
# calculate_risk()/get_risk_level(). These two functions exist here in case you
# want to sanity-check your own weight assumptions during Day 4 tuning, but
# pipeline.py does not call them.

def compute_risk_score(signals: list[Signal]) -> int:
    return min(sum(s.score for s in signals), 100)


def score_to_level(score: int) -> RiskLevel:
    from backend.config import get_settings
    settings = get_settings()
    for threshold, level in settings.risk_thresholds:
        if score >= threshold:
            return level  # type: ignore[return-value]
    return "LOW"