from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.db.main import init_db
from src.auth.routes import auth_router
@asynccontextmanager
async def life_span(app:FastAPI):
    print("application is starting")
    await init_db()
    yield
    print("server shutdown")

app = FastAPI(
    title = "Bookly",
    description = "rest api for book review service",
    lifespan= life_span
)

app.include_router(auth_router, prefix = f"/api/auth", tags= ["auth"])
