import asyncio

from aio_pika import connect
from aio_pika.abc import AbstractIncomingMessage

from src.crud.bet_crud import BetCrud
from src.database.config import Postgres
from src.schemas.bet_schema import ChangeStatus

mq_url = "amqp://betmqmq:betmqmq@rabbitmq:5672/"


async def change_status(message: AbstractIncomingMessage):

    async with Postgres().async_session() as ses:
        bet_crud = BetCrud(ses)

    await bet_crud.update_status(ChangeStatus(**message.headers))


async def start_consumer() -> None:
    await asyncio.sleep(10)
    connection = await connect(mq_url)
    async with connection:
        # Creating a channel
        channel = await connection.channel()

        withdrawal_queue = await channel.declare_queue("status_manage", auto_delete=False)

        await withdrawal_queue.consume(change_status, no_ack=True)

        await asyncio.Future()
