from fastapi import FastAPI
from app.api import auth, books, readers, borrowed_books  # импортируем router

app = FastAPI()

app.include_router(auth.router, prefix="/api")
app.include_router(books.router, prefix="/api")
app.include_router(readers.router, prefix="/api")
app.include_router(borrowed_books.router, prefix="/api")
