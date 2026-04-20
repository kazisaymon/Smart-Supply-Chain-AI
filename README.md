# Supply Chain AI Agent 🚀

একটি উন্নত AI-চালিত সাপ্লাই চেইন ম্যানেজমেন্ট সিস্টেম যা CrewAI ব্যবহার করে।

## 📋 প্রজেক্ট ওভারভিউ

এই প্রজেক্টে রয়েছে:
- **FastAPI Backend**: REST API এবং AI Agents
- **Streamlit Frontend**: ইন্টারঅ্যাক্টিভ ড্যাশবোর্ড
- **CrewAI Agents**: স্বয়ংক্রিয় সাপ্লাই চেইন পরিচালনা
- **SQLite Database**: ডেটা স্টোরেজ
- **Custom Tools**: Email, ট্র্যাকিং, ডাটাবেস অপারেশন

## 🎯 ফিচার

✅ রিয়েল-টাইম ইনভেন্টরি ট্র্যাকিং
✅ স্বয়ংক্রিয় অর্ডার প্রসেসিং
✅ ভেন্ডর ম্যানেজমেন্ট
✅ ডিমান্ড ফোরকাস্টিং
✅ Email নোটিফিকেশন
✅ AI-চালিত সুপারিশ

---

## 🛠️ লোকাল সেটআপ

### প্রয়োজনীয়তা
- Python 3.10+
- Git
- Virtual Environment

### ইনস্টলেশন স্টেপ

```bash
# 1. প্রজেক্ট ক্লোন করুন
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

# .env এ API কী যোগ করুন:
# ANTHROPIC_API_KEY=your_key
# OPENAI_API_KEY=your_key
# SMTP_PASSWORD=your_email_password
```

### লোকাল চালান

```bash
# Terminal 1: FastAPI Backend চালান
python app/main.py
# API: http://localhost:8000

# Terminal 2: Streamlit Frontend চালান
streamlit run app/streamlit_app.py
# Frontend: http://localhost:8501
```

---

## 📦 প্রজেক্ট স্ট্রাকচার

```
supply-chain-ai-agent/
├── app/
│   ├── main.py              # FastAPI Backend
│   ├── streamlit_app.py     # Streamlit UI
│   ├── agents.py            # CrewAI Agents
│   ├── tools.py             # কাস্টম টুলস
│   ├── database.py          # ডাটাবেস লজিক
│   └── config.py            # কনফিগারেশন
├── data/
│   └── inventory.csv        # স্যাম্পল ডেটা
├── .env.example             # এনভায়রনমেন্ট টেমপ্লেট
├── .gitignore               # গিট ইগনোর ফাইল
├── requirements.txt         # পাইথন ডিপেন্ডেন্সি
├── setup_instructions.md    # সেটআপ গাইড
└── deployment_guide.md      # ডিপ্লয়মেন্ট গাইড
```

---

## 🚀 ডিপ্লয়মেন্ট

### GitHub এ পুশ করুন
```bash
git add .
git commit -m "Initial supply chain AI agent setup"
git push origin main
```

### Streamlit Cloud এ ডিপ্লয় করুন
1. streamlit.io তে সাইন আপ করুন
2. "New app" → GitHub repo সিলেক্ট করুন
3. Main file path: `app/streamlit_app.py`
4. Deploy করুন

### FastAPI Vercel/Railway এ ডিপ্লয় করুন
দেখুন: `deployment_guide.md`

---

## 📚 API এন্ডপয়েন্ট

```
GET  /api/inventory          - ইনভেন্টরি লিস্ট
POST /api/orders             - নতুন অর্ডার
GET  /api/orders/{order_id}  - অর্ডার ডিটেইলস
POST /api/agents/run         - এআই এজেন্ট চালান
```

---

## 🔐 এনভায়রনমেন্ট ভেরিয়েবল

```
ANTHROPIC_API_KEY=xxx
OPENAI_API_KEY=xxx
DATABASE_URL=sqlite:///supply_chain.db
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
SMTP_FROM_EMAIL=your_email@gmail.com
```

---

## 🤝 কন্ট্রিবিউট করুন

```bash
git checkout -b feature/your-feature
# ... কোড করুন ...
git push origin feature/your-feature
# Pull Request তৈরি করুন
```

---

## 📄 লাইসেন্স

MIT License - দেখুন LICENSE ফাইল

---

## 📧 সাপোর্ট

যেকোনো সমস্যার জন্য GitHub Issues এ জানান।
