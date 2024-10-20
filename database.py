from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Construct the DATABASE_URL incorporating the encoded password
DATABASE_URL = f"mysql+aiomysql://root:admin@localhost:3306/provet"

# Create an asynchronous engine with echo=True for SQL query logging
engine = create_async_engine(DATABASE_URL, echo=True)

# Configure sessionmaker for creating AsyncSession instances
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)

# Base class for declarative class definitions
Base = declarative_base()