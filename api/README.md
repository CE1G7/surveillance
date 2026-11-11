# API application
## To run:

1. Make a Python virtual environment with ```python -m venv venv```

1. Enter the venv:

    * Linux and macOS: ```source venv/bin/activate```
    * Windows: ```venv\Scripts\activate```

1. Install the requirements: ```pip install -r requirements.txt```

1. Start the api with ```fastapi run main.py```

# Endpoints:
## Auth

| Method | Endpoint | Notes |
| --- | --- | --- |
| `POST` | `/api/v1/auth/login` |  |
| `POST` | `/api/v1/auth/refresh` |  |
| `POST` | `/api/v1/auth/logout` | Revokes the refresh token server-side |

## Users

| Method | Endpoint | Access |
| --- | --- | --- |
| `GET` | `/api/v1/users/me` | User |
| `PATCH` | `/api/v1/users/me/password` | User |
| `GET` | `/api/v1/users` | Admin |
| `POST` | `/api/v1/users` | Admin |
| `GET` | `/api/v1/users/{id}` | Admin |
| `PUT` | `/api/v1/users/{id}` | Admin |
| `DELETE` | `/api/v1/users/{id}` | Admin |

## Areas

> **Scope:** Specifies what cameras are in the area; each user is assigned an area.

| Method | Endpoint | Access |
| --- | --- | --- |
| `GET` | `/api/v1/areas` | User |
| `GET` | `/api/v1/areas/{id}/status` | User |
| `POST` | `/api/v1/areas` | Admin |
| `PUT` | `/api/v1/areas/{id}` | Admin |
| `DELETE` | `/api/v1/areas/{id}` | Admin |
| `GET` | `/api/v1/areas/{id}/logs` | Admin |

## Cameras

> **Authorization:** Server-side validation based on the user's assigned area.

| Method | Endpoint | Access |
| --- | --- | --- |
| `GET` | `/api/v1/cameras` | User |
| `GET` | `/api/v1/cameras/{id}` | User |
| `POST` | `/api/v1/cameras` | Admin |
| `PUT` | `/api/v1/cameras/{id}` | Admin |
| `DELETE` | `/api/v1/cameras/{id}` | Admin |

## Events

> **Authorization:** Server-side validation based on the user's assigned area.

| Method | Endpoint | Notes |
| --- | --- | --- |
| `GET` | `/api/v1/events?from&to&area_id` | Filterable by time range and area |
| `GET` | `/api/v1/events/{id}` |  |
| `PUT` | `/api/v1/events/{id}/star` | Add star status |
| `DELETE` | `/api/v1/events/{id}/star` | Remove star status |
| `GET` | `/api/v1/events/stream` | Server-Sent Events (SSE) |

## Media

> **Authorization:** Server-side validation based on the user's assigned area.

| Method | Endpoint |
| --- | --- |
| `GET` | `/api/v1/media/streams/{id}` |
| `GET` | `/api/v1/media/clips/{id}` |
| `GET` | `/api/v1/media/snapshots/{id}` |

## Edge

| Method | Endpoint |
| --- | --- |
| `GET` | `/api/v1/edge/config` |
| `POST` | `/api/v1/edge/heartbeat` |
| `POST` | `/api/v1/edge/events/{uuid}` |
| `PUT` | `/api/v1/edge/events/{uuid}/clip` |

# Schemas:

### `Role` (Enum)

`operator` | `admin`

### `CameraKind` (Enum)

`fixed` | `drone`

### `BBox`

| Field | Type | Notes |
| --- | --- | --- |
| `x` | `float` | X coordinate |
| `y` | `float` | Y coordinate |
| `w` | `float` | Width |
| `h` | `float` | Height |

### `Zone`

| Field | Type | Notes |
| --- | --- | --- |
| `id` | `string | null` | Zone ID |
| `name` | `string` | Zone name |
| `polygon` | `array[[x, y]]` | Array of 2D coordinates normalized to 0..1 |

---

## Auth

### `LoginRequest`

