# Импорт функций для подключения к базе данных и создания сессий
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# URL подключения к базе данных PostgreSQL
DATABASE_URL = "postgresql+psycopg2://postgres:admin@localhost:5432/library_db"

# Создание движка базы данных
engine = create_engine(DATABASE_URL)

# Создание фабрики сессий для взаимодействия с базой
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
