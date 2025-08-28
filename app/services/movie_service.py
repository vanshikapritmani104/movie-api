import uuid
from typing import Sequence
from sqlmodel import Session
from fastapi import HTTPException, status

from ..models import Movie
from ..schemas import MovieCreate, MovieUpdate
from ..dao.movie_dao import MovieDAO


class MovieService:
    def __init__(self, session: Session):
        self.dao = MovieDAO(session)

    def list_movies(self, offset: int = 0, limit: int = 50) -> Sequence[Movie]:
        return self.dao.list(offset=offset, limit=limit)

    def get_movie(self, movie_id: str) -> Movie:
        movie = self.dao.get(movie_id)
        if not movie:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Movie not found"
            )
        return movie

    def create_movie(self, data: MovieCreate) -> Movie:
        movie = Movie(
            id=str(uuid.uuid4()),   # generates unique ID
            title=data.title.strip(),
            director=data.director,
            releaseYear=data.releaseYear,
            genre=data.genre,
            rating=data.rating,
        )
        return self.dao.create(movie)

    def update_movie(self, movie_id: str, data: MovieUpdate) -> Movie:
        movie = self.dao.get(movie_id)
        if not movie:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Movie not found"
            )

        # apply partial updates
        if data.title is not None:
            movie.title = data.title.strip()
        if data.director is not None:
            movie.director = data.director
        if data.releaseYear is not None:
            movie.releaseYear = data.releaseYear
        if data.genre is not None:
            movie.genre = data.genre
        if data.rating is not None:
            movie.rating = data.rating

        return self.dao.update(movie)

    def delete_movie(self, movie_id: str) -> None:
        movie = self.dao.get(movie_id)
        if not movie:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Movie not found"
            )
        self.dao.delete(movie)