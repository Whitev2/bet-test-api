import time

import pytest
from httpx import AsyncClient

from src.routers.event_router import router

base_url = 'http://localhost:8001'


@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_simple_workflow(anyio_backend):
    test_id = '10'

    test_event = {
        'event_id': test_id,
        'coefficient': 1.0,
        'deadline': int(time.time()) + 600,
        'state': 1
    }

    async with AsyncClient(app=router, base_url=base_url) as ac:
        create_response = await ac.post('/event', json=test_event)
        print(create_response)

    assert create_response.status_code == 200

    async with AsyncClient(app=router, base_url=base_url) as ac:
        response = await ac.get(f'/event/{test_id}')

    assert response.status_code == 200
    assert response.json() == test_event

    updated_event = test_event.copy()
    updated_event['state'] = 2

    async with AsyncClient(app=router, base_url=base_url) as ac:
        update_response = await ac.post('/event', json={'event_id': test_id, 'state': 2})

    assert update_response.status_code == 200

    async with AsyncClient(app=router, base_url=base_url) as ac:
        response = await ac.get(f'/event/{test_id}')

    assert response.status_code == 200
    assert response.json() == updated_event
