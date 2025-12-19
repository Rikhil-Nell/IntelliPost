from fastapi import APIRouter
from .routers import login, draft, comment

router = APIRouter()

router.include_router(login.router, prefix="/login", tags=["login"])
router.include_router(draft.router, prefix="/draft", tags=["draft"])
router.include_router(comment.router, prefix="/comment", tags=["comment"])
