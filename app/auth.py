from jose import JWTError, jwt
from typing import Dict
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlmodel import Session
from . import database, models, config

setting = config.Setting()


SECRET_KEY = f"{setting.secret_key}"

ALGORITHM = f"{setting.algorithm}"

ACCESS_TOKEN_EXPIRE_MINUTES = setting.expiry_time

oauth2_schema=OAuth2PasswordBearer(tokenUrl="login")

def get_token(payload: Dict):

    payload["exp"] = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_token(token, CredentialException):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id: int = payload.get("user_id")

        if not id:
            raise CredentialException
    except JWTError:
        raise CredentialException
    return id

async def get_user(token: str = Depends(oauth2_schema), db: Session = Depends(database.get_session)):
    redentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},)
    
    id = verify_token(token, redentials_exception)

    user = await db.get(models.UserRecord, id)

    return user
    
    
    