# 🚀 সাপ্লাই চেইন AI এজেন্ট - শুরু করার গাইড

## 📌 দ্রুত শুরু (5 মিনিটে)

### পূর্বশর্ত
- Python 3.10+
- Git
- API Keys (Anthropic এবং OpenAI)

### ইনস্টলেশন

```bash
# 1. রিপোজিটরি ক্লোন করুন
git clone https://github.com/yourusername/supply-chain-ai-agent.git
cd supply-chain-ai-agent

# 2. Virtual Environment তৈরি করুন
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# 3. ডিপেন্ডেন্সি ইনস্টল করুন
pip install -r requirements.txt

# 4. .env ফাইল তৈরি করুন
cp .env.example .env

# 5. .env এ API কী যোগ করুন (উদাহরণ)
# ANTHROPIC_API_KEY=sk-ant-xxx
# OPENAI_API_KEY=sk-xxx
# SMTP_PASSWORD=আপনার_gmail_পাস্ওয়ার্ড
```

---

## 🏃 লোকাল চালানোর নির্দেশনা

### টার্মিনাল 1: FastAPI Backend চালান

```bash
# লোকাল ডেটাবেস ইনিশিয়ালাইজ করুন (প্রথমবার)
python app/database.py

# FastAPI সার্ভার শুরু করুন
python app/main.py

# API উপলব্ধ হবে: http://localhost:8000
# API ডকুমেন্টেশন: http://localhost:8000/docs
```

### টার্মিনাল 2: Streamlit Frontend চালান

```bash
# Streamlit অ্যাপ চালান
streamlit run app/streamlit_app.py

# ব্রাউজার খোলে: http://localhost:8501
```

---

## 🔑 API কী পাওয়ার নির্দেশনা

### Anthropic API কী পান

1. https://console.anthropic.com/login এ যান
2. আপনার অ্যাকাউন্ট তৈরি করুন বা লগইন করুন
3. "API Keys" সেকশনে যান
4. নতুন API কী জেনারেট করুন
5. `.env` ফাইলে যোগ করুন:
   ```
   ANTHROPIC_API_KEY=sk-ant-xxxxx
   ```

### OpenAI API কী পান

1. https://platform.openai.com/api-keys এ যান
2. আপনার অ্যাকাউন্ট তৈরি করুন বা লগইন করুন
3. "API keys" এ নতুন কী তৈরি করুন
4. `.env` ফাইলে যোগ করুন:
   ```
   OPENAI_API_KEY=sk-proj-xxxxx
   ```

### Gmail এর জন্য App Password পান

