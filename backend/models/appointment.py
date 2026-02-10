"""
Appointment SQLAlchemy model
"""

from sqlalchemy import Column, Integer, String
from .base import Base


class Appointment(Base):
    """Appointment database model"""
    __tablename__ = "appointments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
