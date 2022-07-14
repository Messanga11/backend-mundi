from minio.error import (ResponseError, BucketAlreadyOwnedByYou,BucketAlreadyExists)
from minio import Minio
from core.config import Config


minioClient = Minio(Config.MINIO_URL,
                access_key=Config.MINIO_KEY,
                secret_key=Config.MINIO_SECRET,
                secure=Config.MINIO_SECURE)

# function for upload file in aws
def upload_file(path, file_name, content_type):

  try:
    minioClient.make_bucket(Config.MINIO_BUCKET)
  except BucketAlreadyOwnedByYou as err: 
    print(err)
    pass
  except BucketAlreadyExists as err:
    print(err)
    pass
  except ResponseError as err:
    print(err)
    raise
  finally:
    # Upload the image
    try:
      minioClient.fput_object(Config.MINIO_BUCKET, file_name, path, content_type=content_type)
      url =  minioClient.presigned_get_object(Config.MINIO_BUCKET, file_name)
      return (Config.MINIO_API_URL+file_name, file_name)
    except ResponseError as err:
      return err

def get_file_url(file_name):
  try:
    return minioClient.presigned_get_object(Config.MINIO_BUCKET, file_name)
  except ResponseError as err:
    print(err)
    return err

def get_cloud_file(file_name):
  try:
    return minioClient.get_object(Config.MINIO_BUCKET, file_name)
  except ResponseError as err:
    print(err)
    return err

def delete_cloud_file(image_name):
  try:
    minioClient.remove_object(Config.MINIO_BUCKET, image_name)
  except ResponseError as err:
    print(err)
    return err
