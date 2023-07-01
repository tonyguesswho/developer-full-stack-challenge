from routers.api import api_router

from core.config import settings

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError


from starlette.middleware.cors import CORSMiddleware


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME, openapi_url=f"/openapi.json", docs_url="/"
    )
    # Set all CORS enabled origins
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    app.include_router(api_router, prefix=settings.API_STR)

    return app


app = create_app()


@app.get("/ping", name="Healthcheck", tags=["Healthcheck"])
async def healthcheck():
    return {"success": "pong!"}
