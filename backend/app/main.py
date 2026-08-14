import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.repositories.link_repository import InMemoryLinkRepository
from app.services.link_service import LinkService
from app.middleware.request_logger import RequestLoggerMiddleware
from app.routers.link_router import router as link_router
from app.routers.redirect_router import router as redirect_router
from app.schemas.link import ApiResponse, MetaResponse

def create_app(repo=None) -> FastAPI:
    app = FastAPI(
        title="Go Links API",
        description="Internal URL shortcut service written in Python FastAPI",
        version="1.0.0"
    )

    # Enable CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add custom request logger middleware
    app.add_middleware(RequestLoggerMiddleware)

    # Dependency Injection
    repository = repo or InMemoryLinkRepository(seed=True)
    app.state.repo = repository
    app.state.link_service = LinkService(repository)

    # Include Routers
    app.include_router(link_router)
    app.include_router(redirect_router)

    # Health Check Endpoint
    @app.get("/health", tags=["Health"])
    async def health_check():
        return {"status": "ok", "service": "go-links-python-backend"}

    # Centralized Exception Handler for HTTP Exceptions
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        req_id = getattr(request.state, "request_id", "unknown")
        
        status_code = getattr(exc, "status_code", 500)
        detail = getattr(exc, "detail", str(exc))

        if isinstance(detail, dict):
            err_code = detail.get("code", "INTERNAL_ERROR")
            err_msg = detail.get("message", "An error occurred")
        else:
            err_code = "VALIDATION_ERROR" if status_code == 422 else ("NOT_FOUND" if status_code == 404 else "INTERNAL_ERROR")
            err_msg = str(detail)

        return JSONResponse(
            status_code=status_code,
            content=ApiResponse(
                success=False,
                error={"code": err_code, "message": err_msg},
                meta=MetaResponse(requestId=req_id)
            ).model_dump()
        )

    return app

app = create_app()
