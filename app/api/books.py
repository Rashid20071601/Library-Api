from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy.exc import IntegrityError

from app.models.book import Book
from app.schemas.book import BookOut, BookCreate, BookUpdate
from app.db.session import get_db
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter()


# возвращает список всех книг в библиотеке (доступен всем)
@router.get("/books", response_model=List[BookOut])
def list_books(db: Session = Depends(get_db)):

    # Получаем все книги из базы
    books = db.query(Book).all()
    return books  # Сериализация происходит автоматически через BookOut


# Защищённый эндпоинт: создаёт новую книгу в библиотеке
@router.post("/books", response_model=BookOut, status_code=status.HTTP_201_CREATED)
def create_book(book_in: BookCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Создание объекта книги из входных данных
    book = Book(**book_in.dict()) # Распаковываем словарь из Pydantic-модели в аргументы конструктора ORM-модели

    db.add(book)
    try:
        db.commit()
        db.refresh(book)
        return book
    except IntegrityError:
        # Если ISBN уже существует
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Книга с таким ISBN уже существует"
        )
    

@router.patch("/books/{book_id}", response_model=BookOut)
def update_book(book_id: int, book_in: BookUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Поиск книги по ID
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")

    # Проверка на дубликат ISBN, если был передан
    if book_in.isbn and book_in.isbn != book.isbn:
        isbn_exists = db.query(Book).filter(Book.isbn == book_in.isbn).first()
        if isbn_exists:
            raise HTTPException(
                status_code=400,
                detail="Книга с таким ISBN уже существует"
            )

    # Обновление только переданных полей
    for field, value in book_in.dict(exclude_unset=True).items():
        setattr(book, field, value)

    db.commit()
    db.refresh(book)

    return book


@router.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Поиск книги по ID
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")

    # Удаление книги из базы
    db.delete(book)
    db.commit()

    # Возвращаем 204 No Content в ответе
    return
