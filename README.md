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
- Docker 
- Git

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

## 🐳🐳 Instruções para Rodar o Projeto com Docker Compose

Estas instruções são voltadas para facilitar a avaliação do sistema completo (frontend + backend), utilizando Docker Compose.

---

### 📁 Estrutura esperada da pasta

Antes de rodar a aplicação, crie uma pasta e coloque dentro dela os seguintes elementos:

```
/sua-pasta-projeto
├── .env
├── docker-compose.yml
├── backend/           # Clonado do GitHub
│   └── ...
└── frontend/          # Clonado do GitHub
    └── ...
```

---

### 📥 Passo a Passo para Executar o Projeto

#### 1. Clone os repositórios

Dentro da pasta criada:

```bash
git clone https://github.com/seu-usuario/SistemaTestesIA-backend.git backend
git clone https://github.com/seu-usuario/SistemaTestesIA-frontend.git frontend
```

#### 2. Adicione os arquivos `.env` e `docker-compose.yml`

Coloque os arquivos `.env` e `docker-compose.yml` (fornecidos separadamente) **na raiz da pasta**, como no exemplo acima.

> ⚠️ O arquivo `.env` contém as chaves de API do OpenAI e Gemini, conforme o exemplo abaixo:
>
> ```env
> GEMINI_API_KEY=chave_fornecida_aqui
> OPENAI_API_KEY=chave_fornecida_aqui
> ```

O arquivo .env com as chaves foi fornecido através da plataforma de entrega do MVP da PUC.

O sistema utiliza a versão paga da API da OpenIA. A chave fornecida no arquivo está funcionando e possui créditos suficientes em doláres para que os professores possam avaliar o sistema.

Não é possível utilizar o sistema com a IA GEMINI pois não houve tempo hábil de testar a versão gratuita dela. Contudo o arquivo .env deve conter a sua chave para que instalação funcione

#### 3. Rode o Docker Compose

Execute o seguinte comando no terminal:

```bash
docker-compose up --build
```

Isso iniciará tanto o backend (porta 8000) quanto o frontend (porta 3000).

---

### 🌐 Acessos

- **Frontend**: [http://localhost:3000](http://localhost:3000)
- **Backend (Swagger UI)**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

### 🧪 Observações

- O frontend usa `CHOKIDAR_USEPOLLING=true` para suportar hot reload no WSL (Windows Subsystem for Linux).
- Precisei testar a execução via Docker através da WSL Ubuntu em meu Windows, pois o instalador Windows não funcionava em minha máquina. Favor levar isso em consideração.
- Certifique-se de que as portas 3000 e 8000 estejam livres antes de iniciar a aplicação.

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
Aluno da Pós-Graduação em Desenvolvimento Fullstack
