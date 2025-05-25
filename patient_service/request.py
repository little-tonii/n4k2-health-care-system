from datetime import datetime
from pydantic import BaseModel, validator


class CreateAppointmentRequest(BaseModel):
    doctor_id: int
    date: str  # format: yyyy/mm/dd
    time: str  # format: hh:mm
    reason: str

    @validator('date')
    def validate_date(cls, v):
        try:
            datetime.strptime(v, '%Y/%m/%d')
            return v
        except ValueError:
            raise ValueError('Date must be in format yyyy/mm/dd')

    @validator('time')
    def validate_time(cls, v):
        try:
            datetime.strptime(v, '%H:%M')
            return v
        except ValueError:
            raise ValueError('Time must be in format hh:mm')
