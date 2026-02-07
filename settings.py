from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    SEMAPHORE_LIMIT: int = 4

    PROCESSING_API_URL: str = "http://0.0.0.0:8080/api/upload"
    RESULT_API_URL: str = "http://0.0.0.0:8080/api/download"

    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_SESSION_TOKEN: str = ""
    AWS_REGION: str = "us-west-2"

    BUCKET: str = "shv-hack-upload"
    QUEUE_URL: str = (
        "https://sqs.us-west-2.amazonaws.com/371168335772/video_processing"
    )

    class Config:
        env_file = ".env"


settings = Settings()
