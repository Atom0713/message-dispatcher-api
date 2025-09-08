import structlog
from fastapi import APIRouter, Depends, FastAPI, Response
from fastapi.responses import JSONResponse

from service.schemas import MessageContent, Messages, MessagesQuery, query_params
from service.services import RecipientMessagesService
from service.db import create_table, dynamodb
from contextlib import asynccontextmanager

app = FastAPI()

api_v1_router = APIRouter(prefix="/api/v1")

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_table(dynamodb)
    yield


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
    return {"status": "ok"}


@api_v1_router.post("/recipients/{recipient_id}/messages/delete")
def bulk_delete_messages(recipient_id: str, messages: Messages) -> dict:
    return {"status": "ok"}


@api_v1_router.get("/recipients/{recipient_id}/messages/new")
def fetch_new_messages(recipient_id: str) -> dict:
    return {"messages": [{"message_id": "dummy_message_id", "content": "dummy content"}]}


@api_v1_router.get("/recipients/{recipient_id}/messages")
def fetch_messages_by_filter(recipient_id: str, query: MessagesQuery = Depends(query_params)) -> dict:
    return {"messages": [{"message_id": "dummy_message_id", "content": "dummy content"}]}


app.include_router(api_v1_router)
