from sqlmodel import SQLModel, Field
from typing import Optional
class MovieBase(SQLModel):
    title: str
    director: str
    releaseYear: int
    genre: str
    rating: float
class Movie(MovieBase, table=True):   
    id: Optional[int] = Field(default=None, primary_key=True)
class MovieCreate(MovieBase):         
    pass
class MovieRead(MovieBase):           
    id: int