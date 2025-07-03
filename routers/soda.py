import instructor
from fastapi import APIRouter, Depends
from openai import OpenAI
from sqlmodel import Session

from models.engine import get_db
from models.soda import SodaInstructor

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
        "extract the user intention (buy, sell, restock, etc), "
        f"soda name (coke, pepsi, etc) and quantity from the following prompt: {prompt}"
    )

    data = client.chat.completions.create(
        model="gpt-4.1-nano",
        response_model=SodaInstructor,
        messages=[
            {"role": "user", "content": prompt_msg},
        ],
    )

    print(data)
