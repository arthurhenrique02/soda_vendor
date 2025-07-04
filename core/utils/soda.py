import datetime

from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlmodel import Session, select

from core.utils.transaction import create_transaction
from models.soda import Soda, SodaInstructor


def create_soda(name: str, qty: int, db: Session):
    """
    Create a new soda entry in the database.

    :param intention: The intention of the action (buy, sell, restock).
    :param name: The name of the soda.
    :param qty: The quantity of the soda.
    :param db: Database session.
    """

    soda = Soda(name=name, qty=qty)

    db.add(soda)
    db.commit()
    db.refresh(soda)

    return soda


def update_soda(soda_id: int, name: str, qty: int, db: Session):
    """
    Update an existing soda entry in the database.

    :param soda_id: The ID of the soda to update.
    :param name: The new name of the soda.
    :param qty: The new quantity of the soda.
    :param db: Database session.
    """

    soda = db.get(Soda, soda_id)

    if not soda:
        return None

    soda.qty = qty

    db.add(soda)
    db.commit()
    db.refresh(soda)

    return soda


def delete_soda(soda_id: int, db: Session):
    """
    Delete a soda entry from the database.

    :param soda_id: The ID of the soda to delete.
    :param db: Database session.
    """

    soda = db.get(Soda, soda_id)

    if not soda:
        return None

    soda.qty = 0
    db.add(soda)
    db.commit()
    return soda


def get_soda_by_name(name: str, db: Session):
    """
    Retrieve a soda entry from the database.

    :param soda_id: The ID of the soda to retrieve.
    :param db: Database session.
    """
    statement = select(Soda).where(Soda.name == name)
    soda = db.exec(statement).one_or_none()

    if not soda:
        return None

    return soda


def list_sodas(db: Session):
    """
    List all soda entries in the database.

    :param db: Database session.
    """

    statement = select(Soda)

    sodas = db.exec(statement).all()

    if not sodas:
        return None

    return sodas


def make_decision(data: SodaInstructor, db: Session):
    """
    Make a decision based on the user's intention and manipulate the database accordingly.

    :param data: The SodaInstructor data containing user intention, name, and quantity.
    :param db: Database session.
    """

    soda = None

    if data.name.strip():
        soda = get_soda_by_name(data.name, db)

    response = None

    match data.intention:
        case "buy":
            if not soda:
                raise HTTPException(
                    status_code=404, detail=f"Soda '{data.name}' not found."
                )

            if soda.qty < data.qty:
                raise HTTPException(
                    status_code=400,
                    detail=f"Not enough quantity for '{data.name}'. Available: {soda.qty}, Requested: {data.qty}.",
                )

            soda.qty -= data.qty
            update_soda(soda.id, soda.name, soda.qty, db)
            response = JSONResponse(
                content={
                    "detail": f"Successfully bought {data.qty} of '{data.name}'. Remaining quantity: {soda.qty}."
                },
                media_type="json",
                status_code=200,
            )
        case "restock":
            if not soda:
                soda = create_soda(data.name, data.qty, db)
                response = JSONResponse(
                    content={
                        "detail": f"Soda '{data.name}' created with quantity {data.qty}."
                    },
                    media_type="json",
                    status_code=201,
                )

            soda.qty += data.qty
            update_soda(soda.id, soda.name, soda.qty, db)
            response = JSONResponse(
                content={
                    "detail": f"Soda '{data.name}' restocked with quantity {data.qty}."
                },
                media_type="json",
                status_code=200,
            )
        case "delete":
            if not soda:
                raise HTTPException(
                    status_code=404, detail=f"Soda '{data.name}' not found."
                )

            delete_soda(soda.id, db)
            response = JSONResponse(
                content={"detail": f"Soda '{data.name}' deleted successfully."},
                media_type="json",
                status_code=200,
            )
        case "list":
            sodas = list_sodas(db)
            if not sodas:
                response = JSONResponse(
                    content={"detail": "No sodas available."},
                    media_type="json",
                    status_code=200,
                )

            response = JSONResponse(
                content=[soda.model_dump() for soda in sodas],
                media_type="json",
                status_code=200,
            )

        case "retrieve":
            if not soda:
                raise HTTPException(
                    status_code=404, detail=f"Soda '{data.name}' not found."
                )

            response = JSONResponse(
                content={"detail": f"Soda '{soda.name}' has quantity {soda.qty}."},
                media_type="json",
                status_code=200,
            )
        case _:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid intention: {data.intention}. "
                "Expected one of: buy, restock, delete, list, retrieve.",
            )

    if data.intention in ["buy", "restock", "delete"]:
        create_transaction(
            soda_id=soda.id,
            transaction_type=data.intention,
            date=datetime.datetime.today(),
            db=db,
        )

    return response
