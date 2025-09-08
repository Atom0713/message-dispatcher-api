from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel


class MessageContent(BaseModel):
    content: str


class Messages(BaseModel):
    messages: list[str]


class MessagesQuery(BaseModel):
    start_date: datetime | date
    end_date: datetime | date
    order: str


@dataclass
class RecipientMessage:
    recipient_id: str
    message_id: str
    content: str


class Ordering(Enum):
    ASC = "asc"
    DESC = "desc"
