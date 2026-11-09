from fastapi import APIRouter

from src.mock_assets.data import CAMERAS, t
from src.schemas import CameraIn, CameraOut

router = APIRouter(prefix="/cameras", tags=["cameras"])


def _from_body(camera_id: int, body: CameraIn) -> CameraOut:
    return CameraOut(
        id=camera_id, name=body.name, kind=body.kind, area_id=body.area_id, enabled=body.enabled,
        stream_path=f"camera-{camera_id}", zones=body.zones, rtsp_url=body.rtsp_url,
        created_at=t("2026-11-09T12:00:00+00:00"),
    )


@router.get("", response_model=list[CameraOut])
def list_cameras(area_id: int | None = None):
    return CAMERAS


@router.get("/{camera_id}", response_model=CameraOut)
def get_camera(camera_id: int):
    return CAMERAS[0].model_copy(update={"id": camera_id})


@router.post("", response_model=CameraOut, status_code=201)
def create_camera(body: CameraIn):
    return _from_body(99, body)


@router.put("/{camera_id}", response_model=CameraOut)
def update_camera(camera_id: int, body: CameraIn):
    return _from_body(camera_id, body)


@router.delete("/{camera_id}", status_code=204)
def delete_camera(camera_id: int):
    return None
