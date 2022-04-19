from typing import List, Optional
from pydantic import BaseModel

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: str
    class Config:
        orm_mode = True

class UserToken(User):
    token: str

# Job Schemas
class JobBase(BaseModel):
    company: str
    title: str
    description: Optional[str] = None
    status: Optional[str] = None
    url: str

class JobCreate(JobBase):
    pass

class Job(JobBase):
    id: int
    owner_id: str
    class Config:
        orm_mode = True


    




