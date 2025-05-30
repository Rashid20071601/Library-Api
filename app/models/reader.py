from sqlalchemy import Column, Integer, String
from app.db.base_class import Base


class Reader(Base):
    __tablename__ = 'readers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)