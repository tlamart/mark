from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return({"message":"hello world!"})

@app.get("/books")
def get_books():
    return []
# TODOUM connect to SQLite and return list of every book

@app.post("/books")
def add_book():
    pass
# TODOUM

@app.patch("/books/{id}")
def update_book_id(id :int):
    pass
# TODOUM