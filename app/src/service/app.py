from fastapi import APIRouter, FastAPI

app = FastAPI()

api_v1_router = APIRouter(prefix="/api/v1")

@api_v1_router.get("/")
def read_root():
    return {"status": "ok"}

app.include_router(api_v1_router)
