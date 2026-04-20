# সাপ্লাই চেইন AI এজেন্ট - সম্পূর্ণ ডিপ্লয়মেন্ট গাইড

## 📋 বিষয়বস্তু
1. [GitHub সেটআপ](#github-সেটআপ)
2. [Streamlit Cloud ডিপ্লয়মেন্ট](#streamlit-cloud-ডিপ্লয়মেন্ট)
3. [FastAPI Vercel ডিপ্লয়মেন্ট](#fastapi-vercel-ডিপ্লয়মেন্ট)
4. [FastAPI Railway ডিপ্লয়মেন্ট](#fastapi-railway-ডিপ্লয়মেন্ট)
5. [ডাটাবেস সেটআপ](#ডাটাবেস-সেটআপ)
6. [সিকিউরিটি এবং বেস্ট প্র্যাক্টিস](#সিকিউরিটি-এবং-বেস্ট-প্র্যাক্টিস)

---

## GitHub সেটআপ

### ধাপ 1: GitHub এ রিপোজিটরি তৈরি করুন

```bash
# লোকাল রিপোজিটরি ইনিশিয়ালাইজ করুন (যদি করা না হয়ে থাকে)
git init
git add .
git commit -m "Initial supply chain AI agent setup"

# GitHub এ নতুন রিপোজিটরি তৈরি করুন এবং লিংক করুন
git remote add origin https://github.com/yourusername/supply-chain-ai-agent.git
git branch -M main
git push -u origin main
```

### ধাপ 2: .gitignore ফাইল নিশ্চিত করুন

`.env` এবং অন্যান্য সংবেদনশীল ফাইল GitHub এ পুশ করবেন না:

```
# .gitignore এ থাকা উচিত:
.env
.env.local
__pycache__/
*.db
.venv/
.streamlit/secrets.toml
```

### ধাপ 3: GitHub Secrets সেট করুন

GitHub এর Settings → Secrets and variables → Actions এ যান এবং যোগ করুন:

```
ANTHROPIC_API_KEY=your_key
OPENAI_API_KEY=your_key
DATABASE_URL=your_database_url
```

---

## Streamlit Cloud ডিপ্লয়মেন্ট

### ধাপ 1: Streamlit Community Cloud এ সাইন আপ করুন

1. https://streamlit.io/ এ যান
2. "Create app" বাটনে ক্লিক করুন
3. GitHub account দিয়ে সাইন ইন করুন

### ধাপ 2: অ্যাপ ডিপ্লয় করুন

```
Repository: yourusername/supply-chain-ai-agent
Branch: main
Main file path: app/streamlit_app.py
```

### ধাপ 3: Secrets কনফিগার করুন

Streamlit Cloud এর Advanced settings এ `.streamlit/secrets.toml` তৈরি করুন:

```toml
ANTHROPIC_API_KEY = "your_key"
OPENAI_API_KEY = "your_key"
SMTP_USER = "your_email@gmail.com"
SMTP_PASSWORD = "your_app_password"

# API কানেকশন
API_BASE_URL = "https://your-fastapi-backend.com"
```

### ধাপ 4: requirements.txt আপডেট করুন (Streamlit এর জন্য)

`requirements.txt` এ নিশ্চিত করুন এই প্যাকেজগুলি আছে:

```
streamlit==1.28.1
streamlit-option-menu==0.3.6
plotly==5.18.0
pandas==2.1.3
requests==2.31.0
```

### Streamlit ডিপ্লয়মেন্ট কমান্ড

```bash
# লোকাল টেস্টিং
streamlit run app/streamlit_app.py

# ক্লাউডে ডিপ্লয় হবে স্বয়ংক্রিয়ভাবে GitHub এ পুশ করলে
```

---

## FastAPI Vercel ডিপ্লয়মেন্ট

### ধাপ 1: Vercel CLI ইনস্টল করুন

```bash
npm install -g vercel
```

### ধাপ 2: Vercel প্রজেক্ট ইনিশিয়ালাইজ করুন

```bash
vercel login
vercel
```

### ধাপ 3: vercel.json তৈরি করুন

প্রজেক্ট রুটে `vercel.json` তৈরি করুন:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "app/main.py",
      "use": "@vercel/python",
      "config": {
        "maxLambdaSize": "50mb"
      }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app/main.py"
    }
  ],
  "env": {
    "ANTHROPIC_API_KEY": "@anthropic_api_key",
    "OPENAI_API_KEY": "@openai_api_key",
    "DATABASE_URL": "@database_url",
    "SMTP_USER": "@smtp_user",
    "SMTP_PASSWORD": "@smtp_password"
  }
}
```

### ধাপ 4: Vercel এ এনভায়রনমেন্ট ভেরিয়েবল সেট করুন

```bash
vercel env add ANTHROPIC_API_KEY
vercel env add OPENAI_API_KEY
vercel env add DATABASE_URL
vercel env add SMTP_USER
vercel env add SMTP_PASSWORD
```

### ধাপ 5: ডিপ্লয় করুন

```bash
vercel --prod
```

---

## FastAPI Railway ডিপ্লয়মেন্ট

### ধাপ 1: Railway তে সাইন আপ করুন

https://railway.app/ এ যান এবং GitHub দিয়ে সাইন ইন করুন

### ধাপ 2: নতুন প্রজেক্ট তৈরি করুন

1. "New Project" ক্লিক করুন
2. "Deploy from GitHub repo" নির্বাচন করুন
3. আপনার রিপোজিটরি সিলেক্ট করুন

### ধাপ 3: PostgreSQL ডাটাবেস যোগ করুন (Optional)

```bash
# Railway ড্যাশবোর্ডে "Add" → "Database" → "PostgreSQL"
```

### ধাপ 4: এনভায়রনমেন্ট ভেরিয়েবল সেট করুন

Railway Dashboard এ Variables এ যোগ করুন:

```
ANTHROPIC_API_KEY=your_key
OPENAI_API_KEY=your_key
DATABASE_URL=postgresql://user:password@host:5432/dbname
SMTP_USER=your_email
SMTP_PASSWORD=your_password
```

### ধাপ 5: Procfile তৈরি করুন

প্রজেক্ট রুটে `Procfile` তৈরি করুন:

```
web: python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

---

## ডাটাবেস সেটআপ

### PostgreSQL (প্রোডাকশনের জন্য সুপারিশকৃত)

#### Railway এ:
```bash
# Railway থেকে DATABASE_URL কপি করুন এবং .env এ সেট করুন
DATABASE_URL=postgresql://user:password@host:5432/dbname
```

#### স্থানীয়ভাবে:
```bash
# PostgreSQL ইনস্টল করুন (macOS)
brew install postgresql
brew services start postgresql

# ডাটাবেস এবং ইউজার তৈরি করুন
createdb supply_chain
createuser supply_chain_user -P
psql supply_chain -c "ALTER ROLE supply_chain_user WITH CREATEDB CREATEROLE;"
```

### SQLite (ডেভেলপমেন্টের জন্য)

ডিফল্ট হিসেবে কাজ করে:

```bash
DATABASE_URL=sqlite:///supply_chain.db
```

---

## সম্পূর্ণ ডিপ্লয়মেন্ট ওয়ার্কফ্লো

### স্টেপ 1: লোকাল টেস্টিং

```bash
# Backend চালান
python app/main.py

# Frontend চালান (নতুন টার্মিনালে)
streamlit run app/streamlit_app.py
```

### স্টেপ 2: GitHub এ পুশ করুন

```bash
git add .
git commit -m "Deploy to production"
git push origin main
```

### স্টেপ 3: Streamlit Cloud এ ডিপ্লয় করুন

- Streamlit Cloud স্বয়ংক্রিয়ভাবে ডিপ্লয় করবে

### স্টেপ 4: FastAPI ডিপ্লয় করুন

**Option A: Vercel**
```bash
vercel --prod
```

**Option B: Railway**
- Railway Dashboard এ ডিপ্লয় স্বয়ংক্রিয়

### স্টেপ 5: Streamlit এ API URL আপডেট করুন

Streamlit Cloud এর Secrets এ:
```toml
API_BASE_URL = "https://your-fastapi-backend.com"
```

---

## 🔐 সিকিউরিটি এবং বেস্ট প্র্যাক্টিস

### 1. এনভায়রনমেন্ট ভেরিয়েবল

```bash
# কখনো .env ফাইল কমিট করবেন না
# সর্বদা ক্লাউড প্ল্যাটফর্মে secrets ব্যবহার করুন
```

### 2. API সিকিউরিটি

```python
# CORS সেটআপ (main.py)
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("ALLOWED_ORIGINS", "").split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
```

### 3. ডাটাবেস সিকিউরিটি

```python
# অথেন্টিকেশন যোগ করুন (ভবিষ্যতে)
# HTTPS ব্যবহার করুন
# Prepared statements ব্যবহার করুন (SQLAlchemy করে)
```

### 4. লগিং এবং মনিটরিং

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
```

---

## 📊 মনিটরিং এবং লগিং

### Vercel এ লগ দেখুন

```bash
vercel logs
```

### Railway এ লগ দেখুন

- Railway Dashboard → Logs ট্যাব

### Streamlit Cloud এ লগ দেখুন

- Streamlit Cloud → Logs ট্যাব

---

## 🆘 সমস্যা সমাধান

### API সংযোগ বিচ্ছিন্ন হলে

```python
# streamlit_app.py এ চেক করুন
API_BASE_URL = "http://localhost:8000"  # লোকাল
# বা
API_BASE_URL = "https://your-fastapi-backend.com"  # প্রোডাকশন
```

### ডাটাবেস কানেকশন সমস্যা

```bash
# DATABASE_URL চেক করুন
echo $DATABASE_URL

# ডাটাবেস সংযোগ পরীক্ষা করুন
python -c "from database import engine; engine.connect()"
```

### CORS ত্রুটি

```python
# main.py এ CORS সেটআপ চেক করুন
# allow_origins সঠিক করুন
```

---

## 📈 স্কেলিং সুপারিশ

1. **ডাটাবেস**: PostgreSQL ব্যবহার করুন (SQLite নয়)
2. **Cache**: Redis যোগ করুন অনুসন্ধানের জন্য
3. **Queue**: Celery যোগ করুন দীর্ঘমেয়াদী কাজের জন্য
4. **CDN**: Cloudflare ব্যবহার করুন স্থির ফাইলের জন্য

---

## 📚 অতিরিক্ত রিসোর্স

- [FastAPI ডকুমেন্টেশন](https://fastapi.tiangolo.com/)
- [Streamlit ডকুমেন্টেশন](https://docs.streamlit.io/)
- [CrewAI ডকুমেন্টেশন](https://docs.crewai.com/)
- [Vercel ডকুমেন্টেশন](https://vercel.com/docs)
- [Railway ডকুমেন্টেশন](https://docs.railway.app/)

---

## ✅ চেকলিস্ট

- [ ] GitHub রিপোজিটরি সেটআপ করা হয়েছে
- [ ] .gitignore কনফিগার করা হয়েছে
- [ ] GitHub Secrets সেট করা হয়েছে
- [ ] Streamlit Cloud ডিপ্লয় করা হয়েছে
- [ ] FastAPI ডিপ্লয় করা হয়েছে (Vercel/Railway)
- [ ] এনভায়রনমেন্ট ভেরিয়েবল সব জায়গায় সেট করা হয়েছে
- [ ] API URL Streamlit এ আপডেট করা হয়েছে
- [ ] লাইভ টেস্টিং সম্পন্ন হয়েছে

---

**শুভকামনা! আপনার সাপ্লাই চেইন AI এজেন্ট এখন চালু আছে! 🚀**
