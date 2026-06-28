from fastapi import APIRouter

router = APIRouter()

from .analytics import router as analytics_router
from .research import router as research_router
from .trades import router as trades_router
from .plans import router as plans_router
from .journal import router as journal_router
from .risk import router as risk_router
from .health import router as health_router

router.include_router(analytics_router, prefix="/analytics", tags=["analytics"])
router.include_router(research_router, prefix="/research", tags=["research"])
router.include_router(trades_router, prefix="/trades", tags=["trades"])
router.include_router(plans_router, prefix="/plans", tags=["plans"])
router.include_router(journal_router, prefix="/journal", tags=["journal"])
router.include_router(risk_router, prefix="/risk", tags=["risk"])
router.include_router(health_router, prefix="/health", tags=["health"])
