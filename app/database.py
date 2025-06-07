

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./patient_data.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()    


# class PatientMessage(Base):
#     __tablename__ = 'messages'
#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     mobile = Column(String, index=True)
#     message = Column(String)
#     category = Column(String)
#     confidence = Column(Float)
#     timestamp = Column(DateTime, default=datetime.utcnow)
