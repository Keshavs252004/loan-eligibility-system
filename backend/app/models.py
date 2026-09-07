from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Boolean
from sqlalchemy.sql import func
from .database import Base

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    mobile = Column(String(10), unique=True, nullable=False, index=True)
    email = Column(String(100), nullable=False)
    dob = Column(Date, nullable=False)
    city = Column(String(50), nullable=False)
    pincode = Column(String(6), nullable=False)

    loan_type = Column(String(50), nullable=False)
    employment_type = Column(String(50), nullable=False)
    monthly_income = Column(Float, nullable=False)
    loan_amount = Column(Float, nullable=False)
    property_value = Column(Float, nullable=False)

    credit_score = Column(Integer, nullable=True)
    bre_status = Column(String(20), nullable=True)
    rejection_reasons = Column(String(500), nullable=True)

    consent = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class BRERule(Base):
    __tablename__ = "bre_rules"

    id = Column(Integer, primary_key=True, index=True)
    field_name = Column(String(50), nullable=False)
    operator = Column(String(5), nullable=False)
    value = Column(String(50), nullable=False)
    description = Column(String(200), nullable=True)
    active = Column(Boolean, default=True)


class AdminUser(Base):
    __tablename__ = "admin_users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    hashed_password = Column(String(200), nullable=False)