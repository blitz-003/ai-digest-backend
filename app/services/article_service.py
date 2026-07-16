from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.category import Category
from app.models.article import Article
from app.models.profile import Profile
from app.schemas.article import (
    CreateArticleRequest,
    UpdateArticleRequest,
)

from app.utils.article import (
    calculate_reading_time,
    generate_slug,
)

class ArticleService:
    @staticmethod
    def get_all_articles(
        db: Session,
        page: int,
        limit: int,
        search: str | None,
        category_id,
    ):
        query = db.query(Article)

        query = query.filter()

        if search:
            query = query.filter(
                or_(
                    Article.title.ilike(f"%{search}%"),
                    Article.summary.ilike(f"%{search}%"),
                )
            )

        if category_id:
            query = query.filter(
                Article.category_id == category_id
            )

        return (
            query.order_by(
                Article.created_at.desc()
            )
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )
      

    @staticmethod
    def get_article(db: Session, article_id):
        return db.query(Article).filter(
            Article.id == article_id
        ).first()

    @staticmethod
    def create_article(
        db: Session,
        article_data: CreateArticleRequest,
        current_user: Profile,
    ):
        article = Article(
    title=article_data.title,
    slug=generate_slug(article_data.title),
    summary=article_data.summary,
    content=article_data.content,
    cover_image=article_data.cover_image,
    category_id=article_data.category_id,
    author_id=current_user.id,
    reading_time=calculate_reading_time(
        article_data.content
    ),
)

        db.add(article)
        db.commit()
        db.refresh(article)

        return article

    @staticmethod
    def update_article(
        db: Session,
        article: Article,
        article_data: UpdateArticleRequest,
    ):
        update_data = article_data.model_dump(
            exclude_unset=True
        )
        if "title" in update_data:
            update_data["slug"] = generate_slug(
                update_data["title"]
            )

        if "content" in update_data:
            update_data["reading_time"] = (
                calculate_reading_time(
                    update_data["content"]
                )
            )

        for field, value in update_data.items():
            setattr(article, field, value)

        db.commit()
        db.refresh(article)

        return article

    @staticmethod
    def delete_article(
        db: Session,
        article: Article,
    ):
        db.delete(article)
        db.commit()

        # ADD THIS HERE
    @staticmethod
    def check_article_permission(
        article: Article,
        current_user: Profile,
    ):
        if (
            article.author_id != current_user.id
            and current_user.role != "admin"
        ):
            raise PermissionError("Not allowed.")