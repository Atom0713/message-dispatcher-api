from dataclasses import dataclass
from datetime import date, datetime

from pydantic import BaseModel


class MessageContent(BaseModel):
    content: str


class Messages(BaseModel):
    messages: list[str]


class MessagesQuery(BaseModel):
    start_date: datetime | date
    end_date: datetime | date


@dataclass
class RecipientMessage:
    recipient_id: str
    message_id: str
    content: str
