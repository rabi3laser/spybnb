# 🕵️ SpyBnB

> Airbnb competitor price monitoring for smart hosts

## Features

- 🔍 Scan competitors in any location
- 💰 Track price changes in real-time
- 📊 Analytics dashboard
- 🔔 Price alerts via email
- 📈 Historical price data

## Tech Stack

- **Backend:** FastAPI (Python)
- **Database:** Supabase
- **Scraping:** Apify
- **Frontend:** Next.js
- **Payments:** Stripe

## Quick Start

```bash
# Clone
git clone https://github.com/rabi3laser/spybnb.git
cd spybnb

# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp ../.env.example .env
uvicorn main:app --reload
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/scan | Start a new scan |
| GET | /api/scan/{id} | Get scan results |
| GET | /api/scans | List user scans |
| POST | /api/alerts | Create price alert |
| GET | /api/alerts | List alerts |
| DELETE | /api/alerts/{id} | Delete alert |

## License

MIT
