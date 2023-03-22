from fastapi import Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from src.core.oauth2 import JWTBearer, JwtHandler
from src.database.config import Postgres


async def get_session() -> AsyncSession:
    """
    Dependency function that yields db sessions
    """
    async with Postgres().async_session() as session:
        yield session
        await session.commit()


class JWTValidateUser(BaseModel):
    user_id: str


async def current_user(token: str = Depends(JWTBearer())) -> JWTValidateUser:

    error = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Credentials are not valid')
    if token is None:
        raise error

    payload = JwtHandler().decode_access_token(token)

    if payload is None:
        raise error

    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not found")

    return JWTValidateUser(user_id=user_id)
