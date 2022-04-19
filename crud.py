from fastapi import HTTPException
from os import stat
from sqlalchemy.orm import Session
import models, schemas

#CREATE -- USER
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


#GET -- USER
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.id == user_id).first()


#CREATE -- JOB
def create_user_job(db: Session, job : schemas.JobCreate, user_id: str):
    print(job.dict())
    db_job = models.Job(**job.dict(), owner_id=user_id)
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

# RETRIEVE -- JOB
def get_jobs(db: Session, user_id: str, skip: int = 0, limit: int = 100):
    return db.query(models.User).filter(models.User.id == user_id).first().jobs

# UPDATE -- JOB
def update_job(db: Session, job : schemas.JobCreate, user_id: str, job_id: int):
    db_job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if db_job is None:
        raise HTTPException(status_code=404, detail='Job not found')
    if db_job.owner_id != user_id:
        raise HTTPException(status_code=401, detail='Job does not belong to user')
    for col, data in job.dict().items():
        setattr(db_job, col, data)
    db.commit()
    db.refresh(db_job)
    return db_job

# DELETE -- JOB
def delete_job(db: Session, user_id: str, job_id: int):
    db_job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if db_job is None:
        raise HTTPException(status_code=404, detail='Job not found')
    if db_job.owner_id != user_id:
        raise HTTPException(status_code=401, detail='Job does not belong to user')
    db.delete(db_job)
    db.commit()
    return db_job
    

    
