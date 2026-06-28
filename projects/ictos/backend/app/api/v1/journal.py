from fastapi import APIRouter, HTTPException
from typing import List
from sqlmodel import Session, select
from ...models.journal_entry import JournalEntry
from ...database import engine

router = APIRouter()

@router.get("/", response_model=list[JournalEntry])
async def list_entries() -> List[JournalEntry]:
    with Session(engine) as session:
        return session.exec(select(JournalEntry)).all()

@router.post("/", response_model=JournalEntry)
async def create_entry(entry: JournalEntry) -> JournalEntry:
    with Session(engine) as session:
        session.add(entry)
        session.commit()
        session.refresh(entry)
        return entry
