from sqlmodel import SQLModel, Field


class Soda(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True, nullable=False)
    qty: int = Field(default=0, nullable=False)

    def __repr__(self):
        return f"Soda({self.id}, name='{self.name}', qty={self.qty})"