from fastapi import FastAPI, HTTPException, Query
from typing import List
from models import BookingRequest, get_class_response
from db import get_all_classes, create_booking, get_bookings_by_email, seed_classes, get_all_bookings
import uvicorn

app = FastAPI(title="Fitness Studio Booking API", description="API for booking fitness classes at a fictional fitness studio", version="1.0")

# Seeding Initial Data
seed_classes()

@app.get("/classes", response_model=List[get_class_response])
def list_classes(timezone: str = Query("Asia/Kolkata", description="Your local timezone")):
    return get_all_classes(timezone)

@app.post("/book")
def book_class(request: BookingRequest):
    try:
        # Check for duplicate booking
        existing = [b for b in get_bookings_by_email(request.client_email) if b.class_id == request.class_id]
        if existing:
            raise HTTPException(status_code=409, detail="You have already booked this class.")
        booking = create_booking(request)
        return booking
    except ValueError as e:
        # Overbooking or class not found
        if str(e) == "No available slots":
            raise HTTPException(status_code=409, detail="No available slots for this class.")
        if str(e) == "Class not found":
            raise HTTPException(status_code=404, detail="Class not found.")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid booking request.")

@app.get("/bookings")
def get_bookings(email: str):
    results = get_bookings_by_email(email)
    if not results:
        raise HTTPException(status_code=404, detail="No bookings found for this email")
    return results

@app.get("/bookings/all")
def get_all_bookings_api():
    """API endpoint to get all bookings in the system."""
    all_bookings = get_all_bookings()
    if not all_bookings:
        raise HTTPException(status_code=404, detail="No bookings found")
    return all_bookings


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)