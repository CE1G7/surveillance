from uuid import UUID

from fastapi import APIRouter
from fastapi.responses import FileResponse

from src.mock_assets.data import ASSETS, CAMERAS, t
from src.schemas import CameraKind, StreamAccess, StreamEndpoint

router = APIRouter(prefix="/media", tags=["media"])


def _endpoint(base_url: str, path: str) -> StreamEndpoint:
    return StreamEndpoint(
        whep_url=f"{base_url}/{path}/whep",
        hls_url=f"{base_url}/{path}/index.m3u8",
        token="mock-stream-token",
        expires_at=t("2026-11-09T22:00:00+00:00"),
    )


@router.get("/streams/{stream_id}", response_model=StreamAccess)
def get_stream(stream_id: int):
    camera = next((c for c in CAMERAS if c.id == stream_id), CAMERAS[0])
    return StreamAccess(
        stream_id=stream_id,
        camera_name=camera.name,
        kind=camera.kind if camera.id == stream_id else CameraKind.fixed,
        local=_endpoint("https://edge.site.example", camera.stream_path),
        remote=_endpoint("https://media.example.com", camera.stream_path),
    )


# FileResponse supports HTTP Range requests, so the sample clip can be seeked in a <video> tag.
@router.get("/clips/{clip_id}", response_class=FileResponse)
def get_clip(clip_id: UUID):
    return FileResponse(ASSETS / "sample_clip.mp4", media_type="video/mp4")


@router.get("/snapshots/{snapshot_id}", response_class=FileResponse)
def get_snapshot(snapshot_id: UUID):
    return FileResponse(ASSETS / "sample_snapshot.jpg", media_type="image/jpeg")
