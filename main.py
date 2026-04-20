"""
FastAPI Backend - সাপ্লাই চেইন AI এজেন্ট
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import uvicorn
import os
from dotenv import load_dotenv

from database import DatabaseManager, Inventory, Order, Supplier, engine, SessionLocal
from agents import run_supply_chain_agent
from tools import EmailTool, DatabaseTool, TrackingTool, AnalyticsTool

load_dotenv()

# FastAPI App Setup
app = FastAPI(
    title="সাপ্লাই চেইন AI এজেন্ট API",
    description="AI-চালিত সাপ্লাই চেইন ম্যানেজমেন্ট সিস্টেম",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Database Initialization
DatabaseManager.init_db()

# Tools
email_tool = EmailTool()
db_tool = DatabaseTool()
tracking_tool = TrackingTool()
analytics_tool = AnalyticsTool()


# ============================================
# Pydantic Models
# ============================================

class InventoryCreate(BaseModel):
    product_name: str
    sku: str
    quantity: int
    reorder_level: int
    price: float
    supplier_id: str


class InventoryUpdate(BaseModel):
    quantity_change: int
    notes: str = ""


class OrderCreate(BaseModel):
    order_number: str
    supplier_id: str
    product_sku: str
    quantity: int
    unit_price: float
    expected_delivery: datetime


class OrderStatusUpdate(BaseModel):
    status: str  # pending, confirmed, shipped, delivered


class SupplierCreate(BaseModel):
    supplier_id: str
    supplier_name: str
    email: str
    phone: str
    location: str
    lead_time_days: int = 5


# ============================================
# Dependency
# ============================================

def get_db():
    """ডাটাবেস সেশন পান"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============================================
# Health Check
# ============================================

@app.get("/", tags=["Health"])
@app.get("/health", tags=["Health"])
def health_check():
    """হেলথ চেক এন্ডপয়েন্ট"""
    return {
        "status": "✅ সুস্থ",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }


# ============================================
# Inventory Endpoints
# ============================================

@app.get("/api/inventory", tags=["Inventory"])
def get_all_inventory(db: Session = Depends(get_db)):
    """সব ইনভেন্টরি আইটেম পান"""
    items = DatabaseManager.get_all_inventory(db)
    return {
        "count": len(items),
        "items": [item.to_dict() for item in items]
    }


@app.get("/api/inventory/{sku}", tags=["Inventory"])
def get_inventory_by_sku(sku: str, db: Session = Depends(get_db)):
    """SKU দিয়ে ইনভেন্টরি পান"""
    item = DatabaseManager.get_inventory(db, sku)
    if not item:
        raise HTTPException(status_code=404, detail="ইনভেন্টরি আইটেম পাওয়া যায়নি")
    return item.to_dict()


@app.post("/api/inventory", tags=["Inventory"])
def create_inventory(inventory: InventoryCreate, db: Session = Depends(get_db)):
    """নতুন ইনভেন্টরি আইটেম তৈরি করুন"""
    existing = DatabaseManager.get_inventory(db, inventory.sku)
    if existing:
        raise HTTPException(status_code=400, detail="SKU ইতিমধ্যে বিদ্যমান")
    
    item = DatabaseManager.add_inventory(
        db, inventory.product_name, inventory.sku,
        inventory.quantity, inventory.reorder_level,
        inventory.price, inventory.supplier_id
    )
    return {"success": True, "item": item.to_dict()}


@app.patch("/api/inventory/{sku}", tags=["Inventory"])
def update_inventory(sku: str, update: InventoryUpdate, 
                     db: Session = Depends(get_db)):
    """ইনভেন্টরি আপডেট করুন"""
    item = DatabaseManager.update_inventory(
        db, sku, update.quantity_change, update.notes
    )
    if not item:
        raise HTTPException(status_code=404, detail="ইনভেন্টরি আইটেম পাওয়া যায়নি")
    return {"success": True, "item": item.to_dict()}


