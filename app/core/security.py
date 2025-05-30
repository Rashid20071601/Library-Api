from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# То же значение, что и в auth.py

# Определяем URL, откуда ожидается получить токен
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")


# Хеширование пароля при регистрации
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Проверка соответствия пароля и его хеша при логине
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)



# Зависимость, которая проверяет JWT-токен и возвращает текущего пользователя
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:

    # Общая ошибка, которую возвращаем, если токен некорректен или пользователь не найден
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось подтвердить учетные данные!",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Расшифровка токена и извлечение user_id
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        # Ошибка валидации JWT
        raise credentials_exception

    # Поиск пользователя в базе данных по user_id
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception

    # Авторизация прошла успешно — возвращаем объект пользователя
    return user