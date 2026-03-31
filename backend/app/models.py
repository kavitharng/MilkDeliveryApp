from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base

subscription_table = Table(
    "subscription",
    Base.metadata,
    Column(
        "customer_id",
        Integer,
        ForeignKey("customers.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "vendor_id",
        Integer,
        ForeignKey("vendors.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Vendor(Base):
    __tablename__ = "vendors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    customers = relationship(
        "Customer",
        secondary=subscription_table,
        back_populates="vendors",
    )


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    vendors = relationship(
        "Vendor",
        secondary=subscription_table,
        back_populates="customers",
    )
