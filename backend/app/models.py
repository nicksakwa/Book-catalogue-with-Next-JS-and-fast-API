from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(100), index=True, nullable=False)
    author = Column(String(100), index=True, nullable=False)
    publication_year = Column(Integer, index=True, nullable=True)
    isbn = Column(String(13), unique=True, index=True, nullable=True)