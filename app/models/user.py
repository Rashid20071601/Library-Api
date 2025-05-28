from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.db.base import Base

# Модель пользователя (таблица users в базе данных)
class User(Base):
    __tablename__ = "users"  # Название таблицы

    id = Column(Integer, primary_key=True, autoincrement=True)  # Уникальный идентификатор
    email = Column(String, unique=True, index=True, nullable=False)  # Email пользователя
    hashed_password = Column(String, nullable=False)  # Хэшированный пароль
    created_at = Column(DateTime, default=datetime.utcnow)  # Дата создания (по умолчанию текущее время)
