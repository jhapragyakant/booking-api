import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from fastapi.testclient import TestClient
from main import app
from db import classes, bookings

client = TestClient(app)

class TestBookingAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Setup once before all tests."""
        cls.client = client

    def setUp(self):
        """Reset data before each test."""
        bookings.clear()  # Reset bookings to avoid test contamination

    def test_get_classes(self):
        """Test that /classes returns a list of fitness classes."""
        response = self.client.get("/classes")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)
        self.assertIn("name", data[0])

    def test_successful_booking(self):
        """Test booking a class with available slots."""
        class_id = classes[0].id
        payload = {
            "class_id": class_id,
            "client_name": "Alice",
            "client_email": "alice@example.com"
        }
        response = self.client.post("/book", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["class_id"], class_id)
        self.assertEqual(data["client_name"], "Alice")
        self.assertEqual(data["client_email"], "alice@example.com")
        self.assertIn("booked_at", data)

    def test_booking_with_missing_fields(self):
        """Test booking with incomplete data."""
        payload = {"client_name": "Bob"}
        response = self.client.post("/book", json=payload)
        self.assertEqual(response.status_code, 422)  # Unprocessable Entity

    def test_overbooking(self):
        """Test that overbooking is prevented."""
        class_id = classes[1].id
        # Book the class until it’s full
        for i in range(10):
            self.client.post("/book", json={
                "class_id": class_id,
                "client_name": f"User{i}",
                "client_email": f"user{i}@mail.com"
            })

        # One extra booking — should fail
        response = self.client.post("/book", json={
            "class_id": class_id,
            "client_name": "Extra",
            "client_email": "extra@mail.com"
        })
        self.assertEqual(response.status_code, 409)
        self.assertIn("No available slots", response.text)

    def test_get_bookings_by_email(self):
        """Test /bookings returns bookings for a given email."""
        class_id = classes[2].id
        email = "check@user.com"
        self.client.post("/book", json={
            "class_id": class_id,
            "client_name": "Check User",
            "client_email": email
        })

        response = self.client.get(f"/bookings?email={email}")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(any(b["client_email"] == email for b in response.json()))


if __name__ == "__main__":
    unittest.main()
