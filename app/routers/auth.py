from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import users, tokens

from app import models, oauth2

from app.utils import hash


router = APIRouter(tags=['Authentication'])


@router.post('/login', response_model=tokens.Token)
def login(user_credentials: users.UserLogin, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid email or password")

    
    if not hash.verify_hash(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid email or password")


    # Create a token
    # Return token

    access_token = oauth2.create_access_token(data = {"user_id": user.id})


    return {
        "status": 200,
        "access_token": access_token,
        "token_type": "bearer"
    }