# main.py

import asyncio
import logging
import os
from typing import Dict

from dotenv import load_dotenv

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field
from telegram import Update
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    ExtBot,
)

# Configuração do logging para exibir informações úteis no console
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# --- Modelos de Dados da API (Pydantic) ---


class MessagePayload(BaseModel):
    """
    Modelo Pydantic para validar o corpo da requisição POST.
    Garante que 'chat_id' e 'text' sejam fornecidos.
    """

    chat_id: int = Field(
        ...,
        description="O ID do chat do Telegram para onde a mensagem será enviada.",
        examples=[123456789],
    )
    text: str = Field(
        ...,
        description="O conteúdo da mensagem a ser enviada.",
        examples=["Olá do FastAPI!"],
    )


# --- Lógica de Segurança da API ---

API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)


async def verify_api_key(api_key: str = Depends(API_KEY_HEADER)):
    """
    Dependência que valida a chave de API presente no cabeçalho da requisição.
    """
    correct_api_key = os.getenv("API_KEY")
    if not correct_api_key or api_key != correct_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Chave de API inválida ou não fornecida",
        )
    return api_key




# --- Lógica dos Handlers do Bot do Telegram ---


async def start_command_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    Handler para o comando /start. Envia uma mensagem de boas-vindas.
    """
    if update.effective_chat:
        await update.effective_chat.send_message(
            "Olá! Eu sou um bot de demonstração. "
            "Use /id para ver o seu chat_id ou envie uma requisição POST "
            "para /send_message para me fazer enviar uma mensagem."
        )
    else:
        logger.warning("O comando /start foi recebido, mas o chat não foi encontrado.")


async def id_command_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    Handler para o comando /id. Responde com o chat_id da conversa.
    """
    if update.effective_chat:
        chat_id = update.effective_chat.id
        await update.effective_chat.send_message(f"O ID deste chat é: `{chat_id}`")
    else:
        logger.warning("O comando /id foi recebido, mas o chat não foi encontrado.")


# --- Configuração e Lógica da API Web (FastAPI) ---


def setup_fastapi_app(bot_app: Application) -> FastAPI:
    """
    Cria e configura a aplicação FastAPI, incluindo a rota para enviar mensagens.
    """
    fastapi_app = FastAPI()

    @fastapi_app.post("/send_message")
    async def send_message(
        payload: MessagePayload, _: str = Depends(verify_api_key)
    ) -> Dict[str, str]:
        """
        Endpoint para enviar uma mensagem para um chat_id específico.
        Valida o corpo da requisição com o modelo Pydantic MessagePayload.
        """
        bot: ExtBot = bot_app.bot
        await bot.send_message(chat_id=payload.chat_id, text=payload.text)
        return {"status": "mensagem enviada com sucesso"}

    return fastapi_app


# --- Lógica Principal de Orquestração ---


async def main() -> None:
    """
    Função principal que inicializa e executa o bot do Telegram e o servidor FastAPI.
    """
    # 1. Carregar variáveis de ambiente do arquivo .env
    load_dotenv()

    # 2. Obter o token do bot da variável de ambiente
    telegram_token = os.getenv("TELEGRAM_TOKEN")
    if not telegram_token:
        raise ValueError(
            "A variável de ambiente TELEGRAM_TOKEN não foi configurada."
        )

    # 3. Obter a chave de API da variável de ambiente
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("A variável de ambiente API_KEY não foi configurada.")

    # 4. Configurar a aplicação do bot do Telegram
    bot_app = (
        ApplicationBuilder()
        .token(telegram_token)
        .read_timeout(30)
        .write_timeout(30)
        .build()
    )

    # 3. Adicionar os handlers de comando
    bot_app.add_handler(CommandHandler("start", start_command_handler))
    bot_app.add_handler(CommandHandler("id", id_command_handler))

    # 4. Configurar a aplicação FastAPI
    fastapi_app = setup_fastapi_app(bot_app)

    # 5. Configurar o servidor Uvicorn
    uvicorn_config = uvicorn.Config(
        app=fastapi_app, host="0.0.0.0", port=8000, log_level="info"
    )
    uvicorn_server = uvicorn.Server(uvicorn_config)

    # 6. Executar o bot e o servidor web concorrentemente
    async with bot_app:
        logger.info("Iniciando o bot do Telegram...")
        await bot_app.initialize()
        await bot_app.start()
        await bot_app.updater.start_polling()

        logger.info("Iniciando o servidor FastAPI na porta 8000...")
        await uvicorn_server.serve()

        logger.info("Desligando o bot...")
        await bot_app.updater.stop()
        await bot_app.stop()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Aplicação encerrada pelo usuário.")
