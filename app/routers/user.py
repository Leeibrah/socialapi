
from fastapi import status, HTTPException, Depends, APIRouter
from typing import List

from sqlalchemy.orm import Session

from app import models
from app.schemas import users
from app.database import get_db
from app.utils import hash


router = APIRouter(prefix="/users", tags=['Users'])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=users.User)
def create_user(user: users.UserCreate, db: Session = Depends(get_db)):

    # Create Hash for password
    hashed_password = hash.hash_password(user.password)
    user.password = hashed_password
    
    new_user  = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)


    return new_user


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=users.User)
def get_user(id: int, db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist")
    
    return user