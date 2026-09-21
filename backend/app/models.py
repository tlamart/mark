from sqlmodel import Field, SQLModel

class Books(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    author: str
    current_page: int
    total_page: int
    reading_time: int | None = Field(default=0)