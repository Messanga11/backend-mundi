from cruds.base_crud import BaseCrud
import models

class PublicationCrud(BaseCrud):

    def __init__(self, db):
        super(PublicationCrud, self).__init__(models.PublicationModel, db)