| Field | Type | Notes |
| --- | --- | --- |
| `email` | `string` | Format: email |
| `password` | `string` |  |

### `RefreshRequest`

| Field | Type | Notes |
| --- | --- | --- |
| `refresh_token` | `string` |  |

### `TokenPair`

| Field | Type | Notes |
| --- | --- | --- |
| `access_token` | `string` |  |
| `refresh_token` | `string` |  |
| `token_type` | `string` | Default: `"bearer"` |
| `expires_in` | `integer` | Duration in seconds |

---

## Users

### `UserOut`

| Field | Type | Notes |
| --- | --- | --- |
| `id` | `integer` |  |
| `email` | `string` |  |
| `name` | `string` |  |
| `role` | `Role` | `operator` | `admin` |
| `area_ids` | `array[integer]` | Assigned area IDs |
| `created_at` | `datetime` |  |

### `UserCreate`

| Field | Type | Notes |
| --- | --- | --- |
| `email` | `string` | Format: email |
| `name` | `string` |  |
| `password` | `string` | Minimum length: 8 |
| `role` | `Role` | Default: `"operator"` |
| `area_ids` | `array[integer]` | Default: `[]` |

### `UserUpdate`

| Field | Type | Notes |
| --- | --- | --- |
| `email` | `string` | Format: email |
| `name` | `string` |  |
| `role` | `Role` |  |
| `area_ids` | `array[integer]` |  |
| `password` | `string | null` | Optional; minimum length: 8 |

### `PasswordChange`

| Field | Type | Notes |
| --- | --- | --- |
| `current_password` | `string` |  |
| `new_password` | `string` | Minimum length: 8 |

---

## Areas

### `AreaIn`

| Field | Type | Notes |
| --- | --- | --- |
| `name` | `string` |  |
| `description` | `string / null` |  |

### `AreaOut`

| Field | Type | Notes |
| --- | --- | --- |
| `id` | `integer` |  |
| `name` | `string` |  |
| `description` | `string / null` |  |
| `camera_ids` | `array[integer]` |  |

### `AreaStatus`

| Field | Type | Notes |
| --- | --- | --- |
| `area_id` | `integer` |  |
| `edge_online` | `boolean` |  |
| `last_heartbeat` | `datetime / null` |  |
| `cameras` | `array[AreaCameraStatus]` |  |

### `AreaCameraStatus`

| Field | Type | Notes |
| --- | --- | --- |
| `camera_id` | `integer` |  |
| `name` | `string` |  |
| `streaming` | `boolean / null` |  |

### `AuditLogOut`

| Field | Type | Notes |
| --- | --- | --- |
| `id` | `integer` |  |
| `timestamp` | `datetime` |  |
| `user_id` | `integer / null` |  |
| `action` | `string` |  |
| `area_id` | `integer / null` |  |
| `detail` | `string / null` |  |

---

## Cameras

### `CameraIn`

| Field | Type | Notes |
| --- | --- | --- |
| `name` | `string` |  |
| `kind` | `CameraKind` | Default: `"fixed"` |
| `area_id` | `integer` |  |
| `rtsp_url` | `string` |  |
| `enabled` | `boolean` | Default: `true` |
| `zones` | `array[Zone]` | Default: `[]` |

### `CameraOut`

| Field | Type | Notes |
| --- | --- | --- |
| `id` | `integer` |  |
| `name` | `string` |  |
| `kind` | `CameraKind` |  |
| `area_id` | `integer` |  |
| `enabled` | `boolean` |  |
| `stream_path` | `string` |  |
| `zones` | `array[Zone]` |  |
| `rtsp_url` | `string / null` |  |
| `created_at` | `datetime` |  |

---

## Events

### `EventOut`

