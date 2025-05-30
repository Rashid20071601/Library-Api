from pydantic import BaseModel, EmailStr, Field

# Схема для отображения читателя
class ReaderOut(BaseModel):
    id: int
    name: str
    email: EmailStr

    model_config = {
        "from_attributes": True
    }


# Схема для создания нового читателя
class ReaderCreate(BaseModel):
    name: str
    email: EmailStr


# Схема для обновления читателя (все поля необязательные)
class ReaderUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None