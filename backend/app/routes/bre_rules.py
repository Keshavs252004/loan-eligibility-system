from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import BRERule
from ..schemas import BRERuleCreate, BRERuleResponse
from ..auth import get_current_admin

router = APIRouter(prefix="/api/admin/bre-rules", tags=["BRE Rules"])


@router.get("/", response_model=list[BRERuleResponse])
def get_rules(db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    return db.query(BRERule).all()


@router.post("/", response_model=BRERuleResponse)
def create_rule(rule: BRERuleCreate, db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    new_rule = BRERule(**rule.dict())
    db.add(new_rule)
    db.commit()
    db.refresh(new_rule)
    return new_rule


@router.put("/{rule_id}", response_model=BRERuleResponse)
def update_rule(rule_id: int, rule: BRERuleCreate, db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    existing_rule = db.query(BRERule).filter(BRERule.id == rule_id).first()
    if not existing_rule:
        raise HTTPException(status_code=404, detail="Rule not found")

    for key, value in rule.dict().items():
        setattr(existing_rule, key, value)

    db.commit()
    db.refresh(existing_rule)
    return existing_rule


@router.delete("/{rule_id}")
def delete_rule(rule_id: int, db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    existing_rule = db.query(BRERule).filter(BRERule.id == rule_id).first()
    if not existing_rule:
        raise HTTPException(status_code=404, detail="Rule not found")

    db.delete(existing_rule)
    db.commit()
    return {"message": "Rule deleted successfully"}