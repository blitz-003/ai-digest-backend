from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_user
from app.dependencies.database import get_db
from app.dependencies.role import require_role
from app.models.profile import Profile
from app.schemas.article import (
    ArticleResponse,
    CreateArticleRequest,
    UpdateArticleRequest,
)
from app.services.article_service import ArticleService
from fastapi import Query

router = APIRouter(
    prefix="/articles",
    tags=["Articles"],
)


@router.get(
    "",
    response_model=list[ArticleResponse],
)
def get_articles(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: str | None = None,
    category_id: UUID | None = None,
    db: Session = Depends(get_db),
):
    return ArticleService.get_all_articles(
        db=db,
        page=page,
        limit=limit,
        search=search,
        category_id=category_id,
    )
@router.get(
    "/{article_id}",
    response_model=ArticleResponse,
)
def get_article(
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

    return article


@router.post(
    "",
    response_model=ArticleResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role("reader","author", "admin"))],
)
def create_article(
    article_data: CreateArticleRequest,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user),
):
    return ArticleService.create_article(
        db,
        article_data,
        current_user,
    )


@router.patch(
    "/{article_id}",
    response_model=ArticleResponse,
    dependencies=[Depends(require_role("reader","author", "admin"))],
)
def update_article(
    article_id: UUID,
    article_data: UpdateArticleRequest,
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
    try:
        ArticleService.check_article_permission(
            article,
            current_user,
        )
    except PermissionError as e:
        raise HTTPException(
            status_code=403,
            detail=str(e),
        )
    return ArticleService.update_article(
        db,
        article,
        article_data,
    )


@router.delete(
    "/{article_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_role("reader","author", "admin"))],
)
def delete_article(
    article_id: UUID,
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

    try:
        ArticleService.check_article_permission(
            article,
            current_user,
        )
    except PermissionError as e:
        raise HTTPException(
            status_code=403,
            detail=str(e),
        )

    ArticleService.delete_article(
        db,
        article,
    )