import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware  # <-- CORS FIX IMPORT
from sqlalchemy.orm import Session
from typing import List

from .database import engine, Base, get_db
from . import models, schemas
from . import crud 

# 1. Database Setup
def create_tables():
    Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
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
@app.post("/api/v1/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)

@app.get("/api/v1/books/", response_model=List[schemas.Book])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    books = crud.get_books(db, skip=skip, limit=limit)
    return books


# GET a single book by id
@app.get("/api/v1/books/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book(db, book_id=book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


# PUT to update a book
@app.put("/api/v1/books/{book_id}", response_model=schemas.Book)
def update_book(book_id: int, book_update: schemas.BookUpdate, db: Session = Depends(get_db)):
    updated = crud.update_book(db, book_id=book_id, book_update=book_update)
    if not updated:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated


# DELETE a book
@app.delete("/api/v1/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_book(db, book_id=book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"detail": "Book deleted"}

# Placeholder for GET / (Optional health check)
@app.get("/")
def read_root():
    return {"Hello": "FastAPI is running!"}