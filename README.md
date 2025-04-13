# Sistema de Geração de Testes com IA

Este projeto é um sistema backend desenvolvido em Python que utiliza inteligência artificial para gerar questões de prova com base em conteúdos fornecidos. Ele foi elaborado como parte da disciplina da pós-graduação e demonstra integração entre IA, banco de dados e uma API para comunicação com um frontend.

## 📁 Estrutura do Projeto

- `main.py` — Arquivo principal com a API desenvolvida usando FastAPI.
- `requirements.txt` — Lista de dependências necessárias para rodar o projeto.
- `Dockerfile` — Configuração para containerização da aplicação.
- `tests.db` — Banco de dados SQLite com as questões geradas.
- `.gitignore` — Arquivo para ignorar arquivos desnecessários no repositório.
- `README.md` — Documentação do projeto.

---

## ⚙️ Instalação e Execução Local

### Pré-requisitos

- Python 3.11 ou superior
- Docker (opcional, mas recomendado para execução isolada)
- Git (para clonar o repositório)

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/SistemaTestesIA-backend.git
cd SistemaTestesIA-backend
```

### 2. Crie o ambiente virtual (opcional, mas recomendado)

```bash
python -m venv venv
source venv/bin/activate  # no Linux/macOS
venv\Scripts\activate     # no Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute a aplicação

```bash
uvicorn main:app --reload
```

A API estará disponível em: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🐳 Executando com Docker

Se preferir rodar com Docker:

### 1. Construa a imagem

```bash
docker build -t sistema-testes-ia .
```

### 2. Rode o container

```bash
docker run -d -p 8000:8000 sistema-testes-ia
```

A aplicação estará acessível em [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧠 Funcionalidade

- Recebe um conteúdo textual.
- Gera questões de múltipla escolha ou discursivas utilizando IA.
- Armazena as questões em banco de dados SQLite.
- Expõe endpoints RESTful para interação com a aplicação.

---

## 📄 Licença

Este projeto foi desenvolvido exclusivamente para fins educacionais e não possui fins comerciais.

---

## 👨‍🏫 Autor

Ricardo Mitrano  
Aluno da Pós-Graduação em [Nome da Instituição]
