from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_user
from app.dependencies.database import get_db
from app.models.profile import Profile
from app.services.article_service import ArticleService
from app.services.comment_service import CommentService
from app.schemas.comment import (
    CommentResponse,
    CreateCommentRequest,
    UpdateCommentRequest,
)

router = APIRouter(
    prefix="/comments",
    tags=["Comments"],
)


@router.get(
    "/article/{article_id}",
    response_model=list[CommentResponse],
)
def get_comments(
    article_id: UUID,
    db: Session = Depends(get_db),
):
    return CommentService.get_comments_by_article(
        db,
        article_id,
    )


@router.post(
    "/article/{article_id}",
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_comment(
    article_id: UUID,
    comment_data: CreateCommentRequest,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user),
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

    return CommentService.create_comment(
        db,
        article,
        current_user,
        comment_data,
    )


@router.patch(
    "/{comment_id}",
    response_model=CommentResponse,
)
def update_comment(
    comment_id: UUID,
    comment_data: UpdateCommentRequest,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user),
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

    if (
        comment.author_id != current_user.id
        and current_user.role != "admin"
    ):
        raise HTTPException(
            status_code=403,
            detail="Not allowed",
        )

    return CommentService.update_comment(
        db,
        comment,
        comment_data,
    )


@router.delete(
    "/{comment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_comment(
    comment_id: UUID,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user),
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

    if (
        comment.author_id != current_user.id
        and current_user.role != "admin"
    ):
        raise HTTPException(
            status_code=403,
            detail="Not allowed",
        )

    CommentService.delete_comment(
        db,
        comment,
    )