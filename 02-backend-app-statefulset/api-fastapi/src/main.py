import os 
import time
import logging
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase
from sqlalchemy.exc import OperationalError

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Databse config
DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_NAME = os.getenv("POSTGRES_DB")

SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

# SLQAlchey setup
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Database Model
class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)

# Retry Logic for Table Creation
# This prevents the app from crashing if Postgres is still booting up
def create_tables_with_retry(max_retries=5, delay=5):
    for i in range(max_retries):
        try:
            logger.info(f"Connecting to database (Attempt {i+1}/{max_retries})...")
            Base.metadata.create_all(bind=engine)
            logger.info("Tables created successfully.")
            return
        except OperationalError as e:
            if i == max_retries - 1:
                logger.error("Could not connect to database after several attempts.")
                raise e
            logger.warning(f"Database not ready, retrying in {delay} seconds...")
            time.sleep(delay)

# Create the application instance
app = FastAPI()

@app.on_event("startup")
def on_startup():
    # This only runs when the server starts, not during unit tests
    create_tables_with_retry()

# 5. Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API Endpoints
@app.get("/")
async def read_root():
    """
    Handles GET requests to the root URL (/).
    Returns a simple JSON message.
    """
    return {"message": "Hello from your k8s cluster!"}

# Health Check Endpoint for Kubernetes Probes
@app.get("/healthz")
async def health_check():
    """
    Returns 200 OK to tell Kubernetes the container is healthy.
    """
    return {"status": "ok"}

@app.get("/db-test")
def test_db_connection(db: Session = Depends(get_db)):
    try:
        # Simple query to check if connection is alive
        result = db.execute(text("SELECT 1"))
        return {"database_status": "Connected", "result": result.fetchone()[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")

@app.post("/users/")
def create_user(name: str, email: str, db: Session = Depends(get_db)):
    new_user = User(name=name, email=email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user