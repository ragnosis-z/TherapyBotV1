"""Error Log Model"""

from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime

from app.database import Base


class ErrorLog(Base):
    """Error log model for tracking system defects and halts"""

    __tablename__ = "error_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Error details
    error_type = Column(String(100), nullable=False)  # e.g., 'DatabaseError', 'SystemHalt'
    error_message = Column(Text, nullable=False)
    stack_trace = Column(Text, nullable=True)
    
    # Context
    module_name = Column(String(255), nullable=True)
    severity = Column(String(50), default="error")  # warning, error, critical
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<ErrorLog(id={self.id}, type={self.error_type}, severity={self.severity})>"
