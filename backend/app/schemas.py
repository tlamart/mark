from pydantic import BaseModel

class Book(BaseModel):
    title: str
    author: str
    current_page: int
    total_page: int
    reading_time : int | None = 0

class Book_update(BaseModel):
    current_page: int | None = None
    reading_time : int | None = None