from pydantic import BaseModel


class AdminStatsResponse(BaseModel):
    users: int
    articles: int
    comments: int
    categories: int