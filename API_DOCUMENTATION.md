# 📚 সাপ্লাই চেইন AI এজেন্ট - API ডকুমেন্টেশন

**Base URL**: `http://localhost:8000` (স্থানীয়) বা `https://your-api-url.com` (প্রোডাকশন)

---

## 🏥 স্বাস্থ্য চেক

### GET /health
API সার্ভারের অবস্থা পরীক্ষা করুন

**Response:**
```json
{
  "status": "✅ সুস্থ",
  "timestamp": "2024-01-15T10:30:00.000Z",
  "version": "1.0.0"
}
```

---

## 📦 ইনভেন্টরি এন্ডপয়েন্ট

### GET /api/inventory
সমস্ত ইনভেন্টরি আইটেম পান

**Response:**
```json
{
  "count": 20,
  "items": [
    {
      "id": 1,
      "product_name": "ল্যাপটপ",
      "sku": "LAP001",
      "quantity": 10,
      "reorder_level": 5,
      "price": 50000.0,
      "supplier_id": "SUP001",
      "last_updated": "2024-01-15T10:00:00",
      "is_active": true
    }
  ]
}
```

---

### GET /api/inventory/{sku}
নির্দিষ্ট ইনভেন্টরি আইটেম পান

**Example:** `GET /api/inventory/LAP001`

**Response:**
```json
{
  "id": 1,
  "product_name": "ল্যাপটপ",
  "sku": "LAP001",
  "quantity": 10,
  "reorder_level": 5,
  "price": 50000.0,
  "supplier_id": "SUP001",
  "last_updated": "2024-01-15T10:00:00",
  "is_active": true
}
```

---

### POST /api/inventory
নতুন ইনভেন্টরি আইটেম তৈরি করুন

**Request Body:**
```json
{
  "product_name": "ট্যাবলেট",
  "sku": "TAB001",
  "quantity": 20,
  "reorder_level": 5,
  "price": 30000.0,
  "supplier_id": "SUP001"
}
```

**Response:**
```json
{
  "success": true,
  "item": {
    "id": 21,
    "product_name": "ট্যাবলেট",
    "sku": "TAB001",
    "quantity": 20,
    "reorder_level": 5,
    "price": 30000.0,
    "supplier_id": "SUP001",
    "last_updated": "2024-01-15T10:30:00",
    "is_active": true
  }
}
```

---

### PATCH /api/inventory/{sku}
ইনভেন্টরি আইটেম আপডেট করুন

**Example:** `PATCH /api/inventory/LAP001`

**Request Body:**
```json
{
  "quantity_change": 5,
  "notes": "নতুন স্টক গ্রহণ"
}
```

**Response:**
```json
{
  "success": true,
  "item": {
    "id": 1,
    "product_name": "ল্যাপটপ",
    "sku": "LAP001",
    "quantity": 15,  // Updated
    "reorder_level": 5,
    "price": 50000.0,
    "supplier_id": "SUP001",
    "last_updated": "2024-01-15T10:45:00",
    "is_active": true
  }
}
```

---

### GET /api/inventory/low-stock
কম স্টক আইটেম পান (সতর্কতা)

**Response:**
```json
{
  "count": 3,
  "items": [
    {
      "id": 14,
      "product_name": "প্রসেসর",
      "sku": "CPU001",
      "quantity": 1,
      "reorder_level": 1,
      "price": 25000.0,
      "supplier_id": "SUP001",
      "last_updated": "2024-01-15T10:00:00",
      "is_active": true
    }
  ]
}
```

---

## 📋 অর্ডার এন্ডপয়েন্ট

### GET /api/orders
সমস্ত অর্ডার পান (অপশনাল: স্ট্যাটাস ফিল্টার)

**Query Parameters:**
- `status` (optional): "pending", "confirmed", "shipped", "delivered"

**Example:** `GET /api/orders?status=pending`

**Response:**
```json
{
  "count": 5,
  "orders": [
    {
      "id": 1,
      "order_number": "ORD001",
      "supplier_id": "SUP001",
      "product_sku": "LAP001",
      "quantity": 10,
      "unit_price": 50000.0,
      "total_price": 500000.0,
      "order_date": "2024-01-15T09:00:00",
      "expected_delivery": "2024-01-18T00:00:00",
      "status": "pending",
      "created_at": "2024-01-15T09:00:00"
    }
  ]
}
```

---

### GET /api/orders/{order_id}
নির্দিষ্ট অর্ডার পান

**Example:** `GET /api/orders/1`

**Response:** (উপরের অর্ডার অবজেক্ট দেখুন)

---

