from sqlalchemy.ext.asyncio import AsyncSession
from src.repository.contacts import ContactRepository
from src.schemas import ContactCreate, ContactUpdate
from src.database.models import User

class ContactService:
    def __init__(self, db: AsyncSession):
        self.repo = ContactRepository(db)

    async def create_contact(self, contact_data: ContactCreate, user: User):
        return await self.repo.create_contact(contact_data, user)

    async def get_contacts(self, user: User):
        return await self.repo.get_contacts(user)

    async def get_contact(self, contact_id: int, user: User):
        return await self.repo.get_contact_by_id(contact_id, user)

    async def update_contact(self, contact_id: int, contact_data: ContactUpdate, user: User):
        contact = await self.repo.get_contact_by_id(contact_id, user)
        if not contact:
            return None
        return await self.repo.update_contact(contact, contact_data)

    async def delete_contact(self, contact_id: int, user: User):
        contact = await self.repo.get_contact_by_id(contact_id, user)
        if not contact:
            return None
        await self.repo.delete_contact(contact)
        return contact

    async def search_contacts(self, query_str: str, user: User):
        return await self.repo.search_contacts(query_str, user)

    async def get_upcoming_birthdays(self, user: User):
        return await self.repo.get_upcoming_birthdays(user)
