from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.core.config import settings
from app.core.limiter import limiter
from app.modules.auth.router import router as auth_router
from app.modules.projects.router import router as projects_router
from app.modules.tasks.router import router as tasks_router
from app.modules.notifications.router import router as notifications_router

app = FastAPI(title=settings.app_name, version="1.0.0", description="TaskFlow — API для управления проектами и задачами")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(CORSMiddleware, allow_origins=settings.allowed_origins, allow_credentials=True, allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"], allow_headers=["Authorization", "Content-Type"])
app.include_router(auth_router); app.include_router(projects_router); app.include_router(tasks_router); app.include_router(notifications_router)

@app.get("/", tags=["Health"])
def root(): return {"message": "TaskFlow API is running", "docs": "/docs"}

@app.get("/health", tags=["Health"])
def health(): return {"status": "ok"}
