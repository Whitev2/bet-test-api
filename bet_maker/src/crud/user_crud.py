import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exc
from fastapi import HTTPException, status

from src.core.oauth2 import create_tokens
from src.core.oauth2_form import OAuth2PasswordRequestForm
from src.core.security import Security
from src.database.models.user_models.user_model import User
from src.schemas.user_schema import UserResponse
from src.schemas.auth_schema import SignUp


class UserCrud:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def _get_by_id(self, user_id: str) -> User | None:
        return await self._session.get(User, user_id)

    async def _get_by_email(self, email: str) -> User | None:

        query = (
            select(User)
            .where(User.email == email)
        )
        result = await self._session.execute(query)
        user = result.first()

        if user is None:
            return None

        return user[0]

    async def get_user(self, user_id: str = None, email: str = None) -> UserResponse | None:
        if user_id:
            user = await self._get_by_id(user_id)

        elif email:
            user = await self._get_by_email(email)
        else:
            raise Exception

        if user is None:
            return None

        await self._close_session()

        return UserResponse(**user.__dict__)

    async def _close_session(self):
        if self._session.is_active:
            await self._session.close()

    async def create(self, create_data: SignUp) -> UserResponse:
        user = User(**create_data.dict(
            exclude={"password"}),
            uid=str(uuid.uuid4()),
            password=Security().hash_password(create_data.password)
                    )

        try:
            self._session.add(user)
            await self._session.commit()
        except exc.IntegrityError:
            await self._session.rollback()

        await self._close_session()
        return UserResponse(**user.__dict__)

    async def validate_user(self, form_data: OAuth2PasswordRequestForm):
        user = await self._get_by_email(email=form_data.email)

        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect email, user not found")

        password_check = Security().verify_password(form_data.password, user.password)

        if not password_check:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

        return await create_tokens(user_id=user.uid)

    async def logout(self, token: str):
        pass
