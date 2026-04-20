"""
Database Models এবং Operations
SQLAlchemy দিয়ে তৈরি
"""

from datetime import datetime
from typing import List, Optional
from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os
from dotenv import load_dotenv

load_dotenv()

# Database URL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///supply_chain.db")
DATABASE_ECHO = os.getenv("DATABASE_ECHO", "False").lower() == "true"

# SQLAlchemy Setup
engine = create_engine(DATABASE_URL, echo=DATABASE_ECHO, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# ============================================
# Models
# ============================================

class Inventory(Base):
    """ইনভেন্টরি মডেল"""
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(255), index=True)
    sku = Column(String(100), unique=True, index=True)
    quantity = Column(Integer, default=0)
    reorder_level = Column(Integer, default=10)
    price = Column(Float, default=0.0)
    supplier_id = Column(String(100))
    last_updated = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    def to_dict(self):
        return {
            "id": self.id,
            "product_name": self.product_name,
            "sku": self.sku,
            "quantity": self.quantity,
            "reorder_level": self.reorder_level,
            "price": self.price,
            "supplier_id": self.supplier_id,
            "last_updated": self.last_updated.isoformat(),
            "is_active": self.is_active
        }


class Order(Base):
    """অর্ডার মডেল"""
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(100), unique=True, index=True)
    supplier_id = Column(String(100), index=True)
    product_sku = Column(String(100), index=True)
    quantity = Column(Integer)
    unit_price = Column(Float)
    total_price = Column(Float)
    order_date = Column(DateTime, default=datetime.utcnow)
    expected_delivery = Column(DateTime)
    status = Column(String(50), default="pending")  # pending, confirmed, shipped, delivered
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "order_number": self.order_number,
            "supplier_id": self.supplier_id,
            "product_sku": self.product_sku,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "total_price": self.total_price,
            "order_date": self.order_date.isoformat(),
            "expected_delivery": self.expected_delivery.isoformat() if self.expected_delivery else None,
            "status": self.status,
            "created_at": self.created_at.isoformat()
        }


class Supplier(Base):
    """সাপ্লায়ার মডেল"""
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    supplier_id = Column(String(100), unique=True, index=True)
    supplier_name = Column(String(255))
    email = Column(String(255))
    phone = Column(String(20))
    location = Column(String(255))
    lead_time_days = Column(Integer, default=5)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "supplier_id": self.supplier_id,
            "supplier_name": self.supplier_name,
            "email": self.email,
            "phone": self.phone,
            "location": self.location,
            "lead_time_days": self.lead_time_days,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat()
        }


class StockMovement(Base):
    """স্টক মুভমেন্ট লগ"""
    __tablename__ = "stock_movements"

    id = Column(Integer, primary_key=True, index=True)
    product_sku = Column(String(100), index=True)
    movement_type = Column(String(50))  # in, out, adjustment
    quantity = Column(Integer)
    reference_id = Column(String(100))  # order_id বা অন্য রেফারেন্স
    notes = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "product_sku": self.product_sku,
            "movement_type": self.movement_type,
            "quantity": self.quantity,
            "reference_id": self.reference_id,
            "notes": self.notes,
            "created_at": self.created_at.isoformat()
        }


# ============================================
# Database Operations
# ============================================

