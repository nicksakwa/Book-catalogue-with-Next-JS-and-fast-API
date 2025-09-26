# book-catalog-app/backend/app/main.py

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # <-- NEW IMPORT
from sqlalchemy.orm import Session
from typing import List

from .database import engine, Base, get_db
from . import models, schemas, crud

# 1. Database Setup (same as before)
def create_tables():
    Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # This runs on startup
    create_tables()
    yield

# 2. FastAPI Application Instance
app = FastAPI(lifespan=lifespan)

# 3. CORS CONFIGURATION (THE FIX)
origins = [
    # Allow requests from the frontend running locally (standard browser access)
    "http://localhost:3000",
    # Allow requests from the frontend service running inside Docker (using its internal hostname)
    "http://frontend:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, PUT, DELETE, OPTIONS)
    allow_headers=["*"],  # Allows all headers
)

# 4. API Endpoints (same as before)
# ... (Keep the rest of your API endpoints: POST, GET, PUT, DELETE)
# ...
# For example:
# @app.post("/api/v1/books/", response_model=schemas.Book)
# def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
#     # ... implementation ...
#     pass
# ...