from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def root():
    return {"Go to http://127.0.0.1:8000/docs :)"}