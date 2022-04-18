from enum import unique
from operator import index
from turtle import back
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base
import uuid, secrets
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    token = Column(String, unique=True)
    jobs = relationship("Job", back_populates="owner")

    def __init__(self, email, password, token='', id=''):
        self.id = self.set_id()
        self.email = email
        self.hashed_password = self.set_pw(password)
        self.token = self.set_token()

    def set_id(self):
        return str(uuid.uuid4())[:8]
    
    def set_pw(self, password):
        return pwd_context.hash(password)
    
    def set_token(self):
        return secrets.token_hex(24)

    def verify_password(self, password):
        return pwd_context.verify(password, self.hashed_password)

class Job(Base):
    __tablename__ = "jobs"
    id = Column(String, primary_key=True, index=True)
    company = Column(String)
    title = Column(String)
    description = Column(String)
    status = Column(String)
    url = Column(String)
    owner_id = Column(String, ForeignKey("users.id"))

    owner = relationship("User", back_populates="jobs")



    


