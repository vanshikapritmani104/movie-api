from typing import Optional
from sqlmodel import SQLModel

class MovieCreate(SQLModel):
    title: str
    director: str
    release_year: int   # changed from releaseYear
    genre: str
    rating: float

class MovieUpdate(SQLModel):
    title: Optional[str] = None
    director: Optional[str] = None
    release_year: Optional[int] = None   # changed
    genre: Optional[str] = None
    rating: Optional[float] = None

class MovieRead(SQLModel):
    id: int
    title: str
    director: str
    release_year: int   # changed
    genre: str
    rating: float