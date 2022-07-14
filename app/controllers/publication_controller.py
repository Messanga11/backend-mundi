from fastapi import APIRouter, Depends

import schemas
from core import dependencies
import cruds


publication_router = APIRouter(prefix="/publications", tags=["publications"])

@publication_router.get("")
def get_all_categories(db=Depends(dependencies.get_db)):
    return cruds.publication_crud.get_categories(db)

@publication_router.get("/{user_name}", response_model=schemas.Publication)
def get_single_publication(user_name:str, db=Depends(dependencies.get_db)):
    return cruds.publication_crud.get_single_publication(user_name, db)

@publication_router.post("", response_model=schemas.Publication)
def create_publication(publication_in:schemas.Publication ,db=Depends(dependencies.get_db)):
    return cruds.publication_crud.create_publication(publication_in, db)

@publication_router.put("", response_model=schemas.Publication)
def update_publication(publication_in:schemas.Publication, db=Depends(dependencies.get_db)):
    return cruds.publication_crud.update_publication(publication_in, db)

@publication_router.delete("/{publication_uuid}", response_model=schemas.MsgOk)
def get_single_publication(publication_uuid:str, db=Depends(dependencies.get_db)):
    return cruds.publication_crud.delete_publication(publication_uuid, db)