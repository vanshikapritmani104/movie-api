from typing import List
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from ..database import get_session
from ..services.movie_service import MovieService
from ..schemas import MovieCreate, MovieUpdate, MovieRead

router = APIRouter(prefix="/movies", tags=["Movies"])

@router.get("", response_model=List[MovieRead], summary="List all movies with pagination")
def list_movies(
    offset: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(50, ge=1, le=200, description="Max items to return"),
    session: Session = Depends(get_session),
):
    return MovieService(session).list_movies(offset=offset, limit=limit)

@router.get("/{movie_id}", response_model=MovieRead, summary="Get a movie by ID")
def get_movie(movie_id: str, session: Session = Depends(get_session)):
    return MovieService(session).get_movie(movie_id)

@router.post("", response_model=MovieRead, status_code=201, summary="Create a new movie")
def create_movie(payload: MovieCreate, session: Session = Depends(get_session)):
    return MovieService(session).create_movie(payload)

@router.put("/{movie_id}", response_model=MovieRead, summary="Update an existing movie")
def update_movie(movie_id: str, payload: MovieUpdate, session: Session = Depends(get_session)):
    return MovieService(session).update_movie(movie_id, payload)

@router.delete("/{movie_id}", status_code=204, summary="Delete a movie by ID")
def delete_movie(movie_id: str, session: Session = Depends(get_session)):
    MovieService(session).delete_movie(movie_id)
    return None