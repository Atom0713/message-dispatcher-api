import time
from datetime import UTC, datetime, timedelta

from moto import mock_aws
from service.config import settings
from service.schemas import Messages, MessagesQuery, Ordering
from service.services import RecipientMessagesService


@mock_aws
def test_create_action(setup_dynamodb):
    # Arrange
    dynamodb_client = setup_dynamodb
    # Act
    recipient_id: str = "dummy_recipient_id"
    RecipientMessagesService().create(recipient_id, content="Dummy content")

    # Assert
    response = dynamodb_client.query(
        TableName=settings.table_name,
        ExpressionAttributeValues={
            ":v1": {
                "S": f"Recipient_{recipient_id}",
            },
        },
        KeyConditionExpression="recipient_id = :v1",
    )
    items = response.get("Items")
    assert items
    assert items[0]


@mock_aws
def test_get_new_action(setup_dynamodb):
    # Arrange
    dynamodb_client = setup_dynamodb
    recipient_id: str = "dummy_recipient_id"
    RecipientMessagesService().create(recipient_id, content="Dummy content")
    RecipientMessagesService().create(recipient_id, content="Dummy content 2")
    # Act
    new_items: list[dict] = RecipientMessagesService().get_new(recipient_id)

    # Assert
    assert len(new_items) == 2
    for item in new_items:
        response = dynamodb_client.query(
            TableName=settings.table_name,
            IndexName="new_messages_index",
            KeyConditionExpression="recipient_id = :rid AND fetched = :fetched",
            ExpressionAttributeValues={":rid": {"S": item["recipient_id"]}, ":fetched": {"N": "1"}},
        )
        items = response.get("Items")
        assert items
        assert items[0]


@mock_aws
def test_get_all_with_date_filter_asc(setup_dynamodb):
    # Arrange
    recipient_id: str = "dummy_recipient_id"
    RecipientMessagesService().create(recipient_id, content="Dummy content")
    time.sleep(1)
    RecipientMessagesService().create(recipient_id, content="Dummy content 2")
    # Act
    query: MessagesQuery = MessagesQuery(
        start_date=datetime.now(UTC) - timedelta(minutes=5), end_date=datetime.now(UTC), order=Ordering.ASC.value
    )
    all_items: list[dict] = RecipientMessagesService().get_all(recipient_id, query)

    # Assert
    assert len(all_items) == 2
    # Act
    new_items: list[dict] = RecipientMessagesService().get_new(recipient_id)
    assert len(new_items) == 2

    all_items: list[dict] = RecipientMessagesService().get_all(recipient_id, query)

    # Assert
    assert len(all_items) == 2
    assert all_items[0]["created_at"] < all_items[1]["created_at"]


@mock_aws
def test_get_all_with_date_filter_desc(setup_dynamodb):
    # Arrange
    recipient_id: str = "dummy_recipient_id"
    RecipientMessagesService().create(recipient_id, content="Dummy content")
    time.sleep(1)
    RecipientMessagesService().create(recipient_id, content="Dummy content 2")
    # Act
    query: MessagesQuery = MessagesQuery(
        start_date=datetime.now(UTC) - timedelta(minutes=5), end_date=datetime.now(UTC), order=Ordering.DESC.value
    )
    all_items: list[dict] = RecipientMessagesService().get_all(recipient_id, query)

    # Assert
    assert len(all_items) == 2
    # Act
    new_items: list[dict] = RecipientMessagesService().get_new(recipient_id)
    assert len(new_items) == 2

    all_items: list[dict] = RecipientMessagesService().get_all(recipient_id, query)

    # Assert
    assert len(all_items) == 2
    assert all_items[0]["created_at"] > all_items[1]["created_at"]


@mock_aws
def test_delete_message(setup_dynamodb):
    # Arrange
    recipient_id: str = "dummy_recipient_id"
    RecipientMessagesService().create(recipient_id, content="Dummy content")
    # Act
    query: MessagesQuery = MessagesQuery(
        start_date=datetime.now(UTC) - timedelta(minutes=5), end_date=datetime.now(UTC), order=Ordering.DESC.value
    )
    all_items: list[dict] = RecipientMessagesService().get_all(recipient_id, query)
    assert len(all_items) == 1
    RecipientMessagesService().delete(recipient_id, all_items[0]["message_id"])
    all_items: list[dict] = RecipientMessagesService().get_all(recipient_id, query)

    # Assert
    assert len(all_items) == 0


@mock_aws
def test_bulk_delete_message(setup_dynamodb):
    # Arrange
    recipient_id: str = "dummy_recipient_id"
    RecipientMessagesService().create(recipient_id, content="Dummy content")
    RecipientMessagesService().create(recipient_id, content="Dummy content")
    # Act
    query: MessagesQuery = MessagesQuery(
        start_date=datetime.now(UTC) - timedelta(minutes=5), end_date=datetime.now(UTC), order=Ordering.DESC.value
    )
    all_items: list[dict] = RecipientMessagesService().get_all(recipient_id, query)
    assert len(all_items) == 2
    messages_to_delete: list[str] = [item["message_id"] for item in all_items]
    RecipientMessagesService().bulk_delete(recipient_id, Messages(messages=messages_to_delete))
    all_items: list[dict] = RecipientMessagesService().get_all(recipient_id, query)

    # Assert
    assert len(all_items) == 0
