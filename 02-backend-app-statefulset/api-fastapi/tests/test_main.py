import os
import unittest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.main import app, get_db, Base
from factories import UserFactory

os.environ["POSTGRES_USER"] = "test_user"
os.environ["POSTGRES_PASSWORD"] = "test_pass"

# Setup an in-memory SQLite database for testing
SQLALCHEMY_DATABSE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABSE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False,
    bind=engine
)

# Dependency override to reroute the session to TestingSessionLocal
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Apply override to Fastappi app
app.dependency_overrides[get_db] = override_get_db

class TestUserAPI(unittest.TestCase):
    """Test User API"""

    def setUp(self):
        Base.metadata.create_all(bind=engine)
        self.client = TestClient(app)
    
    def tearDown(self):
        Base.metadata.drop_all(bind=engine)
    
    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_read_root(self):
        """Test the root endpoint returns the correct message."""
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {"message": "Hello from your k8s cluster!"})

    def test_create_user(self):
        """Test creating a user via POST /users/."""
        resp = self.client.post(
            "/users/",
            params={UserFactory()}
        )


if __name__ == "__main__":
    unittest.main()