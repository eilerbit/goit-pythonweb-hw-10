import asyncio
from faker import Faker
from sqlalchemy import select
from src.database.models import Contact, User
from src.database.db import get_db
from src.services.auth import Hash

fake = Faker()

DEFAULT_USERNAME = "default_user"
DEFAULT_EMAIL = "default@example.com"
DEFAULT_PASSWORD = "defaultpassword"

async def seed_contacts():
    async for session in get_db():
        result = await session.execute(select(User).filter_by(email=DEFAULT_EMAIL))
        user = result.scalars().first()

        if not user:
            hashed_pw = Hash().get_password_hash(DEFAULT_PASSWORD)
            user = User(
                username=DEFAULT_USERNAME,
                email=DEFAULT_EMAIL,
                hashed_password=hashed_pw,
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)
            print("Default user created.")

        # Now seed 10 contacts associated with the default user.
        for _ in range(10):
            contact = Contact(
                first_name=fake.first_name()[:20],
                last_name=fake.last_name()[:20],
                email=fake.unique.email(),
                phone=fake.unique.phone_number()[:20],
                birthday=fake.date_of_birth(),
                additional_data=fake.text(),
                user_id=user.id,
            )
            session.add(contact)
        await session.commit()
        print("Seeding complete!")
        break

if __name__ == "__main__":
    asyncio.run(seed_contacts())
