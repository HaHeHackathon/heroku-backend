from sqlalchemy import create_engine, Column, String, Integer, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./bus_info.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class BusInfo(Base):
    __tablename__ = "bus_info"

    id = Column(Integer, primary_key=True, index=True)
    bus_line = Column(String, index=True)
    route = Column(String)
    total_stations = Column(Integer)
    stations = Column(JSON)

# Create the database tables
Base.metadata.create_all(bind=engine)