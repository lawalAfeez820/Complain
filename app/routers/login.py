from .. import models, auth
from sqlmodel import Session,select
from fastapi import HTTPException, Depends, APIRouter, status
from app.database import get_session

route = APIRouter(
    tags=["LOGIN"],
    prefix="/login"
)
from fastapi.security import OAuth2PasswordRequestForm
@route.post("/" , response_model=models.LoginReturn)
async def login(login: OAuth2PasswordRequestForm= Depends(), db: Session = Depends(get_session)):
    query= await db.exec(select(models.UserRecord).where(models.UserRecord.secret_code == int(login.password)))
    query = query.first()
    if not query:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Invalid credentials")
    token = auth.get_token({"user_id": query.id})

    token = models.LoginReturn(access_token = token, token_type = "bearer")

    return token