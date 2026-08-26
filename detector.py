import csv
import re
from urllib.parse import urlparse


urgent_keywords = [
    "urgent", "immediately", "immediate", "next 10 minutes", "today",
    "final warning", "deadline", "suspended", "blocked", "closed",
    "disconnected", "expire", "prevent", "avoid", "warning"
]

payment_keywords = [
    "pay", "payment", "fee", "charge", "transfer", "deposit", "donation",
    "processing fee", "registration fee", "delivery charge",
    "processing charge", "outstanding amount"
]

sensitive_keywords = [
    "otp", "password", "pin", "cvv", "card number", "bank details",
    "banking credentials", "personal information", "customer id",
    "security code", "verification code", "account details",
    "payment information", "banking information", "card information",
    "booking information"
]

reward_keywords = [
    "won", "winner", "prize", "reward", "cashback", "guaranteed returns",
    "guaranteed profit", "guaranteed daily profits", "exclusive discount",
    "discount voucher", "free"
]

link_reference_keywords = [
    "click here", "click this link", "click the link", "link provided",
    "provided link", "attached link", "verification link",
    "provided website", "provided page", "using this link",
    "using the link", "through the link"
]

url_keywords = [
    "verify", "login", "account", "update", "confirm",
    "payment", "secure", "password", "claim", "reward"
]

safe_sensitive_phrases = [
    "never share", "do not share", "don't share",
    "never provide", "do not provide", "don't provide",
    "will never ask"
]

known_brands = {
    "flipkart": "flipkart.com",
    "amazon": "amazon.com",
    "google": "google.com",
    "microsoft": "microsoft.com",
    "apple": "apple.com",
    "paytm": "paytm.com",
    "sbi": "sbi.co.in"
}

signal_scores = {
    "URGENT_LANGUAGE": 10,
    "SUSPICIOUS_DOMAIN": 30,
    "UNREALISTIC_REWARD": 25,
    "PAYMENT_REQUEST": 20,
    "SENSITIVE_INFORMATION_REQUEST": 25,
    "BRAND_DOMAIN_MISMATCH": 30
}


def find_urls(message):
    return re.findall(r'https?://\S+', message)


def detect_urgent(text):
    text = text.lower()

    urgent_phrases = [
        "next 10 minutes",
        "next few minutes",
        "within one hour",
        "within 24 hours"
    ]

    for phrase in urgent_phrases:
        if phrase in text:
            return phrase

    for word in urgent_keywords:
        if re.search(r'\b' + re.escape(word) + r'\b', text):
            return word

    return None


def detect_payment(text):
    text = text.lower()

    safe_payment_phrases = [
        "payment was successful",
        "payment of",
        "payment has been completed",
        "payment was completed",
        "successfully completed",
        "successfully paid"
    ]

    for phrase in safe_payment_phrases:
        if phrase in text:
            return None

    for word in payment_keywords:
        if re.search(r'\b' + re.escape(word) + r'\b', text):
            return word

    return None


def detect_sensitive_info(text):
    text = text.lower()

    for phrase in safe_sensitive_phrases:
        if phrase in text:
            return None

    request_words = [
        "send", "enter", "entering", "provide", "share",
        "submit", "give", "reply with", "type", "confirm",
        "verify your", "update your", "submit your"
    ]

    for sensitive_word in sensitive_keywords:
        if not re.search(r'\b' + re.escape(sensitive_word) + r'\b', text):
            continue

        for request_word in request_words:
            if request_word in text:
                return sensitive_word

    return None


def detect_reward(text):
    text = text.lower()

    for url in find_urls(text):
        text = text.replace(url, "")

    for word in reward_keywords:
        if re.search(r'\b' + re.escape(word) + r'\b', text):
            return word

    return None


def find_brand(text):
    text = text.lower()

    for brand in known_brands:
        if re.search(r'\b' + re.escape(brand) + r'\b', text):
            return brand

    return None


def check_brand_mismatch(text, urls):
    signals = []
    brand = find_brand(text)

    if not brand:
        return signals

    official_domain = known_brands[brand]

    for url in urls:
        domain = urlparse(url).netloc.lower()

        if not domain.endswith(official_domain):
            signals.append({
                "type": "BRAND_DOMAIN_MISMATCH",
                "evidence": f"{brand} claimed, but domain is {domain}"
            })

    return signals


