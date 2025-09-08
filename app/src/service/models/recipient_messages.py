from datetime import UTC, datetime

from service.config import settings
from service.db import dynamodb
from service.schemas import RecipientMessage
from service.utility import DATETIME_FORMAT


class RecipinetMessagesModel:
    TABLE_NAME: str = settings.table_name
    PK_PREFIX: str = "Recipient_"
    _required_attributes_: list[str] = ["recipient_id", "message_id", "content", "fetched", "created_at"]

    def save(self, recipient_messages: RecipientMessage) -> None:
        self.before_save(recipient_messages)
        self._save()

    def before_save(self, recipient_messages: RecipientMessage) -> None:
        self.created_at = datetime.now(UTC).strftime(DATETIME_FORMAT)
        self.fetched = False
        self.recipient_id = f"{self.PK_PREFIX}{recipient_messages.recipient_id}"
        self.content = recipient_messages.content
        self.message_id = recipient_messages.message_id

    def _save(self) -> None:
        _ = dynamodb.put_item(
            TableName=self.TABLE_NAME,
            Item={
                "recipient_id": {"S": self.recipient_id},
                "message_id": {"S": self.message_id},
                "content": {"S": self.content},
                "fetched": {"BOOL": self.fetched},
                "created_at": {"S": self.created_at},
            },
        )

    def get_new() -> None:
        pass

    def get_all_by_date() -> None:
        pass

    def delete() -> None:
        pass

    def bulk_delete() -> None:
        pass
