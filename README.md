# message-dispatcher-api
REST API for sending and retrieving messages

## Assumptions
- The following REST API is intended for internal use only

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

#### Stopping the containers
```bash
make down
```