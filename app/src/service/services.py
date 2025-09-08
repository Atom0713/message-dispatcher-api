import uuid

import structlog

from service.models.recipient_messages import RecipinetMessagesModel
from service.schemas import MessagesQuery, RecipientMessage

logger = structlog.get_logger()


class RecipientMessagesService:
    def create(self, recipient_id: str, content: str) -> None:
        recipient_message: RecipientMessage = RecipientMessage(recipient_id, self._generate_message_id(), content)
        RecipinetMessagesModel().save(recipient_message)
        logger.info("Saved new message for recipient.")

    def _generate_message_id(self) -> str:
        return str(uuid.uuid4())

    def get_new(self, recipient_id: str) -> list[dict]:
        return RecipinetMessagesModel().get_new(recipient_id)

    def get_all(self, recipient_id: str, query: MessagesQuery) -> list[dict]:
        return RecipinetMessagesModel().get_all_with_filter(recipient_id, query)
