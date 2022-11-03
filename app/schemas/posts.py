from pydantic import BaseModel, EmailStr
from datetime import datetime

from app.schemas.users import User

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass 

# Remove this
class PostUpdate(PostBase):
    pass


class Post(PostBase):
    id: int
    user: User
    created_at: datetime

    class Config:
        orm_mode = True

class PostwithVote(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True