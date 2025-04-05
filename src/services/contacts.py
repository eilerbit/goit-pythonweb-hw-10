from sqlalchemy.ext.asyncio import AsyncSession
from src.repository.contacts import ContactRepository
from src.schemas import ContactCreate, ContactUpdate

class ContactService:
    def __init__(self, db: AsyncSession):
        self.repo = ContactRepository(db)

    async def create_contact(self, contact_data: ContactCreate):
        return await self.repo.create_contact(contact_data)

    async def get_contacts(self):
        return await self.repo.get_contacts()

    async def get_contact(self, contact_id: int):
        return await self.repo.get_contact_by_id(contact_id)

    async def update_contact(self, contact_id: int, contact_data: ContactUpdate):
        contact = await self.repo.get_contact_by_id(contact_id)
        if not contact:
            return None
        return await self.repo.update_contact(contact, contact_data)

    async def delete_contact(self, contact_id: int):
        contact = await self.repo.get_contact_by_id(contact_id)
        if not contact:
            return None
        await self.repo.delete_contact(contact)
        return contact

    async def search_contacts(self, query_str: str):
        return await self.repo.search_contacts(query_str)

    async def get_upcoming_birthdays(self):
        return await self.repo.get_upcoming_birthdays()
