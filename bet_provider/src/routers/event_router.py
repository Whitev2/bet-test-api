from pathlib import Path
import time
from fastapi import HTTPException, APIRouter

from src.database.fake_db import events
from src.rabbit.publisher import publish_new_state
from src.schemas.event_schema import Event, UpdateState

router = APIRouter()


@router.post('/event')
async def create_event(event: Event):
    if event.event_id not in events:
        events[event.event_id] = event
        return {}

    for p_name, p_value in event.dict(exclude_unset=True).items():
        setattr(events[event.event_id], p_name, p_value)

    return {}


@router.get('/event/{event_id}')
async def get_event(event_id: str = Path(default=None)):
    if event_id in events:
        return events[event_id]

    raise HTTPException(status_code=404, detail="Event not found")


@router.put('/event')
async def change_status(update_data: UpdateState):
    if update_data.event_id in events:
        event: Event = events[update_data.event_id]
        setattr(events[event.event_id], 'state', update_data.state)

        # rabbitMQ
        await publish_new_state(update_data.event_id, update_data.state)

    return {}


@router.get('/events')
async def get_events():
    return list(e for e in events.values() if time.time() < e.deadline)
