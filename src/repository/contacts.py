from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date, timedelta
from src.database.models import Contact, User
from src.schemas import ContactCreate, ContactUpdate

class ContactRepository:
    def __init__(self, session: AsyncSession):
        self.db = session

    async def create_contact(self, contact_data: ContactCreate, user: User) -> Contact:
        new_contact = Contact(**contact_data.dict(), user_id=user.id)
        self.db.add(new_contact)
        await self.db.commit()
        await self.db.refresh(new_contact)
        return new_contact

    async def get_contacts(self, user: User) -> list[Contact]:
        stmt = select(Contact).where(Contact.user_id == user.id)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_contact_by_id(self, contact_id: int, user: User) -> Contact | None:
        stmt = select(Contact).where(Contact.id == contact_id, Contact.user_id == user.id)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def update_contact(self, contact: Contact, contact_data: ContactUpdate) -> Contact:
        for field, value in contact_data.dict(exclude_unset=True).items():
            setattr(contact, field, value)
        self.db.add(contact)
        await self.db.commit()
        await self.db.refresh(contact)
        return contact

    async def delete_contact(self, contact: Contact):
        await self.db.delete(contact)
        await self.db.commit()

    async def search_contacts(self, query_str: str, user: User) -> list[Contact]:
        stmt = select(Contact).where(Contact.user_id == user.id,
            or_(
                Contact.first_name.ilike(f"%{query_str}%"),
                Contact.last_name.ilike(f"%{query_str}%"),
                Contact.email.ilike(f"%{query_str}%")
            )
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_upcoming_birthdays(self, user: User) -> list[Contact]:
        today = date.today()
        end_date = today + timedelta(days=7)
        stmt = select(Contact).where(Contact.user_id == user.id, Contact.birthday.between(today, end_date))
        result = await self.db.execute(stmt)
        return result.scalars().all()
