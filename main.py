import fastapi


from fastapi import FastAPI
from config import settings

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

@app.get('/')
async def home_page():
    return {'Project': 'FastAPI Job Tracker'}