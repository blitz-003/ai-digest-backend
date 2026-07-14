from fastapi import FastAPI

from app.core.config import settings
from app.db.database import engine
from app.integrations.supabase import supabase
from app.api.v1 import api_router
from app.api.v1.profile import router as profile_router
from app.api.v1.category import router as category_router
from app.api.v1.admin import router as admin_router
from app.api.v1.article import router as article_router
from app.api.v1.comment import router as comment_router





app = FastAPI(title="AI Digest API")

app.include_router(api_router, prefix="/api/v1")

app.include_router(profile_router, prefix="/api/v1")
app.include_router(category_router, prefix="/api/v1")
app.include_router(admin_router, prefix="/api/v1")


app.include_router(comment_router, prefix="/api/v1")


app.include_router(article_router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "AI Digest API"}


@app.get("/health")
def health():
    return {
        "status": "ok",
        "database": str(engine.url).split("@")[-1],
        "supabase": settings.SUPABASE_URL,
    }



