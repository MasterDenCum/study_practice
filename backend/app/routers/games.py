from fastapi import APIRouter, Depends
import sqlite3

from ..database import get_db
from ..schemas import GameResponse

router = APIRouter(prefix="/api", tags=["Games"])


@router.get("/games", response_model=list[GameResponse])
def get_games(db: sqlite3.Connection = Depends(get_db)):
    """Получение списка всех игр"""
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Games")
    return [dict(row) for row in cursor.fetchall()]
