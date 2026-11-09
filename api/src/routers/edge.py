from uuid import UUID

from fastapi import APIRouter, Request, Response

from src.mock_assets.data import CAMERAS, t
from src.schemas import (
    ClipAck,
    DetectionSettings,
    EdgeCameraConfig,
    EdgeConfig,
    EdgeEventAck,
    EdgeEventCreate,
    HeartbeatIn,
    HeartbeatOut,
)

router = APIRouter(prefix="/edge", tags=["edge"])


@router.get("/config", response_model=EdgeConfig)
def get_config(response: Response):
    response.headers["ETag"] = '"1"'
    return EdgeConfig(
        version=1,
        cameras=[EdgeCameraConfig(**c.model_dump(exclude={"created_at"})) for c in CAMERAS],
        detection=DetectionSettings(),
        retention_days=7,
    )


@router.post("/heartbeat", response_model=HeartbeatOut)
def heartbeat(body: HeartbeatIn):
    return HeartbeatOut(server_time=t("2026-11-09T22:00:00+00:00"), latest_config_version=1, config_changed=False)


@router.post("/events/{event_id}", response_model=EdgeEventAck, status_code=201)
def create_event(event_id: UUID, body: EdgeEventCreate):
    """Real behaviour: 201 on first receipt, 200 with created=false on a retry. The mock always answers 201."""
    return EdgeEventAck(
        id=event_id,
        created=True,
        has_snapshot=body.snapshot_base64 is not None,
        has_clip=False,
        clip_upload_url=f"/api/v1/edge/events/{event_id}/clip",
    )


@router.put(
    "/events/{event_id}/clip",
    response_model=ClipAck,
    openapi_extra={"requestBody": {"required": True, "content": {"video/mp4": {"schema": {"type": "string", "format": "binary"}}}}},
)
async def upload_clip(event_id: UUID, request: Request):
    """Raw video bytes in the body (Content-Type: video/mp4)."""
    data = await request.body()
    return ClipAck(id=event_id, size_bytes=len(data))
