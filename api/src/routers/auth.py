from fastapi import APIRouter

from src.schemas import LoginRequest, RefreshRequest, TokenPair

router = APIRouter(prefix="/auth", tags=["auth"])

TOKENS = TokenPair(access_token="mock-access-token", refresh_token="mock-refresh-token", expires_in=900)


@router.post("/login", response_model=TokenPair)
def login(body: LoginRequest):
    return TOKENS


@router.post("/refresh", response_model=TokenPair)
def refresh(body: RefreshRequest):
    return TOKENS


@router.post("/logout", status_code=204)
def logout(body: RefreshRequest):
    return None
