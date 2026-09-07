from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from ..database import get_db
from ..models import Lead
from ..schemas import LeadCreate, LeadResponse
from ..credit_score import fetch_credit_score
from ..bre_engine import evaluate_bre
from typing import Optional
from fastapi import Query

router = APIRouter(prefix="/api", tags=["Leads"])


def calculate_age(dob: date) -> int:
    today = date.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return age


@router.post("/leads", response_model=LeadResponse)
def create_lead(lead_data: LeadCreate, db: Session = Depends(get_db)):

    # Module 8: Duplicate check
    existing_lead = db.query(Lead).filter(Lead.mobile == lead_data.mobile).first()
    if existing_lead:
        raise HTTPException(status_code=400, detail="Lead already exists")

    # Module 2: Fetch credit score (graceful failure handling)
    credit_score = fetch_credit_score(lead_data.mobile)
    if credit_score is None:
        credit_score = 0  # fallback value

    # Calculate age from DOB for BRE
    age = calculate_age(lead_data.dob)

    # Prepare data dict for BRE engine
    bre_input = {
        "age": age,
        "monthly_income": lead_data.monthly_income,
        "credit_score": credit_score,
        "loan_amount": lead_data.loan_amount,
        "property_value": lead_data.property_value,
    }

    # Module 3: Run BRE
    bre_status, reasons = evaluate_bre(db, bre_input)

    # Save lead to DB
    new_lead = Lead(
        full_name=lead_data.full_name,
        mobile=lead_data.mobile,
        email=lead_data.email,
        dob=lead_data.dob,
        city=lead_data.city,
        pincode=lead_data.pincode,
        loan_type=lead_data.loan_type,
        employment_type=lead_data.employment_type,
        monthly_income=lead_data.monthly_income,
        loan_amount=lead_data.loan_amount,
        property_value=lead_data.property_value,
        credit_score=credit_score,
        bre_status=bre_status,
        rejection_reasons=", ".join(reasons) if reasons else None,
        consent=lead_data.consent,
    )

    db.add(new_lead)
    db.commit()
    db.refresh(new_lead)

    return LeadResponse(
        status="success",
        lead_id=new_lead.id,
        credit_score=credit_score,
        bre_status=bre_status,
        reasons=reasons,
    )
@router.get("/leads")
def get_leads(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = None,
    status_filter: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Lead)

    if search:
        query = query.filter(
            (Lead.full_name.ilike(f"%{search}%")) |
            (Lead.mobile.ilike(f"%{search}%"))
        )

    if status_filter:
        query = query.filter(Lead.bre_status == status_filter)

    total = query.count()
    leads = query.order_by(Lead.created_at.desc()).offset((page - 1) * limit).limit(limit).all()

    result = [
        {
            "lead_id": lead.id,
            "customer_name": lead.full_name,
            "mobile": lead.mobile,
            "loan_type": lead.loan_type,
            "credit_score": lead.credit_score,
            "bre_status": lead.bre_status,
            "created_at": lead.created_at,
        }
        for lead in leads
    ]

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "leads": result
    }