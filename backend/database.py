import json
import logging
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from config import get_settings
from models import Base, VerifiedDomain
from typing import Generator

logger = logging.getLogger(__name__)
settings = get_settings()

connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
engine = create_engine(settings.database_url, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

VERIFIED_DOMAINS_PATH = Path(__file__).parent / "data" / "verified_domains.json"


def init_db() -> None:
    """Create tables and reseed verified domains. Safe to call on every startup —
    handles Render's free-tier ephemeral filesystem resetting on redeploy."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(VerifiedDomain).count() == 0 and VERIFIED_DOMAINS_PATH.exists():
            with open(VERIFIED_DOMAINS_PATH) as f:
                for entry in json.load(f):
                    db.add(VerifiedDomain(brand_name=entry["brand"], domain=entry["domain"]))
            db.commit()
            logger.info("Seeded verified_domains table")
    finally:
        db.close()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()