@app.get("/api/inventory/low-stock", tags=["Inventory"])
def get_low_stock_items(db: Session = Depends(get_db)):
    """কম স্টক আইটেম পান"""
    items = DatabaseManager.get_low_stock_items(db)
    return {
        "count": len(items),
        "items": [item.to_dict() for item in items]
    }


# ============================================
# Orders Endpoints
# ============================================

@app.get("/api/orders", tags=["Orders"])
def get_all_orders(status: Optional[str] = None, 
                   db: Session = Depends(get_db)):
    """সব অর্ডার পান"""
    orders = DatabaseManager.get_all_orders(db, status)
    return {
        "count": len(orders),
        "orders": [order.to_dict() for order in orders]
    }


@app.get("/api/orders/{order_id}", tags=["Orders"])
def get_order(order_id: int, db: Session = Depends(get_db)):
    """নির্দিষ্ট অর্ডার পান"""
    order = DatabaseManager.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="অর্ডার পাওয়া যায়নি")
    return order.to_dict()


@app.post("/api/orders", tags=["Orders"])
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    """নতুন অর্ডার তৈরি করুন"""
    new_order = DatabaseManager.create_order(
        db, order.order_number, order.supplier_id,
        order.product_sku, order.quantity,
        order.unit_price, order.expected_delivery
    )
    
    # সাপ্লায়ারকে ইমেইল পাঠান
    supplier = DatabaseManager.get_supplier(db, order.supplier_id)
    if supplier:
        email_tool.send_order_confirmation(supplier.email, new_order)
    
    return {"success": True, "order": new_order.to_dict()}


@app.patch("/api/orders/{order_id}", tags=["Orders"])
def update_order_status(order_id: int, update: OrderStatusUpdate,
                        db: Session = Depends(get_db)):
    """অর্ডার স্ট্যাটাস আপডেট করুন"""
    order = DatabaseManager.update_order_status(db, order_id, update.status)
    if not order:
        raise HTTPException(status_code=404, detail="অর্ডার পাওয়া যায়নি")
    return {"success": True, "order": order.to_dict()}


# ============================================
# Suppliers Endpoints
# ============================================

@app.get("/api/suppliers", tags=["Suppliers"])
def get_all_suppliers(db: Session = Depends(get_db)):
    """সব সাপ্লায়ার পান"""
    suppliers = DatabaseManager.get_all_suppliers(db)
    return {
        "count": len(suppliers),
        "suppliers": [supplier.to_dict() for supplier in suppliers]
    }


@app.get("/api/suppliers/{supplier_id}", tags=["Suppliers"])
def get_supplier(supplier_id: str, db: Session = Depends(get_db)):
    """সাপ্লায়ার পান"""
    supplier = DatabaseManager.get_supplier(db, supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="সাপ্লায়ার পাওয়া যায়নি")
    return supplier.to_dict()


@app.post("/api/suppliers", tags=["Suppliers"])
def create_supplier(supplier: SupplierCreate, db: Session = Depends(get_db)):
    """নতুন সাপ্লায়ার যোগ করুন"""
    new_supplier = DatabaseManager.add_supplier(
        db, supplier.supplier_id, supplier.supplier_name,
        supplier.email, supplier.phone, supplier.location,
        supplier.lead_time_days
    )
    return {"success": True, "supplier": new_supplier.to_dict()}


# ============================================
# AI Agents Endpoints
# ============================================

