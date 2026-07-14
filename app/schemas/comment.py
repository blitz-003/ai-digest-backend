from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CommentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    content: str
    author_id: UUID
    article_id: UUID
    created_at: datetime
    updated_at: datetime


class CreateCommentRequest(BaseModel):
    content: str


class UpdateCommentRequest(BaseModel):
    content: str