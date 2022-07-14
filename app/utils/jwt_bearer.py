from typing import Union
from fastapi import Request, HTTPException, Depends, status
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer
from core import dependencies
from core.config import Config
import models
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from decouple import config

# Schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    uuid: Union[str, None] = None

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
SECRET_KEY = config("secret")
ALGORITHM = config("algorithm")

class JwtBearer(HTTPBearer):
    
    def verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return pwd_context.hash(password)
    
    def authenticate_user(self, phone_number: str, password: str):
        db = models.SessionLocal()
        user = db.query(models.UserModel).filter(models.UserModel.phonenumber == phone_number).first()
        if not user:
            raise Config.credentials_exception
        if not self.verify_password(password, user.password):
            raise Config.credentials_exception
        return user 

    def create_access_token(self, data: dict, expires_delta: Union[timedelta, None] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(day=30)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(dependencies.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    uuid = None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        uuid = payload.get("sub")
        if uuid is None:
            raise credentials_exception
    except JWTError as e:
        raise credentials_exception
    user = db.query(models.UserModel).filter(models.UserModel.uuid == uuid).first()
    if user is None:
        user = db.query(models.Provider).filter(models.Provider.uuid == uuid).first()
        if not user:
            raise credentials_exception
    return user

jwtBearer = JwtBearer()