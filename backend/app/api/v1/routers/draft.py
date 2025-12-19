from fastapi import APIRouter, Depends, HTTPException, UploadFile, Query, Response
from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession

from app.schemas.draft_schema import DraftRead
from app.crud.draft_crud import draft_crud
from app.api.deps import get_db, get_current_user
from app.models.user_model import User
from app.controllers.draft import draft_create, get_drafts_by_id_controller, generate_report_controller

router = APIRouter()

@router.post("/", response_model=DraftRead, status_code=201)
async def create_draft(
    file: UploadFile,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    draft = await draft_create(file=file, db=db, current_user=current_user)
    
    return draft

@router.get("/{draft_id}", response_model=DraftRead)
async def get_draft(
    draft_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    draft = await draft_crud.get(db, id=draft_id, user_id=current_user.id)
    if not draft:
        raise HTTPException(status_code=404, detail="Draft not found")
    return draft

@router.delete("/{draft_id}", status_code=204)
async def delete_draft(
    draft_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    draft = await draft_crud.remove(db, id=draft_id, user_id=current_user.id)
    if not draft:
        raise HTTPException(status_code=404, detail="Draft not found")
    return

@router.get("/", response_model=list[DraftRead])
async def get_drafts_by_id(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    limit: int = Query(100, ge=1, le=1000)
):
    drafts = await get_drafts_by_id_controller(db, limit, current_user)
    return drafts

@router.post("/{draft_id}/report")
async def generate_report(
    draft_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        report = await generate_report_controller(
            db=db,
            user_id=current_user.id,
            draft_id=draft_id,
            format="pdf"
        )
        
        return Response(
            content=report,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=draft_{draft_id}_report.pdf"}
        )
            
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Report generation failed: {str(e)}")