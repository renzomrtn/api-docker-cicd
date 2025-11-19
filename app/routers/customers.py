# routers/customers.py
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import Customer as CustomerDB
from ..schemas import Customer, CustomerCreate

router = APIRouter(prefix="/customers", tags=["customers"])

@router.post("/", response_model=Customer)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    #Create a new customer#
    # Check if email already exists
    existing = db.query(CustomerDB).filter(CustomerDB.email == customer.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_customer = CustomerDB(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

@router.get("/", response_model=List[Customer])
def get_customers(db: Session = Depends(get_db)):
    #Get all customers#
    return db.query(CustomerDB).all()

@router.get("/{customer_id}", response_model=Customer)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    #Get a specific customer#
    customer = db.query(CustomerDB).filter(CustomerDB.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.put("/{customer_id}", response_model=Customer)
def update_customer(customer_id: int, customer_update: CustomerCreate, db: Session = Depends(get_db)):
    #Update a customer#
    db_customer = db.query(CustomerDB).filter(CustomerDB.id == customer_id).first()
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    # Check if email is being updated to an existing email
    if db_customer.email != customer_update.email:
        existing = db.query(CustomerDB).filter(CustomerDB.email == customer_update.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
    
    for field, value in customer_update.dict().items():
        setattr(db_customer, field, value)
    
    db.commit()
    db.refresh(db_customer)
    return db_customer

"""