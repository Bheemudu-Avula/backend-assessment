import requests
from models.customer import Customer

URL="http://mock-server:5000/api/customers"

def ingest(db):
    page=1
    total=0
    while True:
        res=requests.get(URL, params={"page":page,"limit":10}).json()["data"]
        if not res: break
        for c in res:
            db.merge(Customer(**c))
            total+=1
        db.commit()
        page+=1
    return total
