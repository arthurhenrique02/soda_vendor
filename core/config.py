from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel

from models.engine import ENGINE, get_db
from routers.soda import router as soda_router
from routers.transaction import router as transaction_router


def configure_cors(application: FastAPI) -> None:
    origins = ["http://localhost:8000"]
    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def configure_routes(application: FastAPI) -> None:
    application.include_router(soda_router)
    application.include_router(transaction_router)


def configure_db() -> None:
    SQLModel.metadata.bind = get_db()
    SQLModel.metadata.create_all(bind=ENGINE)
