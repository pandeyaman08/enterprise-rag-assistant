from fastapi import FastAPI

from app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


@app.get("/health", tags=["System"])
async def health_check() -> dict[str, str]:
    """
    Liveness probe endpoint.

    Used by Docker, load balancers, and (later) Kubernetes readiness/liveness
    probes to verify the service is up. Without it, infrastructure has no
    automated way to know if the app is healthy or should be restarted.
    """
    return {"status": "ok", "app": settings.APP_NAME, "environment": settings.APP_ENV}
