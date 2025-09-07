from datetime import date, datetime

from pydantic import BaseModel


class MessageContent(BaseModel):
    content: str


class Message(BaseModel):
    message_id: str
    content: str


class Messages(BaseModel):
    messages: list[Message]


class MessagesQuery(BaseModel):
    start_date: datetime | date
    end_date: datetime | date
