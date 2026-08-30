# TrustCheck
A system for detecting scam messages, phishing links, fake alerts, lottery scams, and fraudulent offers.

See the evidence, not just the verdict.

TrustCheck is a security-focused application designed to help users identify potentially fraudulent or suspicious messages before they act on them.

Instead of simply saying that a message is "fake" or "safe", TrustCheck analyzes the content for multiple warning signals, calculates a risk score from 0–100, explains why the message may be suspicious, and provides a safer next step.

## 🚀 Features

- 🔍 Scam and suspicious-message detection
- 🔗 Suspicious URL and domain detection
- ⚠️ Urgency and pressure-language detection
- 💳 Payment-request detection
- 🔐 Sensitive-information request detection
- 🎁 Unrealistic reward detection
- 🏦 Brand/domain mismatch detection
- 📊 Risk scoring from **0–100**
- 🟢 LOW, 🟡 SUSPICIOUS, and 🔴 HIGH risk levels
- 💡 Explainable detection results
- 🛡️ Safer-action recommendations
- 💬 Chatbot-style frontend
- 🌐 REST API backend

## ❗ Problem

Scam messages commonly use urgency, fake rewards, suspicious links, impersonation, and requests for sensitive information to trick users.

Examples include:

- Fake KYC or bank alerts
- Lottery and prize scams
- Fake deals and offers
- Phishing links
- Suspicious payment requests
- Requests for sensitive information

Users often need more than a simple **"safe" or "unsafe"** label.

TrustCheck aims to answer:

> **"Why does this message look suspicious, and what should I do next?"**

---
## 💡 Our Solution

TrustCheck analyzes a message using a rule-based detection engine.

The system looks for predefined suspicious patterns and signals, combines them into a risk score, determines the corresponding risk level, and explains the evidence behind the result.

Instead of:

"This message is suspicious."

TrustCheck provides:

Risk Score → Risk Level → Signals → Explanation → Safer Next Step

This makes the result easier for a user to understand and act upon.

## 🧠 Detection

TrustCheck currently uses a **rule-based detection system**.

The detection engine checks submitted content for signals including:

- `URGENT_LANGUAGE`
- `SUSPICIOUS_DOMAIN`
- `UNREALISTIC_REWARD`
- `PAYMENT_REQUEST`
- `SENSITIVE_INFORMATION_REQUEST`
- `BRAND_DOMAIN_MISMATCH`

These signals are used by the analysis pipeline to determine the overall risk of the submitted content.

For the detailed internal detection and processing flow, see **[ARCHITECTURE.md](ARCHITECTURE.md)**.

---

## 📊 Risk Scoring

TrustCheck calculates a risk score between **0 and 100**.

The score is mapped to the project's configured risk thresholds and classified into:

- **LOW**
- **SUSPICIOUS**
- **HIGH**

The result also contains detected signals and supporting explanation so users can understand the reason behind the assessment.

---

## 🌐 API

The TrustCheck backend is deployed using **Render**.

### Base URL

```text
https://trustcheck-p6fz.onrender.com/
```
The backend provides API endpoints for message analysis and related services.

### Analyze Message

```text
POST /api/analyze
```

### Request

```json
{
  "message": "Your bank account will be blocked today. Complete your KYC immediately."
}
```

The API returns an analysis containing information such as:

- Risk score
- Risk level
- Detected signals
- URLs
- Brands
- Explanation
- Recommended safe action

The exact request and response structures are defined by the backend API schemas.

## 🖥️ Frontend

TrustCheck includes a chatbot-style frontend where users can enter a message or suspicious URL.

The interface is designed to display:

- Risk level
- Risk score
- Detected signals
- Explanation
- Relevant links or brands
- Safer next step

The frontend was initially developed using mock responses and is being connected to the deployed backend API.

## 🧪 Testing

TrustCheck includes a CSV-based test dataset containing examples of:

- Fake KYC messages
- Fake lottery messages
- Fake deals
- Suspicious links
- Sensitive-information requests
- Brand mismatches
- Legitimate messages and promotions

The dataset contains fields such as:

- `id`
- `category`
- `message`
- `expected_risk`
- `expected_signals`

The current detection baseline achieved approximately 87% accuracy on the project's test evaluation.

The project also includes backend tests for validating the analysis pipeline.

## 🛠️ Technology Stack

### Frontend

- Kotlin
- Android
- Jetpack Compose
- Retrofit

### Backend

- Python
- FastAPI
- Pydantic
- Uvicorn

### Detection

- Python
- Rule-based detection
- Keyword analysis
- URL analysis

### Data & Testing

- CSV test dataset
- Backend automated tests

### Deployment

- Render

### Version Control

- Git
- GitHub
- Branches and Pull Requests

## 🔐 Safety

TrustCheck is designed as a second-opinion security tool.

Users should still:

- Avoid clicking suspicious links.
- Verify important requests through official channels.
- Avoid sharing sensitive information through unverified messages.
- Independently verify important financial or account-related communications.

## ⚠️ Disclaimer

TrustCheck is a prototype designed to assist users in identifying potentially suspicious messages and links.

No automated detection system can guarantee that every message is safe or fraudulent. A risk score should not be treated as absolute proof.

Users should independently verify important communications through trusted official channels.
