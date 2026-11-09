from fastapi import APIRouter

from src.mock_assets.data import USERS, t
from src.schemas import PasswordChange, UserCreate, UserOut, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


# /me routes come before /{user_id} so "me" is not parsed as an id.
@router.get("/me", response_model=UserOut)
def read_me():
    return USERS[0]


@router.patch("/me/password", status_code=204)
def change_my_password(body: PasswordChange):
    return None


@router.get("", response_model=list[UserOut])
def list_users(area_id: int | None = None, role: str | None = None):
    return USERS


@router.post("", response_model=UserOut, status_code=201)
def create_user(body: UserCreate):
    return UserOut(id=99, email=body.email, name=body.name, role=body.role, area_ids=body.area_ids,
                   created_at=t("2026-11-09T12:00:00+00:00"))


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int):
    return USERS[0].model_copy(update={"id": user_id})


@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: int, body: UserUpdate):
    return UserOut(id=user_id, email=body.email, name=body.name, role=body.role, area_ids=body.area_ids,
                   created_at=t("2026-11-01T08:00:00+00:00"))


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int):
    return None
