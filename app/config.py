from pydantic import BaseModel
from dotenv import load_dotenv
import os
load_dotenv()
class Settings(BaseModel):
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./movies.sqlite3")
settings = Settings()