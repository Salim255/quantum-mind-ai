# app/db/session.py

# ---------------------------------------------------------
# SQLAlchemy imports
# ---------------------------------------------------------
# create_engine  → creates the connection engine to PostgreSQL
# sessionmaker   → factory that generates database sessions
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# ---------------------------------------------------------
# DATABASE_URL: PostgreSQL connection string
# ---------------------------------------------------------
# Format:
#   postgresql://USERNAME:PASSWORD@HOST:PORT/DATABASE
#
# Example:
#   postgresql://postgres:mysecretpassword@localhost:5432/mydb
#
# IMPORTANT:
# - Never hardcode credentials in production
# - Use environment variables (.env) instead
# - This is fine for local development
#
DATABASE_URL = "postgresql://postgres:password@localhost:5432/mydb"

# ---------------------------------------------------------
# ENGINE: the core database connection object
# ---------------------------------------------------------
# create_engine() establishes the connection to PostgreSQL.
#
# pool_pre_ping=True:
#   - Ensures SQLAlchemy checks if a connection is still alive
#   - Prevents "connection closed" errors after long inactivity
#   - Recommended for production setups
#
# No connect_args needed for PostgreSQL (only for SQLite)
#
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

# ---------------------------------------------------------
# SessionLocal: session factory
# ---------------------------------------------------------
# autocommit=False:
#   - You must explicitly call db.commit()
#   - Gives you full control over transactions
#
# autoflush=False:
#   - Prevents SQLAlchemy from automatically flushing changes
#   - Avoids unexpected queries being executed too early
#
# bind=engine:
#   - Connects this session factory to your PostgreSQL engine
#
# Every request in FastAPI will use its own session instance.
#
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# ---------------------------------------------------------
# get_db(): FastAPI dependency that provides a DB session
# ---------------------------------------------------------
# This function is used with FastAPI's Depends() system.
#
# How it works:
# - A new database session is created for each incoming request
# - yield gives the session to the route handler
# - finally ensures the session is closed after the request ends
#
# This pattern ensures:
# - No session leaks
# - Clean, isolated transactions per request
# - Production‑grade resource management
#

def get_db():
    # Create a new database session for the current request
    db = SessionLocal()
    try:
        # Provide the session to the route handler
        yield db
    finally:
        # Always close the session after the request finishes
        db.close()