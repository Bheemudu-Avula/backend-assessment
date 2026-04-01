from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models.customer import Customer
from services.ingestion import ingest
import time

app = FastAPI()


def wait_for_db():
    for i in range(10):
        try:
            Base.metadata.create_all(bind=engine)
            print("Database connected successfully")
            return
        except Exception as e:
            print("DB not ready, retrying...", e)
            time.sleep(3)
    raise Exception("Could not connect to DB after retries")

# Call DB wait function
wait_for_db()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/ingest")
def ingest_api(db: Session = Depends(get_db)):
    count = ingest(db)
    return {"status": "success", "records_processed": count}

@app.get("/api/customers")
def get_customers(page: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    offset = (page - 1) * limit
    data = db.query(Customer).offset(offset).limit(limit).all()
    return data

@app.get("/api/customers/{customer_id}")
def get_customer(customer_id: str, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter_by(customer_id=customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer