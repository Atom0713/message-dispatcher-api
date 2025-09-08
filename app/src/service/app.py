from contextlib import asynccontextmanager

import structlog
from fastapi import APIRouter, Depends, FastAPI, Response
from fastapi.responses import JSONResponse

from service.db import create_table, dynamodb
from service.schemas import MessageContent, Messages, MessagesQuery, query_params
from service.services import RecipientMessagesService

api_v1_router = APIRouter(prefix="/api/v1")

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_table(dynamodb)
    yield


app = FastAPI(lifespan=lifespan)


@api_v1_router.get("/")
def read_root():
    return {"status": "ok"}


@api_v1_router.post("/recipients/{recipient_id}/messages")
def submit_message(recipient_id: str, message_content: MessageContent) -> dict:
    try:
        RecipientMessagesService().create(recipient_id, message_content.content)
    except Exception as e:
        logger.exception(e)
        return JSONResponse(content={"message": "INTERNAL_SERVER_ERROR"}, status_code=500)
    return Response(status_code=200)


@api_v1_router.delete("/recipients/{recipient_id}/messages/{message_id}")
def delete_message(recipient_id: str, message_id: str) -> dict:
    try:
        RecipientMessagesService().delete(recipient_id, message_id)
        logger.info("Deleted message for recipient.", message_id=message_id, recipient_id=recipient_id)
        return Response(status_code=200)
    except Exception as e:
        logger.exception(e)
        return JSONResponse(content={"message": "INTERNAL_SERVER_ERROR"}, status_code=500)


@api_v1_router.post("/recipients/{recipient_id}/messages/delete")
def bulk_delete_messages(recipient_id: str, messages: Messages) -> dict:
    try:
        RecipientMessagesService().bulk_delete(recipient_id, messages)
        return Response(status_code=200)
    except Exception as e:
        logger.exception(e)
        return JSONResponse(content={"message": "INTERNAL_SERVER_ERROR"}, status_code=500)


@api_v1_router.get("/recipients/{recipient_id}/messages/new")
def fetch_new_messages(recipient_id: str) -> dict:
    try:
        return {"messages": RecipientMessagesService().get_new(recipient_id)}
    except Exception as e:
        logger.exception(e)
        return JSONResponse(content={"message": "INTERNAL_SERVER_ERROR"}, status_code=500)


@api_v1_router.get("/recipients/{recipient_id}/messages")
def fetch_messages_by_filter(recipient_id: str, query: MessagesQuery = Depends(query_params)) -> dict:
    try:
        return {"messages": RecipientMessagesService().get_all(recipient_id, query)}
    except Exception as e:
        logger.exception(e)
        return JSONResponse(content={"message": "INTERNAL_SERVER_ERROR"}, status_code=500)


app.include_router(api_v1_router)
