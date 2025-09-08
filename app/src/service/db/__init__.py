import boto3
import structlog
from botocore.exceptions import ClientError

from service.config import settings

logger = structlog.get_logger()

dynamodb = boto3.client(
    "dynamodb",
    endpoint_url=settings.dynamodb_endpoint if settings.dynamodb_endpoint else None,
    region_name=settings.aws_region,
    aws_access_key_id=settings.aws_access_key_id,
    aws_secret_access_key=settings.aws_secret_access_key,
)


def create_table(dynamodb_client) -> None:
    try:
        dynamodb_client.create_table(
            TableName=settings.table_name,
            KeySchema=[
                {"AttributeName": "recipient_id", "KeyType": "HASH"},
                {"AttributeName": "message_id", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "recipient_id", "AttributeType": "S"},
                {"AttributeName": "message_id", "AttributeType": "S"},
                {"AttributeName": "fetched", "AttributeType": "N"},
            ],
            BillingMode="PAY_PER_REQUEST",
            GlobalSecondaryIndexes=[
                {
                    "IndexName": "new_messages",
                    "KeySchema": [
                        {"AttributeName": "recipient_id", "KeyType": "HASH"},
                        {"AttributeName": "fetched", "KeyType": "RANGE"},
                    ],
                    "Projection": {"ProjectionType": "ALL"},
                }
            ],
        )

        dynamodb_client.get_waiter("table_exists").wait(TableName=settings.table_name)
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceInUseException":
            pass
        else:
            logger.exception(e)
            raise
