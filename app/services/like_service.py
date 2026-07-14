from sqlalchemy.orm import Session

from app.models.like import Like
from app.models.profile import Profile


class LikeService:

    @staticmethod
    def toggle_like(
        db: Session,
        article_id,
        current_user: Profile,
    ):
        like = (
            db.query(Like)
            .filter(
                Like.article_id == article_id,
                Like.user_id == current_user.id,
            )
            .first()
        )

        if like:
            db.delete(like)
            db.commit()
            return {
                "liked": False,
            }

        like = Like(
            article_id=article_id,
            user_id=current_user.id,
        )

        db.add(like)
        db.commit()

        return {
            "liked": True,
        }

    @staticmethod
    def count_likes(
        db: Session,
        article_id,
    ):
        return (
            db.query(Like)
            .filter(
                Like.article_id == article_id
            )
            .count()
        )