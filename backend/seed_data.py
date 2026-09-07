from app.database import SessionLocal
from app.models import BRERule, AdminUser
from app.auth import get_password_hash

db = SessionLocal()

# Seed default BRE rules
default_rules = [
    BRERule(field_name="age", operator=">=", value="21", description="Age below minimum requirement (21)"),
    BRERule(field_name="age", operator="<=", value="60", description="Age above maximum limit (60)"),
    BRERule(field_name="monthly_income", operator=">=", value="30000", description="Monthly Income below eligibility criteria"),
    BRERule(field_name="credit_score", operator=">=", value="700", description="Credit Score below minimum requirement"),
    BRERule(field_name="loan_amount", operator="<=", value="0.8*property_value", description="Loan Amount exceeds eligible limit (80% of property value)"),
]
db.add_all(default_rules)

# Seed default admin user
admin_user = AdminUser(
    username="admin",
    hashed_password=get_password_hash("admin123")
)
db.add(admin_user)

db.commit()
db.close()
print("Default BRE rules and admin user seeded successfully!")
print("Admin login -> username: admin, password: admin123")