from os import stat
from fastapi import FastAPI, Request, Depends, HTTPException, Header
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from config import settings
import models, schemas, crud
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from typing import List
from helpers import verify_token

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

models.Base.metadata.create_all(bind=engine)

app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')


# Dependencies
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get('/', response_class=HTMLResponse)
async def home_page(request: Request):
    return templates.TemplateResponse('/pages/home.html', {'request': request})


#CREATE -- User
@app.post('/users', response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail='Email already registered')
    return crud.create_user(db=db, user=user)

#RETRIEVE -- User
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail='user does not exist')
    return db_user

@app.get("/users/{user_id}/{password}", response_model=schemas.UserToken)
def get_token(user_id: str, password: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail='user does not exist')
    if not db_user.verify_password(password):
        raise HTTPException(status_code=401, detail='incorrect password')
    return db_user

# CREATE -- Job
@app.post("/jobs/{user_id}", response_model=schemas.Job)
async def create_job(user_id: str, job: schemas.JobCreate, db: Session = Depends(get_db), x_access_token: str = Header(...)):
    if verify_token(db=db, token=x_access_token, user_id=user_id):
        return crud.create_user_job(db=db, job=job, user_id=user_id)

# RETRIEVE -- Job
@app.get("/jobs/{user_id}", response_model=List[schemas.Job])
def get_jobs(user_id: str, db: Session = Depends(get_db), x_access_token: str = Header(...)):
    if verify_token(db=db, token=x_access_token, user_id=user_id):
        return crud.get_jobs(db, user_id)

# UPDATE -- Job
@app.put("/jobs/{user_id}/{job_id}", response_model=schemas.Job)
def update_job(user_id: str, job_id: int, job: schemas.JobCreate, db: Session = Depends(get_db), x_access_token: str = Header(...)):
    if verify_token(db=db, token=x_access_token, user_id=user_id):
        return crud.update_job(db, job, user_id, job_id)

# DELETE -- Jobs
@app.delete('/jobs/{user_id}/{job_id}', response_model=schemas.Job)
def delete_job(user_id: str, job_id: str, db: Session = Depends(get_db), x_access_token: str = Header(...)):
    if verify_token(db=db, token=x_access_token, user_id=user_id):
        return crud.delete_job(db, user_id, job_id)
















    


