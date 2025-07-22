from sqlalchemy import func
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db
from fastapi import status, HTTPException, Depends, APIRouter, Response
from typing import List, Optional

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


# GET ALL POSTS
@router.get("/all", response_model=List[schemas.PostOut])
async def get_all_posts(db : Session = Depends(get_db), 
                        user_id : int = Depends(oauth2.get_current_user), 
                        limit : int = 10, 
                        skip : int = 0, 
                        search : Optional[str] = ""):
    #cursor.execute('''SELECT * FROM posts''')
    #posts = cursor.fetchall()
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    results = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(
        models.Votes, models.Votes.post_id == models.Post.id).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    #results = list(map(lambda x : x._mapping, results)) ------------> IMPORTANT : TO CHECK THE SHAPE OF JSON BEING RETURNED, NEED TO RUN A LAMBDA FUNCTION TO APPLY ._MAPPING TO EACH ITERABLE

    return results

# GET SINGLE POST
@router.get("/{id}", response_model=schemas.PostOut)
async def get_single_post(id : int, db : Session = Depends(get_db), user_id : int = Depends(oauth2.get_current_user)):

    # cursor.execute('''SELECT * FROM posts WHERE id = %s ''', (str(id),))
    # post = cursor.fetchone()

    #post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Post.id).label("votes")).join(
        models.Votes, models.Votes.post_id == models.Post.id).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 
                            detail = f"Post with id: {id} not found!")
    
    return post
    

# CREATE POST
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
async def create_post(post : schemas.PostCreate, db : Session = Depends(get_db), user_id : int = Depends(oauth2.get_current_user)):

    # cursor.execute('''INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *''', 
    #                (post.title, post.content, post.published))

    # new_post = cursor.fetchone()
    # conn.commit()
    post_dict = post.model_dump()
    post_dict.update({"owner_id" : user_id.id})
    new_post = models.Post(**post_dict)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

# DELETE POST
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id : int, db : Session = Depends(get_db), user_id : int = Depends(oauth2.get_current_user)):
    # cursor.execute('''DELETE FROM posts WHERE id = %s RETURNING *''', (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post = db.query(models.Post).filter(models.Post.id == id)

    if not post.first():
        raise HTTPException(status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {id} not found!")
    
    if post.first().owner_id != user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform that action")

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

# UPDATE POST
@router.put("/{id}", response_model=schemas.PostResponse)
async def update_post(id : int, post : schemas.PostCreate, db : Session = Depends(get_db), user_id = Depends(oauth2.get_current_user)):
    # cursor.execute('''UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *''', (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    if not post_query.first():
        raise HTTPException(status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {id} not found!")
    
    if post_query.first().owner_id != user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this action")

    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()

    return post_query.first()