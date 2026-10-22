
from fastapi import FastAPI

from app.api.repositories import router as repositories_router

app = FastAPI(
    title="RepoPilot API",
    description="AI-powered codebase intelligence and impact analysis",
    version="0.1.0",
)

app.include_router(repositories_router)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "RepoPilot",
        "version": "0.1.0",
    }
