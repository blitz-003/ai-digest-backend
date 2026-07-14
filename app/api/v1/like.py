from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_user
from app.dependencies.database import get_db
from app.models.profile import Profile
from app.services.like_service import LikeService

router = APIRouter(
    prefix="/articles",
    tags=["Likes"],
)


@router.post("/{article_id}/like")
def toggle_like(
    article_id: UUID,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user),
):
    return LikeService.toggle_like(
        db,
        article_id,
        current_user,
    )


@router.get("/{article_id}/likes")
def get_likes(
    article_id: UUID,
    db: Session = Depends(get_db),
):
    return {
        "likes": LikeService.count_likes(
            db,
            article_id,
        )
    }