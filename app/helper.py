from random import randint
from .database import get_session
from fastapi import Depends
from . import models
from sqlmodel import Session, select

async def default(db: Session = Depends(get_session)):
    rand = randint(1000,9999)
    query=await db.exec(select(models.UserRecord).where(models.UserRecord.secret_code == rand))
    query = query.first()
    if not query:
        return rand
    return default(Depends(get_session))

  
