import sqlalchemy
from .. import models, auth
from sqlmodel import Session,select
from fastapi import HTTPException, Depends, APIRouter, status
from app.database import get_session
from typing import Dict, List

route = APIRouter(
    tags=["USER QUERIES"]
)

@route.post("/submitComplaint", response_model=Dict, status_code=status.HTTP_201_CREATED)

async def sub_comp(complain: models.ComplainSubmit, db: Session = Depends(get_session), 
user: models.UserRecord =Depends(auth.get_user)):

   
    complain: models.Complain = models.Complain.from_orm(complain)

    complain.owner_id = user.id

    db.add(complain)
    await db.commit()
    await db.refresh(complain)

    return {"Message": "Complain Successfully Submited"}
    

@route.get("/getAlComplaintsForUser",response_model=List[models.ReturnComplain])
async def get_user_complain(db: Session = Depends(get_session), user: models.UserRecord =Depends(auth.get_user)):

    query= await db.exec(select(models.Complain).where(models.Complain.owner_id == user.id))
    query = query.all()
    

    if not query:
        raise HTTPException(status_code= status.HTTP_409_CONFLICT, detail= f"You haven't make any complain")
    return query