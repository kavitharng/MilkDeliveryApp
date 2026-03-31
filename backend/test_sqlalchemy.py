from app.database import SessionLocal
from app.models import Customer, Vendor


def main():
    db = SessionLocal()

    try:
        vendor = Vendor(name="Anand")
        db.add(vendor)
        db.commit()
        db.refresh(vendor)
        print(f"Created vendor: {vendor.id} - {vendor.name}")

        customer = Customer(name="Anjali")
        db.add(customer)
        db.commit()
        db.refresh(customer)
        print(f"Created customer: {customer.id} - {customer.name}")

        vendor.customers.append(customer)
        db.commit()
        print(f"Created subscription: vendor {vendor.id} <-> customer {customer.id}")

        vendor.customers.remove(customer)
        db.commit()
        print("Deleted subscription only")

        vendor.customers.append(customer)
        db.commit()

        db.delete(vendor)
        db.commit()
        print("Deleted vendor (cascaded to subscription)")

        db.delete(customer)
        db.commit()
        print("Deleted customer")

    finally:
        db.close()


if __name__ == "__main__":
    main()
