from pydantic import BaseModel
from typing import Optional, List


# === User Schemas ===
class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str


# === Game Schemas ===
class GameCreate(BaseModel):
    title: str
    description: str
    price: float
    developer_id: Optional[int] = None


class GameResponse(BaseModel):
    id: int
    title: str
    description: str
    price: float
    developer_id: int


# === Library Schemas ===
class LibraryResponse(BaseModel):
    id: int
    title: str
    description: str


# === Token Schemas ===
class Token(BaseModel):
    access_token: str
    token_type: str
