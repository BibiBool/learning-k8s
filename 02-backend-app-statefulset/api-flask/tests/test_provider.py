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
    - Constraint: Ensure the 'Location' header in the response points to the 
    new resource.

 3. GET /providers/<name>/availability
    - Success (200): Returns available ISO-8601 time slots for a valid provider name.
    - Success (200): Returns an empty list if the provider has no available slots.
    - Error (404): Returns error if the provider name does not exist

Test Infrastructure:
 - Framework: Pytest using the flask-pytest 'client' fixture.
 - Database Isolation: Tests must run within a transaction rollback or a fresh
   database instance to ensure idempotent results.
"""

import pytest

from src.provider import PROVIDERS, app
from tests import status


@pytest.fixture
def client():
    """Fixture to set up the Flask test client and reset data"""
    # Setup: This runs before each test
    app.config.update({"TESTING": True})

    # Resetting the global list (your previous setUp logic)
    PROVIDERS.clear()
    PROVIDERS.extend(
        [
            {"id": 1, "name": "Sanite Belair", "speciality": "Pediatry"},
            {"id": 2, "name": "Catherine Flon", "speciality": "Surgery"},
            {"id": 3, "name": "Toussaint Louverture", "speciality": "Podology"},
        ]
    )

    with app.test_client() as client:
        yield client

    # Teardown (optional): Logic here runs after each test


######################################################################
#  T E S T   C A S E S
######################################################################


def test_get_providers(client):
    """It should get the list of providers"""
    result = client.get("/providers")
    assert result.status_code == status.HTTP_200_OK


def test_create_a_provider(client):
    """It should create a provider"""
    new_provider = {
        "id": 4,
        "name": "Jean-Jacques Dessalines",
        "specialty": "General Medicine",
    }
    result = client.post("/providers", json=new_provider)
    assert result.status_code == status.HTTP_201_CREATED


def test_duplicate_provider(client):
    """It should return an error for duplicates"""
    new_provider = {
        "id": 4,
        "name": "Jean-Jacques Dessalines",
        "specialty": "General Medicine",
    }
    # First request
    result = client.post("/providers", json=new_provider)
    assert result.status_code == status.HTTP_201_CREATED

    # Duplicate request
    result = client.post("/providers", json=new_provider)
    assert result.status_code == status.HTTP_409_CONFLICT