### POST /api/orders
নতুন অর্ডার তৈরি করুন

**Request Body:**
```json
{
  "order_number": "ORD002",
  "supplier_id": "SUP002",
  "product_sku": "MOU001",
  "quantity": 50,
  "unit_price": 500.0,
  "expected_delivery": "2024-01-17T00:00:00"
}
```

**Response:**
```json
{
  "success": true,
  "order": {
    "id": 2,
    "order_number": "ORD002",
    "supplier_id": "SUP002",
    "product_sku": "MOU001",
    "quantity": 50,
    "unit_price": 500.0,
    "total_price": 25000.0,
    "order_date": "2024-01-15T10:30:00",
    "expected_delivery": "2024-01-17T00:00:00",
    "status": "pending",
    "created_at": "2024-01-15T10:30:00"
  }
}
```

---

### PATCH /api/orders/{order_id}
অর্ডার স্ট্যাটাস আপডেট করুন

**Example:** `PATCH /api/orders/1`

**Request Body:**
```json
{
  "status": "confirmed"
}
```

**Status মান:**
- `pending`: পেন্ডিং
- `confirmed`: নিশ্চিত
- `shipped`: পাঠানো
- `delivered`: ডেলিভারড

---

## 👥 সাপ্লায়ার এন্ডপয়েন্ট

### GET /api/suppliers
সমস্ত সাপ্লায়ার পান

**Response:**
```json
{
  "count": 2,
  "suppliers": [
    {
      "id": 1,
      "supplier_id": "SUP001",
      "supplier_name": "টেক সাপ্লাইস",
      "email": "tech@supplier.com",
      "phone": "123456",
      "location": "ঢাকা",
      "lead_time_days": 3,
      "is_active": true,
      "created_at": "2024-01-15T08:00:00"
    }
  ]
}
```

---

### GET /api/suppliers/{supplier_id}
নির্দিষ্ট সাপ্লায়ার পান

**Example:** `GET /api/suppliers/SUP001`

---

### POST /api/suppliers
নতুন সাপ্লায়ার যোগ করুন

**Request Body:**
```json
{
  "supplier_id": "SUP003",
  "supplier_name": "নতুন সাপ্লায়ার",
  "email": "new@supplier.com",
  "phone": "987654",
  "location": "চট্টগ্রাম",
  "lead_time_days": 5
}
```

---

## 🤖 AI এজেন্ট এন্ডপয়েন্ট

### POST /api/agents/run
সাপ্লাই চেইন এআই এজেন্ট চালান

**Query Parameters:**
- `operation_type`: "daily" বা "weekly"

**Example:** `POST /api/agents/run?operation_type=daily`

**Response:**
```json
{
  "success": true,
  "operation": "daily",
  "result": "দৈনিক অপারেশন সম্পন্ন...",
  "timestamp": "2024-01-15T10:30:00"
}
```

**অপারেশন প্রকার:**
- **daily**: দৈনিক অপারেশন
  - ইনভেন্টরি লেভেল চেক করুন
  - পেন্ডিং অর্ডার প্রক্রিয়া করুন
  - চালান ট্র্যাক করুন
  - সতর্কতা পাঠান

- **weekly**: সাপ্তাহিক বিশ্লেষণ
  - ট্রেন্ড বিশ্লেষণ
  - সরবরাহকারী পারফরম্যান্স
  - খরচ অপ্টিমাইজেশন সুপারিশ

---

## 📊 বিশ্লেষণ এন্ডপয়েন্ট

### GET /api/analytics/inventory
ইনভেন্টরি বিশ্লেষণ পান

**Response:**
```json
{
  "total_items": 20,
  "total_inventory_value": 850000.0,
  "average_item_quantity": 15.5,
  "high_value_items": [
    {
      "sku": "GPU001",
      "product": "গ্রাফিক্স কার্ড",
      "quantity": 5,
      "value": 250000.0
    }
  ]
}
```

---

### GET /api/analytics/suppliers
সাপ্লায়ার বিশ্লেষণ পান

**Response:**
```json
{
  "total_suppliers": 2,
  "suppliers": [
    {
      "supplier_id": "SUP001",
      "name": "টেক সাপ্লাইস",
      "total_orders": 10,
      "total_spent": 2500000.0,
      "lead_time": 3
    }
  ]
}
```

---

### GET /api/analytics/orders
অর্ডার বিশ্লেষণ পান

**Response:**
```json
{
  "pending": 5,
  "confirmed": 8,
  "shipped": 3,
  "delivered": 12,
  "total": 28
}
```

---

### GET /api/analytics/dashboard
ড্যাশবোর্ড ডেটা পান (সম্পূর্ণ ওভারভিউ)

