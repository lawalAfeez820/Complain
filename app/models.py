from .database import SQLModel
from sqlmodel import Field, Relationship, Session,select
from typing import Optional, List
from sqlalchemy import Column, String, Integer
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from datetime import datetime
from .helper import default
from pydantic import EmailStr
from random import randint
import uuid





class UserRecord(SQLModel, table =True):
    id: Optional[int] = Field(default=None, primary_key= True)

    secret_code: Optional[int] = Field(sa_column=Column(Integer, unique=True, default=lambda: int(str(uuid.uuid4().int)[:6])))
    
    name: str

    email: str = Field(sa_column=Column(String, unique=True, nullable=  False))

    created_at: Optional[datetime] = Field(sa_column= Column(TIMESTAMP(timezone=True), 
    server_default=text("now()")))

    is_admin: Optional[bool] = Field(default= False)

    #list_of_complaints: List["Complain"] = Relationship(back_populates="owner")
    complains: List["Complain"] = Relationship(back_populates="owner")
    

class ComplainSubmit(SQLModel):
    summary:str
    title:str
    rating:int

class ReturnComplain(ComplainSubmit):
    created_at: datetime
    id: int

class Complain(ComplainSubmit, table = True):
    id: Optional[int] = Field(default=None, primary_key= True)
    owner_id: Optional[int] = Field(default=None,foreign_key="userrecord.id")
    created_at: Optional[datetime] = Field(sa_column= Column(TIMESTAMP(timezone=True), 
    server_default=text("now()")))
    #owner: Optional[UserRecord] = Relationship(back_populates="list_of_complaints")
    owner: Optional[UserRecord] = Relationship(back_populates="complains")

class Register(SQLModel):
    name: str
    email: EmailStr

class Login(SQLModel):
    secret_code: int

class LoginReturn(SQLModel):
    token: str
    token_type: str

class RegisterReturn(Login):
    created_at: datetime
    name: str
    email: str
    id: int
    
class ComplainReturn(SQLModel):
     list_of_complaints: List[Complain]







