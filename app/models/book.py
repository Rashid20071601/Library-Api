from sqlalchemy import Column, Integer, String, CheckConstraint
from sqlalchemy.orm import validates
from app.db.base_class import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    publication_year = Column(Integer, nullable=True)
    isbn = Column(String, unique=True, nullable=True)
    copies = Column(Integer, default=1, nullable=False)

    __table_args__ = (
        CheckConstraint("copies >= 0", name="copies_positive"),
    )

    @validates('copies')
    def validate_copies(self, key, value):
        if value < 0:
            raise ValueError("Количество экземпляров не может быть меньше 0")
        return value