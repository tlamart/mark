from fastapi import HTTPException, APIRouter
from app.schemas import Book, Book_update
from app.database import SessionDep
from app.models import Books
from sqlmodel import select

router = APIRouter()

@router.get("/books")
def get_books(session: SessionDep):
    books = session.exec(select(Books)).all()
    return books

@router.get("/books/{id}")
def get_book(id: int, session: SessionDep):
    book = session.get(Books, id)
    if not book:
        raise HTTPException(status_code=404, detail="book not find")
    return book

@router.post("/books")
def add_book(book: Book, session: SessionDep):
    db_book = Books(**book.model_dump())
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book

@router.patch("/books/{id}")
def update_book(id: int, book_update: Book_update, session: SessionDep):
    book = session.get(Books, id)
    if not book:
        raise HTTPException(status_code=404, detail="book not find")
    if book_update.current_page is not None:
        book.current_page = book_update.current_page
    if book_update.reading_time is not None:
        book.reading_time = book_update.reading_time
    session.commit()
    session.refresh(book)
    return book

@router.delete("/books/{id}")
def delete_book(id: int, session: SessionDep):
    book = session.get(Books, id)
    if not book:
        raise HTTPException(status_code=404, detail="book not find")
    session.delete(book)
    session.commit()
    return({"message": "book successfully deleted"})