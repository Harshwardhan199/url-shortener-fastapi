from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import Base, engine
from app import models

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="URL Shortener API",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
def root():
    return {
        "message": "URL Shortener API is running"
    }