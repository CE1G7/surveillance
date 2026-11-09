"""Pydantic request/response schemas."""
from datetime import datetime
from enum import Enum
from typing import Generic, TypeVar
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

T = TypeVar("T")


class Role(str, Enum):
    operator = "operator"
    admin = "admin"


class CameraKind(str, Enum):
    fixed = "fixed"
    drone = "drone"


class Page(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    limit: int


# ---------------------------------------------------------------- auth
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


# ---------------------------------------------------------------- users
class UserOut(BaseModel):
    id: int
    email: str
    name: str
    role: Role
    area_ids: list[int]
    created_at: datetime


class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str = Field(min_length=8)
    role: Role = Role.operator
    area_ids: list[int] = []


class UserUpdate(BaseModel):
    email: EmailStr
    name: str
    role: Role
    area_ids: list[int]
    password: str | None = Field(default=None, min_length=8)


class PasswordChange(BaseModel):
    current_password: str
    new_password: str = Field(min_length=8)


# ---------------------------------------------------------------- areas
class AreaIn(BaseModel):
    name: str
    description: str | None = None


class AreaOut(BaseModel):
    id: int
    name: str
    description: str | None
    camera_ids: list[int]


class AreaCameraStatus(BaseModel):
    camera_id: int
    name: str
    streaming: bool | None  # null when the edge device is offline


class AreaStatus(BaseModel):
    area_id: int
    edge_online: bool
    last_heartbeat: datetime | None
    cameras: list[AreaCameraStatus]


class AuditLogOut(BaseModel):
    id: int
    timestamp: datetime
    user_id: int | None
    action: str
    area_id: int | None
    detail: str | None


# ---------------------------------------------------------------- cameras
class Zone(BaseModel):
    """Restricted-area polygon, coordinates normalised to 0..1."""

    id: str | None = None
    name: str
    polygon: list[tuple[float, float]]


class CameraIn(BaseModel):
    name: str
    kind: CameraKind = CameraKind.fixed
    area_id: int
    rtsp_url: str
    enabled: bool = True
    zones: list[Zone] = []


class CameraOut(BaseModel):
    id: int
    name: str
    kind: CameraKind
    area_id: int
    enabled: bool
    stream_path: str
    zones: list[Zone]
    rtsp_url: str | None  # would only be returned to admins
    created_at: datetime


# ---------------------------------------------------------------- events
class BBox(BaseModel):
    x: float
    y: float
    w: float
    h: float


class EventOut(BaseModel):
    id: UUID
    seq: int
    camera_id: int
    area_id: int
    detected_at: datetime
    received_at: datetime
    confidence: float
    bbox: BBox | None
    zone_id: str | None
    config_version: int
    starred: bool
    has_clip: bool
    snapshot_url: str | None
    clip_url: str | None


# ---------------------------------------------------------------- media
class StreamEndpoint(BaseModel):
    whep_url: str
    hls_url: str
    token: str
    expires_at: datetime
    ready: bool = True


class StreamAccess(BaseModel):
    stream_id: int
    camera_name: str
    kind: CameraKind
    local: StreamEndpoint  # direct to the edge media server (same LAN)
    remote: StreamEndpoint  # via the cloud media server (public network)


# ---------------------------------------------------------------- edge
class EdgeEventCreate(BaseModel):
    camera_id: int
    detected_at: datetime
    confidence: float = Field(ge=0, le=1)
    bbox: BBox | None = None
    zone_id: str | None = None
    config_version: int
    snapshot_base64: str | None = None


class EdgeEventAck(BaseModel):
    id: UUID
    created: bool
    has_snapshot: bool
    has_clip: bool
    clip_upload_url: str


class ClipAck(BaseModel):
    id: UUID
    size_bytes: int


class DetectionSettings(BaseModel):
    confidence_threshold: float = 0.5
    cooldown_seconds: int = 20
    min_frames: int = 3


class EdgeCameraConfig(BaseModel):
    id: int
    name: str
    kind: CameraKind
    area_id: int
    enabled: bool
    rtsp_url: str
    stream_path: str
    zones: list[Zone]


class EdgeConfig(BaseModel):
    version: int
    cameras: list[EdgeCameraConfig]
    detection: DetectionSettings
    retention_days: int


class HeartbeatCamera(BaseModel):
    camera_id: int
    streaming: bool


class HeartbeatIn(BaseModel):
    config_version: int | None = None
    uptime_seconds: int | None = None
    cameras: list[HeartbeatCamera] = []


class HeartbeatOut(BaseModel):
    server_time: datetime
    latest_config_version: int
    config_changed: bool
