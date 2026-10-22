
from pathlib import Path

from fastapi import APIRouter

from app.services.repository_scanner import scan_repository

router = APIRouter(
    prefix="/api/repositories",
    tags=["Repositories"],
)


BACKEND_ROOT = Path(__file__).resolve().parents[2]


@router.post("/scan")
def scan_local_repository():
    """
    Scan RepoPilot's backend and return its structure.
    """
    return scan_repository(str(BACKEND_ROOT))
