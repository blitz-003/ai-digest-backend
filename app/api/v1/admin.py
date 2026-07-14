from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_user
from app.dependencies.database import get_db
from app.dependencies.role import require_role

from app.models.profile import Profile

from app.schemas.admin import AdminStatsResponse
from app.schemas.article import ArticleResponse
from app.schemas.category import CategoryResponse
from app.schemas.comment import CommentResponse
from app.schemas.profile import (
    ProfileResponse,
    UpdateRoleRequest,
)

from app.services.admin_service import AdminService
from app.services.article_service import ArticleService
from app.services.comment_service import CommentService

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(require_role("admin"))],
)


# ==========================
# Users
# ==========================

@router.get(
    "/users",
    response_model=list[ProfileResponse],
)
def get_users(
    db: Session = Depends(get_db),
):
    return AdminService.get_users(db)


@router.patch(
    "/users/{user_id}/role",
    response_model=ProfileResponse,
)
def update_user_role(
    user_id: UUID,
    role_data: UpdateRoleRequest,
    db: Session = Depends(get_db),
):
    user = AdminService.get_user(
        db,
        user_id,
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return AdminService.update_role(
        db,
        user,
        role_data.role,
    )


# ==========================
# Articles
# ==========================

@router.get(
    "/articles",
    response_model=list[ArticleResponse],
)
def get_articles(
    db: Session = Depends(get_db),
):
    return AdminService.get_articles(db)


@router.delete(
    "/articles/{article_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_article(
    article_id: UUID,
    db: Session = Depends(get_db),
):
    article = ArticleService.get_article(
        db,
        article_id,
    )

    if not article:
        raise HTTPException(
            status_code=404,
            detail="Article not found",
        )

    AdminService.delete_article(
        db,
        article,
    )


# ==========================
# Comments
# ==========================

@router.get(
    "/comments",
    response_model=list[CommentResponse],
)
def get_comments(
    db: Session = Depends(get_db),
):
    return AdminService.get_comments(db)


@router.delete(
    "/comments/{comment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_comment(
    comment_id: UUID,
    db: Session = Depends(get_db),
):
    comment = CommentService.get_comment(
        db,
        comment_id,
    )

    if not comment:
        raise HTTPException(
            status_code=404,
            detail="Comment not found",
        )

    AdminService.delete_comment(
        db,
        comment,
    )


# ==========================
# Categories
# ==========================

@router.get(
    "/categories",
    response_model=list[CategoryResponse],
)
def get_categories(
    db: Session = Depends(get_db),
):
    return AdminService.get_categories(db)


# ==========================
# Statistics
# ==========================

@router.get(
    "/stats",
    response_model=AdminStatsResponse,
)
def get_stats(
    db: Session = Depends(get_db),
):
    return AdminService.get_stats(db)