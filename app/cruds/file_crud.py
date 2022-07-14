

from sqlalchemy.orm import Session
from models import Storage, User
from schemas import File
import uuid
from typing import Any, Dict, Optional, Union
from schemas import FileAddSend
from utils.file import FileUtils
from app.main import crud
from sqlalchemy.dialects.postgresql.json import JSONB



class CRUDFile():


    def store_file(self, db: Session, *, base_64: Any, name: str = None) -> Storage:

        file_manager = FileUtils(base64=base_64, name=name)
        storage = file_manager.save(db=db)
        return storage
    
storage = CRUDFile(Storage)