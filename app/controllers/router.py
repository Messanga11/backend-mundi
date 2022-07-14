from fastapi import APIRouter
from .auth_controller import auth_router
from .user_controller import user_router
from .publication_controller import publication_router
from .auth_controller import auth_router


router = APIRouter()
router.include_router(auth_router)
router.include_router(user_router)
router.include_router(publication_router)
router.include_router(auth_router)