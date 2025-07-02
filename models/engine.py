import os
from dotenv import load_dotenv
from sqlmodel import Session, create_engine

load_dotenv()

DATABASE_URL = os.getenv("DB_URL")

ENGINE = create_engine(DATABASE_URL, echo=False)

async def get_db():
    with Session(ENGINE) as session:
        yield session
