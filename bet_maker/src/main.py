import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.database.config import Postgres
from src.rabbit.consumer import start_consumer
from src.routers import bet_router
from src.routers.auth import auth_user

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def init_app():
    app = FastAPI(
        title="Users App",
        description="Handling Our Users",
        version="1",
    )

    @app.on_event("startup")
    async def startup():
        await Postgres().connect_to_storage()

    @app.on_event("shutdown")
    async def shutdown():
        pass
    app.include_router(bet_router.router)
    app.include_router(auth_user.router)

    asyncio.create_task(start_consumer())

    return app


app = init_app()