@app.post("/api/agents/run", tags=["AI Agents"])
def run_agents(operation_type: str = "daily", 
               db: Session = Depends(get_db)):
    """সাপ্লাই চেইন এজেন্ট চালান"""
    try:
        result = run_supply_chain_agent(db, operation_type)
        return {
            "success": True,
            "operation": operation_type,
            "result": result,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# Analytics Endpoints
# ============================================

@app.get("/api/analytics/inventory", tags=["Analytics"])
def get_inventory_analytics(db: Session = Depends(get_db)):
    """ইনভেন্টরি বিশ্লেষণ পান"""
    return analytics_tool.get_inventory_analytics(db)


@app.get("/api/analytics/suppliers", tags=["Analytics"])
def get_supplier_analytics(db: Session = Depends(get_db)):
    """সাপ্লায়ার বিশ্লেষণ পান"""
    return analytics_tool.get_supplier_analytics(db)


@app.get("/api/analytics/orders", tags=["Analytics"])
def get_order_analytics(db: Session = Depends(get_db)):
    """অর্ডার বিশ্লেষণ পান"""
    return db_tool.get_order_status(db)


@app.get("/api/analytics/dashboard", tags=["Analytics"])
def get_dashboard_data(db: Session = Depends(get_db)):
    """ড্যাশবোর্ড ডেটা পান"""
    return {
        "inventory": db_tool.get_inventory_status(db),
        "orders": db_tool.get_order_status(db),
        "timestamp": datetime.utcnow().isoformat()
    }


# ============================================
# Tracking Endpoints
# ============================================

@app.get("/api/tracking/{order_number}", tags=["Tracking"])
def track_order(order_number: str, db: Session = Depends(get_db)):
    """অর্ডার ট্র্যাক করুন"""
    return tracking_tool.get_order_tracking(db, order_number)


@app.get("/api/tracking/delayed", tags=["Tracking"])
def get_delayed_orders(db: Session = Depends(get_db)):
    """বিলম্বিত অর্ডার পান"""
    delayed = tracking_tool.get_delayed_orders(db)
    return {
        "count": len(delayed),
        "delayed_orders": delayed
    }


# ============================================
# Recommendations Endpoints
# ============================================

@app.get("/api/recommendations/reorder/{sku}", tags=["Recommendations"])
def get_reorder_recommendation(sku: str, db: Session = Depends(get_db)):
    """পুনরায় অর্ডার সুপারিশ পান"""
    return db_tool.suggest_reorder_quantity(db, sku)


# ============================================
# Sample Data Endpoints
# ============================================

@app.post("/api/sample-data/init", tags=["Sample Data"])
def initialize_sample_data(db: Session = Depends(get_db)):
    """স্যাম্পল ডেটা সংযোজন করুন (ডেভেলপমেন্টের জন্য)"""
    try:
        # সাপ্লায়ার যোগ করুন
        suppliers = [
            ("SUP001", "টেক সাপ্লাইস", "tech@supplier.com", "123456", "ঢাকা", 3),
            ("SUP002", "ইলেক্ট্রনিক্স ইন্ডাস্ট্রি", "elec@supplier.com", "789012", "চট্টগ্রাম", 5),
        ]
        
        for sup in suppliers:
            existing = DatabaseManager.get_supplier(db, sup[0])
            if not existing:
                DatabaseManager.add_supplier(db, *sup)
        
        # ইনভেন্টরি যোগ করুন
        inventory_items = [
            ("ল্যাপটপ", "LAP001", 10, 5, 50000, "SUP001"),
            ("মাউস", "MOU001", 100, 20, 500, "SUP001"),
            ("কীবোর্ড", "KEY001", 50, 10, 1000, "SUP002"),
        ]
        
        for item in inventory_items:
            existing = DatabaseManager.get_inventory(db, item[1])
            if not existing:
                DatabaseManager.add_inventory(db, *item)
        
        return {"success": True, "message": "স্যাম্পল ডেটা সংযোজিত হয়েছে"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# Error Handlers
# ============================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """HTTP ত্রুটি হ্যান্ডলার"""
    return {
        "error": True,
        "detail": exc.detail,
        "status_code": exc.status_code
    }


# ============================================
# Startup Event
# ============================================

@app.on_event("startup")
async def startup_event():
    """স্টার্টআপ ইভেন্ট"""
    print("🚀 সাপ্লাই চেইন AI এজেন্ট API শুরু হচ্ছে...")
    DatabaseManager.init_db()
    print("✅ ডেটাবেস প্রস্তুত")


# ============================================
# Main
# ============================================

if __name__ == "__main__":
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", 8000))
    reload = os.getenv("API_RELOAD", "true").lower() == "true"

    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload
    )
