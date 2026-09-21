from fastapi import FastAPI
from app.routes import books
from app.database import create_db_and_tables
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

@app.get("/")
def root(name: str | None = None):
    if name:
        return({"message":f"hello {name}!"})
    else:
        return({"message":"hello world!"})

app.include_router(books.router)