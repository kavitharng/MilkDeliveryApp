from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Vendor, Customer

app = FastAPI()

static_dir = Path(__file__).resolve().parents[2] / "frontend"
app.mount("/static", StaticFiles(directory=static_dir), name="static")


class CustomerCreate(BaseModel):
    name: str


class VendorCreate(BaseModel):
    name: str


class CustomerSubscription(BaseModel):
    vendor_id: int


@app.get("/")
def home():
    indexPage = Path(__file__).resolve().parents[2] / "frontend" / "index.html"
    return FileResponse(path=indexPage, media_type="text/html")


@app.get("/api/vendors/{vendor_id}")
def get_vendor(vendor_id: int, db: Session = Depends(get_db)):
    vendor = db.get(Vendor, vendor_id)
    if vendor is None:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return {"id": vendor.id, "name": vendor.name, "customers": vendor.customers}


@app.get("/api/customers/{customer_id}")
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.get(Customer, customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"id": customer.id, "name": customer.name, "vendors": customer.vendors}


@app.post("/api/vendors")
def create_vendor(vendor_data: VendorCreate, db: Session = Depends(get_db)):
    vendor = Vendor(name=vendor_data.name)
    db.add(vendor)
    db.commit()
    db.refresh(vendor)
    return vendor


@app.post("/api/customers")
def create_customer(customer_data: CustomerCreate, db: Session = Depends(get_db)):
    customer = Customer(name=customer_data.name)
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


@app.post("/api/customers/{customer_id}/subscription")
def create_subscription(
    customer_id: int, vendor_data: CustomerSubscription, db: Session = Depends(get_db)
):
    customer = db.get(Customer, customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    vendor = db.get(Vendor, vendor_data.vendor_id)
    if vendor is None:
        raise HTTPException(status_code=404, detail="Vendor not found")
    if vendor in customer.vendors:
        raise HTTPException(
            status_code=400, detail="Customer already has subscription with this Vendor"
        )
    customer.vendors.append(vendor)
    db.commit()
    db.refresh(customer)
    return {"id": customer.id, "name": customer.name, "vendors": customer.vendors}


@app.delete("/api/customers/{customer_id}/subscription/{vendor_id}")
def delete_subscription(
    customer_id: int, vendor_id: int, db: Session = Depends(get_db)
):
    customer = db.get(Customer, customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    vendor = db.get(Vendor, vendor_id)
    if vendor is None:
        raise HTTPException(status_code=404, detail="Vendor not found")
    if vendor not in customer.vendors:
        raise HTTPException(
            status_code=400,
            detail="Customer does not have subscription with this Vendor",
        )
    customer.vendors.remove(vendor)
    db.commit()
    db.refresh(customer)
    return {"id": customer.id, "name": customer.name, "vendors": customer.vendors}
