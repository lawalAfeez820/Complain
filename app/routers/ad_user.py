import sqlalchemy
from .. import models, auth
from sqlmodel import Session,select
from fastapi import HTTPException, Depends, APIRouter, status
from app.database import get_session


route = APIRouter(
    tags=["ADMIN_USER QUERIES"],
    prefix="/viewComplaint"
)

@route.get("/{id}",response_model=models.Complain)
async def view_complain(id: int, db: Session = Depends(get_session), user: models.UserRecord =Depends(auth.get_user)):

    query = await db.get(models.Complain, id)

    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No complain with id {id}")

    if user.id == query.owner_id or user.is_admin:

        return query
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Only admins or the owner of this complaint can view it")