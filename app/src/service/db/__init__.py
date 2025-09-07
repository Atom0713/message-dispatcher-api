import boto3
import structlog
from botocore.exceptions import ClientError

from service.config import settings

logger = structlog.get_logger()

dynamodb = boto3.client(
    "dynamodb",
    endpoint_url=settings.dynamodb_endpoint,
    region_name=settings.aws_region,
    aws_access_key_id=settings.aws_access_key_id,
    aws_secret_access_key=settings.aws_secret_access_key,
)


def create_table() -> None:
    try:
        dynamodb.create_table(
            TableName=settings.table_name,
            KeySchema=[
                {"AttributeName": "recipient_id", "KeyType": "HASH"},
                {"AttributeName": "message_id", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "recipient_id", "AttributeType": "S"},
                {"AttributeName": "message_id", "AttributeType": "S"},
            ],
            BillingMode="PAY_PER_REQUEST",
        )

        dynamodb.get_waiter("table_exists").wait(TableName=settings.table_name)
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceInUseException":
            pass
        else:
            logger.exception(e)
            raise


create_table()
