from typing import Optional

import aio_pika
from aio_pika import Message

from src.schemas.event_schema import EventState

qt_url = "amqp://betmqmq:betmqmq@rabbitmq:5672/"


async def publish_new_state(event_id: str, state: Optional[EventState]) -> None:
    connection = await aio_pika.connect_robust(qt_url,)

    routing_key = "status_manage"

    message = Message(headers={"event_id": event_id, "state": state.name}, body="change".encode())

    async with connection:
        channel = await connection.channel()
        await channel.default_exchange.publish(message, routing_key=routing_key)

    if not connection.is_closed:
        await connection.close()
