# 🚆 RailYatra — Railway Management System

A full-stack Railway Management System with:
- **Backend**: Python + Flask + SQLite
- **Frontend**: HTML + Tailwind CSS (3 pages)
- **Features**: Train search, seat availability map, ticket booking, PNR check

---

## 📁 Project Structure

```
railway/
├── app.py              # Flask backend (all API routes)
├── schema.sql          # SQLite schema + seed data (10 trains)
├── requirements.txt    # Python dependencies
├── railway.db          # Auto-created on first run
└── static/
    ├── index.html      # Train search page
    ├── seats.html      # Seat availability map
    └── booking.html    # Book ticket + PNR status
```

---

## ⚙️ Setup & Run

### 1. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Flask server
```bash
python app.py
```

The server starts at **http://localhost:5000**

> The SQLite database (`railway.db`) is auto-created with seed data on first run.

### 3. Open in browser
Visit: **http://localhost:5000**

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/trains` | Get all trains |
| GET | `/api/trains/search?source=X&destination=Y&date=Z` | Search trains |
| GET | `/api/trains/<id>` | Get train by ID |
| GET | `/api/seats/<train_id>?date=YYYY-MM-DD` | Seat availability map |
| POST | `/api/book` | Book a ticket |
| GET | `/api/bookings/<pnr>` | Get booking by PNR |
| GET | `/api/stations` | All unique stations (for autocomplete) |

### POST /api/book — Request body
```json
{
  "train_id": 1,
  "journey_date": "2026-04-10",
  "passenger_name": "Arjun Sharma",
  "passenger_age": 28,
  "passenger_gender": "Male",
  "passenger_email": "arjun@example.com",
  "passenger_phone": "9876543210"
}
```

---

## 🗄️ Database Schema

- **trains** — train details, routes, fare, seat counts
- **passengers** — passenger info per booking
- **bookings** — links trains + passengers, stores PNR + seat

---

## 🌐 Pages

| Page | URL | Description |
|------|-----|-------------|
| Home | `/` | Search trains by source/destination/date |
| Seats | `/seat-availability` | Visual seat map with available/booked seats |
| Booking | `/booking` | Book a ticket + check PNR status |
