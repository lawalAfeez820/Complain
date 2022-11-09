from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from .database import init_db, get_session
from . import models, auth
from sqlmodel import Session,select
from typing import Dict, List
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
import  sqlalchemy



app= FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    await init_db()


@app.get("/", response_model=Dict)
async def root():
    
    return {"message": "Welcome"}

@app.post("/Register", response_model=models.RegisterReturn, status_code=status.HTTP_201_CREATED)
async def register(detail: models.Register, db: Session = Depends(get_session)):
    try:
        user = models.UserRecord.from_orm(detail)
        db.add(user)
        await db.commit()
        await db.refresh(user)

        return user
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"email already exist, try using another email")

@app.post("/login" , response_model=models.LoginReturn)
async def login(login: OAuth2PasswordRequestForm= Depends(), db: Session = Depends(get_session)):
    query= await db.exec(select(models.UserRecord).where(models.UserRecord.secret_code == int(login.password)))
    query = query.first()
    if not query:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Invalid credentials")
    token = auth.get_token({"user_id": query.id})

    token = models.LoginReturn(access_token = token, token_type = "bearer")

    return token

@app.post("/submitComplaint", response_model=Dict, status_code=status.HTTP_201_CREATED)

async def sub_comp(complain: models.ComplainSubmit, db: Session = Depends(get_session), 
user: models.UserRecord =Depends(auth.get_user)):

   
    complain: models.Complain = models.Complain.from_orm(complain)

    complain.owner_id = user.id

    db.add(complain)
    await db.commit()
    await db.refresh(complain)

    return {"Message": "Complain Successfully Submited"}
    

@app.get("/getAlComplaintsForUser",response_model=List[models.ReturnComplain])
async def get_user_complain(db: Session = Depends(get_session), user: models.UserRecord =Depends(auth.get_user)):

    query= await db.exec(select(models.Complain).where(models.Complain.owner_id == user.id))
    query = query.all()
    

    if not query:
        raise HTTPException(status_code= status.HTTP_409_CONFLICT, detail= f"You haven't make any complain")
    return query

@app.get("/getAlComplaintsForAdmin", response_model=List[models.Complain])
async def get_admin_complain(db: Session = Depends(get_session), user: models.UserRecord =Depends(auth.get_user), limit:int= 20, offset:int=0):

    if not user.is_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Only admins can access this page")

    query= await db.exec(select(models.Complain).limit(limit).offset(offset))
    query= query.all()
    if not query:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail= f"No complain")
    return query


@app.get("/viewComplaint/{id}",response_model=models.Complain)
async def view_complain(id: int, db: Session = Depends(get_session), user: models.UserRecord =Depends(auth.get_user)):

    query = await db.get(models.Complain, id)

    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No complain with id {id}")

    if user.id == query.owner_id or user.is_admin:

        return query
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Only admins or the owner of this complaint can view it")
    
@app.delete("/resolveComplaint/{id}", response_model=Dict)
async def resolve(id:int, db: Session = Depends(get_session), user: models.UserRecord =Depends(auth.get_user)):

    if not user.is_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Only admins can access this route")

    query = await db.get(models.Complain, id)

    db.delete(query)

    db.commit()

    return {"Message": f"Complaint with id {id} has been resoled"}

    










