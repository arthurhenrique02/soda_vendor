from fastapi import APIRouter, Depends, HTTPException
from models.soda import Soda
from sqlmodel import Session
from models.engine import get_db


blueprint_name = "soda"
router = APIRouter(
    prefix=f"/{blueprint_name}",
    tags=[blueprint_name],
    responses={404: {"description": "Not found"}},
)

@router.get("/chat")
async def chat(prompt: str, db: Session = Depends(get_db)):
    """
    Get User`s prompt, watch his intention and manipulate the database
    :return: str
    """
    ...
    