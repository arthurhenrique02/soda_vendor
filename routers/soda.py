import instructor
from fastapi import APIRouter, Depends, HTTPException, Response
from openai import OpenAI
from sqlmodel import Session

from models.engine import get_db
from models.soda import SodaInstructor
from routers.utils.soda import make_decision

blueprint_name = "soda"
router = APIRouter(
    prefix=f"/{blueprint_name}",
    tags=[blueprint_name],
    responses={404: {"description": "Not found"}},
)
client = instructor.from_openai(OpenAI())


@router.get("/chat")
async def chat(prompt: str, db: Session = Depends(get_db)):
    """
    Get User`s prompt, watch his intention and manipulate the database
    :return: str
    """

    prompt_msg = (
        "Considering a soda vending machine context,"
        "extract the user intention, "
        f"soda name (coke, pepsi, etc) and quantity from the following prompt: {prompt}"
    )

    data: SodaInstructor = client.chat.completions.create(
        model="gpt-4.1-nano",
        response_model=SodaInstructor,
        messages=[
            {"role": "user", "content": prompt_msg},
        ],
    )

    if data.intention == "unknown":
        return HTTPException(
            status_code=400,
            detail=f"Invalid intention: {data.intention}. "
                   "Expected one of: buy, sell, restock."
        )

    if not data.name.strip() and data.intention != "list":
        return HTTPException(
            status_code=400,
            detail="Not found soda name in the prompt."
        )

    if data.qty <= 0 and data.intention not in ["list", "retrieve", "delete"]:
        return HTTPException(
            status_code=400,
            detail=f"Invalid quantity: {data.qty}. "
                   "Quantity must be an integer greater than zero."
        )

    reponse = make_decision(data, db)

    if not isinstance(reponse, (HTTPException, Response)):
        return HTTPException(
            status_code=500,
            detail="An unexpected error occurred while processing the request."
        )
    
    return reponse
