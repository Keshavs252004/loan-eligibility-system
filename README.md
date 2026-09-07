# Loan Eligibility & Lead Management System

A full-stack application for loan eligibility checking and lead management, built for MoneyBeing Private Limited's Python Full Stack Intern Assessment.

## Objective
This system allows customers to submit loan applications, automatically fetches their credit score, evaluates eligibility through a configurable Business Rule Engine (BRE), and provides an admin panel for lead and rule management.

## Tech Stack
- Backend: Python (FastAPI)
- Frontend: Next.js (TypeScript + Tailwind CSS)
- Database: MySQL
- Authentication: JWT
- API: REST APIs
- Version Control: Git & GitHub

## Project Structure

project/
├── backend/ # FastAPI backend
│ ├── app/
│ │ ├── main.py
│ │ ├── database.py
│ │ ├── models.py
│ │ ├── schemas.py
│ │ ├── auth.py
│ │ ├── bre_engine.py
│ │ ├── credit_score.py
│ │ └── routes/
│ │ ├── leads.py
│ │ ├── admin.py
│ │ └── bre_rules.py
│ ├── seed_data.py
│ ├── requirements.txt
│ └── .env
└── frontend/ # Next.js frontend
├── app/
│ └── page.tsx
└── .env.local


## Setup Instructions

### Prerequisites
- Python 3.11+
- Node.js (LTS version)
- MySQL Server

### Backend Setup
1. Navigate to backend folder: cd backend
2. Create virtual environment: python -m venv venv
3. Activate virtual environment: venv\Scripts\activate
4. Install dependencies: pip install -r requirements.txt
5. Create a .env file in the backend folder with:
   DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/loan_db
   SECRET_KEY=your-secret-key-here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=60
6. Create the MySQL database: CREATE DATABASE loan_db;
7. Run the seed script: python seed_data.py
8. Start the backend server: uvicorn app.main:app --reload
9. Backend runs at: http://127.0.0.1:8000
10. Interactive API docs (Swagger): http://127.0.0.1:8000/docs

### Frontend Setup
1. Navigate to frontend folder: cd frontend
2. Install dependencies: npm install
3. Create a .env.local file in the frontend folder with:
   NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
4. Start the development server: npm run dev
5. Frontend runs at: http://localhost:3000

## Default Admin Credentials
- Username: admin
- Password: admin123

## Important Notes

### Credit Score API (Mock)
This project uses a mock/demo Credit Score API (simulated in app/credit_score.py) that generates a random score between 300–900. Real credit bureau APIs (CIBIL, Experian, Equifax) require paid subscriptions and KYC-verified business access, which is not feasible within the assessment timeframe. In a production environment, this function would be replaced with an actual API call to a licensed credit bureau service. API failure handling is implemented with a graceful fallback.

### Business Rule Engine (BRE)
BRE rules are not hardcoded — they are stored in the bre_rules database table and evaluated dynamically at runtime. Rules can be added, edited, or deleted via the Admin BRE Management API endpoints, and changes take effect immediately without any code modification.

Default seeded rules:
- Age >= 21
- Age <= 60
- Monthly Income >= 30000
- Credit Score >= 700
- Loan Amount <= 80% of Property Value

### Duplicate Lead Prevention
If a mobile number already exists in the system, the API returns "Lead already exists" instead of creating a duplicate record.

## API Endpoints

- POST /api/leads — Submit a new loan application (fetches credit score, runs BRE, stores lead)
- GET /api/leads — List all leads with search, filter, and pagination
- POST /api/admin/login — Admin login (returns JWT token)
- GET /api/admin/dashboard — Dashboard statistics (total/eligible/rejected leads, avg credit score)
- GET /api/admin/bre-rules — List all BRE rules
- POST /api/admin/bre-rules — Create a new BRE rule
- PUT /api/admin/bre-rules/{id} — Update an existing BRE rule
- DELETE /api/admin/bre-rules/{id} — Delete a BRE rule

## Sample API Response (POST /api/leads)
{
  "status": "success",
  "lead_id": 101,
  "credit_score": 742,
  "bre_status": "Eligible",
  "reasons": []
}

## Author
Keshav Sharma