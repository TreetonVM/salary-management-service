from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    async with engine.begin() as connection:
        pass
    yield
    # Shutdown code
    await engine.dispose()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def read_root():
    return {"message": "Welcome to Remunify!"}
