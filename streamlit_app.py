"""
Streamlit Frontend - সাপ্লাই চেইন AI এজেন্ট ড্যাশবোর্ড
"""

import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px

# Page Configuration
st.set_page_config(
    page_title="সাপ্লাই চেইন AI এজেন্ট",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Styling
st.markdown("""
<style>
    body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .metric-card { 
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .status-badge {
        display: inline-block;
        padding: 5px 10px;
        border-radius: 5px;
        font-weight: bold;
        font-size: 12px;
    }
</style>
""", unsafe_allow_html=True)

# API Configuration
API_BASE_URL = "http://localhost:8000"

# ============================================
# Helper Functions
# ============================================

def make_api_call(endpoint: str, method: str = "GET", data=None):
    """API কল করুন"""
    try:
        url = f"{API_BASE_URL}{endpoint}"
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        elif method == "PATCH":
            response = requests.patch(url, json=data)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"❌ API ত্রুটি: {response.status_code}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("❌ API সার্ভার সংযোগ করতে পারছি না। FastAPI চলছে নিশ্চিত করুন।")
        return None
    except Exception as e:
        st.error(f"❌ ত্রুটি: {str(e)}")
        return None


def status_badge(status: str):
    """স্ট্যাটাস ব্যাজ তৈরি করুন"""
    colors = {
        "pending": "🟡 পেন্ডিং",
        "confirmed": "🟦 নিশ্চিত",
        "shipped": "🟩 পাঠানো",
        "delivered": "✅ ডেলিভারড"
    }
    return colors.get(status, status)


# ============================================
# Main Layout
# ============================================

st.title("📦 সাপ্লাই চেইন AI এজেন্ট ড্যাশবোর্ড")
st.subheader("রিয়েল-টাইম ইনভেন্টরি এবং অর্ডার ম্যানেজমেন্ট সিস্টেম")

# Sidebar Navigation
st.sidebar.title("🧭 নেভিগেশন")
selected_page = st.sidebar.radio(
    "পৃষ্ঠা নির্বাচন করুন",
    ["📊 ড্যাশবোর্ড", "📦 ইনভেন্টরি", "📋 অর্ডার", "👥 সাপ্লায়ার", "🤖 এআই এজেন্ট", "📈 বিশ্লেষণ"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**সিস্টেম তথ্য**")
health = make_api_call("/health")
if health:
    st.sidebar.success(f"✅ সার্ভার: সুস্থ")


# ============================================
# Dashboard Page
# ============================================

if selected_page == "📊 ড্যাশবোর্ড":
    st.header("📊 ড্যাশবোর্ড ওভারভিউ")
    
    # Get Dashboard Data
    dashboard_data = make_api_call("/api/analytics/dashboard")
    
    if dashboard_data:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "📦 মোট আইটেম",
                dashboard_data['inventory'].get('total_items', 0)
            )
        
        with col2:
            st.metric(
                "⚠️ কম স্টক",
                dashboard_data['inventory'].get('low_stock_count', 0)
            )
        
        with col3:
            st.metric(
                "💰 ইনভেন্টরি মূল্য",
                f"${dashboard_data['inventory'].get('total_inventory_value', 0):.2f}"
            )
        
        with col4:
            pending_orders = dashboard_data['orders'].get('pending', 0)
            st.metric(
                "📥 পেন্ডিং অর্ডার",
                pending_orders,
                delta=f"{dashboard_data['orders'].get('total', 0)} মোট"
            )
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Order Status Distribution
            orders = dashboard_data['orders']
            order_status = pd.DataFrame({
                'স্ট্যাটাস': ['পেন্ডিং', 'নিশ্চিত', 'পাঠানো', 'ডেলিভারড'],
                'সংখ্যা': [orders.get('pending', 0), orders.get('confirmed', 0), 
                         orders.get('shipped', 0), orders.get('delivered', 0)]
            })
            
            fig = px.pie(order_status, values='সংখ্যা', names='স্ট্যাটাস',
                        title="📊 অর্ডার স্ট্যাটাস বিতরণ")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Inventory Health
            inventory_health = pd.DataFrame({
                'ক্যাটাগরি': ['সুস্থ', 'কম স্টক'],
                'সংখ্যা': [
                    dashboard_data['inventory'].get('total_items', 0) - 
                    dashboard_data['inventory'].get('low_stock_count', 0),
                    dashboard_data['inventory'].get('low_stock_count', 0)
                ]
            })
            
            fig = px.bar(inventory_health, x='ক্যাটাগরি', y='সংখ্যা',
                        title="📦 ইনভেন্টরি স্বাস্থ্য",
                        color='ক্যাটাগরি',
                        color_discrete_map={'সুস্থ': '#2ecc71', 'কম স্টক': '#e74c3c'})
            st.plotly_chart(fig, use_container_width=True)


# ============================================
# Inventory Page
# ============================================

elif selected_page == "📦 ইনভেন্টরি":
    st.header("📦 ইনভেন্টরি ম্যানেজমেন্ট")
    
    tab1, tab2, tab3 = st.tabs(["📊 দেখুন", "➕ যোগ করুন", "🔄 আপডেট করুন"])
    
    with tab1:
        st.subheader("সমস্ত ইনভেন্টরি আইটেম")
        inventory_data = make_api_call("/api/inventory")
        
        if inventory_data and inventory_data.get('items'):
            df = pd.DataFrame(inventory_data['items'])
            st.dataframe(df, use_container_width=True)
        
        st.markdown("---")
        st.subheader("⚠️ কম স্টক এলার্ট")
        low_stock = make_api_call("/api/inventory/low-stock")
        
        if low_stock and low_stock.get('items'):
            for item in low_stock['items']:
                with st.expander(f"📦 {item['product_name']} - {item['sku']}"):
                    col1, col2, col3 = st.columns(3)
                    col1.metric("বর্তমান স্টক", item['quantity'])
                    col2.metric("পুনরায় অর্ডার স্তর", item['reorder_level'])
                    col3.metric("মূল্য", f"${item['price']:.2f}")
    
    with tab2:
        st.subheader("নতুন আইটেম যোগ করুন")
        
        with st.form("add_inventory_form"):
            product_name = st.text_input("পণ্যের নাম")
            sku = st.text_input("SKU")
            quantity = st.number_input("পরিমাণ", min_value=0)
            reorder_level = st.number_input("পুনরায় অর্ডার স্তর", min_value=0)
            price = st.number_input("মূল্য", min_value=0.0)
            supplier_id = st.text_input("সাপ্লায়ার আইডি")
            
            submitted = st.form_submit_button("✅ যোগ করুন")
            
            if submitted:
                data = {
                    "product_name": product_name,
                    "sku": sku,
                    "quantity": quantity,
                    "reorder_level": reorder_level,
                    "price": price,
                    "supplier_id": supplier_id
                }
                result = make_api_call("/api/inventory", method="POST", data=data)
                if result and result.get('success'):
                    st.success("✅ আইটেম সফলভাবে যোগ করা হয়েছে")
    
    with tab3:
        st.subheader("ইনভেন্টরি আপডেট করুন")
        
        with st.form("update_inventory_form"):
            sku = st.text_input("SKU")
            quantity_change = st.number_input("পরিমাণ পরিবর্তন", value=0)
            notes = st.text_area("নোট", placeholder="পরিবর্তনের কারণ...")
            
            submitted = st.form_submit_button("🔄 আপডেট করুন")
            
            if submitted:
                data = {
                    "quantity_change": quantity_change,
                    "notes": notes
                }
                result = make_api_call(f"/api/inventory/{sku}", method="PATCH", data=data)
                if result and result.get('success'):
                    st.success("✅ ইনভেন্টরি আপডেট করা হয়েছে")


# ============================================
# Orders Page
# ============================================

elif selected_page == "📋 অর্ডার":
    st.header("📋 অর্ডার ম্যানেজমেন্ট")
    
    tab1, tab2, tab3 = st.tabs(["📊 দেখুন", "➕ নতুন অর্ডার", "🔍 ট্র্যাক করুন"])
    
    with tab1:
        st.subheader("সমস্ত অর্ডার")
        status_filter = st.selectbox("স্ট্যাটাস ফিল্টার", ["সব", "pending", "confirmed", "shipped", "delivered"])
        
        endpoint = "/api/orders"
        if status_filter != "সব":
            endpoint += f"?status={status_filter}"
        
        orders_data = make_api_call(endpoint)
        
        if orders_data and orders_data.get('orders'):
            for order in orders_data['orders']:
                with st.expander(f"📦 {order['order_number']}"):
                    col1, col2, col3 = st.columns(3)
                    col1.metric("পণ্য SKU", order['product_sku'])
                    col2.metric("পরিমাণ", order['quantity'])
                    col3.metric("মোট মূল্য", f"${order['total_price']:.2f}")
                    
                    st.write(f"**স্ট্যাটাস:** {status_badge(order['status'])}")
                    st.write(f"**প্রত্যাশিত ডেলিভারি:** {order['expected_delivery']}")
    
    with tab2:
        st.subheader("নতুন অর্ডার তৈরি করুন")
        
        with st.form("create_order_form"):
            order_number = st.text_input("অর্ডার নম্বর")
            supplier_id = st.text_input("সাপ্লায়ার আইডি")
            product_sku = st.text_input("পণ্য SKU")
            quantity = st.number_input("পরিমাণ", min_value=1)
            unit_price = st.number_input("একক মূল্য", min_value=0.0)
            expected_delivery = st.date_input("প্রত্যাশিত ডেলিভারি তারিখ")
            
            submitted = st.form_submit_button("✅ অর্ডার তৈরি করুন")
            
            if submitted:
                data = {
                    "order_number": order_number,
                    "supplier_id": supplier_id,
                    "product_sku": product_sku,
                    "quantity": quantity,
                    "unit_price": unit_price,
                    "expected_delivery": expected_delivery.isoformat() + "T00:00:00"
                }
                result = make_api_call("/api/orders", method="POST", data=data)
                if result and result.get('success'):
                    st.success("✅ অর্ডার সফলভাবে তৈরি করা হয়েছে")
    
    with tab3:
        st.subheader("অর্ডার ট্র্যাক করুন")
        order_number = st.text_input("অর্ডার নম্বর এন্টার করুন")
        
        if st.button("🔍 ট্র্যাক করুন"):
            tracking_data = make_api_call(f"/api/tracking/{order_number}")
            if tracking_data and not tracking_data.get('error'):
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("স্ট্যাটাস", status_badge(tracking_data.get('status')))
                    st.metric("পরিমাণ", tracking_data.get('quantity'))
                with col2:
                    st.metric("মোট মূল্য", f"${tracking_data.get('total_price'):.2f}")
                    st.metric("সরবরাহকারী", tracking_data.get('supplier'))
                
                st.info(f"📅 প্রত্যাশিত ডেলিভারি: {tracking_data.get('expected_delivery')}")


# ============================================
# AI Agents Page
# ============================================

elif selected_page == "🤖 এআই এজেন্ট":
    st.header("🤖 এআই এজেন্ট অটোমেশন")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("▶️ দৈনিক অপারেশন চালান", key="run_daily"):
            with st.spinner("দৈনিক অপারেশন চলছে..."):
                result = make_api_call("/api/agents/run?operation_type=daily", method="POST")
                if result and result.get('success'):
                    st.success("✅ দৈনিক অপারেশন সম্পন্ন")
                    st.json(result)
    
    with col2:
        if st.button("▶️ সাপ্তাহিক বিশ্লেষণ চালান", key="run_weekly"):
            with st.spinner("সাপ্তাহিক বিশ্লেষণ চলছে..."):
                result = make_api_call("/api/agents/run?operation_type=weekly", method="POST")
                if result and result.get('success'):
                    st.success("✅ সাপ্তাহিক বিশ্লেষণ সম্পন্ন")
                    st.json(result)
    
    st.markdown("---")
    st.subheader("📋 এজেন্ট ফিচার")
    
    features = {
        "🗂️ ইনভেন্টরি ম্যানেজার": "স্বয়ংক্রিয়ভাবে কম স্টক সনাক্ত করে এবং পুনরায় অর্ডার সুপারিশ করে",
        "🛒 প্রকিউরমেন্ট বিশেষজ্ঞ": "সেরা দামে স্বয়ংক্রিয়ভাবে অর্ডার প্লেস করে",
        "🚚 লজিস্টিক্স কোঅর্ডিনেটর": "অর্ডার ডেলিভারি ট্র্যাক করে এবং বিলম্ব সামলায়",
        "📊 ডেটা বিশ্লেষক": "ট্রেন্ড বিশ্লেষণ করে এবং অপ্টিমাইজেশন সুপারিশ করে"
    }
    
    for agent, description in features.items():
        st.write(f"**{agent}**: {description}")


# ============================================
# Analytics Page
# ============================================

elif selected_page == "📈 বিশ্লেষণ":
    st.header("📈 বিশ্লেষণ এবং রিপোর্ট")
    
    tab1, tab2 = st.tabs(["📊 ইনভেন্টরি বিশ্লেষণ", "👥 সাপ্লায়ার বিশ্লেষণ"])
    
    with tab1:
        analytics = make_api_call("/api/analytics/inventory")
        
        if analytics:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("মোট আইটেম", analytics.get('total_items', 0))
            
            with col2:
                st.metric(
                    "মোট ইনভেন্টরি মূল্য",
                    f"${analytics.get('total_inventory_value', 0):.2f}"
                )
            
            with col3:
                st.metric(
                    "গড় আইটেম পরিমাণ",
                    f"{analytics.get('average_item_quantity', 0):.0f}"
                )
            
            st.subheader("🏆 উচ্চ মূল্যের আইটেম")
            if analytics.get('high_value_items'):
                df = pd.DataFrame(analytics['high_value_items'])
                st.dataframe(df, use_container_width=True)
    
    with tab2:
        supplier_analytics = make_api_call("/api/analytics/suppliers")
        
        if supplier_analytics:
            st.metric("মোট সাপ্লায়ার", supplier_analytics.get('total_suppliers', 0))
            
            if supplier_analytics.get('suppliers'):
                df = pd.DataFrame(supplier_analytics['suppliers'])
                st.dataframe(df, use_container_width=True)


# ============================================
# Suppliers Page
# ============================================

elif selected_page == "👥 সাপ্লায়ার":
    st.header("👥 সাপ্লায়ার ম্যানেজমেন্ট")
    
    tab1, tab2 = st.tabs(["📊 দেখুন", "➕ যোগ করুন"])
    
    with tab1:
        suppliers = make_api_call("/api/suppliers")
        
        if suppliers and suppliers.get('suppliers'):
            for supplier in suppliers['suppliers']:
                with st.expander(f"👥 {supplier['supplier_name']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**আইডি:** {supplier['supplier_id']}")
                        st.write(f"**ইমেইল:** {supplier['email']}")
                    with col2:
                        st.write(f"**ফোন:** {supplier['phone']}")
                        st.write(f"**লিড টাইম:** {supplier['lead_time_days']} দিন")
    
    with tab2:
        st.subheader("নতুন সাপ্লায়ার যোগ করুন")
        
        with st.form("add_supplier_form"):
            supplier_id = st.text_input("সাপ্লায়ার আইডি")
            supplier_name = st.text_input("সাপ্লায়ারের নাম")
            email = st.text_input("ইমেইল")
            phone = st.text_input("ফোন")
            location = st.text_input("অবস্থান")
            lead_time = st.number_input("লিড টাইম (দিন)", min_value=1)
            
            submitted = st.form_submit_button("✅ সাপ্লায়ার যোগ করুন")
            
            if submitted:
                data = {
                    "supplier_id": supplier_id,
                    "supplier_name": supplier_name,
                    "email": email,
                    "phone": phone,
                    "location": location,
                    "lead_time_days": lead_time
                }
                result = make_api_call("/api/suppliers", method="POST", data=data)
                if result and result.get('success'):
                    st.success("✅ সাপ্লায়ার সফলভাবে যোগ করা হয়েছে")

st.sidebar.markdown("---")
st.sidebar.markdown("**ডেভেলপার তথ্য**")
st.sidebar.info("""
সাপ্লাই চেইন AI এজেন্ট
v1.0.0
""")
