from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_user
from app.dependencies.database import get_db
from app.models.profile import Profile
from app.services.bookmark_service import BookmarkService

router = APIRouter(
    prefix="/bookmarks",
    tags=["Bookmarks"],
)


@router.post("/{article_id}")
def toggle_bookmark(
    article_id: UUID,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user),
):
    return BookmarkService.toggle_bookmark(
        db,
        article_id,
        current_user,
    )


@router.get("")
def get_my_bookmarks(
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user),
):
    return BookmarkService.get_my_bookmarks(
        db,
        current_user,
    )