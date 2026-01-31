from fastapi import FastAPI

from .router import router


def create_app() -> FastAPI:
    """Application factory for the Surf Forecast API."""
    app = FastAPI(
        title="Surf Forecast API",
        description="Wave and surf conditions for any location.",
        version="1.0.0",
    )
    app.include_router(router)
    return app


app = create_app()
