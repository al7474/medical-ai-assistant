"""
Appointment endpoints
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from models import Appointment, User
from schemas.appointment import AppointmentCreate, AppointmentRead
from api.deps import get_db

router = APIRouter(prefix="/appointments", tags=["appointments"])


@router.post("/", response_model=AppointmentRead)
async def create_appointment(
    appointment: AppointmentCreate, 
    db: AsyncSession = Depends(get_db)
):
    """Create a new appointment"""
    # Verify user exists
    user_result = await db.execute(
        select(User).where(User.id == appointment.user_id)
    )
    user = user_result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    new_appointment = Appointment(
        user_id=appointment.user_id,
        description=appointment.description
    )
    db.add(new_appointment)
    await db.commit()
    await db.refresh(new_appointment)
    return new_appointment


@router.get("/", response_model=List[AppointmentRead])
async def list_appointments(db: AsyncSession = Depends(get_db)):
    """List all appointments"""
    result = await db.execute(select(Appointment))
    appointments = result.scalars().all()
    return appointments


@router.get("/{appointment_id}", response_model=AppointmentRead)
async def get_appointment(
    appointment_id: int, 
    db: AsyncSession = Depends(get_db)
):
    """Get a specific appointment by ID"""
    result = await db.execute(
        select(Appointment).where(Appointment.id == appointment_id)
    )
    appointment = result.scalar_one_or_none()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment


@router.delete("/{appointment_id}")
async def delete_appointment(
    appointment_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete an appointment"""
    result = await db.execute(
        select(Appointment).where(Appointment.id == appointment_id)
    )
    appointment = result.scalar_one_or_none()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    await db.delete(appointment)
    await db.commit()
    return {"message": "Appointment deleted successfully", "id": appointment_id}
