from sqlmodel import Session, select
from models.soda import Soda, SodaInstructor
from fastapi import HTTPException, Response


def create_soda(
    name: str,
    qty: int,
    db: Session
):
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


def update_soda(
    soda_id: int,
    name: str,
    qty: int,
    db: Session
):
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


def delete_soda(
    soda_id: int,
    db: Session
):
    """
    Delete a soda entry from the database.
    
    :param soda_id: The ID of the soda to delete.
    :param db: Database session.
    """
    
    soda = db.get(Soda, soda_id)
    
    if not soda:
        return None
    
    db.delete(soda)
    db.commit()

    return soda


def get_soda_by_name(
    name: str,
    db: Session
):
    """
    Retrieve a soda entry from the database.
    
    :param soda_id: The ID of the soda to retrieve.
    :param db: Database session.
    """
    
    soda = db.get(Soda, name)
    
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
        return []
    
    return sodas


def make_decision(data: SodaInstructor, db: Session):
    """
    Make a decision based on the user's intention and manipulate the database accordingly.
    
    :param data: The SodaInstructor data containing user intention, name, and quantity.
    :param db: Database session.
    """
    ["buy", "restock", "delete", "list", "retrieve", "unknown"]


    soda = None

    if data.name.strip():
        soda = get_soda_by_name(data.name, db)


    match data.intention:
        case "buy":
            if not soda:
                raise HTTPException(
                    status_code=404,
                    detail=f"Soda '{data.name}' not found."
                )
            
            if soda.qty < data.qty:
                raise HTTPException(
                    status_code=400,
                    detail=f"Not enough quantity for '{data.name}'. Available: {soda.qty}, Requested: {data.qty}."
                )
            
            soda.qty -= data.qty
            update_soda(soda.id, soda.name, soda.qty, db)
            return Response(
                content=f"Successfully bought {data.qty} of '{data.name}'. Remaining quantity: {soda.qty}.",
                media_type="text/plain",
                status_code=200
            )
        case "restock":
            if not soda:
                soda = create_soda(data.name, data.qty, db)
                return Response(
                    content=f"Soda '{data.name}' created with quantity {data.qty}.",
                    media_type="text/plain",
                    status_code=201
                )
            
            soda.qty += data.qty
            update_soda(soda.id, soda.name, soda.qty, db)
            return Response(
                content=f"Soda '{data.name}' restocked with quantity {data.qty}.",
                media_type="text/plain",
                status_code=200
            )
        case "delete":
            if not soda:
                raise HTTPException(
                    status_code=404,
                    detail=f"Soda '{data.name}' not found."
                )
            
            delete_soda(soda.id, db)
            return Response(
                content=f"Soda '{data.name}' deleted successfully.",
                media_type="text/plain",
                status_code=200
            )
        case "list":
            sodas = list_sodas(db)
            if not sodas:
                return Response(
                    content="No sodas available.",
                    media_type="text/plain",
                    status_code=200
                )
            
            soda_list = "\n".join([f"{soda.name}: {soda.qty}" for soda in sodas])
            return Response(
                content=f"Available sodas:\n{soda_list}",
                media_type="text/plain",
                status_code=200
            )
        
        case "retrieve":
            if not soda:
                raise HTTPException(
                    status_code=404,
                    detail=f"Soda '{data.name}' not found."
                )
            
            return Response(
                content=f"Soda '{soda.name}' has quantity {soda.qty}.",
                media_type="text/plain",
                status_code=200
            )
        case _:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid intention: {data.intention}. "
                       "Expected one of: buy, restock, delete, list, retrieve."
            )



