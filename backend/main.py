from fastapi import FastAPI

from .database import Base, engine
from .router import router


def create_app() -> FastAPI:
    """Application factory for the surf school booking API."""
    # Simple auto-migration for dev; for production use Alembic
    Base.metadata.create_all(bind=engine)

    app = FastAPI(title="Surf School Booking API")
    app.include_router(router)
    return app


app = create_app()


