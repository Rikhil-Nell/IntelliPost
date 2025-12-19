from app.crud.draft_crud import draft_crud
from app.schemas.draft_schema import DraftCreate, DraftRead
from app.utils.pdf_extractor import extract_text_from_pdf
from app.utils.agent import summary_agent
from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession
from app.utils.report_generator import generate_draft_report_data, generate_html_report, html_to_pdf

async def draft_create(file, db, current_user):
    draft = extract_text_from_pdf(file.file)
    summary = await summary_agent.run(draft)
    draft_in = DraftCreate(draft=draft, summary=summary.output)
    draft = await draft_crud.create(db, obj_in=draft_in, user_id=current_user.id)
    return draft

async def get_drafts_by_id_controller(
    db: AsyncSession,
    limit: int,
    current_user,
):
    return await draft_crud.get_drafts_by_user(db, user_id=current_user.id, limit=limit)

#make a controller for report generation
async def generate_report_controller(
        db: AsyncSession,
        user_id: UUID,
        draft_id: UUID,
        format : str = "json"
):
    try:
        report_data = await generate_draft_report_data(db,draft_id,user_id)

        if format == "html":
            return generate_html_report(report_data)
        elif format == "pdf":
            html_content = generate_html_report(report_data)
            return html_to_pdf(html_content)
        else:
            return report_data 
    except ValueError as e:
        raise e
    except Exception as e:
        raise Exception(f"Report generation failed: {str(e)}")

async def get_report_controller(
    db: AsyncSession,
    user_id: UUID,
    draft_id: UUID
):
    """Get report data in JSON format"""
    return await generate_draft_report_data(db, draft_id, user_id)