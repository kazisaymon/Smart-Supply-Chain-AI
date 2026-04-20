"""
CrewAI এর জন্য কাস্টম টুলস
Email, Database, Tracking, Analytics ইত্যাদি
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from typing import List, Dict
import json
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from database import DatabaseManager, Inventory, Order, Supplier

load_dotenv()


# ============================================
# Email Tool
# ============================================

class EmailTool:
    """ইমেইল সেন্ডিং টুল"""

    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", 587))
        self.smtp_user = os.getenv("SMTP_USER")
        self.smtp_password = os.getenv("SMTP_PASSWORD")
        self.from_email = os.getenv("SMTP_FROM_EMAIL", self.smtp_user)

    def send_email(self, to_email: str, subject: str, body: str, 
                   html: bool = False) -> bool:
        """ইমেইল পাঠান"""
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = self.from_email
            msg["To"] = to_email

            if html:
                msg.attach(MIMEText(body, "html"))
            else:
                msg.attach(MIMEText(body, "plain"))

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)

            print(f"✅ ইমেইল পাঠানো হয়েছে: {to_email}")
            return True
        except Exception as e:
            print(f"❌ ইমেইল পাঠাতে ব্যর্থ: {str(e)}")
            return False

    def send_low_stock_alert(self, supplier_email: str, 
                             low_stock_items: List[Inventory]) -> bool:
        """কম স্টক এলার্ট পাঠান"""
        html_body = """
        <html>
            <body style="font-family: Arial;">
                <h2>⚠️ কম স্টক এলার্ট</h2>
                <p>নিম্নলিখিত আইটেমগুলি পুনরায় অর্ডার করার প্রয়োজন:</p>
                <table border="1" cellpadding="10">
                    <tr>
                        <th>পণ্য</th>
                        <th>SKU</th>
                        <th>বর্তমান স্টক</th>
                        <th>পুনরায় অর্ডার স্তর</th>
                    </tr>
        """
        
        for item in low_stock_items:
            html_body += f"""
                    <tr>
                        <td>{item.product_name}</td>
                        <td>{item.sku}</td>
                        <td>{item.quantity}</td>
                        <td>{item.reorder_level}</td>
                    </tr>
            """
        
        html_body += """
                </table>
                <p>অবিলম্বে অর্ডার প্লেস করুন।</p>
            </body>
        </html>
        """

        return self.send_email(
            supplier_email,
            "সাপ্লাই চেইন: কম স্টক এলার্ট",
            html_body,
            html=True
        )

    def send_order_confirmation(self, supplier_email: str, order: Order) -> bool:
        """অর্ডার কনফার্মেশন ইমেইল"""
        html_body = f"""
        <html>
            <body style="font-family: Arial;">
                <h2>📦 অর্ডার কনফার্মেশন</h2>
                <p><strong>অর্ডার নম্বর:</strong> {order.order_number}</p>
                <p><strong>পণ্য SKU:</strong> {order.product_sku}</p>
                <p><strong>পরিমাণ:</strong> {order.quantity}</p>
                <p><strong>মোট মূল্য:</strong> ${order.total_price:.2f}</p>
                <p><strong>প্রত্যাশিত ডেলিভারি:</strong> {order.expected_delivery}</p>
                <p>ধন্যবাদ!</p>
            </body>
        </html>
        """

        return self.send_email(
            supplier_email,
            f"অর্ডার কনফার্মেশন: {order.order_number}",
            html_body,
            html=True
        )


# ============================================
# Database Tool
# ============================================

class DatabaseTool:
    """ডেটাবেস অপারেশন টুল"""

    @staticmethod
    def get_inventory_status(db: Session) -> Dict:
        """ইনভেন্টরি স্ট্যাটাস পান"""
        all_items = DatabaseManager.get_all_inventory(db)
        low_stock = DatabaseManager.get_low_stock_items(db)

        total_value = sum(item.quantity * item.price for item in all_items)
        
        return {
            "total_items": len(all_items),
            "low_stock_count": len(low_stock),
            "total_inventory_value": total_value,
            "low_stock_items": [item.to_dict() for item in low_stock]
        }

    @staticmethod
    def get_order_status(db: Session) -> Dict:
        """অর্ডার স্ট্যাটাস রিপোর্ট"""
        pending = len(DatabaseManager.get_all_orders(db, "pending"))
        confirmed = len(DatabaseManager.get_all_orders(db, "confirmed"))
        shipped = len(DatabaseManager.get_all_orders(db, "shipped"))
        delivered = len(DatabaseManager.get_all_orders(db, "delivered"))

        return {
            "pending": pending,
            "confirmed": confirmed,
            "shipped": shipped,
            "delivered": delivered,
            "total": pending + confirmed + shipped + delivered
        }

    @staticmethod
    def suggest_reorder_quantity(db: Session, product_sku: str, 
                                 days_ahead: int = 30) -> Dict:
        """পুনরায় অর্ডার পরিমাণ সুপারিশ করুন"""
        inventory = DatabaseManager.get_inventory(db, product_sku)
        if not inventory:
            return {"error": "পণ্য পাওয়া যায়নি"}

        supplier = DatabaseManager.get_supplier(db, inventory.supplier_id)
        lead_time = supplier.lead_time_days if supplier else 5

        # সরল ক্যালকুলেশন (প্রকৃত ডিমান্ড ফোরকাস্টিং আরও জটিল হতে পারে)
        movements = DatabaseManager.get_stock_movements(db, product_sku)
        
        # গত 30 দিনের গড় দৈনিক ব্যবহার
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        recent_movements = [m for m in movements if m.created_at > thirty_days_ago]
        outgoing = sum(m.quantity for m in recent_movements if m.movement_type == "out")
        daily_usage = outgoing / 30 if outgoing > 0 else 1

        # পুনরায় অর্ডার পয়েন্ট = (দৈনিক ব্যবহার * লিড টাইম) + নিরাপত্তা স্টক
        safety_stock = inventory.reorder_level
        reorder_point = (daily_usage * lead_time) + safety_stock

        # পুনরায় অর্ডার পরিমাণ = দৈনিক ব্যবহার * 30 দিন
        reorder_qty = int(daily_usage * 30)

        return {
            "product_sku": product_sku,
            "current_stock": inventory.quantity,
            "daily_usage": round(daily_usage, 2),
            "reorder_point": round(reorder_point, 2),
            "suggested_reorder_qty": reorder_qty,
            "lead_time_days": lead_time,
            "safety_stock": safety_stock
        }


# ============================================
# Tracking Tool
# ============================================

class TrackingTool:
    """অর্ডার ট্র্যাকিং টুল"""

    @staticmethod
    def get_order_tracking(db: Session, order_number: str) -> Dict:
        """অর্ডার ট্র্যাকিং ইনফরমেশন পান"""
        order = db.query(Order).filter(Order.order_number == order_number).first()
        
        if not order:
            return {"error": "অর্ডার পাওয়া যায়নি"}

        supplier = DatabaseManager.get_supplier(db, order.supplier_id)
        
        return {
            "order_number": order.order_number,
            "status": order.status,
            "product": order.product_sku,
            "quantity": order.quantity,
            "total_price": order.total_price,
            "order_date": order.order_date.isoformat(),
            "expected_delivery": order.expected_delivery.isoformat() if order.expected_delivery else None,
            "days_until_delivery": (order.expected_delivery - datetime.utcnow()).days if order.expected_delivery else None,
            "supplier": supplier.supplier_name if supplier else "Unknown"
        }

    @staticmethod
    def get_delayed_orders(db: Session) -> List[Dict]:
        """বিলম্বিত অর্ডার খুঁজুন"""
        all_orders = DatabaseManager.get_all_orders(db)
        delayed = []

        for order in all_orders:
            if order.status in ["pending", "confirmed", "shipped"]:
                if order.expected_delivery and order.expected_delivery < datetime.utcnow():
                    delayed.append({
                        "order_number": order.order_number,
                        "status": order.status,
                        "expected_delivery": order.expected_delivery.isoformat(),
                        "days_delayed": (datetime.utcnow() - order.expected_delivery).days
                    })

        return delayed


# ============================================
# Analytics Tool
# ============================================

class AnalyticsTool:
    """বিশ্লেষণ এবং রিপোর্টিং টুল"""

    @staticmethod
    def get_inventory_analytics(db: Session) -> Dict:
        """ইনভেন্টরি বিশ্লেষণ"""
        all_items = DatabaseManager.get_all_inventory(db)
        
        if not all_items:
            return {"error": "কোন ইনভেন্টরি আইটেম নেই"}

        total_value = sum(item.quantity * item.price for item in all_items)
        avg_quantity = sum(item.quantity for item in all_items) / len(all_items)
        
        high_value_items = sorted(
            all_items, 
            key=lambda x: x.quantity * x.price, 
            reverse=True
        )[:5]

        return {
            "total_items": len(all_items),
            "total_inventory_value": round(total_value, 2),
            "average_item_quantity": round(avg_quantity, 2),
            "high_value_items": [
                {
                    "sku": item.sku,
                    "product": item.product_name,
                    "quantity": item.quantity,
                    "value": round(item.quantity * item.price, 2)
                } for item in high_value_items
            ]
        }

    @staticmethod
    def get_supplier_analytics(db: Session) -> Dict:
        """সাপ্লায়ার বিশ্লেষণ"""
        suppliers = DatabaseManager.get_all_suppliers(db)
        
        supplier_stats = []
        for supplier in suppliers:
            orders = db.query(Order).filter(Order.supplier_id == supplier.supplier_id).all()
            total_spent = sum(order.total_price for order in orders)
            
            supplier_stats.append({
                "supplier_id": supplier.supplier_id,
                "name": supplier.supplier_name,
                "total_orders": len(orders),
                "total_spent": round(total_spent, 2),
                "lead_time": supplier.lead_time_days
            })

        return {
            "total_suppliers": len(suppliers),
            "suppliers": supplier_stats
        }


# ============================================
# Integration
# ============================================

def get_all_tools():
    """সব টুলস রিটার্ন করুন"""
    return {
        "email": EmailTool(),
        "database": DatabaseTool(),
        "tracking": TrackingTool(),
        "analytics": AnalyticsTool()
    }


if __name__ == "__main__":
    print("✅ টুলস লোড করা হয়েছে")
