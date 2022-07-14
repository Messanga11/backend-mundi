from datetime import datetime
from email.policy import default
from sqlalchemy import TEXT, Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .base_model import Base

class FriendStatuses():
    ''' Possible friend invitation status '''
    ACCEPTED = "ACCEPTED",
    REJECTED = "REJECTED",
    PENDING = "PENDING",


class UserModel(Base):
    '''
    Store users
    @backrefs
     - friends
     - followers
    '''
    __tablename__ = "users"
    uuid:str = Column(String, primary_key=True)
    firstname:str = Column(String, nullable=True)
    lastname:str = Column(String, nullable=True)
    fullname:str = Column(String, nullable=True)
    position:str = Column(String, nullable=True)
    password_hash:str = Column(String, nullable=False)
    phonenumber:str = Column(String, nullable=False)
    email:str = Column(String, nullable=False)
    birth_day:str = Column(String, nullable=False)
    profile_pic_uuid:str = Column(String, ForeignKey("storages.uuid", ondelete="CASCADE"))
    profile_pic = relationship("Storage", foreign_keys=[profile_pic_uuid])
    date_added = Column(DateTime(timezone=True), default=datetime.now())
    date_modified = Column(DateTime(timezone=True), default=datetime.now(), onupdate=datetime.now())

class UserFollower(Base):
    ''' Store user followers '''
    __tablename__ = "user_followers"
    uuid:str = Column(String, primary_key=True)
    user_uuid:str = Column(ForeignKey("users.uuid", ondelete="CASCADE"))
    follower_uuid:str = Column(ForeignKey("users.uuid", ondelete="CASCADE"), primary_key=True)
    follower = relationship("UserModel", backref="followers", primaryjoin=(UserModel.uuid == follower_uuid))
    date_added = Column(DateTime(timezone=True), default=datetime.now())
    date_modified = Column(DateTime(timezone=True), default=datetime.now(), onupdate=datetime.now())

class UserFriend(Base):
    __tablename__ = "user_friends"
    ''' Store user friend, when status is to pending,this means that the instance is an invitation request '''
    uuid:str = Column(String, primary_key=True)
    user_uuid:str = Column(ForeignKey("users.uuid", ondelete="CASCADE"))
    friend_uuid:str = Column(ForeignKey("users.uuid", ondelete="CASCADE"), primary_key=True)
    friend = relationship("UserModel", backref="friends", primaryjoin=(UserModel.uuid == friend_uuid))
    status:str = Column(String, default=FriendStatuses.PENDING)
    date_added = Column(DateTime(timezone=True), default=datetime.now())
    date_modified = Column(DateTime(timezone=True), default=datetime.now(), onupdate=datetime.now())

class UserConversation(Base):
    __tablename__ = "user_conversations"
    ''' Store user conversations '''
    uuid:str = Column(String, primary_key=True)
    date_added = Column(DateTime(timezone=True), default=datetime.now())
    date_modified = Column(DateTime(timezone=True), default=datetime.now(), onupdate=datetime.now())


class ConversationMessage(Base):
    ''' Store conversation messages '''
    __tablename__ = "conversation_messages"
    uuid:str = Column(String, primary_key=True)
    conversation_uuid:str = Column(ForeignKey("user_conversations.uuid", ondelete="CASCADE"))
    user_uuid:str = Column(ForeignKey("users.uuid", ondelete="CASCADE"))
    content:str = Column(TEXT, nullable=False)
    is_call:bool = Column(Boolean, nullable=False, default=False)
    call_duration:bool = Column(Integer, nullable=True)
    date_added = Column(DateTime(timezone=True), default=datetime.now())
    date_modified = Column(DateTime(timezone=True), default=datetime.now(), onupdate=datetime.now())

class ConversationMember(Base):
    ''' Store conversation messages '''
    __tablename__ = "conversation_members"
    uuid:str = Column(String, primary_key=True)
    conversation_uuid:str = Column(ForeignKey("user_conversations.uuid", ondelete="CASCADE"))
    user_uuid:str = Column(ForeignKey("users.uuid", ondelete="CASCADE"))
    date_added = Column(DateTime(timezone=True), default=datetime.now())
    date_modified = Column(DateTime(timezone=True), default=datetime.now(), onupdate=datetime.now())