from sqlalchemy.orm import Session

from app.models.bookmark import Bookmark
from app.models.profile import Profile


class BookmarkService:

    @staticmethod
    def toggle_bookmark(
        db: Session,
        article_id,
        current_user: Profile,
    ):
        bookmark = (
            db.query(Bookmark)
            .filter(
                Bookmark.article_id == article_id,
                Bookmark.user_id == current_user.id,
            )
            .first()
        )

        if bookmark:
            db.delete(bookmark)
            db.commit()
            return {
                "bookmarked": False,
            }

        bookmark = Bookmark(
            article_id=article_id,
            user_id=current_user.id,
        )

        db.add(bookmark)
        db.commit()

        return {
            "bookmarked": True,
        }

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
            .all()
        )