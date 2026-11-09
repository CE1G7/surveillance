from fastapi import APIRouter

from src.mock_assets.data import AREAS, t
from src.schemas import AreaCameraStatus, AreaIn, AreaOut, AreaStatus, AuditLogOut, Page

router = APIRouter(prefix="/areas", tags=["areas"])


@router.get("", response_model=list[AreaOut])
def list_areas():
    return AREAS


@router.get("/{area_id}/status", response_model=AreaStatus)
def area_status(area_id: int):
    return AreaStatus(
        area_id=area_id,
        edge_online=True,
        last_heartbeat=t("2026-11-09T21:59:50+00:00"),
        cameras=[
            AreaCameraStatus(camera_id=1, name="North Gate", streaming=True),
            AreaCameraStatus(camera_id=2, name="North Fence", streaming=True),
        ],
    )


@router.post("", response_model=AreaOut, status_code=201)
def create_area(body: AreaIn):
    return AreaOut(id=99, name=body.name, description=body.description, camera_ids=[])


@router.put("/{area_id}", response_model=AreaOut)
def update_area(area_id: int, body: AreaIn):
    return AreaOut(id=area_id, name=body.name, description=body.description, camera_ids=[1, 2, 4])


@router.delete("/{area_id}", status_code=204)
def delete_area(area_id: int):
    return None


@router.get("/{area_id}/logs", response_model=Page[AuditLogOut])
def area_logs(area_id: int, page: int = 1, limit: int = 50):
    items = [
        AuditLogOut(id=2, timestamp=t("2026-11-09T20:40:00+00:00"), user_id=2, action="clip_viewed", area_id=area_id, detail="event 2"),
        AuditLogOut(id=1, timestamp=t("2026-11-09T20:35:00+00:00"), user_id=2, action="stream_access", area_id=area_id, detail="camera 1"),
    ]
    return Page[AuditLogOut](items=items, total=len(items), page=page, limit=limit)
