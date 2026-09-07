from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..database import get_db
from ..models import AdminUser, Lead
from ..auth import verify_password, create_access_token, get_current_admin

router = APIRouter(prefix="/api/admin", tags=["Admin"])


@router.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    admin = db.query(AdminUser).filter(AdminUser.username == username).first()
    if not admin or not verify_password(password, admin.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token = create_access_token(data={"sub": admin.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/dashboard")
def dashboard_stats(db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    total_leads = db.query(Lead).count()
    eligible_leads = db.query(Lead).filter(Lead.bre_status == "Eligible").count()
    rejected_leads = db.query(Lead).filter(Lead.bre_status == "Not Eligible").count()

    avg_credit_score_result = db.query(func.avg(Lead.credit_score)).scalar()
    avg_credit_score = round(avg_credit_score_result, 2) if avg_credit_score_result else 0

    return {
        "total_leads": total_leads,
        "eligible_leads": eligible_leads,
        "rejected_leads": rejected_leads,
        "average_credit_score": avg_credit_score,
    }