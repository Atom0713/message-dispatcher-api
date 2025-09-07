import os

import boto3
import pytest
from fastapi.testclient import TestClient
from moto import mock_aws
from service.app import app
from service.db import create_table


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture(autouse=True)
def setup_moto() -> None:
    os.environ["DYNAMODB_ENDPOINT_URL"] = ""


@pytest.fixture(autouse=True)
def setup_dynamodb():
    # Start moto mock
    with mock_aws():
        dynamodb_client = boto3.client("dynamodb", region_name="eu-west-1")
        create_table(dynamodb_client)
        yield dynamodb_client  # run tests inside this context
