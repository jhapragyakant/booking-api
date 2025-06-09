from datetime import datetime, timedelta
from typing import List
from models import FitnessClass, Booking, get_class_response, BookingRequest
from pytz import timezone, utc
import logging
import itertools

# In-memory Storage
classes : List[FitnessClass] = []
bookings : List[Booking] = []

# Unique ID generators
class_id_counter = itertools.count(1)
booking_id_counter = itertools.count(1)

# Implementing logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def seed_classes():
    """Seed the in-memory database with sample fitness classes if not already present."""

    if classes:
        return  # Already seeded

    ist = timezone("Asia/Kolkata")
    now = datetime.now(ist).replace(second=0, microsecond=0)
    
    sample_classes = [
        {"name": "Yoga", "instructor": "Arham", "delta_days": 1},
        {"name": "Zumba", "instructor": "Bishwanath", "delta_days": 2},
        {"name": "HIIT", "instructor": "Charan", "delta_days": 3},
    ]

    for item in sample_classes:
        dt = now + timedelta(days=item["delta_days"], hours=9, minutes=30)  # 9:30 AM IST
        # dt is already timezone-aware, so no need to localize
        utc_dt = dt.astimezone(utc)

        classes.append(FitnessClass(
            id=next(class_id_counter),
            name=item["name"],
            date_time=utc_dt,
            instructor=item["instructor"],
            available_slots=10  # Default slots
        ))

def get_all_classes(user_tz: str) -> List[get_class_response]:
    """Return all fitness classes, converting times to the user's timezone."""
    
    try:
        user_timezone = timezone(user_tz)
    except Exception:
        logger.warning(f"Invalid timezone: {user_tz}. falling back to UTC.")
        user_timezone = utc
    return [
        get_class_response(
            id=cls.id,
            name=cls.name,
            date_time=cls.date_time.astimezone(user_timezone).strftime("%Y-%m-%d %H:%M:%S %Z"),
            instructor=cls.instructor,
            available_slots=cls.available_slots
        ) for cls in classes
    ]

def create_booking(req: BookingRequest) -> Booking:
    """
    Creates a booking for a fitness class.

    - Validates class ID and available slots.
    - Creates a new booking entry with unique ID.
    - Updates the class's available slots.

    Returns the created Booking object.
    """
    
    # Find the class by ID
    fitness_class = next((cls for cls in classes if cls.id == req.class_id), None)
    if not fitness_class:
        logger.error(f"Class ID {req.class_id} not found.")
        raise ValueError("Class not found")
    
    # Check available slots
    if fitness_class.available_slots <= 0:
        logger.error(f"No available slots for class ID {req.class_id}.")
        raise ValueError("No available slots")
    
    # Check for duplicate booking
    for booking in bookings:
        if booking.class_id == req.class_id and booking.client_email.lower() == req.client_email.lower():
            logger.error(f"Duplicate booking attempt for class ID {req.class_id} by {req.client_email}.")
            raise ValueError("Duplicate booking")
    
    # Decrease available slots
    fitness_class.available_slots -= 1

    # Create a new booking
    booking = Booking(
        id=next(booking_id_counter),
        class_id=fitness_class.id,
        class_name=fitness_class.name,
        client_name=req.client_name,
        client_email=req.client_email,
        booked_at=datetime.now(utc)  # Store in UTC
    )

    bookings.append(booking)
    logger.info(f"Booking created: {booking}")
    return booking

def get_bookings_by_email(email: str) -> List[Booking]:
    """Get all bookings for a given client email."""
    
    filtered_bookings = [booking for booking in bookings if booking.client_email.lower() == email.lower()]
    logger.info(f"Bookings retrieved for email {email}: {filtered_bookings}")
    return filtered_bookings

def get_all_bookings() -> List[Booking]:
    """Return all bookings in the system."""
    return bookings