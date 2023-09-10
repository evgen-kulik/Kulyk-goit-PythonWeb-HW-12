from pydantic import BaseSettings


# class Settings(BaseSettings):
#     sqlalchemy_database_url: str = 'postgresql+psycopg2://postgres:567234@localhost:5432/hw_13_postgres'
#     secret_key: str = 'secret_key'
#     algorithm: str = 'HS256'
#     mail_username: str = 'fastapi_kulyk@meta.ua'
#     mail_password: str = 'pythonCourse2023'
#     mail_from: str = 'fastapi_kulyk@meta.ua'
#     mail_port: int = 465
#     mail_server: str = 'smtp.meta.ua'
#     redis_host: str = 'localhost'
#     redis_port: int = 6379


class Settings(BaseSettings):
    sqlalchemy_database_url: str = 'postgresql+psycopg2://user:password@localhost:5432/postgres'
    secret_key: str = 'secret_key'
    algorithm: str = 'HS256'
    mail_username: str = 'example@meta.ua'
    mail_password: str = 'password'
    mail_from: str = 'example@meta.ua'
    mail_port: int = 465
    mail_server: str = 'smtp.meta.ua'
    redis_host: str = 'localhost'
    redis_port: int = 6379

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()