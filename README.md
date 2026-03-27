# 🌱 GreenTrack – Smart Carbon Footprint Tracker for Students

A production-ready web application to track, reduce, and compete on carbon footprint reduction.

![Tech Stack](https://img.shields.io/badge/Flask-3.1-green) ![DB](https://img.shields.io/badge/SQLite-Dev-blue) ![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

- 🔐 **Secure Authentication** – bcrypt hashing, JWT in HTTP-only cookies
- 📊 **Interactive Dashboard** – Chart.js bar & doughnut charts, green score gauge
- 🌿 **Carbon Calculator** – Realistic emission factors for travel, electricity, food
- 💡 **Smart Suggestions** – Personalized eco tips based on your patterns
- 🏆 **Leaderboard** – Compete with students for the lowest carbon footprint
- 🌙 **Dark/Light Mode** – Beautiful glassmorphism UI with smooth animations
- 🔒 **Security** – CSP headers, rate limiting, input sanitization, CORS

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- pip

### 1. Clone & Setup Virtual Environment

```bash
cd "Carbon Footprint"
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Edit `.env` if needed (defaults work for development):

```env
SECRET_KEY=change-this-to-a-very-long-random-string-in-production
JWT_SECRET_KEY=change-this-jwt-secret-key-in-production
DATABASE_URL=sqlite:///instance/greentrack.db
```

### 4. Run the Application

```bash
python -m backend.app
```

Open **http://localhost:5000** in your browser.

---

## 📁 Project Structure

```
├── frontend/               # Static frontend
│   ├── index.html          # Landing page
│   ├── login.html          # Auth (login/signup)
│   ├── dashboard.html      # Dashboard with charts
│   ├── leaderboard.html    # Top 10 rankings
│   ├── style.css           # Glassmorphism design system
│   └── app.js              # API layer, theme, toasts
│
├── backend/                # Flask API
│   ├── app.py              # App factory + server
│   ├── config.py           # Dev/Prod configuration
│   ├── models/             # SQLAlchemy models
│   │   ├── user.py
│   │   ├── carbon_entry.py
│   │   └── carbon_result.py
│   ├── routes/             # API blueprints
│   │   ├── auth.py         # /api/register, login, logout
│   │   ├── data.py         # /api/add-entry, user-data
│   │   └── leaderboard.py  # /api/leaderboard
│   ├── services/           # Business logic
│   │   ├── __init__.py     # Carbon calculator
│   │   └── suggestions.py  # Eco suggestions engine
│   ├── utils/              # Validators & sanitizers
│   └── schemas/            # Schema definitions
│
├── instance/               # SQLite database (auto-created)
├── .env                    # Environment variables
├── requirements.txt        # Python dependencies
└── README.md
```

---

## 📡 API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/register` | No | Create account |
| POST | `/api/login` | No | Login (sets JWT cookie) |
| POST | `/api/logout` | Optional | Clear JWT cookie |
| GET | `/api/me` | Yes | Get current user |
| POST | `/api/add-entry` | Yes | Log carbon entry |
| GET | `/api/user-data` | Yes | Dashboard data + charts |
| GET | `/api/leaderboard` | No | Top 10 rankings |

---

## 🔒 Security Features

| Layer | Implementation |
|-------|---------------|
| Passwords | bcrypt with 12 salt rounds |
| Auth Tokens | JWT in HTTP-only cookies |
| Headers | Flask-Talisman (CSP, HSTS, X-Frame-Options) |
| Rate Limiting | Flask-Limiter (5/min login, 30/min data) |
| Input | Server-side validation + HTML escaping |
| SQL Injection | SQLAlchemy ORM (no raw SQL) |
| XSS | CSP headers + output escaping |
| CORS | Flask-CORS whitelist |

---

## 🌍 Emission Factors

| Source | Factor | Unit |
|--------|--------|------|
| Car | 0.21 | kg CO₂/km |
| Bus | 0.05 | kg CO₂/km |
| Bike | 0.10 | kg CO₂/km |
| Walking | 0.00 | kg CO₂/km |
| Electricity | 0.82 | kg CO₂/unit |
| Veg food | 1.50 | kg CO₂/day |
| Non-veg food | 3.00 | kg CO₂/day |
| Vegan food | 1.20 | kg CO₂/day |

---

## 🚀 Production Deployment

### Backend (Render / Railway)

```bash
# Use gunicorn
gunicorn "backend.app:create_app()" --bind 0.0.0.0:$PORT --workers 4
```

Set environment variables:
- `FLASK_ENV=production`
- `SECRET_KEY=<random-64-char-string>`
- `JWT_SECRET_KEY=<random-64-char-string>`
- `DATABASE_URL=postgresql://...`

### Frontend (Netlify / Vercel)

Deploy the `frontend/` directory as a static site. Update `API_BASE` in `app.js` to point to the backend URL.

### Database

Use PostgreSQL in production. Set `DATABASE_URL` in your environment:

```
postgresql://user:password@host:5432/greentrack
```

---

## 📄 License

MIT License – © 2026 GreenTrack
