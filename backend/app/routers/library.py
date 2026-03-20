from fastapi import APIRouter, Depends, HTTPException
import sqlite3
import datetime

from ..database import get_db
from ..schemas import LibraryResponse
from ..auth import get_current_user

router = APIRouter(prefix="/api", tags=["Library"])


@router.post("/buy/{game_id}")
def buy_game(
    game_id: int,
    current_user: dict = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db)
):
    """Покупка игры и добавление в библиотеку"""
    cursor = db.cursor()
    
    # Проверка, есть ли уже игра в библиотеке
    cursor.execute(
        "SELECT * FROM Library WHERE user_id = ? AND game_id = ?",
        (current_user["id"], game_id)
    )
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="Игра уже есть в библиотеке")

    # Добавление в библиотеку (моментальная доставка)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO Library (user_id, game_id, purchase_date) VALUES (?, ?, ?)",
        (current_user["id"], game_id, now)
    )
    db.commit()
    
    return {"msg": "Игра успешно куплена и добавлена в библиотеку"}


@router.get("/library", response_model=list[LibraryResponse])
def get_library(
    current_user: dict = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db)
):
    """Получение библиотеки пользователя"""
    cursor = db.cursor()
    
    # JOIN для получения купленных игр
    cursor.execute('''
        SELECT Games.id, Games.title, Games.description
        FROM Library
        JOIN Games ON Library.game_id = Games.id
        WHERE Library.user_id = ?
    ''', (current_user["id"],))
    
    return [dict(row) for row in cursor.fetchall()]
