from sqlalchemy import Column, String, Date, Numeric, TIMESTAMP, Text
from database import Base

class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(String, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    phone = Column(String)
    address = Column(Text)
    date_of_birth = Column(String)
    account_balance = Column(String)
    created_at = Column(String)