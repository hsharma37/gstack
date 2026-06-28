from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .api.v1 import router as api_router
from .database import init_db

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.api_prefix)


@app.on_event("startup")
async def on_startup() -> None:
    init_db()


@app.get("/")
async def root() -> dict[str, str]:
    return {
        "status": "ICTOS backend ready",
        "version": settings.app_version,
        "phase": "3",
    }


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "healthy"}
