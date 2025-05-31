from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.book import Book
from app.models.reader import Reader
from app.models.borrowed_book import BorrowedBook
from app.schemas.borrowed_book import BorrowRequest, ReturnRequest, BorrowedInfo
from app.core.security import get_current_user

from datetime import datetime

router = APIRouter()


# Эндпоинт для выдачи книги.
@router.post("/borrow", status_code=status.HTTP_201_CREATED)
def borrow_book(data: BorrowRequest, db: Session = Depends(get_db), user=Depends(get_current_user)):
    # Проверка существования книги и читателя
    book = db.query(Book).filter(Book.id == data.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")

    if book.copies < 1:
        raise HTTPException(status_code=400, detail="Нет доступных экземпляров книги")

    reader = db.query(Reader).filter(Reader.id == data.reader_id).first()
    if not reader:
        raise HTTPException(status_code=404, detail="Читатель не найден")
    
    # Проверка: не более 3-х активных книг у читателя
    active_borrows = db.query(BorrowedBook).filter(
        BorrowedBook.reader_id == data.reader_id,
        BorrowedBook.return_date == None
    ).count()

    if active_borrows >= 3:
        raise HTTPException(
            status_code=400,
            detail="Читатель уже держит максимально допустимое количество книг (3)"
        )

    # Создание записи о выдаче
    record = BorrowedBook(
        book_id=data.book_id,
        reader_id=data.reader_id,
        borrow_date=datetime.utcnow()
    )
    db.add(record)

    # Уменьшаем количество экземпляров
    book.copies -= 1
    db.commit()
    db.refresh(record)

    return {
        "borrow_id": record.id,
        "book_id": book.id,
        "reader_id": reader.id,
        "borrow_date": record.borrow_date
    }


# Возврат книги
@router.post("/return")
def return_book(data: ReturnRequest, db: Session = Depends(get_db), user=Depends(get_current_user)):
    record = db.query(BorrowedBook).filter(BorrowedBook.id == data.borrow_id).first()

    if not record:
        raise HTTPException(status_code=404, detail="Запись о выдаче не найдена")

    if record.return_date:
        raise HTTPException(status_code=400, detail="Книга уже возвращена")

    # Обновляем дату возврата
    record.return_date = datetime.utcnow()

    # Увеличиваем copies у книги
    book = db.query(Book).filter(Book.id == record.book_id).first()
    if book:
        book.copies += 1

    db.commit()
    db.refresh(record)

    return {
        "borrow_id": record.id,
        "book_id": record.book_id,
        "return_date": record.return_date
    }


@router.get("/borrowed/{reader_id}", response_model=List[BorrowedInfo])
def get_borrowed_books(reader_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(BorrowedBook).filter(
        BorrowedBook.reader_id == reader_id,
        BorrowedBook.return_date.is_(None)
    ).all()