from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlmodel import Session, select

from models.transaction import Transaction, TransactionInstructor, TransactionType


def create_transaction(
    soda_id: str, transaction_type: str, qty: int, date: str, db: Session
):
    """
    Create a new transaction entry in the database.

    :param soda_name: The name of the soda involved in the transaction.
    :param transaction_type: The type of transaction (buy, restock, delete).
    :param date: The date of the transaction.
    :param db: Database session.
    """
    transaction = Transaction(
        soda_id=soda_id, type=transaction_type, quantity=qty, date=int(date.timestamp())
    )

    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    return transaction


def filter_transactions(data: TransactionInstructor, db: Session):
    """
    Filter transactions based on soda name, transaction type, and date.

    :param soda_name: The name of the soda to filter by.
    :param transaction_type: The type of transaction to filter by.
    :param date: The date to filter by.
    :param db: Database session.
    :return: List of filtered transactions.
    """
    query = select(Transaction)

    if data.soda_name.strip() not in ["all", ""]:
        from models.soda import Soda

        query = query.join(Soda).where(Soda.name == data.soda_name.strip())

    if data.type != TransactionType.UNKNOWN:
        query = query.where(Transaction.type == data.type)

    if date := data.date:
        if isinstance(date, list):
            # is a date range
            unix_timestamps = [int(d.timestamp()) for d in date]
            query = query.where(
                Transaction.date >= min(unix_timestamps),
                Transaction.date <= max(unix_timestamps),
            )
        else:
            u_date = int(date.timestamp())
            query = query.where(Transaction.date >= u_date)

    transactions = db.exec(query).all()

    if not transactions:
        raise HTTPException(status_code=404, detail="No transactions found.")

    return JSONResponse(
        content=[transaction.model_dump() for transaction in transactions]
    )
