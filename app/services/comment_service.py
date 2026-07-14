from sqlalchemy.orm import Session

from app.models.article import Article
from app.models.comment import Comment
from app.models.profile import Profile
from app.schemas.comment import (
    CreateCommentRequest,
    UpdateCommentRequest,
)


class CommentService:

    @staticmethod
    def get_comments_by_article(
        db: Session,
        article_id,
    ):
        return (
            db.query(Comment)
            .filter(Comment.article_id == article_id)
            .order_by(Comment.created_at.desc())
            .all()
        )

    @staticmethod
    def get_comment(
        db: Session,
        comment_id,
    ):
        return (
            db.query(Comment)
            .filter(Comment.id == comment_id)
            .first()
        )

    @staticmethod
    def create_comment(
        db: Session,
        article: Article,
        current_user: Profile,
        comment_data: CreateCommentRequest,
    ):
        comment = Comment(
            content=comment_data.content,
            author_id=current_user.id,
            article_id=article.id,
        )

        db.add(comment)
        db.commit()
        db.refresh(comment)

        return comment

    @staticmethod
    def update_comment(
        db: Session,
        comment: Comment,
        comment_data: UpdateCommentRequest,
    ):
        comment.content = comment_data.content

        db.commit()
        db.refresh(comment)

        return comment

    @staticmethod
    def delete_comment(
        db: Session,
        comment: Comment,
    ):
        db.delete(comment)
        db.commit()