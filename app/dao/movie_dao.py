from typing import Optional, Sequence
from sqlmodel import Session, select
from ..models import Movie
class MovieDAO:
    def __init__(self, session: Session):
        self.session = session
    def list(self, offset: int = 0, limit: int = 50) -> Sequence[Movie]:
        statement = select(Movie).offset(offset).limit(limit)
        return self.session.exec(statement).all()
    def get(self, movie_id: str) -> Optional[Movie]:
        return self.session.get(Movie, movie_id)
    def create(self, movie: Movie) -> Movie:
        self.session.add(movie)
        self.session.commit()
        self.session.refresh(movie)
        return movie
    def update(self, movie: Movie) -> Movie:
        self.session.add(movie)
        self.session.commit()
        self.session.refresh(movie)
        return movie
    def delete(self, movie: Movie) -> None:
        self.session.delete(movie)
        self.session.commit()