1. আপনার Google অ্যাকাউন্টে যান (https://myaccount.google.com/)
2. Security → 2-Step Verification (চালু করুন যদি না থাকে)
3. Security → App passwords পান
4. Select "Mail" এবং "Windows Computer" 
5. তৈরি পাস্ওয়ার্ড কপি করুন এবং `.env` এ যোগ করুন:
   ```
   SMTP_USER=your_email@gmail.com
   SMTP_PASSWORD=xxxx xxxx xxxx xxxx
   ```

---

## 📊 প্রথম ডেটা যোগ করুন

### সাধারণ মাধ্যমে

```bash
# API ডেটা যোগ করুন
curl -X POST http://localhost:8000/api/sample-data/init
```

### Streamlit এর মাধ্যমে

1. Streamlit ড্যাশবোর্ড খুলুন
2. **👥 সাপ্লায়ার** → **➕ যোগ করুন**
3. সাপ্লায়ার তথ্য ভরুন এবং সংরক্ষণ করুন
4. **📦 ইনভেন্টরি** → **➕ যোগ করুন**
5. পণ্য তথ্য ভরুন এবং সংরক্ষণ করুন

---

## 🤖 AI এজেন্ট চালান

### ম্যানুয়াল চালান

Streamlit ড্যাশবোর্ডে **🤖 এআই এজেন্ট** ট্যাবে যান:

- **দৈনিক অপারেশন**: ইনভেন্টরি চেক, অর্ডার প্রসেসিং, ট্র্যাকিং
- **সাপ্তাহিক বিশ্লেষণ**: ট্রেন্ড বিশ্লেষণ এবং সুপারিশ

### প্রোগ্রামেটিক্যালি চালান

```python
from sqlalchemy.orm import Session
from agents import run_supply_chain_agent
from database import SessionLocal

db = SessionLocal()
result = run_supply_chain_agent(db, "daily")
db.close()
```

### Scheduled চালান (ভবিষ্যত)

```python
# APScheduler যোগ করুন (সময়সূচী চালানোর জন্য)
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
scheduler.add_job(run_daily_operations, 'cron', hour=9, minute=0)
scheduler.start()
```

---

## 📚 প্রজেক্ট স্ট্রাকচার বুঝুন

```
supply-chain-ai-agent/
│
├── app/                          # মূল অ্যাপ্লিকেশন
│   ├── main.py                  # FastAPI ব্যাকএন্ড
│   ├── streamlit_app.py         # Streamlit ফ্রন্টএন্ড
│   ├── agents.py                # CrewAI এজেন্ট
│   ├── tools.py                 # কাস্টম টুলস
│   ├── database.py              # ডেটাবেস অপারেশন
│   └── config.py                # কনফিগারেশন (আসছে)
│
├── data/
│   └── inventory.csv            # স্যাম্পল ডেটা
│
├── docs/
│   ├── API.md                   # API ডকুমেন্টেশন
│   ├── ARCHITECTURE.md          # আর্কিটেকচার
│   └── TROUBLESHOOTING.md       # সমস্যা সমাধান
│
├── tests/                        # ইউনিট টেস্ট (আসছে)
│   └── test_api.py
│
├── .env.example                 # এনভায়রনমেন্ট টেমপ্লেট
├── .gitignore                   # গিট ইগনোর
├── requirements.txt             # পাইথন ডিপেন্ডেন্সি
├── README.md                    # প্রজেক্ট ওভারভিউ
├── SETUP.md                     # এই ফাইল
└── deployment_guide.md          # ডিপ্লয়মেন্ট গাইড
```

---

## 🧪 API টেস্ট করুন

### Swagger UI এ

1. http://localhost:8000/docs খুলুন
2. "Try it out" বাটন ক্লিক করুন
3. প্যারামিটার ভরুন এবং "Execute" করুন

### cURL দিয়ে

```bash
# হেলথ চেক
curl http://localhost:8000/health

# সব ইনভেন্টরি পান
curl http://localhost:8000/api/inventory

# নতুন সাপ্লায়ার যোগ করুন
curl -X POST http://localhost:8000/api/suppliers \
  -H "Content-Type: application/json" \
  -d '{
    "supplier_id": "SUP001",
    "supplier_name": "টেক সাপ্লাইস",
    "email": "tech@supplier.com",
    "phone": "123456",
    "location": "ঢাকা",
    "lead_time_days": 3
  }'

# ড্যাশবোর্ড ডেটা পান
curl http://localhost:8000/api/analytics/dashboard
```

---

## 🔧 সেটিংস কাস্টমাইজ করুন

### .env ফাইল অপশন

```env
# ইনভেন্টরি সেটিংস
LOW_STOCK_THRESHOLD=10          # কম স্টক সীমা
REORDER_QUANTITY=50              # পুনরায় অর্ডার পরিমাণ

# API সেটিংস
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=true                  # ডেভেলপমেন্টের জন্য

# Streamlit সেটিংস
STREAMLIT_THEME_MODE=dark
STREAMLIT_SERVER_PORT=8501

# ডেটাবেস
DATABASE_URL=sqlite:///supply_chain.db

# SMTP (ইমেইল)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USE_TLS=true
```

---

## 🐛 সাধারণ সমস্যা সমাধান

### সমস্যা: "ডাটাবেস সংযোগ ব্যর্থ"

```bash
# সমাধান: ডাটাবেস ফাইল মুছুন এবং পুনরায় তৈরি করুন
rm supply_chain.db
python app/database.py
```

### সমস্যা: "API পোর্ট 8000 ব্যবহারে আছে"

```bash
# সমাধান: অন্য পোর্ট ব্যবহার করুন
python -m uvicorn app.main:app --port 8001
```

### সমস্যা: "SMTP ইমেইল পাঠাতে পারছে না"

```
সমাধান:
1. Gmail App Password সঠিক নিশ্চিত করুন
2. 2FA চেক করুন Google অ্যাকাউন্টে
3. কম নিরাপদ অ্যাপস চালু করুন (যদি প্রয়োজন)
```

### সমস্যা: "API কী অবৈধ"

```
সমাধান:
1. API কী .env এ সঠিক নিশ্চিত করুন
2. কোটা এবং বিলিং চেক করুন
3. কী পুনরায় জেনারেট করুন
```

---

## 🚀 পরবর্তী ধাপ

### স্বল্পমেয়াদী

- [ ] সাপ্লায়ার এবং পণ্য ডেটা যোগ করুন
- [ ] এআই এজেন্ট টেস্ট করুন
- [ ] ইমেইল নোটিফিকেশন কনফিগার করুন
- [ ] কাস্টম রুলস যোগ করুন

### দীর্ঘমেয়াদী

- [ ] GitHub এ পুশ করুন
- [ ] Streamlit Cloud এ ডিপ্লয় করুন
- [ ] FastAPI Railway/Vercel এ ডিপ্লয় করুন
- [ ] PostgreSQL ডাটাবেস সেটআপ করুন
- [ ] প্রোডাকশন সিকিউরিটি যোগ করুন (অথেন্টিকেশন, SSL)

---

## 📖 শিখুন এবং বৃদ্ধি করুন

### সুপারিশকৃত টিউটোরিয়াল

1. **FastAPI**: https://fastapi.tiangolo.com/tutorial/
2. **Streamlit**: https://docs.streamlit.io/library/get-started
3. **CrewAI**: https://docs.crewai.com/
4. **SQLAlchemy**: https://docs.sqlalchemy.org/

### YouTube চ্যানেল

- Traversy Media - FastAPI টিউটোরিয়াল
- Code With Harry - Python এবং ওয়েব ডেভেলপমেন্ট
- Tech with Tim - Streamlit এবং ডেটা অ্যাপস

---

## 💬 সম্প্রদায় এবং সহায়তা

- **GitHub Issues**: বাগ এবং ফিচার রিকোয়েস্টের জন্য
- **Discussions**: প্রশ্ন এবং আলোচনার জন্য
- **Discord** (আসছে): রিয়েল-টাইম চ্যাট

---

## 📞 যোগাযোগ

- **Email**: your_email@example.com
- **GitHub**: @yourusername
- **LinkedIn**: /in/yourprofile

---

## 📄 লাইসেন্স

এই প্রজেক্ট MIT লাইসেন্সের অধীন। বিস্তারিত দেখুন [LICENSE](LICENSE) ফাইলে।

---

**শুরু করতে প্রস্তুত? 🎉 উপরের ধাপগুলি অনুসরণ করুন এবং আপনার সাপ্লাই চেইন অপ্টিমাইজ করুন!**

Happy coding! 💻
