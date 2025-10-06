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

## Gerenciando com PM2 (Produção)

Para rodar a aplicação em um ambiente de produção de forma robusta, é recomendado usar um gerenciador de processos como o [PM2](https://pm2.keymetrics.io/). Ele garante que a aplicação reinicie automaticamente em caso de falhas e facilita o gerenciamento de logs.

### 1. Instalação do PM2

Se você não tiver o PM2 instalado, instale-o globalmente via npm:
```bash
npm install -g pm2
```

### 2. Arquivo de Configuração

O projeto inclui um arquivo de configuração para o PM2, o `ecosystem.config.js`:

```javascript
module.exports = {
  apps: [
    {
      name: 'taveirabot-telegram',
      script: 'main.py',
      // Aponta para o interpretador Python dentro do seu ambiente virtual
      interpreter: '.venv/bin/python',
      // Garante que o bot inicie no diretório correto para encontrar o .env
      cwd: '/home/taveira/repositories/taveirabot-telegram',
      // Reinicia o app automaticamente em caso de falha
      autorestart: true,
      // Não monitora mudanças nos arquivos em produção
      watch: false,
      // Limita as reinicializações em caso de falhas constantes
      max_restarts: 5,
      min_uptime: '1M',
      // Reinicia o app se ele usar mais de 150MB de RAM
      max_memory_restart: "150M",
      // Arquivos de log
      log_date_format: 'YYYY-MM-DD HH:mm:ss',
      error_file: 'logs/error.log',
      out_file: 'logs/out.log',
      merge_logs: true,
    },
  ],
};
```
*Nota: O `cwd` (diretório de trabalho) está configurado com um caminho absoluto. Ajuste-o se você clonar o projeto em um local diferente.*

### 3. Inicialização

1.  **Crie o diretório de logs:**
    ```bash
    mkdir -p logs
    ```

2.  **Inicie la aplicación con PM2:**
    ```bash
    pm2 start ecosystem.config.js
    ```

### 4. Comandos Úteis do PM2

- **Listar processos:**
  ```bash
  pm2 list
  ```
- **Ver logs em tempo real:**
  ```bash
  pm2 logs taveirabot-telegram
  ```
- **Reiniciar a aplicação:**
  ```bash
  pm2 restart taveirabot-telegram
  ```
- **Parar a aplicação:**
  ```bash
  pm2 stop taveirabot-telegram
  ```
- **Remover a aplicação da lista do PM2:**
  ```bash
  pm2 delete taveirabot-telegram
  ```

### 5. Inicialização Automática no Boot do Servidor

Para que o PM2 inicie seus processos automaticamente após um reboot:

1.  **Gere o script de inicialização:**
    ```bash
    pm2 startup
    ```
    (Copie e execute o comando que será exibido na tela).

2.  **Salve a lista de processos atual:**
    ```bash
    pm2 save
    ```