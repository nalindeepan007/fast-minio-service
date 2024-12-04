from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class FileMetadata(Base):
    __tablename__ = "file_metadata"
    id = Column(String, primary_key=True, index=True)
    filename = Column(String(250), unique=True, nullable=False)
    size = Column(Integer, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.now)
    completed = Column(Boolean, default=False)
