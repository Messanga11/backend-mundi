from datetime import datetime
from typing import List
from pydantic import BaseModel

class UserFollower(BaseModel):
    ''' Store user followers '''
    uuid:str
    user_uuid:str 
    follower_uuid:str 
    date_added: datetime 
    date_modified: datetime

class UserFriend(BaseModel):
    ''' Store user friend, when status is to pending,this means that the instance is an invitation request '''
    uuid:str
    user_uuid:str 
    friend_uuid:str 
    status:str 
    date_added: datetime 
    date_modified: datetime

class ConversationMessage(BaseModel):
    ''' Store conversation messages '''
    uuid:str
    conversation_uuid:str 
    first_user_uuid:str 
    second_user_uuid:str 
    content:str 
    is_call:bool 
    call_duration:bool 
    date_added: datetime 
    date_modified: datetime

class UserConversation(BaseModel):
    ''' Store user conversations '''
    uuid:str
    first_user_uuid:str 
    second_user_uuid:str
    messages: List[ConversationMessage]
    date_added: datetime 
    date_modified: datetime

class UserInfo(BaseModel):
    uuid:str
    firstname:str 
    lastname:str 
    fullname:str 
    phonenumber:str 
    email:str 

class UserUpdate(BaseModel):
    uuid:str
    firstname:str 
    lastname:str 
    phonenumber:str 
    email:str 
    profile_base_64: str
    
class UserIn(BaseModel):
    phonenumber:str 
    password:str 

class LoginUserSchema(BaseModel):
    username:str 
    password:str 

class User(UserInfo):
    ''' Store users '''
    followers: List[UserInfo]
    friends: List[UserInfo]
    conversations: List[UserConversation]
    birth_day:str 
    profile_pic:str 
    date_added: datetime 
    date_modified: datetime