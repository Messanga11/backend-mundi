from dataclasses import dataclass
from sqlalchemy.sql import func
from datetime import datetime
from sqlalchemy.dialects.postgresql.json import JSONB
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime
from .base_model import Base

# from hurry.filesize import size, alternative #Todo move that to the right new place 

class Storage(Base):
    
    """ Storage Model for storing file related details in database"""

    __tablename__ = "storages"

    uuid = Column(String, primary_key=True, unique=True)

    file_name: str = Column(Text, default="", nullable=True)
    url: str = Column(Text, default="", nullable=True)
    mimetype: str = Column(Text, default="", nullable=True)

    width = Column(Integer, default=0, nullable=True)
    height = Column(Integer, default=0, nullable=True)
    size = Column(Integer, default=0, nullable=True)

    thumbnail = Column(JSONB, default={}, nullable=True)
    medium = Column(JSONB, default={}, nullable=True)

    date_added: any = Column(DateTime(), server_default=func.now())
    date_modified: any = Column(DateTime(), server_default=func.now(), onupdate=datetime.now())

    def __repr__(self):
        return '<Storage: uuid: {} file_name: {} url: {} />'.format(self.uuid, self.file_name, self.url)


