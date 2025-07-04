import instructor
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from openai import OpenAI
from sqlmodel import Session

from core.utils.transaction import filter_transactions
from models.engine import get_db
from models.transaction import TransactionInstructor, TransactionType

blueprint_name = "transaction"
router = APIRouter(
    prefix=f"/{blueprint_name}",
    tags=[blueprint_name],
    responses={404: {"description": "Not found"}},
)
client = instructor.from_openai(OpenAI())


@router.post("/chat")
async def chat(prompt: str, db: Session = Depends(get_db)):
    """
    Get User's prompt, watch his intention and check in the database
    :return: JSON response or HTTPException
    """

    prompt_msg = (
        "Considering a soda vending machine transactions context,"
        "transaction for what soda (coke, pepsi, fanta, all, etc), type of transaction"
        " (buy, restock, delete) or date, if is a date range, save in a list: {prompt}"
    )

    data: TransactionInstructor = client.chat.completions.create(
        model="gpt-4.1-nano",
        response_model=TransactionInstructor,
        messages=[
            {"role": "user", "content": prompt_msg.format(prompt=prompt)},
        ],
    )

    if (
        not data.soda_name.strip()
        and data.type.value == TransactionType.UNKNOWN
        and not data.date
    ):
        raise HTTPException(
            status_code=400,
            detail="No data returned from the model. Please provide a valid prompt.",
        )

    response = filter_transactions(data, db)

    if not isinstance(response, (HTTPException, dict, JSONResponse)):
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while processing the request.",
        )

    return response
