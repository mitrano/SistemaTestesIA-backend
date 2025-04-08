from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import json
import os
import google.generativeai as genai
from openai import OpenAI

class TestRequest(BaseModel):
    prompt: str
    questions_count: int
    question_type: str
    difficulty: str
    provider: str

class TestResponse(BaseModel):
    id: int
    title: str
    questions: dict

# ✅ Configurar a API Gemini usando variável de ambiente
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    raise ValueError("GEMINI_API_KEY não foi configurada nas variáveis de ambiente.")

# Configurar OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY:
    client = OpenAI(api_key=OPENAI_API_KEY)
else:
    raise ValueError("OPENAI_API_KEY não foi configurada nas variáveis de ambiente.")    

DATABASE = "tests.db"

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🔄 Configurando o banco de dados...")
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('''
        DROP TABLE tests 
    ''')
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
    Crie um teste com {request.questions_count} questões sobre o tema "{request.prompt}".
    Tipo de questão: {request.question_type}.
    Nível de dificuldade: {request.difficulty}.

    Caso o tipo de questão seja MULTIPLE_CHOICE, o resultado deve estar **exclusivamente** no seguinte formato JSON:
    {{
    "questions": [
        {{
        "question": "Texto da pergunta",
        "type": "Multipla",
        "options": ["A", "B", "C", "D"],
        "answer": "Resposta correta"
        }},
        ...
    ]
    }}

        Caso o tipo de questão seja discursive, o resultado deve estar **exclusivamente** no seguinte formato JSON:
    {{
    "questions": [
        {{
        "question": "Texto da pergunta",
        "type": "Discursiva",        
        "options": [],
        "answer": "Resposta correta"
        }},
        ...
    ]
    }}



    """

    if request.provider == "gemini":
        if not GEMINI_API_KEY:
            raise HTTPException(status_code=500, detail="GEMINI_API_KEY não configurada.")
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)

        questions_raw = response.text.strip()

        try:
            json.loads(questions_raw)
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail="A IA não respondeu com um JSON válido.")


        try:
            json.loads(questions_raw)
            questions = questions_raw
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail="Resposta da Gemini não está em formato JSON válido.")


    elif request.provider == "openai":
        if not OPENAI_API_KEY:
            raise HTTPException(status_code=500, detail="OPENAI_API_KEY não configurada.")
        
        completion = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )        
        questions_raw = completion.choices[0].message.content.strip()

        try:
            json.loads(questions_raw)
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail="A IA não respondeu com um JSON válido.")


        try:
            json.loads(questions_raw)
            questions = questions_raw
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail="Resposta do OpenAI não está em formato JSON válido.")

    else:
        raise HTTPException(status_code=400, detail="Provedor de IA inválido. Use 'gemini' ou 'openai'.")


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

    results = []
    for t in tests:
        try:
            parsed_questions = json.loads(t[2])
        except json.JSONDecodeError:
            parsed_questions = {"erro": "Formato inválido no campo 'questions'"}

        results.append({
            "id": t[0],
            "title": t[1],
            "questions": parsed_questions
        })

    return results

@app.delete("/tests/{test_id}")
def delete_test(test_id: int):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tests WHERE id = ?", (test_id,))
    conn.commit()
    conn.close()
    return {"message": "Teste excluído"}
