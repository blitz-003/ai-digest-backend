from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict
from typing import Literal


class ArticleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    slug: str
    summary: str
    content: str
    cover_image: str | None = None
    status: str
    view_count: int
    reading_time: int
    is_featured: bool
    published_at: datetime | None = None
    created_at: datetime
    updated_at: datetime
    author_id: UUID
    category_id: UUID



    title: str
    slug: str
    summary: str
    content: str
    cover_image: str | None = None
    category_id: UUID
class CreateArticleRequest(BaseModel):
    title: str
    summary: str
    content: str
    cover_image: str | None = None
    category_id: UUID
    status: Literal[
        "draft",
        "published",
        "archived",
    ] = "published"

class UpdateArticleRequest(BaseModel):
    title: str | None = None
    slug: str | None = None
    summary: str | None = None
    content: str | None = None
    cover_image: str | None = None
    category_id: UUID | None = None
    status: Literal[
    "draft",
    "published",
    "archived",
] | None = None
    

class ArticleQueryParams(BaseModel):
    page: int = 1
    limit: int = 10
    search: str | None = None
    category_id: UUID | None = None