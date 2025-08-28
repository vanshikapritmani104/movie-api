from fastapi import FastAPI
from app.database import engine
from app import models
from app.routers import movies
app = FastAPI(
    title="Movie Management API",
    version="1.0.0",
    description="A simple Movie CRUD service with pagination, validation, and Swagger docs."
)
@app.on_event("startup")
def on_startup():
    models.SQLModel.metadata.create_all(engine)
app.include_router(movies.router)