from .user_crud import UserCrud
from .publication_crud import PublicationCrud
from .file_crud import CRUDFile
import models

db = models.SessionLocal()
user_crud = UserCrud(db)
storage_crud = CRUDFile()
publication_crud = PublicationCrud(db)