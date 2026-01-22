from fastapi import FastAPI
from app.database import engine

app = FastAPI()

@app.get("/")
def test_db():
    engine.connect()
    return {"message": "PostgreSQL connected successfully (Docker)"}
