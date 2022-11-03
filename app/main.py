
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from app.routers import post, user, auth, vote

from app.config import settings

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ['*']

# Add these to do away with cors error
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Testing Route
# @app.get('/sqlalchemy')
# def test_posts(db: Session = Depends(get_db)):

#     posts = db.query(models.Post).all()

#     return posts

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(post.router)
app.include_router(vote.router)


@app.get("/")
async def root():
    return {"message": "Hello World!!!"}


