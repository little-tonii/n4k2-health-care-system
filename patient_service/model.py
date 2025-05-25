import enum
from sqlalchemy import Column, Enum, ForeignKey, Integer, DateTime, String
from config.database import Base

class AppointmentStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    RESCHEDULED = "rescheduled"
    COMPLETED = "completed"

class AppointmentModel(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    patient_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    time = Column(DateTime, nullable=False)
    reason = Column(String, nullable=False)
    status = Column(Enum(AppointmentStatus), nullable=False, default=AppointmentStatus.PENDING)
