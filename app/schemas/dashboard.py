from pydantic import BaseModel


class DashboardStatsResponse(BaseModel):
    total_articles: int
    published_articles: int
    draft_articles: int