# Импорты библиотек
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
# Импорты из проекта
from app.models.user import User
from app.schemas.user import UserCreate, LoginRequest
from app.core.security import verify_password, get_current_user
from app.crud.user import create_user
from app.db.session import get_db
# Константы для генерации JWT токена
from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from pydantic import BaseModel, EmailStr


router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    # Создание нового пользователя в базе
    user = create_user(db, user_in)
    if user is None:
        # Пользователь с таким email уже существует
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с таким email уже существует"
        )
    # Возвращаем данные нового пользователя
    return {"email": user.email, "id": user.id}


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    # Получение email и пароля из запроса
    email = data.email
    password = data.password

    if not email or not password:
        # Проверка на наличие обязательных полей
        raise HTTPException(status_code=400, detail="Email и пароль обязательны")
    
    # Поиск пользователя по email в базе
    user = db.query(User).filter(User.email == email).first()

    # Проверка пароля
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Неверные учётные данные")

    # Создание токена с user_id и временем истечения
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"user_id": user.id, "exp": expire}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    # Возвращаем access token и тип токена
    return {"access_token": token, "token_type": "bearer"}


# Эндпоинт для получения информации о текущем авторизованном пользователе
@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {"id": current_user.id, "email": current_user.email}

