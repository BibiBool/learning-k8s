"""
Test Cases for the Appointment Web Service

Create a service that provide medical appointment to users
 - API must be RESTful.
 - The endpoint should be called /providers.
 - Database: PostgreSQL with SQLAlchemy ORM.
 - Methodology: Strict Test-Driven Development (TDD).

Test Specifications:
 1. GET /providers
    - Success (200): Returns a list of all healthcare providers.
    - Success (200): Returns an empty list if no providers exist.
    - Schema: Array of objects: [{"id": int, "name": str, "specialty": str}].

 2. POST /providers
    - Success (201): Creates a new provider and returns the created object.
    - Error (400): Returns error if required fields ('name', 'specialty') are missing.
    - Error (409): Returns error if a provider with the same name already exists.
    - Constraint: Ensure the 'Location' header in the response points to the new resource.

 3. GET /providers/<name>/availability
    - Success (200): Returns available ISO-8601 time slots for a valid provider name.
    - Success (200): Returns an empty list if the provider has no available slots.
    - Error (404): Returns error if the provider name does not exist.

Test Infrastructure:
 - Framework: Pytest using the flask-pytest 'client' fixture.
 - Database Isolation: Tests must run within a transaction rollback or a fresh 
   database instance to ensure idempotent results.
"""
import unittest
from tests import status
from src.provider import app

class ProviderTest(unittest.TestCase):
    """Provider tests"""

    def test_get_providers(self):
        """It should get the list of providers"""
        client = app.test_client()
        result = client.get("/providers")
        self.assertEqual(result.status_code, status.HTTP_200_OK)

    def test_create_a_provider(self):
        """It should create a provider"""
        client = app.test_client()
        result = client.post("/providers")
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)


if __name__ == "__main__":
    unittest.main(verbosity=2)