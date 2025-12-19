from app.models.comment_model import Comment
from app.schemas.comment_schema import CommentCreate
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from uuid import UUID

class CommentCRUD:
    def __init__(self, model):
        self.model = model

    async def create(self, db: AsyncSession, *, obj_in: CommentCreate, draft_id: UUID) -> Comment:
        db_obj = Comment(comment=obj_in.comment, 
                        sentiment_analysis=obj_in.sentiment_analysis,
                        sentiment_score=obj_in.sentiment_score,
                        sentiment_keywords=obj_in.sentiment_keywords,
                        draft_id=draft_id)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def create_many(self, db: AsyncSession, *, objs_in: list[CommentCreate], draft_id: UUID) -> list[Comment]:
        comments = []
        for obj_in in objs_in:
            db_obj = Comment(comment=obj_in.comment, 
                sentiment_analysis=obj_in.sentiment_analysis,
                sentiment_score=obj_in.sentiment_score,
                sentiment_keywords=obj_in.sentiment_keywords,
                draft_id=draft_id)
            db.add(db_obj)
            comments.append(db_obj)
        await db.commit()
        for db_obj in comments:
            await db.refresh(db_obj)
        return comments

    async def get_by_draft_id(
        self, db: AsyncSession, draft_id: UUID, limit: int = 100
    ) -> list[Comment]:
        result = await db.exec(
            select(Comment)
            .where(Comment.draft_id == draft_id)
            .limit(limit)
            .order_by(Comment.created_at.desc())
        )
        return result.all()

comment_crud = CommentCRUD(Comment)