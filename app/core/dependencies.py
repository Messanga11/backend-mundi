import models
from fastapi import HTTPException

models.Base.metadata.create_all(bind=models.engine)

    
def get_db():
   db = models.SessionLocal()
   try:
       yield db
   finally:
       db.close()

class OrderFieldChecker:
    def __init__(self, authorized_fields: list = [], order_field:str= ""):
        if order_field and order_field not in authorized_fields:
            raise HTTPException(
                status_code=400, detail="cannot-order-by-this-field")
        else:
            return None

