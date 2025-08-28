from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from app.database import get_session
from app.models import Movie
from app.schemas import MovieCreate, MovieRead, MovieUpdate

router = APIRouter(prefix="/movies", tags=["Movies"])

# Create movie
@router.post("/", response_model=MovieRead, status_code=201, summary="Create Movie")
def create_movie(movie: MovieCreate, session: Session = Depends(get_session)):
    db_movie = Movie(**movie.dict())
    session.add(db_movie)
    session.commit()
    session.refresh(db_movie)
    return db_movie

# List movies
@router.get("/", response_model=List[MovieRead], summary="List Movies")
def list_movies(offset: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    movies = session.exec(select(Movie).offset(offset).limit(limit)).all()
    return movies

# Get single movie
@router.get("/{movie_id}", response_model=MovieRead, summary="Get Movie")
def get_movie(movie_id: int, session: Session = Depends(get_session)):
    movie = session.get(Movie, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

# Update movie
@router.put("/{movie_id}", response_model=MovieRead, summary="Update Movie")
def update_movie(movie_id: int, data: MovieUpdate, session: Session = Depends(get_session)):
    movie = session.get(Movie, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    for key, value in data.dict(exclude_unset=True).items():
        setattr(movie, key, value)
    session.add(movie)
    session.commit()
    session.refresh(movie)
    return movie

# Delete movie
@router.delete("/{movie_id}", status_code=204, summary="Delete Movie")
def delete_movie(movie_id: int, session: Session = Depends(get_session)):
    movie = session.get(Movie, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    session.delete(movie)
    session.commit()
    return None