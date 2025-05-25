from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from typing import Annotated
from datetime import datetime

from config.database import get_db
from config.security import verify_access_token
from patient_service.response import (
    GetDoctorListItem,
    GetDoctorListResponse,
    CreateAppointmentResponse,
    GetAppointmentListResponse,
    AppointmentResponse,
    CancelAppointmentResponse
)
from patient_service.request import CreateAppointmentRequest
from patient_service.model import AppointmentModel, AppointmentStatus
from user_service.model import UserModel, UserRole
from utils.jwt import TokenClaims

router = APIRouter(prefix="/patient", tags=["Patient"])

@router.get(path="/doctor-list", status_code=status.HTTP_200_OK, response_model=GetDoctorListResponse)
async def get_doctor_list(
    session: Annotated[AsyncSession, Depends(get_db)],
    claims: Annotated[TokenClaims, Depends(verify_access_token)],
):
    allowed_roles = [UserRole.PATIENT, UserRole.ADMIN]
    if claims.role not in allowed_roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Không có quyền truy cập")
    result = await session.execute(
        select(UserModel).where(UserModel.role == UserRole.DOCTOR)
    )
    doctors = result.scalars().all()
    doctor_list = [
        GetDoctorListItem(full_name=doctor.full_name, id=doctor.id) # type: ignore
        for doctor in doctors
    ]
    return GetDoctorListResponse(doctors=doctor_list)

@router.post(path="/appointment", status_code=status.HTTP_201_CREATED, response_model=CreateAppointmentResponse)
async def create_appointment(
    request: CreateAppointmentRequest,
    session: Annotated[AsyncSession, Depends(get_db)],
    claims: Annotated[TokenClaims, Depends(verify_access_token)],
):
    if claims.role != UserRole.PATIENT:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Chỉ bệnh nhân mới có thể đặt lịch khám")

    # Verify doctor exists and is a doctor
    doctor = await session.execute(
        select(UserModel).where(
            UserModel.id == request.doctor_id,
            UserModel.role == UserRole.DOCTOR
        )
    )
    doctor = doctor.scalar_one_or_none()
    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy bác sĩ")

    # Convert date and time strings to datetime
    appointment_datetime = datetime.strptime(f"{request.date} {request.time}", "%Y/%m/%d %H:%M")

    # Create appointment
    appointment = AppointmentModel(
        patient_id=claims.id,
        doctor_id=request.doctor_id,
        time=appointment_datetime,
        reason=request.reason,
        status=AppointmentStatus.PENDING
    )
    session.add(appointment)
    await session.commit()
    await session.refresh(appointment)

    return CreateAppointmentResponse(
        id=appointment.id,  # type: ignore
        doctor_id=doctor.id,  # type: ignore
        doctor_name=doctor.full_name,  # type: ignore
        date=appointment.time.strftime("%Y/%m/%d"),  # type: ignore
        time=appointment.time.strftime("%H:%M"),  # type: ignore
        reason=appointment.reason,  # type: ignore
        status=appointment.status.value  # type: ignore
    )

@router.get(path="/appointments", status_code=status.HTTP_200_OK, response_model=GetAppointmentListResponse)
async def get_appointments(
    session: Annotated[AsyncSession, Depends(get_db)],
    claims: Annotated[TokenClaims, Depends(verify_access_token)],
):
    if claims.role != UserRole.PATIENT:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Chỉ bệnh nhân mới có thể xem lịch hẹn của mình")

    # Get appointments for the logged-in patient
    query = select(AppointmentModel).where(AppointmentModel.patient_id == claims.id)
    result = await session.execute(query)
    appointments = result.scalars().all()

    # Get doctor information for each appointment
    appointment_list = []
    for appointment in appointments:
        # Get doctor info
        doctor = await session.execute(
            select(UserModel).where(UserModel.id == appointment.doctor_id)
        )
        doctor = doctor.scalar_one_or_none()

        if doctor:
            appointment_list.append(
                AppointmentResponse(
                    id=appointment.id,  # type: ignore
                    doctor_id=doctor.id,  # type: ignore
                    doctor_name=doctor.full_name,  # type: ignore
                    date=appointment.time.strftime("%Y/%m/%d"),  # type: ignore
                    time=appointment.time.strftime("%H:%M"),  # type: ignore
                    reason=appointment.reason,  # type: ignore
                    status=appointment.status.value  # type: ignore
                )
            )

    return GetAppointmentListResponse(appointments=appointment_list)

@router.delete(path="/appointment/{appointment_id}", status_code=status.HTTP_200_OK, response_model=CancelAppointmentResponse)
async def cancel_appointment(
    appointment_id: int,
    session: Annotated[AsyncSession, Depends(get_db)],
    claims: Annotated[TokenClaims, Depends(verify_access_token)],
):
    if claims.role != UserRole.PATIENT:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Chỉ bệnh nhân mới có thể hủy lịch hẹn")

    # Get the appointment
    appointment = await session.execute(
        select(AppointmentModel).where(
            AppointmentModel.id == appointment_id,
            AppointmentModel.patient_id == claims.id
        )
    )
    appointment = appointment.scalar_one_or_none()

    if not appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy lịch hẹn")

    if appointment.status == AppointmentStatus.CANCELLED: # type: ignore
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Lịch hẹn đã được hủy trước đó")

    if appointment.status == AppointmentStatus.COMPLETED:  # type: ignore
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Không thể hủy lịch hẹn đã hoàn thành")

    # Update appointment status to cancelled
    appointment.status = AppointmentStatus.CANCELLED # type: ignore
    await session.commit()

    return CancelAppointmentResponse()
