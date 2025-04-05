import asyncio
from faker import Faker
from src.database.models import Contact
from src.database.db import get_db

fake = Faker()

async def seed_contacts():
    async for session in get_db():
        for _ in range(10):
            contact = Contact(
                first_name=fake.first_name()[:20],
                last_name=fake.last_name()[:20],
                email=fake.unique.email(),
                phone=fake.unique.phone_number()[:20],
                birthday=fake.date_of_birth(),
                additional_data=fake.text()
            )
            session.add(contact)
        await session.commit()
        print("Seeding complete!")
        break

if __name__ == "__main__":
    asyncio.run(seed_contacts())
