from datetime import UTC, datetime

from boto3.dynamodb.types import TypeDeserializer

from service.config import settings
from service.db import dynamodb
from service.schemas import RecipientMessage
from service.utility import DATETIME_FORMAT


class RecipinetMessagesModel:
    TABLE_NAME: str = settings.table_name
    PK_PREFIX: str = "Recipient_"
    _required_attributes_: list[str] = ["recipient_id", "message_id", "content", "fetched", "created_at"]
    deserializer = TypeDeserializer()

    def save(self, recipient_messages: RecipientMessage) -> None:
        self.before_save(recipient_messages)
        self._save()

    def before_save(self, recipient_messages: RecipientMessage) -> None:
        self.created_at = datetime.now(UTC).strftime(DATETIME_FORMAT)
        self.fetched = "0"
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
                "fetched": {"N": self.fetched},
                "created_at": {"S": self.created_at},
            },
        )

    def get_new(self, recipient_id: str) -> list[dict]:
        items = self._get_new(recipient_id)
        clean_items = [self._clean_item(item) for item in items]
        for item in clean_items:
            self._mark_as_fetched(item["recipient_id"], item["message_id"])
        return clean_items

    def _get_new(self, recipient_id: str) -> list[dict]:
        response = dynamodb.query(
            TableName=settings.table_name,
            IndexName="new_messages",
            KeyConditionExpression="recipient_id = :rid AND fetched = :fetched",
            ExpressionAttributeValues={":rid": {"S": f"{self.PK_PREFIX}{recipient_id}"}, ":fetched": {"N": "0"}},
        )
        return response.get("Items", [])

    def _mark_as_fetched(self, recipient_id: str, message_id: str) -> None:
        dynamodb.update_item(
            TableName=settings.table_name,
            Key={
                "recipient_id": {"S": recipient_id},
                "message_id": {"S": message_id},
            },
            UpdateExpression="SET fetched = :f",
            ExpressionAttributeValues={":f": {"N": "1"}},
        )

    def _clean_item(self, dynamo_item: dict) -> dict:
        """Convert a DynamoDB item dict into a plain Python dict."""
        return {k: self.deserializer.deserialize(v) for k, v in dynamo_item.items()}

    def get_all_by_date() -> None:
        pass

    def delete() -> None:
        pass

    def bulk_delete() -> None:
        pass
