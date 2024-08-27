# main.py

from typing import List

from fastapi import FastAPI, Depends
from sqlalchemy.future import select

from models import Card
from database import get_db, database
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text as sa_text, func

app = FastAPI()

# Pydantic model for request/response handling
class CardSchema(BaseModel):
    index: int
    text: str
    headline: str

    class Config:
        from_attributes = True

class CardCreate(BaseModel):
    text: str

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Endpoint to read all cards
@app.get("/cards/", response_model=List[CardSchema])
async def read_cards(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Card))
    cards = result.scalars().all()
    return cards

# Endpoint to create a new card
@app.post("/cards/", response_model=CardSchema)
async def create_card(card: CardCreate, db: AsyncSession = Depends(get_db)):
    new_card = Card(text=card.text)
    db.add(new_card)
    await db.commit()
    await db.refresh(new_card)
    return new_card

# Endpoint for full-text search
@app.get("/cards/search/", response_model=List[CardSchema])
async def search_cards(search_term: str, db: AsyncSession = Depends(get_db)):
    # Use websearch_to_tsquery for flexible search
    ts_query = func.websearch_to_tsquery('english', search_term)
    
    # Adjust query for more flexible matching
    query = select(
        Card.index,
        Card.text,
        func.ts_headline('english', Card.text, ts_query).label('headline')
    ).where(Card.text_vector.op('@@')(ts_query))
    
    result = await db.execute(query)
    cards = result.all()
    return cards
