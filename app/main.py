from fastapi import FastAPI, Response, status, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db
from . import schemas
from typing import List


models.Base.metadata.create_all(bind=engine)



app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='postgres', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successfull!")
        break

    except Exception as error:
        print("Database connection failed!")
        print("Error:", error)
        time.sleep(2)


# HEALTH CHECK
@app.get("/")
async def root():
    return {"message" : "API is active"}


# ----------------------------POSTS--------------------------------------------------------------------------------------#

# GET ALL POSTS
@app.get("/posts/all", response_model=List[schemas.PostResponse])
async def get_all_posts(db : Session = Depends(get_db)):
    #cursor.execute('''SELECT * FROM posts''')
    #posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

# GET SINGLE POST
@app.get("/posts/{id}", response_model=schemas.PostResponse)
async def get_single_post(id : int, db : Session = Depends(get_db)):

    # cursor.execute('''SELECT * FROM posts WHERE id = %s ''', (str(id),))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 
                            detail = f"Post with id: {id} not found!")
    
    return post
    

# CREATE POST
@app.post("/posts/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
async def create_post(post : schemas.PostCreate, db : Session = Depends(get_db)):

    # cursor.execute('''INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *''', 
    #                (post.title, post.content, post.published))

    # new_post = cursor.fetchone()
    # conn.commit()
    post_dict = post.model_dump()
    new_post = models.Post(**post_dict)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

# DELETE POST
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id : int, db : Session = Depends(get_db)):
    # cursor.execute('''DELETE FROM posts WHERE id = %s RETURNING *''', (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post = db.query(models.Post).filter(models.Post.id == id)

    if not post.first():
        raise HTTPException(status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {id} not found!")

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

# UPDATE POST
@app.put("/posts/{id}", response_model=schemas.PostResponse)
async def update_post(id : int, post : schemas.PostCreate, db : Session = Depends(get_db)):
    # cursor.execute('''UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *''', (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    if not post_query.first():
        raise HTTPException(status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {id} not found!")
    
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()

    return post_query.first()


#----------------------------------------USERS-------------------------------------------------------------------#

@app.post("/users", status_code = status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def create_user(user : schemas.UserCreate, db : Session = Depends(get_db)):
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


#5:50:00