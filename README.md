
# 🧘 Fitness Studio Booking API

A simple backend API for a fictional fitness studio offering Yoga, Zumba, and HIIT classes. Clients can view available classes and book their spots.

## 🚀 Tech Stack

- **Python 3.10+**
- **FastAPI** for building APIs
- **Pydantic** for data validation
- **Uvicorn** as the ASGI server
- **SQLite (in-memory)** for temporary data storage
- **unittest** for testing

---

## 📦 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/fitness-booking-api.git
cd fitness-booking-api
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If you see an error related to `email-validator`, run this:

```bash
pip install pydantic[email]
```

---

## 🧪 Run the Server

```bash
# Make sure you're in the directory where main.py is located
uvicorn main:app --reload
```

Now go to: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧾 API Endpoints

### `GET /classes`
Get all upcoming fitness classes.

**Response Example**:

```json
[
  {
    "id": 1,
    "name": "Yoga",
    "date_time": "2025-06-09T04:00:00Z",
    "instructor": "Arham",
    "available_slots": 10
  }
]
```

### `POST /book`
Book a slot in a class.

**Request Body**:

```json
{
  "class_id": 1,
  "client_name": "Alice",
  "client_email": "alice@example.com"
}
```

**Success Response**:

```json
{
  "id": 1,
  "class_id": 1,
  "class_name": "Yoga",
  "client_name": "Alice",
  "client_email": "alice@example.com",
  "booked_at": "2025-06-08T10:56:44.603022Z"
}
```

### `GET /bookings?email=alice@example.com`
Fetch all bookings by a client email.

---

## 🌐 Timezone Handling

Classes are created in **IST** and stored in **UTC**. When retrieved, times are always in UTC.

---

## ✅ Running Unit Tests

```bash
python -m unittest discover tests
```

---

## 🗂 Directory Structure

```
booking-api/
│
├── main.py              # FastAPI app and routes
├── models.py            # Pydantic models
├── db.py                # In-memory storage logic
├── test/
│   └── test_api.py      # Unit tests
└── requirements.txt     # Dependencies
```

---

## 📽 Loom Video Walkthrough

Watch the [Loom demo video here](#) (insert your Loom video link).

---

## 👨‍💻 Author

- Name: [Your Name]
- Email: [your.email@example.com]
- GitHub: [github.com/yourusername](https://github.com/yourusername)
