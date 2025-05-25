from pydantic import BaseModel, Field
from typing import List

class GetDoctorListItem(BaseModel):
    full_name: str
    id: int

class GetDoctorListResponse(BaseModel):
    doctors: List[GetDoctorListItem]

class CreateAppointmentResponse(BaseModel):
    id: int
    doctor_id: int
    doctor_name: str
    date: str = Field(..., description="Format: yyyy/mm/dd")
    time: str = Field(..., description="Format: hh:mm")
    reason: str
    status: str

class AppointmentResponse(BaseModel):
    id: int
    doctor_id: int
    doctor_name: str
    date: str = Field(..., description="Format: yyyy/mm/dd")
    time: str = Field(..., description="Format: hh:mm")
    reason: str
    status: str

class GetAppointmentListResponse(BaseModel):
    appointments: List[AppointmentResponse]

class CancelAppointmentResponse(BaseModel):
    message: str = "Hủy lịch hẹn thành công"