def check_urls(urls):
    signals = []

    for url in urls:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        reasons = []

        if "@" in domain:
            reasons.append("URL contains @")

        for keyword in url_keywords:
            if keyword in url.lower():
                reasons.append(f"suspicious keyword: {keyword}")
                break

        if domain.count(".") > 2:
            reasons.append("unusually complex domain")

        if len(url) > 100:
            reasons.append("unusually long URL")

        if reasons:
            signals.append({
                "type": "SUSPICIOUS_DOMAIN",
                "evidence": f"{domain}: {', '.join(reasons)}"
            })

    return signals


def detect_suspicious_link_reference(text):
    text = text.lower()

    for phrase in link_reference_keywords:
        if phrase in text:
            return phrase

    return None


def detect_signals(text):
    signals = []

    urgent = detect_urgent(text)
    payment = detect_payment(text)
    sensitive = detect_sensitive_info(text)
    reward = detect_reward(text)

    if urgent:
        signals.append({
            "type": "URGENT_LANGUAGE",
            "evidence": "Urgent or threatening language detected"
        })

    if payment:
        signals.append({
            "type": "PAYMENT_REQUEST",
            "evidence": payment
        })

    if sensitive:
        signals.append({
            "type": "SENSITIVE_INFORMATION_REQUEST",
            "evidence": sensitive
        })

    if reward:
        signals.append({
            "type": "UNREALISTIC_REWARD",
            "evidence": reward
        })

    return signals


def calculate_risk(signals):
    total = 0
    signal_types = {signal["type"] for signal in signals}

    for signal in signals:
        total += signal_scores[signal["type"]]

    if (
        "UNREALISTIC_REWARD" in signal_types
        and "PAYMENT_REQUEST" in signal_types
    ):
        total += 10

    if (
        "URGENT_LANGUAGE" in signal_types
        and "PAYMENT_REQUEST" in signal_types
    ):
        total += 5

    if (
        "URGENT_LANGUAGE" in signal_types
        and "SENSITIVE_INFORMATION_REQUEST" in signal_types
    ):
        total += 5

    if (
        "SENSITIVE_INFORMATION_REQUEST" in signal_types
        and "SUSPICIOUS_DOMAIN" in signal_types
    ):
        total += 10

    if (
        "PAYMENT_REQUEST" in signal_types
        and "SENSITIVE_INFORMATION_REQUEST" in signal_types
    ):
        total += 5

    if "BRAND_DOMAIN_MISMATCH" in signal_types:
        total += 10

    return min(total, 100)


def contextual_risk_bonus(text):
    text = text.lower()
    bonus = 0

    financial_context = [
        "bank", "bank account", "banking", "upi", "debit card",
        "credit card", "fastag", "sim", "kyc", "tax",
        "electricity", "insurance", "loan"
    ]

    verification_context = [
        "verify", "verification", "identity", "kyc",
        "customer id", "password", "otp", "security code"
    ]

    action_words = [
        "send", "enter", "provide", "share", "submit",
        "confirm", "update", "click", "reactivate",
        "restore", "prevent"
    ]

    has_financial_context = any(
        phrase in text for phrase in financial_context
    )

    has_verification_context = any(
        phrase in text for phrase in verification_context
    )

    has_action = any(
        word in text for word in action_words
    )

    if (
        has_financial_context
        and has_verification_context
        and has_action
    ):
        bonus += 10

    if (
        has_financial_context
        and "urgent" in text
        and has_action
    ):
        bonus += 5

    return bonus


def get_risk_level(score):
    if score >= 60:
        return "HIGH"
    elif score >= 30:
        return "SUSPICIOUS"
    else:
        return "LOW"


def analyze_message(text):
    signals = detect_signals(text)

    urls = find_urls(text)
    signals.extend(check_urls(urls))

    link_reference = detect_suspicious_link_reference(text)

    if link_reference:
        signals.append({
            "type": "SUSPICIOUS_DOMAIN",
            "evidence": f"suspicious link reference: {link_reference}"
        })

    signals.extend(check_brand_mismatch(text, urls))

    risk_score = calculate_risk(signals)
    risk_score += contextual_risk_bonus(text)
    risk_score = min(risk_score, 100)

    risk_level = get_risk_level(risk_score)

    return signals, risk_score, risk_level


def test_csv(filename):
    with open(filename, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            message = row["message"]
            signals, risk_score, risk_level = analyze_message(message)

            print("\nID:", row["id"])
            print("Expected:", row["expected_risk"])
            print("Our result:", risk_level)
            print("Score:", risk_score)
            print("Signals:", signals)


if __name__ == "__main__":
    test_csv("test_message.csv")