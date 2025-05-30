from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from fastapi import HTTPException, status

from app.models.reader import Reader
from app.schemas.reader import ReaderOut, ReaderCreate, ReaderUpdate
from app.db.session import get_db
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter()


# Получение списка всех читателей
@router.get("/readers", response_model=List[ReaderOut])
def list_readers(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    readers = db.query(Reader).all()
    return readers


# Получение информации о конкретном читателе по ID
@router.get("/readers/{reader_id}", response_model=ReaderOut)
def get_reader(reader_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    reader = db.query(Reader).filter(Reader.id == reader_id).first()
    if not reader:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Читатель не найден"
        )
    return reader


# Регистрация нового читателя
@router.post("/readers", response_model=ReaderOut, status_code=status.HTTP_201_CREATED)
def create_reader(reader_in: ReaderCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Проверка уникальности email
    existing = db.query(Reader).filter(Reader.email == reader_in.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Читатель с таким email уже существует"
        )

    # Создание объекта и сохранение в БД
    reader = Reader(**reader_in.dict())
    db.add(reader)
    db.commit()
    db.refresh(reader)

    return reader


# Обновление информации о читателе
@router.patch("/readers/{reader_id}", response_model=ReaderOut)
def update_reader(reader_id: int, reader_in: ReaderUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Поиск читателя по ID
    reader = db.query(Reader).filter(Reader.id == reader_id).first()
    if not reader:
        raise HTTPException(status_code=404, detail="Читатель не найден")

    # Проверка уникальности нового email (если он передан и отличается)
    if reader_in.email and reader_in.email != reader.email:
        existing = db.query(Reader).filter(Reader.email == reader_in.email).first()
        if existing:
            raise HTTPException(
                status_code=400,
                detail="Читатель с таким email уже существует"
            )

    # Обновление переданных полей
    for field, value in reader_in.dict(exclude_unset=True).items():
        setattr(reader, field, value)

    db.commit()
    db.refresh(reader)

    return reader


# Удаление читателя
@router.delete("/readers/{reader_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reader(
    reader_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Поиск читателя по ID
    reader = db.query(Reader).filter(Reader.id == reader_id).first()
    if not reader:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Читатель не найден"
        )

    # Удаление из базы
    db.delete(reader)
    db.commit()

    # Возвращаем 204 — операция успешна, но без тела ответа
    return
