from pydantic import BaseModel
from uuid import UUID

class CommentCreate(BaseModel):
    comment: str
    sentiment_analysis: str | None = None
    sentiment_score: str | None = None
    sentiment_keywords: str | None = None

class CommentRead(BaseModel):
    id: UUID
    comment: str
    sentiment_analysis: str | None
    sentiment_score: str | None
    sentiment_keywords: str | None
    draft_id: UUID