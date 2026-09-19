from fastapi import FastAPI
from app.routes import books

app = FastAPI()

@app.get("/")
def root(name: str | None = None):
    if name:
        return({"message":f"hello {name}!"})
    else:
        return({"message":"hello world!"})

app.include_router(books.router)