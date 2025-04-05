from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.db import get_db
from src.schemas import ContactCreate, ContactUpdate, ContactResponse
from src.services.contacts import ContactService

router = APIRouter(prefix="/contacts", tags=["contacts"])

@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(contact: ContactCreate, db: AsyncSession = Depends(get_db)):
    service = ContactService(db)
    return await service.create_contact(contact)

@router.get("/", response_model=List[ContactResponse])
async def read_contacts(
    search: Optional[str] = Query(None, description="Пошук за ім'ям, прізвищем або email"),
    db: AsyncSession = Depends(get_db)
):
    service = ContactService(db)
    if search:
        contacts = await service.search_contacts(search)
    else:
        contacts = await service.get_contacts()
    return contacts

@router.get("/upcoming-birthdays", response_model=List[ContactResponse])
async def upcoming_birthdays(db: AsyncSession = Depends(get_db)):
    service = ContactService(db)
    return await service.get_upcoming_birthdays()

@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    service = ContactService(db)
    contact = await service.get_contact(contact_id)
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact

@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(contact_id: int, contact_data: ContactUpdate, db: AsyncSession = Depends(get_db)):
    service = ContactService(db)
    updated_contact = await service.update_contact(contact_id, contact_data)
    if not updated_contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return updated_contact

@router.delete("/{contact_id}", response_model=ContactResponse)
async def delete_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    service = ContactService(db)
    deleted_contact = await service.delete_contact(contact_id)
    if not deleted_contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return deleted_contact
