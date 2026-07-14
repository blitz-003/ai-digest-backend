from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_user
from app.dependencies.database import get_db
from app.dependencies.role import require_role

from app.models.profile import Profile

from app.schemas.article import ArticleResponse
from app.schemas.comment import CommentResponse
from app.schemas.dashboard import DashboardStatsResponse
from app.schemas.profile import ProfileResponse

from app.schemas.bookmark import BookmarkResponse
from app.services.dashboard_service import DashboardService


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


# =========================
# Reader Dashboard
# =========================

@router.get(
    "/profile",
    response_model=ProfileResponse,
)
def my_profile(
    current_user: Profile = Depends(get_current_user),
):
    return DashboardService.get_profile(current_user)


@router.get(
    "/bookmarks",
    response_model=list[BookmarkResponse],
)
def my_bookmarks(
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user),
):
    return DashboardService.get_my_bookmarks(
        db,
        current_user,
    )

@router.get(
    "/comments",
    response_model=list[CommentResponse],
)
def my_comments(
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user),
):
    return DashboardService.get_my_comments(
        db,
        current_user,
    )


# =========================
# Author Dashboard
# =========================

@router.get(
    "/articles",
    response_model=list[ArticleResponse],
    dependencies=[Depends(require_role("author", "admin"))],
)
def my_articles(
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user),
):
    return DashboardService.get_my_articles(
        db,
        current_user,
    )


@router.get(
    "/stats",
    response_model=DashboardStatsResponse,
    dependencies=[Depends(require_role("author", "admin"))],
)
def dashboard_stats(
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user),
):
    return DashboardService.get_stats(
        db,
        current_user,
    )