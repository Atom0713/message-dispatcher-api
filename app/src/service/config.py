from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    aws_access_key_id: str = "local"
    aws_secret_access_key: str = "local"
    aws_region: str = "eu-west-1"
    dynamodb_endpoint: str = "http://dynamodb:8001"

    class Config:
        env_file = ".env"


settings = Settings()
