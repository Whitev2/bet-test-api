from typing import Union, List

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exc, update
from fastapi import HTTPException, status
from src.database.models.bet_models.bet_model import Bet
from src.database.models.user_models.user_model import User
from src.schemas.bet_schema import BetBase, BetOut, ChangeStatus
from src.config import config


class BetCrud:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def _get_by_id(self, bet_id: Union[str, int]) -> Bet | None:
        return await self._session.get(Bet, str(bet_id))

    async def _get_user_by_id(self, user_id: str) -> User | None:
        return await self._session.get(User, user_id)

    async def _close_session(self):
        if self._session.is_active:
            await self._session.close()

    async def get_bets_from_user(self, user_id: str) -> List[BetOut]:
        user = await self._get_user_by_id(user_id)

        if len(user.bets) == 0:
            return []

        resp_list = list()
        for bet in user.bets:

            resp_list.append(BetOut(**bet.__dict__))

        return resp_list

    async def create_bet(self, user_id, create_data: BetBase) -> BetOut:
        current_events = await self.get_events()

        count = 0
        for event in current_events:
            if str(create_data.event_id) == event.get('event_id'):
                count += 1

        if count == 0:
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="This event not active")

        user = await self._get_user_by_id(user_id)

        bet = Bet(event_id=str(create_data.event_id), amount=str(create_data.amount), status='new')

        user.bets.append(bet)

        try:
            self._session.add(user)
            await self._session.commit()
        except exc.IntegrityError:
            await self._session.rollback()

        await self._close_session()

        return BetOut(**bet.__dict__)

    async def update_status(self, update_data: ChangeStatus):

        query = (
            update(Bet).
            where(Bet.event_id == str(update_data.event_id)).
            values({'status': update_data.state})
        )
        try:
            await self._session.execute(query)
            await self._session.commit()

        except exc.IntegrityError:
            await self._session.rollback()

        await self._close_session()

    @classmethod
    async def get_events(cls):
        async with AsyncClient(base_url=config.provider_event_url) as session:
            response = await session.get('/events')
            return response.json()
