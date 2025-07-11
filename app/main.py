from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange


app = FastAPI()

class Post(BaseModel):
    title : str
    content : str


my_posts = [{"id" : 1, "title" : "Dummy Post", "content" : "This is a dummy post", "rating" : 4}, {"id" : 2, "title" : "This is gonna get deleted", "content" : "Don't delete me ):"}]

def find_post(id : int):
    for p in my_posts:
        if p["id"] == id:
            return p
        

def find_post_index(id : int):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i


@app.get("/")
async def root():
    return {"message" : "API is active"}


@app.get("/posts/all")
async def get_all_posts():
    return(my_posts)


@app.get("/posts/{id}")
async def get_single_post(id : int, response : Response):
    p = find_post(id)

    if not p:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 
                            detail = f"Post with id: {id} not found!")
    
    return p
    


@app.post("/posts/", status_code=status.HTTP_201_CREATED)
async def create_post(post : Post):

    post_dict = post.model_dump()
    
    post_dict["id"] = randrange(0, 100000)
    
    my_posts.append(post_dict)

    return {"message" : f"Created {post_dict}"}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id : int):
    index = find_post_index(id)

    if index == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {id} not found!")

    my_posts.pop(index)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
async def update_post(id : int, post : Post):
    index = find_post_index(id)

    if index == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {id} not found!")
    
    post_dict = post.model_dump()
    post_dict["id"] = id

    my_posts[index] = post_dict

    return {"message" : f"Post updated successfully : {post_dict}"}


#3:0:0