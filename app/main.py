from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

class Post(BaseModel):
    title : str
    content : str
    published : bool = False

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



@app.get("/")
async def root():
    return {"message" : "API is active"}


@app.get("/posts/all")
async def get_all_posts():
    cursor.execute('''SELECT * FROM posts''')
    posts = cursor.fetchall()
    return(posts)


@app.get("/posts/{id}")
async def get_single_post(id : int):

    cursor.execute('''SELECT * FROM posts WHERE id = %s ''', (str(id),))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 
                            detail = f"Post with id: {id} not found!")
    
    return post
    


@app.post("/posts/", status_code=status.HTTP_201_CREATED)
async def create_post(post : Post):

    cursor.execute('''INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *''', 
                   (post.title, post.content, post.published))

    new_post = cursor.fetchone()
    conn.commit()

    return {"message" : f"Created {new_post}"}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id : int):
    cursor.execute('''DELETE FROM posts WHERE id = %s RETURNING *''', (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()

    if not deleted_post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {id} not found!")


    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
async def update_post(id : int, post : Post):
    cursor.execute('''UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *''', (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()

    if not updated_post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {id} not found!")

    return updated_post


