import enum
from sqlalchemy import Integer, String
import sqlalchemy
from sqlalchemy.schema import Column
from config.database import Base


class UserRole(str, enum.Enum):
    PATIENT = "patient"
    DOCTOR = "doctor"
    NURSE = "nurse"
    ADMIN = "ADMIN"
    PHARMACIST = "PHARMACIST"
    INSURANCE_PROVIDER = "insurance_provider"

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    role = Column(sqlalchemy.Enum(UserRole), nullable=False, default=UserRole.PATIENT)