**Response:**
```json
{
  "inventory": {
    "total_items": 20,
    "low_stock_count": 3,
    "total_inventory_value": 850000.0,
    "low_stock_items": [...]
  },
  "orders": {
    "pending": 5,
    "confirmed": 8,
    "shipped": 3,
    "delivered": 12,
    "total": 28
  },
  "timestamp": "2024-01-15T10:30:00"
}
```

---

## 🔍 ট্র্যাকিং এন্ডপয়েন্ট

### GET /api/tracking/{order_number}
অর্ডার ট্র্যাক করুন

**Example:** `GET /api/tracking/ORD001`

**Response:**
```json
{
  "order_number": "ORD001",
  "status": "shipped",
  "product": "LAP001",
  "quantity": 10,
  "total_price": 500000.0,
  "order_date": "2024-01-15T09:00:00",
  "expected_delivery": "2024-01-18T00:00:00",
  "days_until_delivery": 2,
  "supplier": "টেক সাপ্লাইস"
}
```

---

### GET /api/tracking/delayed
বিলম্বিত অর্ডার পান

**Response:**
```json
{
  "count": 1,
  "delayed_orders": [
    {
      "order_number": "ORD001",
      "status": "confirmed",
      "expected_delivery": "2024-01-14T00:00:00",
      "days_delayed": 1
    }
  ]
}
```

---

## 💡 সুপারিশ এন্ডপয়েন্ট

### GET /api/recommendations/reorder/{sku}
পুনরায় অর্ডার সুপারিশ পান

**Example:** `GET /api/recommendations/reorder/LAP001`

**Response:**
```json
{
  "product_sku": "LAP001",
  "current_stock": 10,
  "daily_usage": 0.5,
  "reorder_point": 8.5,
  "suggested_reorder_qty": 15,
  "lead_time_days": 3,
  "safety_stock": 5
}
```

---

## 🧪 নমুনা ডেটা এন্ডপয়েন্ট

### POST /api/sample-data/init
নমুনা ডেটা যোগ করুন (শুধুমাত্র ডেভেলপমেন্ট)

**Response:**
```json
{
  "success": true,
  "message": "স্যাম্পল ডেটা সংযোজিত হয়েছে"
}
```

---

## ❌ ত্রুটি হ্যান্ডলিং

### সাধারণ ত্রুটি প্রতিক্রিয়া

```json
{
  "error": true,
  "detail": "ইনভেন্টরি আইটেম পাওয়া যায়নি",
  "status_code": 404
}
```

### ত্রুটি কোড

| কোড | অর্থ | উদাহরণ |
|------|------|---------|
| 200 | সফল | ডেটা সফলভাবে পাওয়া গেছে |
| 201 | তৈরি | নতুন আইটেম তৈরি হয়েছে |
| 400 | খারাপ অনুরোধ | ইনভেলিড ডেটা ফরম্যাট |
| 404 | পাওয়া যায়নি | আইটেম ডাটাবেসে নেই |
| 500 | সার্ভার ত্রুটি | অপ্রত্যাশিত ত্রুটি |

---

## 🔐 প্রমাণীকরণ (ভবিষ্যত)

আপনার API সুরক্ষার জন্য JWT টোকেন যোগ করুন:

```bash
# প্রতিটি অনুরোধে হেডার যোগ করুন
Authorization: Bearer YOUR_JWT_TOKEN
```

---

## 📝 কিউল কমান্ড উদাহরণ

### সব ইনভেন্টরি পান
```bash
curl http://localhost:8000/api/inventory
```

### নতুন অর্ডার তৈরি করুন
```bash
curl -X POST http://localhost:8000/api/orders \
  -H "Content-Type: application/json" \
  -d '{
    "order_number": "ORD005",
    "supplier_id": "SUP001",
    "product_sku": "LAP001",
    "quantity": 5,
    "unit_price": 50000,
    "expected_delivery": "2024-01-20T00:00:00"
  }'
```

### ড্যাশবোর্ড ডেটা পান
```bash
curl http://localhost:8000/api/analytics/dashboard
```

### দৈনিক এজেন্ট চালান
```bash
curl -X POST http://localhost:8000/api/agents/run?operation_type=daily
```

---

## 🔗 সম্পর্কিত সংস্থান

- [Swagger UI](http://localhost:8000/docs)
- [ReDoc](http://localhost:8000/redoc)
- [OpenAPI Schema](http://localhost:8000/openapi.json)

---

**শেষ আপডেট**: জানুয়ারি ১৫, ২০২৪
**API সংস্করণ**: ১.০.০
