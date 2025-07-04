import datetime
import typing
from enum import Enum

from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel

if typing.TYPE_CHECKING:
    from models.soda import Soda  # noqa: F401


class TransactionType(str, Enum):
    BUY = "buy"
    RESTOCK = "restock"
    DELETE = "delete"
    UNKNOWN = "unknown"


class Transaction(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    soda_id: int = Field(foreign_key="soda.id", nullable=False)
    type: TransactionType = Field(nullable=False)
    quantity: int = Field(default=0, nullable=False)
    date: int = Field(
        default_factory=lambda: int(datetime.datetime.today().timestamp()),
        nullable=False,
    )

    soda: typing.Optional["Soda"] = Relationship(back_populates="transactions")

    def __repr__(self):
        return f"Transaction({self.id}, soda_id={self.soda_id}, action='{self.action}', quantity={self.quantity})"


class TransactionInstructor(BaseModel):
    soda_name: str
    type: TransactionType
    date: typing.List[datetime.datetime] | datetime.datetime | None = None
