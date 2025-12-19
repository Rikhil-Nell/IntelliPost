from fastapi import APIRouter, Depends, BackgroundTasks
from sqlmodel.ext.asyncio.session import AsyncSession

# Imports from your project structure
from app.api.deps import get_db, get_current_user
from app.services.r2_service import R2Service
from app.controllers.r2 import genarate_upload_url
from app.controllers.mail import initialize_mail, process_mail_task, get_all_mails, get_mail
from app.models.user_model import User

router = APIRouter()

# Endpoint 1: The Handshake
@router.post("/generate_upload_url")
async def genreate_upload_url(current_user = Depends(get_current_user)):
    return await genarate_upload_url(user_id=current_user.id)

# Endpoint 2: The Trigger
@router.post("/process")
async def process_mail(
    file_key: str,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_mail = await initialize_mail(user_id=current_user.id, file_key=file_key, db=db)
    
    background_tasks.add_task(
        process_mail_task, 
        new_mail.id, 
        file_key, 
        db
    )
    
    return new_mail

# # Endpoint 3: The History (With Dynamic Image Links)
# @router.get("/", response_model=list[MailResponse])
# def get_mail_history(
#     db: AsyncSession = Depends(get_db),
#     current_user = Depends(get_current_user)
# ):
#     r2 = R2Service()
    
#     # Fetch user's mails
#     statement = select(Mail).where(Mail.user_id == current_user.id).order_by(Mail.created_at.desc())
#     results = db.exec(statement).all()
    
#     # Hydrate with fresh URLs
#     response_list = []
#     for mail in results:
#         # Generate a link valid for 1 hour
#         temp_url = r2.generate_read_url(mail.image_s3_key)
        
#         # We manually map this because the DB doesn't have the signed URL
#         mail_resp = MailResponse.model_validate(mail)
#         mail_resp.image_url = temp_url 
#         response_list.append(mail_resp)
        
#     return response_list