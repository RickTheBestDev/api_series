from fastapi import FastAPI
from typing import Optional 

app = FastAPI()

@app.get("/")
def read_root():
    return {"mensagem": "Olá Mundo!"}

@app.get("/itens/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

@app.get("/soma/{num1}/{num2}")
def read_soma (num1: int, num2: int):
    return {"resultado": num1 + num2}

@app.get("/adicao/{a}/{b}")
def adicao (a: int, b: int):
    return {"soma": a + b}