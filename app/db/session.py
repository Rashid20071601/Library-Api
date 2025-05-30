# Импорт функций для подключения к базе данных и создания сессий
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Загрузка переменных окружения из .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


# Создание движка базы данных
engine = create_engine(DATABASE_URL)

# Создание фабрики сессий для взаимодействия с базой
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Зависимость для FastAPI: возвращает подключение к БД и закрывает его после запроса
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()