from moto import mock_aws
from service.config import settings
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
