import sqlalchemy
from .. import models, auth
from sqlmodel import Session,select
from fastapi import HTTPException, Depends, APIRouter, status
from app.database import get_session

route = APIRouter(
    tags=["Registration"],
    prefix="/Register"
)

@route.post("/", response_model=models.RegisterReturn, status_code=status.HTTP_201_CREATED)
async def register(detail: models.Register, db: Session = Depends(get_session)):
    try:
        user = models.UserRecord.from_orm(detail)
        db.add(user)
        await db.commit()
        await db.refresh(user)

        return user
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"email already exist, try using another email")