from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.engine import ENGINE, get_db
from sqlmodel import SQLModel
# from routers.soda import


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
    ...

def configure_db() -> None:
    SQLModel.metadata.bind = get_db()
    SQLModel.metadata.create_all(bind=ENGINE)
