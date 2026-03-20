from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
import sqlite3

from ..database import get_db
from ..schemas import UserCreate, Token
from ..auth import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/api", tags=["Users"])


@router.post("/register")
def register(user: UserCreate, db: sqlite3.Connection = Depends(get_db)):
    """Регистрация нового пользователя"""
    cursor = db.cursor()
    hashed = hash_password(user.password)

    try:
        cursor.execute(
            "INSERT INTO Users (username, email, password_hash, role) VALUES (?, ?, ?, ?)",
            (user.username, user.email, hashed, 'Игрок')
        )
        db.commit()
        return {"msg": "Пользователь успешно зарегистрирован"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Пользователь или email уже существует")


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: sqlite3.Connection = Depends(get_db)):
    """Авторизация пользователя"""
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Users WHERE username = ?", (form_data.username,))
    user = cursor.fetchone()

    if not user or not verify_password(form_data.password, user['password_hash']):
        raise HTTPException(status_code=400, detail="Неверный логин или пароль")

    token = create_access_token(data={"sub": user["username"]})
    return {"access_token": token, "token_type": "bearer"}
