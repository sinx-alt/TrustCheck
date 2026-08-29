from sqlalchemy import String, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class VerifiedDomain(Base):
    __tablename__ = "verified_domains"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    brand_name: Mapped[str] = mapped_column(String, unique=True, index=True)
    domain: Mapped[str] = mapped_column(String)


class AnalysisHistory(Base):
    __tablename__ = "analysis_history"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    message: Mapped[str] = mapped_column(String)
    risk_score: Mapped[int] = mapped_column(Integer)
    risk_level: Mapped[str] = mapped_column(String)