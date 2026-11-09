from fastapi import FastAPI

app = FastAPI(
    title="Diabetic Retinopathy API",
    description="API de dépistage de la rétinopathie diabétique",
    version="1.0.0"
)

@app.get("/")
def accueil():
    return {
        "message": "Bienvenue",
        "status": "online"
    }

@app.get("/api/v1/health")
def health_check():
    return {
        "status": "healthy",
        "service": "backend",
        "version": "1.0.0"
    }