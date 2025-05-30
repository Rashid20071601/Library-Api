from sqlalchemy import Column, Integer, ForeignKey, DateTime
from datetime import datetime
from app.db.base_class import Base

class BorrowedBook(Base):
    __tablename__ = "borrowed_books"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    reader_id = Column(Integer, ForeignKey("readers.id", ondelete="CASCADE"), nullable=False)
    borrow_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    return_date = Column(DateTime, nullable=True)
