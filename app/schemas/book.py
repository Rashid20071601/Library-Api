from pydantic import BaseModel, Field


# Схема для возврата информации о книге
class BookOut(BaseModel):
    id: int
    title: str
    author: str
    publication_year: int | None
    isbn: str | None
    copies: int

    model_config = {
        "from_attributes": True      # Позволяет Pydantic преобразовывать из ORM-моделей (SQLAlchemy → Pydantic)
    }


# Схема для валидации входных данных при создании новой книги
class BookCreate(BaseModel):
    title: str
    author: str
    publication_year: int | None = None
    isbn: str | None = None
    copies: int = Field(1, ge=0)  # Минимум 0 экземпляров


# Схема для обновления книги (все поля необязательны)
class BookUpdate(BaseModel):
    title: str | None
    author: str | None
    publication_year: int | None
    isbn: str | None
    copies: int = Field(default=None, ge=0)