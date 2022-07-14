
from typing import List
from fastapi import APIRouter, Depends, Request
from utils.jwt_bearer import get_current_user, jwtBearer
import schemas
from core import dependencies
import cruds
import models

user_router = APIRouter(prefix="/users", tags=["users"])

@user_router.get("", response_model=schemas.DataList[schemas.UserInfo])
def get_all_users(
    request: Request,
    db=Depends(dependencies.get_db),
    page: int = 1,
    per_page: int = 10,
    order="desc",
    order_field: str = "first_name",
    keyword: str = None,
    current_user: models.UserModel=Depends(get_current_user)):
    return cruds.user_crud.get_users(db, request, page, per_page, order, order_field, keyword)

@user_router.get("/verify")
def verify_user(token:str, db=Depends(dependencies.get_db)):
    return cruds.user_crud.verify_user(token, db)

@user_router.get("/{phone_number}")
def get_single_user(phone_number:str, db=Depends(dependencies.get_db)):
    return cruds.user_crud.get_single_user(phone_number, db)

@user_router.post("")
def create_user(user_in:schemas.UserIn ,db=Depends(dependencies.get_db)):
    return cruds.user_crud.create(user_in, db)

@user_router.put("")
def update_user(user_in:schemas.UserUpdate, db=Depends(dependencies.get_db)):
    profile_pic = cruds.storage_crud.store_file(db)
    user_obj = user_in.dict(exclude=("profile_base_64"))
    return cruds.user_crud.update(user_in, db)

@user_router.delete("/{user_uuid}")
def get_single_user(
    user_uuid:str,
    db=Depends(dependencies.get_db),
    current_user: models.UserModel=Depends(get_current_user)):
    return cruds.user_crud.delete(user_uuid, db)

def check_user(data:schemas.LoginUserSchema, db=Depends(dependencies.get_db)):
    user = cruds.user_crud.get_single_user_phone_number(data.phone_number, db)
    if user:
        return user
    return None

@user_router.post("/login")
def login_provider(login_form:schemas.LoginUserSchema, db=Depends(dependencies.get_db)):
    return jwtBearer.authenticate_user(phone_number=login_form.username, password=login_form.password)