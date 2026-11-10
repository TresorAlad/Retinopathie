from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database.connection import Base, engine
from app.models import User, Patient, Screening
from app.routes.auth import router as auth_router
from app.routes.patients import router as patients_router
from app.routes.screenings import router as screenings_router
from app.routes.health import router as health_router
from app.routes.mobile import router as mobile_router
from app.routes.blockchain import router as blockchain_router
from app.database.connection import SessionLocal
from app.services.system_user import ensure_mobile_system_user

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        ensure_mobile_system_user(db)
    finally:
        db.close()
    yield

app = FastAPI(
    title="Diabetic Retinopathy API",
    description="API de dépistage de la rétinopathie diabétique",
    version="1.0.0",
    lifespan=lifespan,
)
app.include_router(auth_router)
app.include_router(patients_router)
app.include_router(screenings_router)
app.include_router(health_router)
app.include_router(mobile_router)
app.include_router(blockchain_router)

@app.get("/")
def accueil():
    return {"message": "Bienvenue sur l'API de dépistage de la rétinopathie diabétique", "status": "online"}

@app.get("/api/v1/health")
def health_check():
    return {"status": "healthy", "service": "backend", "version": "1.0.0"}
