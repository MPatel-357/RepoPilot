
from fastapi import FastAPI

app = FastAPI(
    title="RepoPilot API",
    description="AI-powered codebase intelligence and impact analysis",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "RepoPilot",
        "version": "0.1.0"
    }

