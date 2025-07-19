from fastapi import FastAPI, Response, status, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db
from typing import List
from .routers import post, user, auth


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

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


# 6: 50: 00


