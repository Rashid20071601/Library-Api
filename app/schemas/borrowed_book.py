from pydantic import BaseModel
from datetime import datetime

class BorrowRequest(BaseModel):
    book_id: int
    reader_id: int


class ReturnRequest(BaseModel):
    borrow_id: int
    reader_id: int


class BorrowedInfo(BaseModel):
    id: int
    book_id: int
    borrow_date: datetime
    return_date: datetime | None

    class Config:
        from_attributes = True  # т.к. данные из ORM
