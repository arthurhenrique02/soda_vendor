import os
import typing

from sqlmodel import Session, create_engine

DATABASE_URL = os.getenv("DB_URL")

ENGINE = create_engine(DATABASE_URL, echo=False)


def get_db() -> typing.Generator[Session, None, None]:
    with Session(ENGINE) as session:
        yield session
