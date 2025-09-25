from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from . import models, schemas
from .database import engine, Base, get_db

# Create the database tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI()

# --- CRUD Operations ---

@app.get("/books", response_model=List[schemas.Book])
def read_books(db: Session = Depends(get_db)):
    """Return a list of all books."""
    return db.query(models.Book).all()

@app.get("/books/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    """Return a single book by ID."""
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@app.post("/books", response_model=schemas.Book, status_code=status.HTTP_201_CREATED)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    """Create a new book."""
    db_book = models.Book(**book.model_dump(exclude_unset=True))
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@app.put("/books/{book_id}", response_model=schemas.Book)
def update_book(book_id: int, book: schemas.BookUpdate, db: Session = Depends(get_db)):
    """Update an existing book by ID."""
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # Update fields only if they are provided in the request body
    update_data = book.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_book, key, value)
    
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """Delete a book by ID."""
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book is None:
        # Returning 204 even if not found is acceptable for DELETE (idempotent)
        return
    
    db.delete(db_book)
    db.commit()
    return