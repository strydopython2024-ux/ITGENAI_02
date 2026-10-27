from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.database import init_db
from app.routes.auth import router as auth_router
from app.routes.data import router as data_router
from app.routes.analysis import router as analysis_router
from app.routes.dashboard import router as dashboard_router
from app.routes.ai import router as ai_router
from app.routes import ai


@asynccontextmanager
async def lifespan(_app):
    init_db()
    yield


app = FastAPI(
    title="Intelligent Information Flow API", version="1.0.0", lifespan=lifespan
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5000", "http://localhost:5000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router)
app.include_router(data_router)
app.include_router(analysis_router)
app.include_router(dashboard_router)
app.include_router(ai.router)


@app.get("/health")
def health():
    return {"success": True, "message": "Backend is running"}
