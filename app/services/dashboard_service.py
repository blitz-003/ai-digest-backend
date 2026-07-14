from sqlalchemy.orm import Session

from app.models.article import Article
from app.models.bookmark import Bookmark
from app.models.comment import Comment
from app.models.profile import Profile


class DashboardService:

    @staticmethod
    def get_profile(
        current_user: Profile,
    ):
        return current_user

    @staticmethod
    def get_my_bookmarks(
        db: Session,
        current_user: Profile,
    ):
        return (
            db.query(Bookmark)
            .filter(
                Bookmark.user_id == current_user.id
            )
            .order_by(
                Bookmark.created_at.desc()
            )
            .all()
        )

    @staticmethod
    def get_my_comments(
        db: Session,
        current_user: Profile,
    ):
        return (
            db.query(Comment)
            .filter(
                Comment.author_id == current_user.id
            )
            .order_by(
                Comment.created_at.desc()
            )
            .all()
        )

    @staticmethod
    def get_my_articles(
        db: Session,
        current_user: Profile,
    ):
        return (
            db.query(Article)
            .filter(
                Article.author_id == current_user.id
            )
            .order_by(
                Article.created_at.desc()
            )
            .all()
        )

    @staticmethod
    def get_stats(
        db: Session,
        current_user: Profile,
    ):
        total_articles = (
            db.query(Article)
            .filter(
                Article.author_id == current_user.id
            )
            .count()
        )

        published_articles = (
            db.query(Article)
            .filter(
                Article.author_id == current_user.id,
                Article.status == "published",
            )
            .count()
        )

        draft_articles = (
            db.query(Article)
            .filter(
                Article.author_id == current_user.id,
                Article.status == "draft",
            )
            .count()
        )

        return {
            "total_articles": total_articles,
            "published_articles": published_articles,
            "draft_articles": draft_articles,
        }