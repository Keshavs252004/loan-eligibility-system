from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import date
from typing import Optional, List

class LeadCreate(BaseModel):
    full_name: str = Field(..., min_length=2)
    mobile: str = Field(..., min_length=10, max_length=10)
    email: EmailStr
    dob: date
    city: str
    pincode: str = Field(..., min_length=6, max_length=6)

    loan_type: str          # "Home Loan" or "Loan Against Property (LAP)"
    employment_type: str    # "Salaried" or "Self Employed"
    monthly_income: float = Field(..., gt=0)
    loan_amount: float = Field(..., gt=0)
    property_value: float = Field(..., gt=0)

    consent: bool

    @field_validator("mobile")
    @classmethod
    def mobile_must_be_digits(cls, v):
        if not v.isdigit():
            raise ValueError("Mobile number must contain only digits")
        return v

    @field_validator("consent")
    @classmethod
    def consent_must_be_true(cls, v):
        if not v:
            raise ValueError("Consent is mandatory to proceed")
        return v

    @field_validator("loan_type")
    @classmethod
    def validate_loan_type(cls, v):
        allowed = ["Home Loan", "Loan Against Property (LAP)"]
        if v not in allowed:
            raise ValueError(f"loan_type must be one of {allowed}")
        return v

    @field_validator("employment_type")
    @classmethod
    def validate_employment_type(cls, v):
        allowed = ["Salaried", "Self Employed"]
        if v not in allowed:
            raise ValueError(f"employment_type must be one of {allowed}")
        return v


class LeadResponse(BaseModel):
    status: str
    lead_id: int
    credit_score: Optional[int] = None
    bre_status: Optional[str] = None
    reasons: Optional[List[str]] = None

    class Config:
        from_attributes = True


class BRERuleCreate(BaseModel):
    field_name: str
    operator: str   # >=, <=, ==, >, 
    value: str
    description: Optional[str] = None
    active: bool = True


class BRERuleResponse(BRERuleCreate):
    id: int

    class Config:
        from_attributes = True