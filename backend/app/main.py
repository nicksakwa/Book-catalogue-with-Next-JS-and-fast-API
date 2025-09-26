# book-catalog-app/backend/app/main.py

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware  # <-- CORS FIX IMPORT
from sqlalchemy.orm import Session
from typing import List

from .database import engine, Base, get_db
# ----------------------------------------------------------------------
# IMPORT FIX: Explicitly import 'crud' on its own line to solve the ImportError
from . import models, schemas
from . import crud 
# ----------------------------------------------------------------------

# 1. Database Setup
def create_tables():
    Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # This runs on startup
    create_tables()
    yield

# 2. FastAPI Application Instance
app = FastAPI(lifespan=lifespan)

# 3. CORS CONFIGURATION (NETWORK SECURITY FIX)
origins = [
    # Allow frontend running on localhost:3000
    "http://localhost:3000",
    # Allow frontend service running inside Docker (internal network)
    "http://frontend:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (POST, GET, etc.)
    allow_headers=["*"],  # Allows all headers
)

# 4. API Endpoints
# IMPORTANT: Replace these placeholders with your actual endpoint functions!

# Placeholder for POST /api/v1/books/ (Add Book)
@app.post("/api/v1/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    # This is where your CRUD logic (create_book) is called
    return crud.create_book(db=db, book=book)

# Placeholder for GET /api/v1/books/ (List Books)
@app.get("/api/v1/books/", response_model=List[schemas.Book])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # This is where your CRUD logic (get_books) is called
    books = crud.get_books(db, skip=skip, limit=limit)
    return books

# Placeholder for GET / (Optional health check)
@app.get("/")
def read_root():
    return {"Hello": "FastAPI is running!"}