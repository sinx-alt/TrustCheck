# TrustCheck — System Architecture

## 1. Purpose

This document describes the technical architecture of **TrustCheck**, including its system components, communication flow, detection pipeline, API contract, risk-scoring process, repository structure, testing strategy, and deployment model.

TrustCheck is designed as a rule-based security analysis system that examines suspicious messages and URLs, identifies predefined warning signals, calculates a risk score, and returns an explainable security assessment.

The architecture separates the user interface, API layer, analysis pipeline, detection logic, scoring logic, and supporting data so that each component can be developed and tested independently.

---

# 2. Architecture Goals

The architecture is designed around the following goals:

- **Separation of concerns**
- **Explainable detection**
- **Stable API communication**
- **Independent module development**
- **Easy testing and validation**
- **Simple integration between frontend and backend**
- **Clear and maintainable code structure**
- **Ability to extend the detection engine later**

The detection system is intentionally rule-based in the current prototype rather than dependent on a machine-learning model.

---

# 3. High-Level Architecture

```text
                         ┌─────────────────────────┐
                         │          USER           │
                         │                         │
                         │  Enters message / URL   │
                         └────────────┬────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │   Android Frontend      │
                         │                         │
                         │ Kotlin + Jetpack       │
                         │ Compose                 │
                         └────────────┬────────────┘
                                      │
                                      │ Retrofit
                                      │ POST /api/analyze
                                      ▼
                         ┌─────────────────────────┐
                         │     FastAPI Backend     │
                         │                         │
                         │ Request validation      │
                         │ API routing             │
                         └────────────┬────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │    Analysis Pipeline    │
                         │                         │
                         │ Input → Detection →     │
                         │ Scoring → Explanation   │
                         └────────────┬────────────┘
                                      │
                    ┌─────────────────┴─────────────────┐
                    │                                   │
                    ▼                                   ▼
        ┌─────────────────────────┐          ┌─────────────────────────┐
        │    Detection Engine     │          │     Supporting Data     │
        │                         │          │ Test Dataset            │
        │ Rule-based analysis     │          │ Configuration           │
        │ Keyword analysis        │          │ API Schemas             │
        │ URL analysis            │          └─────────────────────────┘
        │ Brand/domain checks     │
        └────────────┬────────────┘
                     │
                     ▼
        ┌─────────────────────────┐
        │     Risk Scoring        │
        │                         │
        │ Signals → Score 0–100   │
        │ Score → Risk Level      │
        └────────────┬────────────┘
                     │
                     ▼
        ┌─────────────────────────┐
        │   Structured Response   │
        │                         │
        │ Score                   │
        │ Risk level              │
        │ Signals                 │
        │ URLs / Brands           │
        │ Explanation             │
        │ Safer action            │
        └────────────┬────────────┘
                     │
                     │ JSON
                     ▼
        ┌─────────────────────────┐
        │     Android Frontend    │
        │                         │
        │ Display analysis result │
        └─────────────────────────┘
```

# 4. System Components

## 4.1 Android Frontend

The frontend is an Android application built using Kotlin and Jetpack Compose.

Responsibilities:
- Accept user messages or URLs
- Send analysis requests to the backend
- Receive the analysis response
- Display risk level, score, signals, explanation, and safer action

The frontend communicates with the backend through Retrofit.

---

## 4.2 FastAPI Backend

The backend provides the REST API responsible for receiving analysis requests and coordinating the detection pipeline.

Responsibilities:
- Validate incoming requests
- Route API requests
- Invoke the analysis pipeline
- Return structured JSON responses

The main analysis endpoint is:

```text
POST /api/analyze
```

---

## 4.3 Analysis Pipeline

The analysis pipeline coordinates the main processing stages:

Input Message
     ↓
Request Validation
     ↓
Content / URL Analysis
     ↓
Signal Detection
     ↓
Risk Scoring
     ↓
Risk Classification
     ↓
Explanation Generation
     ↓
Structured API Response

The pipeline keeps the API layer separate from the underlying detection and scoring logic.

## 4.4 Detection Engine

The detection engine currently uses rule-based analysis.

It checks the submitted content for predefined suspicious signals:

- URGENT_LANGUAGE
- SUSPICIOUS_DOMAIN
- UNREALISTIC_REWARD
- PAYMENT_REQUEST
- SENSITIVE_INFORMATION_REQUEST
- BRAND_DOMAIN_MISMATCH

The detector can analyze message text, URLs, and relevant brand/domain relationships.
---

## 5. Risk Scoring

After the detection engine identifies suspicious signals, the scoring layer combines the detected signals to calculate a risk score between **0 and 100**.

The score is then classified into the configured risk levels:

```text
0 ─────────────────────────────── 100
│              │                 │
LOW        SUSPICIOUS           HIGH
```

## 6. API Communication

The Android frontend communicates with the FastAPI backend through a REST API using Retrofit.

### Analysis Endpoint

```text
POST /api/analyze
```

### Request

```json
{
  "message": "Your bank account will be blocked today. Complete your KYC immediately."
}
```

### Response

The backend processes the submitted message and returns a structured JSON response containing information such as:

- Risk score
- Risk level
- Detected signals
- URLs
- Brands
- Explanation
- Recommended safer action

