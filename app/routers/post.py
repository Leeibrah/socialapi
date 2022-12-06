
from optparse import Option
from fastapi import APIRouter, Response, status, HTTPException, Depends
from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy import func

from app import models, oauth2
from app.schemas import posts
from app.database import engine, get_db


models.Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/posts", tags=['Posts'])


# Stored in Memory
my_posts = [
    {
        "id": 1,
        "title": "Post 1",
        "content": "Content of post 1"
    },
    {
        "id": 2,
        "title": "Post 2",
        "content": "Content of post 2"
    }
]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


# Get all Posts
@router.get("/", 
    status_code=status.HTTP_200_OK,
    response_model=List[posts.PostwithVote]
)
def get_posts(db: Session = Depends(get_db), limit: int = 2, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    # Skip is used for pagination: 1st page skips = 0, Second page skips = 20, Third page skips 40 and so on

    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return results


# Get all Posts for a specific user
@router.get("/loggedin/user", status_code=status.HTTP_200_OK, response_model=List[posts.Post])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 3):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).filter(models.Post.user_id == current_user.id).limit(limit).all()

    return posts

# Create a New Post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=posts.Post)
# def create_posts(payload: dict = Body(...)):
def create_posts(post: posts.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # print(post)

    # print(post.dict())
    # return {"message": "Successfully created post."}
    # return {"message": f"title: {post['title']}, content: {post['content']}"}
    # post_dict = post.dict()
    # post_dict['id'] = randrange(0, 15)
    # my_posts.routerend(post_dict)
    # query = """ INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """

    # cursor.execute(
    #     query, (post.title, post.content, post.published) 
    # )

    # new_post = cursor.fetchone()

    # # Save data to postgres
    # conn.commit()


    # Replace title=post.title, content=post.content, published=post.published with a **post.dict
    print("Logged in User is:", current_user.name)
    print(post.dict())

    new_post = models.Post(
        # title=post.title, content=post.content, published=post.published
        user_id = current_user.id,
        **post.dict()
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post

# Get the lastest Post
@router.get("/latest")
def get_latest_post(db: Session = Depends(get_db)):

    # Get the last post : Iterate through entire list then get the last object
    # This is too heavy
    # all_posts = db.query(models.Post).all()
    # latest = all_posts[len(all_posts)-1]

    # Instead do this
    latest = db.query(models.Post).order_by(models.Post  .id.desc()).first()

    return latest


# Get Single Post
@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=posts.PostwithVote)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # query = """ SELECT * FROM posts WHERE id = %s """

    # post = find_post(id)
    # cursor.execute(
    #     query, (str(id),)
    # )

    # post = cursor.fetchone()

    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found!"
        )

    return post


# Update Post
@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=posts.Post)
def update_post(id: int, updated_post: posts.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # query = """ UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """
    

    # cursor.execute(query, (post.title, post.content, post.published, str(id),))
       
    # updated_post = cursor.fetchone()

    # conn.commit()

    # index = find_index_post(id)

    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_posts[updated_post] = post_dict

    print("Logged in User is:", current_user.name)

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id: {id} does not exist"
        )
    
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized: Not the Owner of the Post!")

    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()


# Delete Post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # query = """ DELETE FROM posts WHERE id = %s RETURNING *"""
    # index = find_index_post(id)

    # cursor.execute(
    #     query, (str(id),)
    # )

    # deleted_post = cursor.fetchone()
    
    # conn.commit()

    post = db.query(models.Post).filter(models.Post.id == id)

    if not post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with the ID: {id} not available for deletion"
        )
    
    # if post.user_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized: Not the Owner of the Post!")

    post.delete(synchronize_session=False)

    db.commit()
    

    # my_posts.pop(deleted_post)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
