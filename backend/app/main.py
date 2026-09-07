from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .routes import leads, admin, bre_rules

app = FastAPI(title="Loan Eligibility & Lead Management API")

# CORS Middleware - allows frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(leads.router)
app.include_router(admin.router)
app.include_router(bre_rules.router)

@app.get("/")
def root():
    return {"message": "Loan Eligibility API is running"}