from fastapi import APIRouter, Depends, FastAPI

from service.schemas import MessageContent, Messages, MessagesQuery, query_params

app = FastAPI()

api_v1_router = APIRouter(prefix="/api/v1")


@api_v1_router.get("/")
def read_root():
    return {"status": "ok"}


@api_v1_router.post("/recipients/{recipient_id}/messages")
def submit_message(recipient_id: str, message_content: MessageContent) -> dict:
    return {"delivery": "pending"}


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