class DatabaseManager:
    """ডেটাবেস অপারেশন ম্যানেজার"""

    @staticmethod
    def init_db():
        """ডেটাবেস টেবিল তৈরি করুন"""
        Base.metadata.create_all(bind=engine)
        print("✅ ডেটাবেস ইনিশিয়ালাইজ করা হয়েছে")

    @staticmethod
    def get_db():
        """সেশন পান"""
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    # ============ Inventory Operations ============

    @staticmethod
    def add_inventory(db: Session, product_name: str, sku: str, quantity: int, 
                      reorder_level: int, price: float, supplier_id: str):
        """নতুন প্রোডাক্ট যোগ করুন"""
        inventory = Inventory(
            product_name=product_name,
            sku=sku,
            quantity=quantity,
            reorder_level=reorder_level,
            price=price,
            supplier_id=supplier_id
        )
        db.add(inventory)
        db.commit()
        db.refresh(inventory)
        return inventory

    @staticmethod
    def get_inventory(db: Session, sku: str) -> Optional[Inventory]:
        """SKU দিয়ে ইনভেন্টরি পান"""
        return db.query(Inventory).filter(Inventory.sku == sku).first()

    @staticmethod
    def get_all_inventory(db: Session) -> List[Inventory]:
        """সব ইনভেন্টরি পান"""
        return db.query(Inventory).filter(Inventory.is_active == True).all()

    @staticmethod
    def get_low_stock_items(db: Session) -> List[Inventory]:
        """কম স্টক আইটেম পান"""
        return db.query(Inventory).filter(
            Inventory.quantity <= Inventory.reorder_level,
            Inventory.is_active == True
        ).all()

    @staticmethod
    def update_inventory(db: Session, sku: str, quantity_change: int, notes: str = ""):
        """ইনভেন্টরি আপডেট করুন"""
        inventory = DatabaseManager.get_inventory(db, sku)
        if inventory:
            inventory.quantity += quantity_change
            inventory.last_updated = datetime.utcnow()
            db.commit()
            db.refresh(inventory)
            
            # স্টক মুভমেন্ট লগ করুন
            DatabaseManager.add_stock_movement(
                db, sku, "in" if quantity_change > 0 else "out", 
                abs(quantity_change), notes
            )
            return inventory
        return None

    # ============ Order Operations ============

    @staticmethod
    def create_order(db: Session, order_number: str, supplier_id: str, 
                     product_sku: str, quantity: int, unit_price: float, 
                     expected_delivery):
        """নতুন অর্ডার তৈরি করুন"""
        order = Order(
            order_number=order_number,
            supplier_id=supplier_id,
            product_sku=product_sku,
            quantity=quantity,
            unit_price=unit_price,
            total_price=quantity * unit_price,
            expected_delivery=expected_delivery,
            status="pending"
        )
        db.add(order)
        db.commit()
        db.refresh(order)
        return order

    @staticmethod
    def get_order(db: Session, order_id: int) -> Optional[Order]:
        """অর্ডার পান"""
        return db.query(Order).filter(Order.id == order_id).first()

    @staticmethod
    def get_all_orders(db: Session, status: str = None) -> List[Order]:
        """সব অর্ডার পান"""
        query = db.query(Order)
        if status:
            query = query.filter(Order.status == status)
        return query.all()

    @staticmethod
    def update_order_status(db: Session, order_id: int, status: str):
        """অর্ডার স্ট্যাটাস আপডেট করুন"""
        order = DatabaseManager.get_order(db, order_id)
        if order:
            order.status = status
            db.commit()
            db.refresh(order)
            return order
        return None

    # ============ Supplier Operations ============

    @staticmethod
    def add_supplier(db: Session, supplier_id: str, supplier_name: str,
                     email: str, phone: str, location: str, lead_time_days: int = 5):
        """সাপ্লায়ার যোগ করুন"""
        supplier = Supplier(
            supplier_id=supplier_id,
            supplier_name=supplier_name,
            email=email,
            phone=phone,
            location=location,
            lead_time_days=lead_time_days
        )
        db.add(supplier)
        db.commit()
        db.refresh(supplier)
        return supplier

    @staticmethod
    def get_supplier(db: Session, supplier_id: str) -> Optional[Supplier]:
        """সাপ্লায়ার পান"""
        return db.query(Supplier).filter(Supplier.supplier_id == supplier_id).first()

    @staticmethod
    def get_all_suppliers(db: Session) -> List[Supplier]:
        """সব সাপ্লায়ার পান"""
        return db.query(Supplier).filter(Supplier.is_active == True).all()

    # ============ Stock Movement Operations ============

    @staticmethod
    def add_stock_movement(db: Session, product_sku: str, movement_type: str,
                          quantity: int, reference_id: str = "", notes: str = ""):
        """স্টক মুভমেন্ট লগ করুন"""
        movement = StockMovement(
            product_sku=product_sku,
            movement_type=movement_type,
            quantity=quantity,
            reference_id=reference_id,
            notes=notes
        )
        db.add(movement)
        db.commit()
        db.refresh(movement)
        return movement

    @staticmethod
    def get_stock_movements(db: Session, product_sku: str) -> List[StockMovement]:
        """পণ্যের স্টক মুভমেন্ট হিস্ট্রি পান"""
        return db.query(StockMovement).filter(
            StockMovement.product_sku == product_sku
        ).order_by(StockMovement.created_at.desc()).all()


# ডেটাবেস ইনিশিয়ালাইজ করুন
if __name__ == "__main__":
    DatabaseManager.init_db()
