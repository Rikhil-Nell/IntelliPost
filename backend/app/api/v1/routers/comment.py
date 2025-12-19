from fastapi import APIRouter, Depends, UploadFile, File, status, Query
from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession

from app.schemas.comment_schema import CommentCreate, CommentRead
from app.api.deps import get_db, get_current_user
from app.models.user_model import User
from app.controllers.comment import (
    add_comment_controller,
    add_comments_from_csv_controller,
    get_comments_by_draft_controller,
)

router = APIRouter()

@router.post("/draft/{draft_id}", response_model=CommentRead, status_code=201)
async def add_comment(
    draft_id: UUID,
    comment_in: CommentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await add_comment_controller(draft_id, comment_in, db)

@router.post("/draft/{draft_id}/csv", response_model=list[CommentRead], status_code=201)
async def add_comments_from_csv(
    draft_id: UUID,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await add_comments_from_csv_controller(draft_id, file, db)

@router.get("/draft/{draft_id}", response_model=list[CommentRead])
async def get_comments_by_draft(
    draft_id: UUID,
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    comments = await get_comments_by_draft_controller(draft_id, limit, db)
    return comments