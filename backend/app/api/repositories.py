
from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.repository_scanner import scan_repository
from app.services.dependency_graph import build_dependency_graph
from app.services.impact_analyzer import analyze_impact


router = APIRouter(
    prefix="/api/repositories",
    tags=["Repositories"],
)

BACKEND_ROOT = Path(__file__).resolve().parents[2]


class ImpactRequest(BaseModel):
    target_file: str


@router.post("/scan")
def scan_local_repository():
    return scan_repository(str(BACKEND_ROOT))


@router.get("/graph")
def get_dependency_graph():
    return build_dependency_graph(str(BACKEND_ROOT))


@router.post("/impact")
def get_change_impact(request: ImpactRequest):
    try:
        return analyze_impact(
            str(BACKEND_ROOT),
            request.target_file,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        ) from error
