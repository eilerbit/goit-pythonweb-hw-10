from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Date

Base = declarative_base()

class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    birthday = Column(Date, nullable=True)
    additional_data = Column(String, nullable=True)