The API schemas define the expected request and response structure.

## 7. Detection Signal Logic

The detection engine evaluates the submitted message and any URLs it contains using predefined rules.

The following signals are currently supported:

- `URGENT_LANGUAGE` — detects urgency, pressure, or immediate-action language.
- `SUSPICIOUS_DOMAIN` — identifies potentially suspicious or untrusted domains.
- `UNREALISTIC_REWARD` — detects claims of prizes, rewards, or offers that appear unusually attractive.
- `PAYMENT_REQUEST` — detects requests for payments, transfers, fees, or deposits.
- `SENSITIVE_INFORMATION_REQUEST` — detects requests for sensitive information such as credentials or personal details.
- `BRAND_DOMAIN_MISMATCH` — identifies cases where a claimed brand does not match the associated domain.

Each detected signal is passed to the risk-scoring layer for further evaluation.

The detection engine is rule-based and explainable, allowing the system to identify which signals contributed to the final assessment.

---

## 8. End-to-End Data Flow

The complete TrustCheck processing flow is:

```text
┌──────────────┐
│     User     │
└──────┬───────┘
       │
       ▼
┌──────────────────┐
│  Android App     │
└──────┬───────────┘
       │
       │ HTTPS / Retrofit
       ▼
┌──────────────────┐
│ FastAPI Backend  │
│  /api/analyze    │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Request          │
│ Validation       │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Analysis         │
│ Pipeline         │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Detection        │
│ Engine           │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Detected         │
│ Signals          │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Risk Scoring     │
│ & Classification │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Explanation &    │
│ Safer Action     │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ JSON Response    │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Android App      │
│ Result Display   │
└──────────────────┘

## 9. Error Handling

TrustCheck handles common errors at different stages of the system to prevent invalid requests or unexpected failures from affecting the user experience.

### 9.1 Input Validation

The backend validates the incoming analysis request before processing it.

- Empty or invalid messages are rejected.
- The API validates the request structure using Pydantic schemas.
- Invalid requests return an appropriate API error response.

### 9.2 API Communication Errors

If the Android application cannot communicate with the backend:

- The application should not display a misleading security result.
- The user is informed that the analysis could not be completed.
- The user can retry the analysis.

### 9.3 Backend Processing Errors

Unexpected errors during analysis are handled by the backend so that the API can return an appropriate error response instead of exposing internal implementation details.

### 9.4 Safe Failure Behavior

TrustCheck follows a fail-safe approach for analysis failures.

If the system cannot complete an analysis, it does not treat the message as automatically safe. The user is advised to verify the communication through a trusted official channel.

This ensures that a technical failure is not mistaken for a security assessment.

## 10. Repository Structure

TrustCheck is organized into separate Git branches so that the frontend, detection logic, backend, and integration work can be developed independently.

### Main Branch

The `main` branch contains the integrated project structure and project documentation.

```text
TrustCheck/
├── .vscode/
├── backend/
├── data/
├── detector/
├── .gitignore
├── ARCHITECTURE.md
├── README.md
├── runtime.txt
└── trustcheck.db

### Frontend Branch

The frontend branch contains the Android application developed using Kotlin and Jetpack Compose.
frontend/
├── app/
├── gradle/
├── .gitignore
├── README.md
├── build.gradle.kts
├── gradle.properties
├── gradlew
├── gradlew.bat
└── settings.gradle.kts

### Backend Branch

The backend branch contains the FastAPI backend and supporting backend resources.

backend/
├── .vscode/
├── backend/
├── data/
├── .gitignore
├── README.md
├── __init__.py
├── detector.py
└── trustcheck.db

### Detection Branch

The detection branch contains the rule-based detection engine.

detection/
├── detector/
├── .gitignore
└── README.md

### Integration Branch

The integration branch is used for combining and testing project components and contains the project test data.

integration/
├── data/
├── .gitignore
└── README.md
## 11. Testing and Validation

TrustCheck is tested using a labelled dataset containing scam, suspicious, and legitimate messages.

Testing covers:

- Detection of predefined warning signals
- Risk score and risk-level calculation
- API request and response validation
- Android–backend integration

The test results are used to identify incorrect detections and improve the rule-based detection logic.

## 12. Deployment

The TrustCheck backend is deployed using Render.

Android Application
        │
        │ HTTPS
        ▼
Render
        │
        ▼
FastAPI Backend
        │
        ├── Analysis Pipeline
        ├── Detection Engine
        └── Risk Scoring

Production backend:

https://trustcheck-p6fz.onrender.com/

The frontend uses the backend API for message analysis through:
```
POST /api/analyze
```

## 13. Current Limitations

The current prototype has several limitations:

- Detection is primarily rule-based.
- Detection quality depends on the defined rules and test dataset.
- Some suspicious messages may not be detected.
- Some legitimate messages may be classified as suspicious.
- A risk score should not be treated as absolute proof of fraud.

The architecture is designed so that the detection engine can be improved or extended in future versions without requiring major changes to the frontend.

## 14. Future Improvements

Possible future improvements include:

- Machine-learning-based detection
- Improved URL and domain reputation analysis
- Larger and more diverse datasets
- More advanced brand verification
- Continuous improvement of detection rules
- Additional security and privacy features
