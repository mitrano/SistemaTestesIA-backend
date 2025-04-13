# Importa o FastAPI para criar a aplicação web
from fastapi import FastAPI, HTTPException
# Importa o Body para capturar corpo de requisições
from fastapi import Body
# Importa BaseModel do Pydantic para validação de dados
from pydantic import BaseModel
# Importa List da biblioteca typing para anotar listas
from typing import List
# Importa middleware para habilitar CORS
from fastapi.middleware.cors import CORSMiddleware
# Importa SQLite para persistência local dos testes
import sqlite3
# Importa JSON para serialização e desserialização
import json
# Importa os para acessar variáveis de ambiente
import os
# Importa a biblioteca do Gemini (Google)
import google.generativeai as genai
# Importa o cliente da API OpenAI
from openai import OpenAI

# Define o formato do corpo esperado na criação de testes
class TestRequest(BaseModel):
    prompt: str
    questions_count: int
    question_type: str
    difficulty: str
    provider: str

# Define a estrutura de resposta de um teste
class TestResponse(BaseModel):
    id: int
    title: str
    questions: dict

# ✅ Configurar a API Gemini usando variável de ambiente
# Configura a chave da API Gemini a partir da variável de ambiente
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# Configura a chave da API Gemini a partir da variável de ambiente
if GEMINI_API_KEY:
# Configura a chave da API Gemini a partir da variável de ambiente
    genai.configure(api_key=GEMINI_API_KEY)
else:
# Configura a chave da API Gemini a partir da variável de ambiente
    raise ValueError("GEMINI_API_KEY não foi configurada nas variáveis de ambiente.")

# Configurar OpenAI
# Configura a chave da API OpenAI a partir da variável de ambiente
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# Configura a chave da API OpenAI a partir da variável de ambiente
if OPENAI_API_KEY:
# Configura a chave da API OpenAI a partir da variável de ambiente
    client = OpenAI(api_key=OPENAI_API_KEY)
else:
# Configura a chave da API OpenAI a partir da variável de ambiente
    raise ValueError("OPENAI_API_KEY não foi configurada nas variáveis de ambiente.")    

# Define o nome do arquivo SQLite usado como banco de dados
DATABASE = "tests.db"

# Importa o decorador asynccontextmanager para o ciclo de vida do FastAPI
from contextlib import asynccontextmanager

@asynccontextmanager
# Função executada no início da aplicação para configurar o banco de dados
async def lifespan(app: FastAPI):
    print("🔄 Configurando o banco de dados...")
# Define o nome do arquivo SQLite usado como banco de dados
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

# Cria a instância da aplicação FastAPI
app = FastAPI(lifespan=lifespan)

# Configura o middleware CORS para permitir requisições de outras origens
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint para criação de um novo teste com IA
@app.post("/tests")
async def create_test(request: TestRequest):
    prompt = f"""
    Crie um teste com {request.questions_count} questões sobre o tema "{request.prompt}".
    Tipo de questão: {request.question_type}.
    Nível de dificuldade: {request.difficulty}.

    Caso o tipo de questão solictada acima seja "mixed" você deve gerar metade das questões como múltipla escolha e a outra metada discursiva.

    Caso o tipo de questão gerada por você seja MULTIPLE_CHOICE, o resultado deve estar **exclusivamente** no seguinte formato JSON:
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

        Caso o tipo de questão gerada por você seja discursive, o resultado deve estar **exclusivamente** no seguinte formato JSON:
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
# Configura a chave da API Gemini a partir da variável de ambiente
        if not GEMINI_API_KEY:
# Configura a chave da API Gemini a partir da variável de ambiente
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
# Configura a chave da API OpenAI a partir da variável de ambiente
        if not OPENAI_API_KEY:
# Configura a chave da API OpenAI a partir da variável de ambiente
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


# Define o nome do arquivo SQLite usado como banco de dados
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tests (title, questions) VALUES (?, ?)",
        (request.prompt, questions)
    )
    conn.commit()
    conn.close()

    return {"message": "Teste criado com sucesso"}

# Endpoint que retorna a lista de testes existentes no banco de dados
@app.get("/tests")
def get_tests():
# Define o nome do arquivo SQLite usado como banco de dados
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, questions FROM tests ORDER BY id DESC")
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

# Endpoint que permite excluir um teste pelo ID
@app.delete("/tests/{test_id}")
def delete_test(test_id: int):
# Define o nome do arquivo SQLite usado como banco de dados
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tests WHERE id = ?", (test_id,))
    conn.commit()
    conn.close()
    return {"message": "Teste excluído"}

# Endpoint que atualiza as questões de um teste específico
@app.put("/tests/{test_id}/questions")
def update_test_questions(test_id: int, questions: dict = Body(...)):
    try:
        questions_json = json.dumps(questions)
    except Exception:
        raise HTTPException(status_code=400, detail="Formato de perguntas inválido. Deve ser um JSON.")

# Define o nome do arquivo SQLite usado como banco de dados
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tests SET questions = ? WHERE id = ?",
        (questions_json, test_id)
    )
    conn.commit()
    conn.close()

    return {"message": "Perguntas atualizadas com sucesso"}

# Modelo de entrada para avaliação de resposta discursiva
class EvaluationRequest(BaseModel):
    question: str
    correct_answer: str
    user_answer: str

# Endpoint que avalia a resposta do aluno comparando com o gabarito
@app.post("/evaluate")
async def evaluate_answer(request: EvaluationRequest):  
    if not request.question or not request.correct_answer:
        raise HTTPException(status_code=400, detail="Pergunta e gabarito são obrigatórios.")

    prompt = f"""
    Você é um avaliador de questões discursivas. 
    Abaixo está uma pergunta, uma resposta correta (gabarito) e a resposta de um aluno.

    Sua tarefa é:
    1. Comparar a resposta do aluno com o gabarito.
    2. Atribuir uma nota de 0 a 1:
       - 1 se estiver completamente correta,
       - Entre 0.1 e 0.9 se estiver parcialmente correta,
       - 0 se estiver incorreta ou vazia.
    3. Justificar brevemente a nota com base na comparação.

    Formato da resposta (em JSON):
    {{
      "score": <número entre 0 e 1>,
      "justification": "<explicação curta>"
    }}

    Pergunta: {request.question}
    Gabarito: {request.correct_answer}
    Resposta do aluno: {request.user_answer}
    """

    try:
# Configura a chave da API OpenAI a partir da variável de ambiente
        if OPENAI_API_KEY:
            completion = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0,
                max_tokens=300,
            )
            content = completion.choices[0].message.content.strip()
# Configura a chave da API Gemini a partir da variável de ambiente
        elif GEMINI_API_KEY:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            content = response.text.strip()
        else:
            raise HTTPException(status_code=500, detail="Nenhuma IA configurada corretamente.")

        # Tenta extrair JSON mesmo de texto misturado
        try:
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            json_str = content[json_start:json_end]
            result = json.loads(json_str)
        except Exception as e:
            raise ValueError(f"Erro ao interpretar resposta como JSON: {e}")

        score = float(result["score"])
        justification = result["justification"]
        return {
            "score": round(max(0.0, min(score, 1.0)), 2),
            "justification": justification
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao avaliar resposta: {str(e)}")
