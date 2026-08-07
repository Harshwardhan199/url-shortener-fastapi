from contextlib import asynccontextmanager

from fastapi import FastAPI

import app.models
from app.api import router
from app.config import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="URL Shortener API",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(
    router,
    tags=["URL Shortener"],
)


@app.get("/")
def root():
    return {
        "message": "URL Shortener API is running"
    }