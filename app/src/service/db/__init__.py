import boto3
from service.config import settings

dynamodb = boto3.client(
    "dynamodb",
    endpoint_url=settings.dynamodb_endpoint,
    region_name=settings.aws_region,
    aws_access_key_id=settings.aws_access_key_id,
    aws_secret_access_key=settings.aws_secret_access_key,
)


async def create_table() -> None:
    # Create the DynamoDB table.
    table = dynamodb.create_table(
        TableName="recipient_messages",
        KeySchema=[
            {"AttributeName": "recipient_id", "KeyType": "HASH"},
            {"AttributeName": "message_id", "KeyType": "RANGE"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "username", "AttributeType": "S"},
            {"AttributeName": "last_name", "AttributeType": "S"},
        ],
    )

    # Wait until the table exists.
    table.wait_until_exists()
