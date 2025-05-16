import enum
from sqlalchemy import Column, Date, Enum, ForeignKey, Integer, Time
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
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    status = Column(Enum(AppointmentStatus), nullable=False, default=AppointmentStatus.PENDING)

class ScheduleModel(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    doctor_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    nurse_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
