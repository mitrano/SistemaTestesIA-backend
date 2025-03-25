from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import sqlite3
import json

class TestRequest(BaseModel):
    prompt: str
    questions_count: int
    question_type: str
    difficulty: str

class TestResponse(BaseModel):
    id: int
    title: str
    questions: dict

# ✅ Definir o cliente corretamente

DATABASE = "tests.db"

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🔄 Configurando o banco de dados...")
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            questions TEXT
        )
    ''')
    conn.commit()
    conn.close()
    yield
    print("✅ Banco de dados configurado com sucesso!")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/tests")
async def create_test(request: TestRequest):
    prompt = f"""
    Crie um teste de {request.questions_count} questões sobre {request.prompt}.
    Tipo: {request.question_type}.
    Dificuldade: {request.difficulty}.
    Formato JSON: {{ "questions": [{{ "question": "", "options": [], "answer": "" }}] }}
    """

    # ✅ Usando o objeto `client` corretamente
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um gerador de testes de múltipla escolha."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )

    questions = response.choices[0].message.content.strip()

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tests (title, questions) VALUES (?, ?)",
        (request.prompt, questions)
    )
    conn.commit()
    conn.close()

    return {"message": "Teste criado com sucesso"}

@app.get("/tests")
def get_tests():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, questions FROM tests")
    tests = cursor.fetchall()
    conn.close()
    return [{"id": t[0], "title": t[1], "questions": json.loads(t[2])} for t in tests]

@app.delete("/tests/{test_id}")
def delete_test(test_id: int):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tests WHERE id = ?", (test_id,))
    conn.commit()
    conn.close()
    return {"message": "Teste excluído"}
