from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import HTTPException

app = FastAPI()

class Book(BaseModel):
    title: str
    author: str
    current_page: int
    total_page: int
    reading_time : int = 0
    id: int

class Book_update(BaseModel):
    current_page: int | None = None
    reading_time : int | None = None

books = [
    Book(
    title = "one piece 1",
    author = "eiichiro oda",
    current_page = 0,
    reading_time = 0,
    total_page = 100,
    id = 1),
    Book(
    title = "one piece 2",
    author = "eiichiro oda",
    reading_time = 0,
    current_page = 0,
    total_page = 100,
    id = 2),
    Book(
    title = "one piece 3",
    author = "eiichiro oda",
    reading_time = 0,
    current_page = 0,
    total_page = 100,
    id = 3)
]

@app.get("/")
def root(name: str | None = None):
    if name:
        return({"message":f"hello {name}!"})
    else:
        return({"message":"hello world!"})

@app.get("/books")
def get_books():
    return books

@app.get("/books/{id}")
def get_book(id :int):
    for book in books:
        if book.id == id:
            return book
    raise HTTPException(status_code=404, detail="book not find")

@app.post("/books")
def add_book(book: Book):
    books.append(book)
    return books

@app.patch("/books/{id}")
def update_book(id :int, book_update: Book_update):
    for book in books:
        if book.id == id:
            if book_update.current_page is not None:
                book.current_page = book_update.current_page
            if book_update.reading_time is not None:
                book.reading_time = book_update.reading_time
            return book
    raise HTTPException(status_code=404, detail="book not find")

@app.delete("/books/{id}")
def delete_book(id :int):
    for i in range(0, len(books)):
        if books[i].id == id:
            books.pop(i)
            return({"message": "book successfully deleted"})
    raise HTTPException(status_code=404, detail=f"book_id {id} not find")