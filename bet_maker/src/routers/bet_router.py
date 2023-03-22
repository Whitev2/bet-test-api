from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.bet_crud import BetCrud
from src.routers.dopends import get_session, JWTValidateUser, current_user
from src.schemas.bet_schema import BetBase, BetOut
from src.schemas.response_schema import Message

router = APIRouter()


@router.get("/events")
async def get_events(db_session: AsyncSession = Depends(get_session)):
    bet_crud: BetCrud = BetCrud(db_session)
    return await bet_crud.get_events()


@router.get("/bets")
async def get_user_bets(db_session: AsyncSession = Depends(get_session),
                        user_data: JWTValidateUser = Depends(current_user)):
    bet_crud: BetCrud = BetCrud(db_session)
    return await bet_crud.get_bets_from_user(user_id=user_data.user_id)


@router.post("/bet",
             response_model=BetOut,
             status_code=201,
             responses={201: {"model": BetOut, "description": "Bet successfully created"},
                        400: {"model": Message, "description": "If the sum is less than 0"},
                        409: {"model": Message, "description": "Conflict, bet already exist"}})
async def send_bet(create_data: BetBase,
                   user_data: JWTValidateUser = Depends(current_user),
                   db_session: AsyncSession = Depends(get_session)):
    bet_crud: BetCrud = BetCrud(db_session)
    return await bet_crud.create_bet(user_id=user_data.user_id, create_data=create_data)
