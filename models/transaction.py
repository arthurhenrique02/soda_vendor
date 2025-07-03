from pydantic import BaseModel
from sqlmodel import Field, SQLModel
import typing


class Transaction(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    soda_id: int = Field(foreign_key="soda.id", nullable=False)
    action: typing.Literal["buy", "restock", "delete"]
    quantity: int = Field(default=0, nullable=False)

    def __repr__(self):
        return f"Transaction({self.id}, soda_id={self.soda_id}, action='{self.action}', quantity={self.quantity})"