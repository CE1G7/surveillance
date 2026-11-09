import asyncio
from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse

from src.mock_assets.data import EVENTS
from src.schemas import EventOut, Page

router = APIRouter(prefix="/events", tags=["events"])


@router.get("", response_model=Page[EventOut])
def list_events(
    from_: Annotated[datetime | None, Query(alias="from")] = None,
    to: datetime | None = None,
    area_id: int | None = None,
    camera_id: int | None = None,
    starred: bool | None = None,
    page: int = 1,
    limit: int = 50,
):
    """Filters are accepted but ignored: always returns the same three events."""
    return Page[EventOut](items=EVENTS, total=len(EVENTS), page=page, limit=limit)


# Declared before /{event_id} so "stream" is not parsed as an id.
@router.get("/stream", response_class=StreamingResponse)
async def stream_events():
    """Server-Sent Events: repeats the newest static event every 5 seconds."""

    async def generate():
        yield "retry: 3000\n\n"
        while True:
            event = EVENTS[0]
            yield f"id: {event.seq}\nevent: event\ndata: {event.model_dump_json()}\n\n"
            await asyncio.sleep(5)

    return StreamingResponse(generate(), media_type="text/event-stream", headers={"Cache-Control": "no-cache"})


@router.get("/{event_id}", response_model=EventOut)
def get_event(event_id: UUID):
    return EVENTS[0].model_copy(update={"id": event_id})


@router.put("/{event_id}/star", response_model=EventOut)
def star_event(event_id: UUID):
    return EVENTS[0].model_copy(update={"id": event_id, "starred": True})


@router.delete("/{event_id}/star", response_model=EventOut)
def unstar_event(event_id: UUID):
    return EVENTS[0].model_copy(update={"id": event_id, "starred": False})
