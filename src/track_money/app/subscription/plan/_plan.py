from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String

from track_money.app.domain_exception import DomainException
from track_money.app.infra.database import Base


class Plan(Base):
    __tablename__ = "plans"
    __table_args__ = {"schema": "subscription"}
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(24), unique=True, index=True, nullable=False)
    max_number_accounts = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    is_free = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False)

    def __init__(self, name: str, max_number_accounts: int, price: float):
        DomainException.validate(name and len(name) <= 24, "Plan name must be a non-empty string with a maximum length of 24 characters.")
        self.name = name

        DomainException.validate(max_number_accounts and max_number_accounts >= 0, "Max number of accounts must be a positive integer.")
        self.max_number_accounts = max_number_accounts

        DomainException.validate(price is not None and price >= 0, "Price must be a non-negative float.")
        self.price = price
        
        self.is_free = True if price == 0 else False
        self.created_at = datetime.now(timezone.utc)