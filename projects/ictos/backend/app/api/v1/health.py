from fastapi import APIRouter
from typing import Any

router = APIRouter()

@router.get("/")
async def health() -> dict[str, Any]:
    return {"status": "healthy", "service": "ictos-backend"}
