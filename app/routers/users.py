from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.user import get_user, get_users
from app.database import get_db
from app.dependencies.auth import get_current_active_user, role_required
from app.schemas.auth import UserInDB


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserInDB)
async def read_users_me(
    current_user: Annotated[UserInDB, Depends(get_current_active_user)]
):
    return current_user


@router.get("/", response_model=List[UserInDB])
def read_users(
    db: Session = Depends(get_db),
    # current_user: Annotated[UserInDB, Depends(role_required("admin"))],
    skip: int = 0,
    limit: int = 100
):
    users = get_users(db, skip=skip, limit=limit)
    return users