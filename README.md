# message-dispatcher-api
REST API for sending and retrieving messages

## Assumptions
- The following REST API is intended for internal use only
- This API is not responsible for managing recipient contact information (e.g. email, phone numbers).
- Recipients are identified only by UUIDs to protect privacy and decouple message management from delivery details.
- The service’s main role is to store messages and expose them through an API.
- The API only provides message management functionality (submit, fetch, delete). Actual delivery to recipients is out of scope.
- Each message belongs to exactly one recipient.

### Database Model (DynamoDB)
| Field               | Role                                                                                                                                    |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| `recipient_id` (PK) | Partition Key. UUID identifying the recipient. All messages for the same recipient are grouped together.                                |
| `message_id`        | Sort Key (unique per recipient). Used to uniquely identify a message.                                                                   |
| `content`           | String. The actual message content.                                                                                                     |
| `fetched`           | Boolean (or numeric flag, e.g. `0`/`1`). Marks whether the message has been fetched already. Indexed for quick queries of new messages. |
| `created_at`        | Timestamp. Used to order messages by creation time. Also indexed for range queries (pagination).                                        |


#### Indexes:
**Index1:** Supports efficient queries for “unfetched” messages (fetched = 0).

**Index2:** Supports queries ordered by created_at (pagination, history).

## 🚀 Getting Started

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) installed on your system

## Development
**🛠 Build the Docker image**

```bash
make build
```
**Run the app**
```bash
make run
```
**Check if the app is running**

```bash
curl http://localhost:8000/api/v1/
```

### Running Tests & Code Quality Checks

#### Run Tests
```bash
make pytest
```
Runs the test suite inside the container.
Equivalent to: pytest .
#### Linting & Formatting
```bash
make check
```
Runs ruff check and verifies formatting without modifying files.

#### Run tests + code checks together
```bash
make test
```

**Auto-fix issues (imports, linting, formatting)**
```bash
make fix
```
- Runs ruff check --fix
- Formats code with ruff format

**Format only**
```bash
make format
```
**Sort imports only**
```bash
make isort
```
Uses ruff --select I --fix to reorder imports consistently.
## DEMO

### Running the Service with Docker Compose

#### Build and start the containers
```bash
make up
```
This will:
- Start the FastAPI application (default at http://localhost:8000/api/v1/)
- Start a local DynamoDB instance (accessible on port 8001)

#### Access the API

Once running, you can test the service:
- API root: http://localhost:8000/api/v1/
- Interactive API docs (Swagger UI): http://localhost:8000/docs
- ReDoc docs: http://localhost:8000/redoc

----

#### Example Usage with curl
**Submit a message**
```bash
curl -X POST "http://localhost:8000/api/v1/recipients/dummy_recipient_id/messages" \
     -H "Content-Type: application/json" \
     -d '{"content": "dummy message"}'
```
**Fetch new messages**
```bash
curl -X GET "http://localhost:8000/api/v1/recipients/dummy_recipient_id/messages/new"
```

**Fetch all messages with date filter**

**NOTE:** Timestamps are in UTC so filter on now() - 2h
```bash
curl -X GET "http://localhost:8000/api/v1/recipients/dummy_recipient_id/messages?start_date=2025-09-08T08:00:00&end_date=2025-09-08T12:00:00&order=asc"
```

**Delete message**
```bash
curl -X DELETE "http://localhost:8000/api/v1/recipients/dummy_recipient_id/messages/dummy_message_id"
```

**Bulk delete messages**
```bash
curl -X POST "http://localhost:8000/api/v1/recipients/dummy_recipient_id/messages/delete" \
     -H "Content-Type: application/json" \
     -d '{"messages": ["dummy_message_id"]}'
```
#### Stopping the containers
```bash
make down
```