from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# -------- Data Model for Fitness Class (Database Simulation) --------
class FitnessClass(BaseModel):
    """Represents a fitness class with schedule, instructor, and slots info."""
    id: int
    name: str  # e.g., Yoga, Zumba
    date_time: datetime  # Class start time (timezone-aware UTC)
    instructor: str
    available_slots: int

# -------- Model for Class Response (to Client) --------
class get_class_response(BaseModel):
    """Response model for sending class info to the client in user timezone."""
    id: int
    name: str
    date_time: str  # converted to user timezone (for display)
    instructor: str
    available_slots: int

# -------- Request Schema for Booking a Class --------
class BookingRequest(BaseModel):
    """Request schema for booking a fitness class."""
    class_id: int = Field(..., gt=0, description="ID of the class to book")
    client_name: str = Field(..., min_length=1, description="Name of the client")
    client_email: EmailStr  # built-in email validator

# -------- Booking Object (Storage + Response) --------
class Booking(BaseModel):
    """Represents a booking made by a client for a fitness class."""
    id: int
    class_id: int
    class_name: str
    client_name: str
    client_email: EmailStr
    booked_at: datetime  # timestamp in UTC
