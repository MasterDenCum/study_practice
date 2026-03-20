from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import init_db
from app.routers import users, games, library

# Инициализация БД при старте
init_db()

app = FastAPI(title="Nexus Play API")

# Настройка CORS для связи с React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(users.router)
app.include_router(games.router)
app.include_router(library.router)


@app.get("/")
def root():
    """Корневой эндпоинт"""
    return {"message": "Nexus Play API", "status": "running"}


@app.get("/health")
def health():
    """Проверка здоровья"""
    return {"status": "healthy"}
