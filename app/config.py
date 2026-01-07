from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Remote Server Manager API"
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    DATABASE_URL: str

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: str
    SMTP_FROM: str

    class Config:
        env_file = ".env"
        extra = "allow" 

settings = Settings()
