from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers import event_router

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
        title="Provider App",
        description="Handling Our Users",
        version="1",
    )

    @app.on_event("startup")
    async def startup():
        pass

    @app.on_event("shutdown")
    async def shutdown():
        pass

    app.include_router(event_router.router)

    return app


app = init_app()


