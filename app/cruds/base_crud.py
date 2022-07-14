import math
from typing import Any, Dict, List
from core import dependencies
import schemas
from sqlalchemy import or_
from models.base_model import SessionLocal
from utils.errors import Errors

class BaseCrud():
    def __init__(self, model, db):
        self.model = model
        self.db = db
      
    def get_all(self, criterions:List[tuple]):
        record_query = self.db.query(self.model)
        
        if len(criterions) > 0:
            for criterion in criterions:
                record_query = record_query.filter(self.model[criterion[0]] == criterion[1])
        
        return record_query.all()
        
    def get_by_pagination(self, page:int, per_page:int, keyword:str, order: str, order_field: str, keyword_search_prop: str, additional_filters:List[tuple] = []):
        record_query = self.db.query(self.model)
        
        if len(additional_filters) > 0:
            for add_filter in additional_filters:
                record_query = record_query.filter(self.model[add_filter[0]] == add_filter[1])
        
        if keyword:
            record_query = record_query\
                        .filter(self.model[keyword_search_prop].ilike("%" + keyword + "%"))

        if order in ["asc", "ASC"] and order_field and order_field:
            record_query = record_query.order_by(getattr(self.model, order_field).asc())

        if order in ["desc", "DESC"] and order_field and order_field:
            record_query = record_query.order_by(getattr(self.model, order_field).desc())

        total = record_query.count()
        result = record_query.offset((page-1)*per_page).limit(per_page).all()

        return schemas.DataList(
            total = total,
            pages = math.ceil(total / per_page),
            current_page = page,
            per_page = per_page,
            data = result
        )
    
    def get_by_property(self, data_to_compare:str, prop_to_compare="uuid"):
        obj = self.db.query(self.model).filter(self.model[prop_to_compare] == data_to_compare)
        if not obj:
            raise Errors.not_found_error
        return obj
    
    def create(self, data:dict):
        model_instance = self.model(**data)
        self.db.add(model_instance) 
        self.db.commit()
    
    def update(self, data:dict, value_to_compare, prop_to_compare="uuid"):
        model_instance = self.get_by_property(value_to_compare, prop_to_compare)
        for k, v in data.items():
            model_instance[k] = v if k in data else model_instance[k]
        self.db.commit()
    
    # def delete(self, data:dict, value_to_compare, prop_to_compare="uuid"):
    #     model_instance = self.get_by_property(value_to_compare, prop_to_compare)
    #     model_instance.delete()
    #     self.db.commitdate_created()
