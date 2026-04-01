from flask import Flask, jsonify, request
import json, os

app = Flask(__name__)
DATA_FILE = os.path.join(os.path.dirname(__file__), "data/customers.json")

def load_data():
    with open(DATA_FILE) as f:
        return json.load(f)

@app.get("/api/customers")
def get_customers():
    page = int(request.args.get("page",1))
    limit = int(request.args.get("limit",10))
    data = load_data()
    start = (page-1)*limit
    end = start+limit
    return {"data": data[start:end], "total": len(data), "page": page, "limit": limit}

@app.get("/api/customers/<cid>")
def get_one(cid):
    for c in load_data():
        if c["customer_id"] == cid:
            return c
    return {"error":"not found"},404

@app.get("/api/health")
def health():
    return {"status":"ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
