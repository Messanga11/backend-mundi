import os 
import uuid
from app.models.storage_model import Storage
from core.config import Config
from PIL import Image 
from base64 import b64decode
from utils.uploads import upload_file
from sqlalchemy.orm import Session
from fastapi import FastAPI, File, UploadFile



def rreplace(s, old, new, occurrence):
  li = s.rsplit(old, occurrence)
  return new.join(li)


class FileUtils(object):

    def __init__(self, my_file: UploadFile = None, base64: str = None, name: str = None):

        if (not my_file and not base64) or (my_file and base64):
          raise Exception("Provide only file or base64")
          
        if base64:
          # saved base 64 as file
          if len(base64.split(",")) != 2:
            raise Exception("Invalid base 64")
          info = base64.split(",")[0].split(";")[0].split(":")[1]
          self.blob_name = "{}{}".format(uuid.uuid1(), "-{}".format(name) if name else ".{}".format(info.split("/")[1]))
          self.path_file = os.path.join(Config.UPLOADED_FILE_DEST, self.blob_name)
          self.mimetype = info
          bytes = b64decode(base64.split(",")[1], validate=True)
          f = open(self.path_file, 'wb')
          f.write(bytes)
          f.close()

        else:
          self.blob_name = "{}-{}".format(uuid.uuid1(), my_file.filename)
          self.path_file = os.path.join(Config.UPLOADED_FILE_DEST, self.blob_name)
          with open(self.path_file, 'wb') as out_file:
            content = my_file.file.read()
            out_file.write(content)
          # file.save(self.path_file)
          self.mimetype = my_file.content_type

        self.size = os.stat(self.path_file).st_size
        self.is_image = False
        self.thumbnail = {}  
        self.medium = {}
        self.width = 0
        self.height = 0
        if self.mimetype.split("/")[0] in ["image"]:
          self.is_image = True
          

    def __repr__(self):
        return '<FileUtils: blob_name: {} path_file: {} mimetype: {} is_image: {} width: {} height: {}/>'.format(self.blob_name, self.path_file, self.mimetype, self.is_image, self.width, self.height)

    def __generate_cropped_image(self):

      #medium size
      self.image_pillow.thumbnail((Config.IMAGE_MEDIUM_WIDTH, Config.IMAGE_MEDIUM_WIDTH), Image.ANTIALIAS)
      self.image_pillow.save(rreplace(self.path_file, '.', '_medium.', 1))
      self.medium = {
        "width": self.image_pillow.size[0],
        "height": self.image_pillow.size[1],
        "size":  os.stat(rreplace(self.path_file, '.', '_medium.', 1)).st_size,
        "url": "",
        "file_name": rreplace(self.blob_name, '.', '_medium.', 1) 
      }  

      #Thumbnail
      self.image_pillow.thumbnail((Config.IMAGE_THUMBNAIL_WIDTH, Config.IMAGE_THUMBNAIL_WIDTH), Image.ANTIALIAS)
      self.image_pillow.save(rreplace(self.path_file, '.', '_thumbnail.', 1))
      self.thumbnail = {
        "width": self.image_pillow.size[0],
        "height": self.image_pillow.size[1],
        "size":  os.stat(rreplace(self.path_file, '.', '_thumbnail.', 1)).st_size,
        "url": "",
        "file_name": rreplace(self.blob_name, '.', '_thumbnail.', 1) 
      }  


    def __get_image_info(self):
      self.image_pillow = Image.open(r"{}".format(self.path_file))
      self.width, self.height = self.image_pillow.size 

    def save(self, db: Session):
      print(self.is_image)
      if self.is_image:
        self.__get_image_info()
        self.__generate_cropped_image()

      url, test = upload_file(self.path_file, self.blob_name, content_type=self.mimetype)
      os.remove(self.path_file)

      if "file_name" in self.thumbnail:
        url_thumbnail, test = upload_file(rreplace(self.path_file, '.', '_thumbnail.', 1), self.thumbnail["file_name"], content_type=self.mimetype)
        self.thumbnail["url"] = url_thumbnail
        os.remove(rreplace(self.path_file, '.', '_thumbnail.', 1))

      if "file_name" in self.medium:
        url_medium, test = upload_file(rreplace(self.path_file, '.', '_medium.', 1), self.medium["file_name"], content_type=self.mimetype)
        self.medium["url"] = url_medium
        os.remove(rreplace(self.path_file, '.', '_medium.', 1))


      db_obj = Storage(
          uuid=str(uuid.uuid4()),
          file_name=self.blob_name,
          url= url,
          width=self.width,
          height=self.height,
          size= self.size,
          thumbnail=self.thumbnail,
          medium=self.medium
      )
      db.add(db_obj)
      db.commit()
      db.refresh(db_obj)

      return db_obj