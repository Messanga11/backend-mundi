from .publicaion_schema import *
from .user_schemas import *

from typing import Any, List, TypeVar, Generic
from pydantic.generics import GenericModel
from pydantic import BaseModel

T = TypeVar("T")
class DataList(GenericModel, Generic[T]):
    per_page: int
    total: int
    current_page: int
    data: List[T]
    
    class Config:
        orm_mode = True
        
class MsgOk(BaseModel):
    message: str

class ItemI18N(BaseModel):
    fr: str
    en: str
    
    class Config:
        orm_mode = True
        
    
class LoginUserSchema(BaseModel):
    username: str
    password: str
    