from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app

from clincode_api.config import settings
from clincode_api.db.session import engine, Base
from clincode_api.auth.routes import router as auth_router
from clincode_api.routes.documents import router as documents_router
from clincode_api.routes.suggestions import router as suggestions_router
from clincode_api.routes.review import router as review_router
from clincode_api.routes.queries import router as queries_router
from clincode_api.routes.export import router as export_router
from clincode_api.routes.admin import router as admin_router
from clincode_api.routes.investigate import router as investigate_router


def create_app() -> FastAPI:
    """FastAPI application factory for ClinCode API Service."""
    # Ensure database schema is ready
    Base.metadata.create_all(bind=engine)

    app = FastAPI(
        title=settings.PROJECT_NAME,
        version="0.1.0",
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url="/docs"
    )

    # Configure CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Mount Prometheus metrics endpoint
    metrics_app = make_asgi_app()
    app.mount("/metrics", metrics_app)

    # Health check endpoint
    @app.get("/health", tags=["Health"])
    def health_check():
        return {
            "status": "healthy",
            "service": "clincode_api",
            "database": "connected"
        }

    # Include routers under API V1 prefix
    v1_router_prefix = settings.API_V1_STR
    app.include_router(auth_router, prefix=v1_router_prefix)
    app.include_router(documents_router, prefix=v1_router_prefix)
    app.include_router(suggestions_router, prefix=v1_router_prefix)
    app.include_router(review_router, prefix=v1_router_prefix)
    app.include_router(queries_router, prefix=v1_router_prefix)
    app.include_router(export_router, prefix=v1_router_prefix)
    app.include_router(admin_router, prefix=v1_router_prefix)
    app.include_router(investigate_router, prefix=v1_router_prefix)

    return app


app = create_app()
