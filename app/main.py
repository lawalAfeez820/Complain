from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from .database import init_db, get_session
from . import models, auth
from sqlmodel import Session,select
from typing import Dict, List
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
import  sqlalchemy
from .routers import login, reg, user, ad_user, admin


app= FastAPI()

origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(login.route)
app.include_router(reg.route)
app.include_router(user.route)
app.include_router(admin.route)
app.include_router(ad_user.route)




@app.on_event("startup")
async def on_startup():
    await init_db()


@app.get("/", response_model=Dict)
async def root():
    
    return {"message": "Welcome"}






    










