from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password


# Создание нового пользователя в базе данных
def create_user(db: Session, user_in: UserCreate) -> User:
    # Хешируем пароль перед сохранением
    hashed_pw = hash_password(user_in.password)

    # Создаем ORM-объект пользователя
    user = User(email=user_in.email, hashed_password=hashed_pw)

    db.add(user)
    try:
        # Пытаемся сохранить пользователя в базе
        db.commit()
        # Обновляем объект, чтобы получить его ID и другие поля
        db.refresh(user)
        return user
    except IntegrityError:
        # Если email уже занят (уникальность нарушена), откатываем транзакцию
        db.rollback()
        return None