| Field | Type | Notes |
| --- | --- | --- |
| `id` | `uuid` |  |
| `seq` | `integer` |  |
| `camera_id` | `integer` |  |
| `area_id` | `integer` |  |
| `detected_at` | `datetime` |  |
| `received_at` | `datetime` |  |
| `confidence` | `float` | `0.0` .. `1.0` |
| `bbox` | `BBox / null` |  |
| `zone_id` | `string / null` |  |
| `config_version` | `integer` |  |
| `starred` | `boolean` |  |
| `has_clip` | `boolean` |  |
| `snapshot_url` | `string / null` |  |
| `clip_url` | `string / null` |  |

---

## Media

### `StreamAccess`

| Field | Type | Notes |
| --- | --- | --- |
| `stream_id` | `integer` |  |
| `camera_name` | `string` |  |
| `kind` | `CameraKind` |  |
| `local` | `StreamEndpoint` |  |
| `remote` | `StreamEndpoint` |  |

### `StreamEndpoint`

| Field | Type | Notes |
| --- | --- | --- |
| `whep_url` | `string` |  |
| `hls_url` | `string` |  |
| `token` | `string` |  |
| `expires_at` | `datetime` |  |
| `ready` | `boolean` | Default: `true` |

---

## Edge

### `EdgeConfig`

| Field | Type | Notes |
| --- | --- | --- |
| `version` | `integer` |  |
| `cameras` | `array[EdgeCameraConfig]` |  |
| `detection` | `DetectionSettings` |  |
| `retention_days` | `integer` |  |

### `EdgeCameraConfig`

| Field | Type | Notes |
| --- | --- | --- |
| `id` | `integer` |  |
| `name` | `string` |  |
| `kind` | `CameraKind` |  |
| `area_id` | `integer` |  |
| `enabled` | `boolean` |  |
| `rtsp_url` | `string` |  |
| `stream_path` | `string` |  |
| `zones` | `array[Zone]` |  |

### `DetectionSettings`

| Field | Type | Notes |
| --- | --- | --- |
| `confidence_threshold` | `float` | Default: `0.5` |
| `cooldown_seconds` | `integer` | Default: `20` |
| `min_frames` | `integer` | Default: `3` |

### `HeartbeatIn`

| Field | Type | Notes |
| --- | --- | --- |
| `config_version` | `integer / null` |  |
| `uptime_seconds` | `integer / null` |  |
| `cameras` | `array[HeartbeatCamera]` | Default: `[]` |

### `HeartbeatCamera`

| Field | Type | Notes |
| --- | --- | --- |
| `camera_id` | `integer` |  |
| `streaming` | `boolean` |  |

### `HeartbeatOut`

| Field | Type | Notes |
| --- | --- | --- |
| `server_time` | `datetime` |  |
| `latest_config_version` | `integer` |  |
| `config_changed` | `boolean` |  |

### `EdgeEventCreate`

| Field | Type | Notes |
| --- | --- | --- |
| `camera_id` | `integer` |  |
| `detected_at` | `datetime` |  |
| `confidence` | `float` | Min: `0.0`, Max: `1.0` |
| `bbox` | `BBox / null` |  |
| `zone_id` | `string / null` |  |
| `config_version` | `integer` |  |
| `snapshot_base64` | `string / null` |  |

### `EdgeEventAck`

| Field | Type | Notes |
| --- | --- | --- |
| `id` | `uuid` |  |
| `created` | `boolean` | `false` on retry/duplicate |
| `has_snapshot` | `boolean` |  |
| `has_clip` | `boolean` |  |
| `clip_upload_url` | `string` |  |

### `ClipAck`

| Field | Type | Notes |
| --- | --- | --- |
| `id` | `uuid` |  |
| `size_bytes` | `integer` |  |

---

## Pagination & System

### `Page[AuditLogOut]`

| Field | Type | Notes |
| --- | --- | --- |
| `items` | `array[AuditLogOut]` |  |
| `total` | `integer` |  |
| `page` | `integer` |  |
| `limit` | `integer` |  |

### `Page[EventOut]`

| Field | Type | Notes |
| --- | --- | --- |
| `items` | `array[EventOut]` |  |
| `total` | `integer` |  |
| `page` | `integer` |  |
| `limit` | `integer` |  |