# Standard library imports
import datetime
from typing import List

# Third-party imports
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import Column, Integer, Float, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# ------------------------------------------------------------------------------
# Database Setup
# ------------------------------------------------------------------------------

# Replace this with your actual PostgreSQL connection string.
DATABASE_URL = (
    "postgresql+asyncpg://health_db_scy8_user:dBza7ktDGvrHkUMwREPHzraQ4BGv3dsH@"
    "dpg-cuunb823esus73aaskng-a.oregon-postgres.render.com/health_db_scy8"
)

# Base class for SQLAlchemy models.
Base = declarative_base()

class HealthMetric(Base):
    """
    SQLAlchemy model for storing wearable health data.
    """
    __tablename__ = "health_metrics"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    timestamp = Column(DateTime(timezone=True), index=True)
    heart_rate = Column(Integer)
    steps = Column(Integer)
    calories = Column(Float)

# ------------------------------------------------------------------------------
# Pydantic Schemas
# ------------------------------------------------------------------------------

class HealthMetricIn(BaseModel):
    """
    Pydantic model for incoming health data.
    """
    user_id: int
    timestamp: datetime.datetime
    heart_rate: int
    steps: int
    calories: float

class AggregatedMetrics(BaseModel):
    """
    Pydantic model for the aggregated health metrics response.
    """
    average_heart_rate: float
    total_steps: int
    total_calories: float

# ------------------------------------------------------------------------------
# Async Database Engine and Session Setup
# ------------------------------------------------------------------------------

# Create an asynchronous engine for the database.
engine = create_async_engine(DATABASE_URL, echo=True)
# SessionLocal is our async session maker.
SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# ------------------------------------------------------------------------------
# FastAPI Application Setup
# ------------------------------------------------------------------------------

app = FastAPI(title="Real-Time Health Metrics API")

@app.on_event("startup")
async def on_startup():
    """
    Create database tables on startup.
    """
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

# ------------------------------------------------------------------------------
# API Endpoints
# ------------------------------------------------------------------------------

@app.post("/ingest")
async def ingest_data(metrics: List[HealthMetricIn]):
    """
    Ingest a batch of health metric records.
    """
    async with SessionLocal() as session:
        for record in metrics:
            new_record = HealthMetric(
                user_id=record.user_id,
                timestamp=record.timestamp,
                heart_rate=record.heart_rate,
                steps=record.steps,
                calories=record.calories,
            )
            session.add(new_record)
        await session.commit()
    return {"message": f"Ingested {len(metrics)} records successfully"}

@app.get("/metrics", response_model=AggregatedMetrics)
async def get_metrics(user_id: int, start: datetime.datetime, end: datetime.datetime):
    """
    Retrieve aggregated health metrics for a specified user and time range.
    """
    async with SessionLocal() as session:
        query = (
            select(
                func.avg(HealthMetric.heart_rate).label("average_heart_rate"),
                func.sum(HealthMetric.steps).label("total_steps"),
                func.sum(HealthMetric.calories).label("total_calories")
            )
            .where(HealthMetric.user_id == user_id)
            .where(HealthMetric.timestamp >= start)
            .where(HealthMetric.timestamp <= end)
        )
        result = await session.execute(query)
        agg = result.fetchone()

        if agg.average_heart_rate is None:
            raise HTTPException(
                status_code=404, detail="No data found for given parameters"
            )

        return AggregatedMetrics(
            average_heart_rate=round(agg.average_heart_rate, 2),
            total_steps=agg.total_steps,
            total_calories=agg.total_calories
        )
