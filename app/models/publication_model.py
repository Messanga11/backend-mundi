from datetime import datetime
from email.policy import default
from sqlalchemy import TEXT, Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from .base_model import Base

class PublicationTypes():
    """Publication type available on the platform """
    SHORT = "SHORT"
    STORY = "STORY"
    NORMAL = "NORMAL"

class LikeModel(Base):
    ''' Associate a like to an user '''
    __tablename__ = "likes"
    uuid:str = Column(String, primary_key=True)
    user_uuid:str = Column(String, ForeignKey("users.uuid", ondelete="CASCADE"))
    publication_uuid:str = Column(String, ForeignKey("publications.uuid", ondelete="CASCADE"))
    date_added = Column(DateTime(timezone=True), default=datetime.now())
    date_modified = Column(DateTime(timezone=True), default=datetime.now(), onupdate=datetime.now())

class CommentLikeModel(Base):
    ''' Associate a like to a comment '''
    __tablename__ = "comment_likes"
    uuid:str = Column(String, primary_key=True)
    user_uuid:str = Column(String, ForeignKey("users.uuid", ondelete="CASCADE"))
    comment_uuid:str = Column(String, ForeignKey("comments.uuid", ondelete="CASCADE"))
    date_added = Column(DateTime(timezone=True), default=datetime.now())
    date_modified = Column(DateTime(timezone=True), default=datetime.now(), onupdate=datetime.now())

class CommentModel(Base):
    ''' Associate a comment to a publication '''
    __tablename__ = "comments"
    uuid:str = Column(String, primary_key=True)
    comment_to_respond_uuid:str = Column(String, ForeignKey("comments.uuid", ondelete="CASCADE"))
    user_uuid:str = Column(String, ForeignKey("users.uuid", ondelete="CASCADE"))
    publication_uuid:str = Column(String, ForeignKey("publications.uuid", ondelete="CASCADE"))
    content = Column(TEXT, nullable=False)
    date_added = Column(DateTime(timezone=True), default=datetime.now())
    date_modified = Column(DateTime(timezone=True), default=datetime.now(), onupdate=datetime.now())

class PublicationModel(Base):
    ''' Store user publications, stories ans shorts.
        @param file_url is used to store either images or videos.
        @param user_sharer is used to store user who shared a publication, and if its defined, it means that the publication is a share.
    '''
    __tablename__ = "publications"
    uuid:str = Column(String, primary_key=True)
    user_sharer_uuid:str = Column(String, ForeignKey("users.uuid", ondelete="CASCADE"))
    user_sharer = relationship("UserModel", foreign_keys=[user_sharer_uuid])
    user_uuid:str = Column(String, ForeignKey("users.uuid", ondelete="CASCADE"))
    user = relationship("UserModel", foreign_keys=[user_uuid])
    content = Column(TEXT, nullable=False)
    publication_type = Column(String, default=PublicationTypes.NORMAL, nullable=False)
    file_url:str = Column(String, nullable=True)
    date_added = Column(DateTime(timezone=True), default=datetime.now())
    date_modified = Column(DateTime(timezone=True), default=datetime.now(), onupdate=datetime.now())