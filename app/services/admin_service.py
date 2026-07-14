from sqlalchemy.orm import Session

from app.models.article import Article
from app.models.category import Category
from app.models.comment import Comment
from app.models.profile import Profile


class AdminService:

    @staticmethod
    def get_users(
        db: Session,
    ):
        return (
            db.query(Profile)
            .order_by(Profile.created_at.desc())
            .all()
        )

    @staticmethod
    def get_articles(
        db: Session,
    ):
        return (
            db.query(Article)
            .order_by(Article.created_at.desc())
            .all()
        )

    @staticmethod
    def get_comments(
        db: Session,
    ):
        return (
            db.query(Comment)
            .order_by(Comment.created_at.desc())
            .all()
        )

    @staticmethod
    def get_categories(
        db: Session,
    ):
        return (
            db.query(Category)
            .order_by(Category.created_at.desc())
            .all()
        )

    @staticmethod
    def get_stats(
        db: Session,
    ):
        return {
            "users": db.query(Profile).count(),
            "articles": db.query(Article).count(),
            "comments": db.query(Comment).count(),
            "categories": db.query(Category).count(),
        }

    @staticmethod
    def get_user(
        db: Session,
        user_id,
    ):
        return (
            db.query(Profile)
            .filter(Profile.id == user_id)
            .first()
        )

    @staticmethod
    def update_role(
        db: Session,
        user: Profile,
        role: str,
    ):
        user.role = role

        db.commit()
        db.refresh(user)

        return user

    @staticmethod
    def delete_article(
        db: Session,
        article: Article,
    ):
        db.delete(article)
        db.commit()

    @staticmethod
    def delete_comment(
        db: Session,
        comment: Comment,
    ):
        db.delete(comment)
        db.commit()