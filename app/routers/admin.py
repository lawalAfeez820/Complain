from .. import models, auth
from sqlmodel import Session,select
from fastapi import HTTPException, Depends, APIRouter, status
from app.database import get_session
from typing import List, Dict

route = APIRouter(
    tags=["ADMIN QUERIES"]

)

@route.get("/getAlComplaintsForAdmin", response_model=List[models.Complain])
async def get_admin_complain(db: Session = Depends(get_session), user: models.UserRecord =Depends(auth.get_user), limit:int= 20, offset:int=0):

    if not user.is_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Only admins can access this page")

    query= await db.exec(select(models.Complain).limit(limit).offset(offset))
    query= query.all()
    if not query:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail= f"No complain")
    return query


@route.delete("/resolveComplaint/{id}", response_model=Dict)
async def resolve(id:int, db: Session = Depends(get_session), user: models.UserRecord =Depends(auth.get_user)):

    if not user.is_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Only admins can access this route")

    query = await db.get(models.Complain, id)

    db.delete(query)

    db.commit()

    return {"Message": f"Complaint with id {id} has been resoled"}

