import logging

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from backend.config import get_settings
from backend.database import init_db, get_db
from backend.schemas import AnalyzeRequest, AnalyzeResponse
from backend.pipeline import analyze_message

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
settings = get_settings()

app = FastAPI(title="TrustCheck API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.exception_handler(Exception)
async def unhandled_exception_handler(request, exc):
    logger.exception("Unhandled error while processing request")
    return JSONResponse(
        status_code=500,
        content={"detail": "Something went wrong analyzing this message. Please try again."},
    )


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "environment": settings.environment}


@app.post("/api/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest, db: Session = Depends(get_db)) -> AnalyzeResponse:
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    try:
        result = analyze_message(request)
    except Exception:
        logger.exception("Detection pipeline failed")
        raise HTTPException(status_code=502, detail="Detection engine failed to process this message.")

    # Optional: log to history table, non-blocking — never let a logging failure break the response
    try:
        from models import AnalysisHistory
        db.add(AnalysisHistory(
            message=request.message,
            risk_score=result.risk_score,
            risk_level=result.risk_level,
        ))
        db.commit()
    except Exception:
        logger.warning("Failed to write analysis history — continuing anyway")
        db.rollback()

    return result