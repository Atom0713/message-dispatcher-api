from moto import mock_aws
from service.config import settings
from service.services import RecipientMessagesService


@mock_aws
def test_create_and_get_user(setup_dynamodb):
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
