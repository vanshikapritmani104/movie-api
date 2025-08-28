from sqlmodel import SQLModel, Field
from typing import Optional

class MovieBase(SQLModel):
    title: str
    director: str
    releaseYear: int
    genre: str
    rating: float

class Movie(MovieBase, table=True):   # <-- DB model
    id: Optional[int] = Field(default=None, primary_key=True)

class MovieCreate(MovieBase):         # <-- request schema
    pass

class MovieRead(MovieBase):           # <-- response schema
    id: int