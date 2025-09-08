from datetime import UTC, datetime

from boto3.dynamodb.types import TypeDeserializer

from service.config import settings
from service.db import dynamodb
from service.schemas import MessagesQuery, Ordering, RecipientMessage
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
            IndexName="new_messages_index",
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

    def get_all_with_filter(self, recipient_id: str, query: MessagesQuery) -> None:
        items: list[dict] = self._get_all_with_date_filter(recipient_id, query)
        return [self._clean_item(item) for item in items]

    def _get_all_with_date_filter(self, recipient_id: str, query: MessagesQuery) -> list[dict]:
        response = dynamodb.query(
            TableName=settings.table_name,
            IndexName="message_date_filter_index",
            KeyConditionExpression="recipient_id = :rid AND created_at BETWEEN :start AND :end",
            ExpressionAttributeValues={
                ":rid": {"S": f"{self.PK_PREFIX}{recipient_id}"},
                ":start": {"S": query.start_date.strftime(DATETIME_FORMAT)},
                ":end": {"S": query.end_date.strftime(DATETIME_FORMAT)},
            },
            ScanIndexForward=True if query.order == Ordering.ASC.value else False,
        )
        return response.get("Items", [])

    def delete(self, recipient_id: str, message_id: str) -> None:
        dynamodb.delete_item(
            TableName=settings.table_name,
            Key={
                "recipient_id": {"S": f"{self.PK_PREFIX}{recipient_id}"},
                "message_id": {"S": message_id},
            },
        )

    def bulk_delete() -> None:
        pass
