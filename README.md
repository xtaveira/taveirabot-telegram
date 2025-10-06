# TaveiraBot Telegram

Este projeto é um bot híbrido para o Telegram, construído em Python, que combina um bot interativo com uma API web para envio de mensagens.

## Funcionalidades

O projeto é dividido em dois componentes principais que rodam de forma concorrente:

### 1. Bot do Telegram

- **Interação Direta:** O bot responde a comandos enviados pelos usuários no Telegram.
- **Comandos Disponíveis:**
  - `/start`: Envia uma mensagem de boas-vindas e instruções básicas.
  - `/id`: Responde com o `chat_id` da conversa atual. Este ID é útil para enviar mensagens através da API.

### 2. API Web (FastAPI)

- **Ponte para Notificações:** Expõe um endpoint web seguro para permitir que sistemas externos enviem mensagens através do bot.
- **Endpoint:**
  - `POST /send_message`: Envia uma mensagem para um `chat_id` específico.
- **Segurança:** O endpoint é protegido por uma chave de API. Requisições devem incluir um cabeçalho `X-API-Key` para autenticação.

## Tecnologias Utilizadas

- **Python 3.12+**
- **python-telegram-bot:** Para a lógica do bot do Telegram.
- **FastAPI:** Para a criação da API web.
- **Uvicorn:** Como servidor ASGI para a aplicação FastAPI.
- **python-dotenv:** Para gerenciar as variáveis de ambiente.

## Como Usar

### 1. Configuração

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/seu-usuario/taveirabot-telegram.git
    cd taveirabot-telegram
    ```

2.  **Crie o arquivo de ambiente:**
    Copie o arquivo `.env.example` para um novo arquivo chamado `.env`.
    ```bash
    cp .env.example .env
    ```

3.  **Preencha as variáveis de ambiente** no arquivo `.env`:
    - `TELEGRAM_TOKEN`: O token de acesso do seu bot, fornecido pelo [BotFather](https://t.me/BotFather).
    - `API_KEY`: Uma chave secreta de sua escolha para proteger o endpoint da API.

### 2. Instalação e Execução

1.  **Crie e ative um ambiente virtual** (recomendado):
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

2.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Execute a aplicação:**
    ```bash
    python main.py
    ```
    O bot do Telegram começará a receber comandos e a API estará disponível em `http://0.0.0.0:8000`.

## Uso da API

Para enviar uma mensagem através da API, faça uma requisição `POST` para o endpoint `/send_message`.

**Exemplo com `curl`:**

```bash
curl -X POST "http://127.0.0.1:8000/send_message" \
-H "Content-Type: application/json" \
-H "X-API-Key: SUA_CHAVE_DE_API_SECRETA" \
-d '{
  "chat_id": 123456789,
  "text": "Olá do FastAPI!"
}'
```

Substitua `SUA_CHAVE_DE_API_SECRETA` pela chave que você definiu no arquivo `.env` e `123456789` pelo `chat_id` de destino.