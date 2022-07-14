from datetime import datetime
from pydantic import BaseModel
from .user_schemas import UserInfo


class Like(BaseModel):
    ''' Associate a like to an user '''
    uuid:str
    user_uuid:str 
    publication_uuid:str 
    date_added: datetime 
    date_modified: datetime 

class CommentLike(BaseModel):
    ''' Associate a like to a comment '''
    uuid:str
    user_uuid:str 
    comment_uuid:str 
    date_added: datetime 
    date_modified: datetime 

class Comment(BaseModel):
    ''' Associate a comment to a publication '''
    uuid:str
    comment_to_respond_uuid:str 
    user_uuid:str 
    publication_uuid:str 
    content:str 
    date_added: datetime 
    date_modified: datetime 

class Publication(BaseModel):
    ''' Store user publications, stories ans shorts.
        @param file_url is used to store either images or videos.
        @param user_sharer is used to store user who shared a publication, and if its defined, it means that the publication is a share.
    '''
    uuid:str
    user_sharer_uuid:str 
    user_share: UserInfo
    user_uuid:str 
    user:UserInfo
    content:str
    file_url:str 
    date_added: datetime 
    date_modified: datetime 