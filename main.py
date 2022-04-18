from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from config import settings
import models, schemas, crud
from database import SessionLocal, engine
from sqlalchemy.orm import Session

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
async def user_test(user: schemas.UserCreate, db: Session = Depends(get_db)):
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
    return db_user.__dict__


@app.get("/users/{user_id}/{password}", response_model=schemas.UserToken)
def get_token(user_id: str, password: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail='user does not exist')
    if not db_user.verify_password(password):
        raise HTTPException(status_code=401, detail='incorrect password')
    return db_user.__dict__


