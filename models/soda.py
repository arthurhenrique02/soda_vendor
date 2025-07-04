import typing

from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel

if typing.TYPE_CHECKING:
    from models.transaction import Transaction  # noqa: F401


class Soda(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True, nullable=False)
    qty: int = Field(default=0, nullable=False)

    transactions: typing.List["Transaction"] = Relationship(back_populates="soda")

    def __repr__(self):
        return f"Soda({self.id}, name='{self.name}', qty={self.qty})"


class SodaInstructor(BaseModel):
    intention: typing.Literal["buy", "restock", "delete", "list", "retrieve", "unknown"]
    name: str
    qty: int
