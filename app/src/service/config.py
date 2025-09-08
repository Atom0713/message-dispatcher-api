import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    aws_access_key_id: str = "local"
    aws_secret_access_key: str = "local"
    aws_region: str = "eu-west-1"
    dynamodb_endpoint: str | None = os.getenv("DYNAMODB_ENDPOINT")
    table_name: str = "recipient_messages"

    class Config:
        env_file = ".env"


settings = Settings()
