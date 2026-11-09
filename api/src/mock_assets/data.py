"""Static data returned by the mock endpoints."""
from datetime import datetime
from pathlib import Path
from uuid import UUID

from src.schemas import (
    AreaOut,
    BBox,
    CameraKind,
    CameraOut,
    EventOut,
    Role,
    UserOut,
    Zone,
)

ASSETS = Path(__file__).parent / "mock_assets"


def t(value: str) -> datetime:
    return datetime.fromisoformat(value)


ZONE = Zone(id="z-gate", name="Gate approach", polygon=[(0.10, 0.20), (0.80, 0.20), (0.80, 0.90), (0.10, 0.90)])

USERS = [
    UserOut(id=1, email="admin@example.com", name="Ada Admin", role=Role.admin, area_ids=[1, 2], created_at=t("2026-11-01T08:00:00+00:00")),
    UserOut(id=2, email="operator@example.com", name="Olivia Operator", role=Role.operator, area_ids=[1], created_at=t("2026-11-02T08:00:00+00:00")),
    UserOut(id=3, email="bridge.operator@example.com", name="Bo Bridge", role=Role.operator, area_ids=[2], created_at=t("2026-11-03T08:00:00+00:00")),
]

AREAS = [
    AreaOut(id=1, name="Substation North", description="Transformer yard and access road", camera_ids=[1, 2, 4]),
    AreaOut(id=2, name="Bridge East", description="East bridge pylons and walkway", camera_ids=[3]),
]

CAMERAS = [
    CameraOut(id=1, name="North Gate", kind=CameraKind.fixed, area_id=1, enabled=True, stream_path="north-gate-1", zones=[ZONE],
              rtsp_url="rtsp://viewer:secret@192.168.10.11/stream1", created_at=t("2026-11-01T09:00:00+00:00")),
    CameraOut(id=2, name="North Fence", kind=CameraKind.fixed, area_id=1, enabled=True, stream_path="north-fence-2", zones=[ZONE],
              rtsp_url="rtsp://viewer:secret@192.168.10.12/stream1", created_at=t("2026-11-01T09:05:00+00:00")),
    CameraOut(id=3, name="Bridge Pylon", kind=CameraKind.fixed, area_id=2, enabled=True, stream_path="bridge-pylon-3", zones=[ZONE],
              rtsp_url="rtsp://viewer:secret@192.168.10.21/stream1", created_at=t("2026-11-01T09:10:00+00:00")),
    CameraOut(id=4, name="Drone", kind=CameraKind.drone, area_id=1, enabled=True, stream_path="drone-4", zones=[],
              rtsp_url="rtmp://edge.local/live/drone", created_at=t("2026-11-01T09:15:00+00:00")),
]

_BBOX = BBox(x=0.40, y=0.30, w=0.10, h=0.30)


def _event(n: int, camera_id: int, area_id: int, detected: str, confidence: float, starred: bool, has_clip: bool) -> EventOut:
    event_id = UUID(f"00000000-0000-4000-8000-{n:012d}")
    return EventOut(
        id=event_id, seq=n, camera_id=camera_id, area_id=area_id,
        detected_at=t(detected), received_at=t(detected), confidence=confidence, bbox=_BBOX,
        zone_id="z-gate", config_version=1, starred=starred, has_clip=has_clip,
        snapshot_url=f"/api/v1/media/snapshots/{event_id}",
        clip_url=f"/api/v1/media/clips/{event_id}" if has_clip else None,
    )


EVENTS = [
    _event(3, 3, 2, "2026-11-09T20:33:00+00:00", 0.88, False, False),  # newest, clip still uploading
    _event(2, 2, 1, "2026-11-09T19:56:00+00:00", 0.76, True, True),
    _event(1, 1, 1, "2026-11-09T18:05:00+00:00", 0.91, False, True),
]
