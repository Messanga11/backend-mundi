from fastapi import status, HTTPException


class Config():
    DATABASE_URL="postgresql+psycopg2://cd97b8dccbafa693:6b9df25125b0@localhost:5432/mundi_db"
    # DATABASE_URL = "postgresql+psycopg2://postgres:6b9df25125b065610f5b6db237b28690@db:5432/surepath"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    # Minio config information with AWS
    MINIO_API_URL: str = "http://localhost:9000/api/v1/storages/file/get/"
    MINIO_URL: str = "http://localhost:9050"
    MINIO_KEY: str = "cbdcb2dc9911889143082b9f1f4a045aa20c121f"
    MINIO_SECRET: str = "0f04cfbb8e664a112fd8279cb8cba8c2077807a6693891ef0aead48db043"
    MINIO_SECURE: bool = True
    MINIO_BUCKET: str = "develop"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


app_config = Config()