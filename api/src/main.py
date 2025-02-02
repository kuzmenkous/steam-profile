from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from .core.config import settings
from .core.caching import init_caching

from .profile.router import router as profile_router
from .user.router import router as user_router


# Lifespan events
@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: F811
    # Initialize the cache backend
    init_caching()
    yield


# App configuration
app = FastAPI(
    title=settings.app.name,
    debug=settings.app.debug,
    version=str(settings.app.version),
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static directory
app.mount(
    f"/{settings.static.directory}",
    StaticFiles(directory=settings.static.directory),
)

# Include routers
ROUTERS: list[APIRouter] = [profile_router, user_router]
for router in ROUTERS:
    app.include_router(router, prefix=f"/api/v{settings.app.version}")
