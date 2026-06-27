from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyResponse

router = APIRouter(
    prefix="/companies",
    tags=["Companies"]
)


# ---------------------------------
# Create Company
# ---------------------------------
@router.post("/", response_model=CompanyResponse)
def create_company(
    company: CompanyCreate,
    db: Session = Depends(get_db)
):

    existing = db.query(Company).filter(
        Company.name == company.name
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Company already exists"
        )

    new_company = Company(
        name=company.name,
        description=company.description,
        industry=company.industry
    )

    db.add(new_company)
    db.commit()
    db.refresh(new_company)

    return new_company


# ---------------------------------
# Get All Companies
# ---------------------------------
@router.get("/", response_model=list[CompanyResponse])
def get_companies(
    db: Session = Depends(get_db)
):

    return db.query(Company).all()


# ---------------------------------
# Get Company By ID
# ---------------------------------
@router.get("/{company_id}", response_model=CompanyResponse)
def get_company(
    company_id: int,
    db: Session = Depends(get_db)
):

    company = db.query(Company).filter(
        Company.id == company_id
    ).first()

    if not company:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    return company


# ---------------------------------
# Update Company
# ---------------------------------
@router.put("/{company_id}", response_model=CompanyResponse)
def update_company(
    company_id: int,
    data: CompanyCreate,
    db: Session = Depends(get_db)
):

    company = db.query(Company).filter(
        Company.id == company_id
    ).first()

    if not company:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    company.name = data.name
    company.description = data.description
    company.industry = data.industry

    db.commit()
    db.refresh(company)

    return company


# ---------------------------------
# Delete Company
# ---------------------------------
@router.delete("/{company_id}")
def delete_company(
    company_id: int,
    db: Session = Depends(get_db)
):

    company = db.query(Company).filter(
        Company.id == company_id
    ).first()

    if not company:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    db.delete(company)
    db.commit()

    return {
        "message": "Company deleted successfully"
    }