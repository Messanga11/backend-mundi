from cruds.base_crud import BaseCrud
import models

class UserCrud(BaseCrud):

    def __init__(self, db):
        super(UserCrud, self).__init__(models.UserModel, db)
