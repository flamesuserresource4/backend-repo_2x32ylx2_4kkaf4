import os
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
from pydantic import BaseModel

from database import db, create_document, get_documents
from schemas import Laptop

app = FastAPI(title="Laptop Store API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Laptop Store API is running"}

@app.get("/schema")
def get_schema_info():
    # Expose available schemas for tooling/introspection
    return {"collections": ["user", "product", "laptop"]}

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = os.getenv("DATABASE_NAME") or "Unknown"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    return response

# ----- Laptop endpoints -----

class CreateLaptopRequest(Laptop):
    pass

@app.post("/api/laptops")
def create_laptop(payload: CreateLaptopRequest):
    try:
        inserted_id = create_document("laptop", payload)
        return {"id": inserted_id, "message": "Laptop created"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/laptops")
def list_laptops(
    brand: Optional[str] = Query(default=None, description="Filter by brand"),
    min_price: Optional[float] = Query(default=None, ge=0),
    max_price: Optional[float] = Query(default=None, ge=0),
    q: Optional[str] = Query(default=None, description="Search by name contains"),
    limit: int = Query(default=50, ge=1, le=200)
):
    try:
        filter_query = {}
        if brand:
            filter_query["brand"] = {"$regex": f"^{brand}$", "$options": "i"}
        if min_price is not None or max_price is not None:
            price_filter = {}
            if min_price is not None:
                price_filter["$gte"] = float(min_price)
            if max_price is not None:
                price_filter["$lte"] = float(max_price)
            filter_query["price"] = price_filter
        if q:
            filter_query["name"] = {"$regex": q, "$options": "i"}

        docs = get_documents("laptop", filter_query, limit)
        # Convert ObjectId to str safely
        for d in docs:
            if "_id" in d:
                d["id"] = str(d.pop("_id"))
        return {"items": docs, "count": len(docs)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/brands")
def get_brands():
    try:
        pipeline = [
            {"$group": {"_id": "$brand", "count": {"$sum": 1}}},
            {"$sort": {"_id": 1}}
        ]
        results = list(db["laptop"].aggregate(pipeline)) if db is not None else []
        brands = [
            {"name": r.get("_id"), "count": r.get("count", 0)} for r in results if r.get("_id")
        ]
        return {"items": brands}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
