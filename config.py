from pydantic import BaseSettings
class Settings(BaseSettings):
    PROJECT_NAME: str = 'CT Alumni Job Tracker'
    PROJECT_VERSION: str = '1.0.0'

settings = Settings()