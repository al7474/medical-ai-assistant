"""
Medical Profile API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models import User, MedicalProfile
from schemas.medical_profile import (
    MedicalProfileCreate,
    MedicalProfileUpdate,
    MedicalProfileResponse,
    MedicalProfileContext
)
from api.deps import get_db, get_current_user

router = APIRouter(prefix="/medical-profile", tags=["medical-profile"])


@router.post("/", response_model=MedicalProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_medical_profile(
    profile_data: MedicalProfileCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Create medical profile for current user
    
    **Required authentication**
    """
    # Check if profile already exists
    result = await db.execute(
        select(MedicalProfile).where(MedicalProfile.user_id == current_user.id)
    )
    existing_profile = result.scalar_one_or_none()
    
    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Medical profile already exists. Use PUT to update."
        )
    
    # Convert medications and surgeries to dict format
    medications_dict = [med.model_dump() for med in (profile_data.current_medications or [])]
    surgeries_dict = [surg.model_dump() for surg in (profile_data.past_surgeries or [])]
    emergency_contact_dict = profile_data.emergency_contact.model_dump() if profile_data.emergency_contact else {}
    
    # Create profile
    profile = MedicalProfile(
        user_id=current_user.id,
        blood_type=profile_data.blood_type,
        height_cm=profile_data.height_cm,
        weight_kg=profile_data.weight_kg,
        date_of_birth=profile_data.date_of_birth,
        allergies=profile_data.allergies or [],
        chronic_conditions=profile_data.chronic_conditions or [],
        current_medications=medications_dict,
        past_surgeries=surgeries_dict,
        family_history=profile_data.family_history or {},
        smoking_status=profile_data.smoking_status,
        alcohol_consumption=profile_data.alcohol_consumption,
        exercise_frequency=profile_data.exercise_frequency,
        emergency_contact=emergency_contact_dict,
        notes=profile_data.notes
    )
    
    db.add(profile)
    await db.commit()
    await db.refresh(profile)
    
    return profile


@router.get("/me", response_model=MedicalProfileResponse)
async def get_my_medical_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get medical profile for current user
    
    **Required authentication**
    """
    result = await db.execute(
        select(MedicalProfile).where(MedicalProfile.user_id == current_user.id)
    )
    profile = result.scalar_one_or_none()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medical profile not found. Create one first."
        )
    
    return profile


@router.put("/me", response_model=MedicalProfileResponse)
async def update_my_medical_profile(
    profile_data: MedicalProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update medical profile for current user
    
    **Required authentication**
    """
    result = await db.execute(
        select(MedicalProfile).where(MedicalProfile.user_id == current_user.id)
    )
    profile = result.scalar_one_or_none()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medical profile not found. Create one first."
        )
    
    # Update only provided fields
    update_data = profile_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(profile, field, value)
    
    await db.commit()
    await db.refresh(profile)
    
    return profile


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_my_medical_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete medical profile for current user
    
    **Required authentication**
    """
    result = await db.execute(
        select(MedicalProfile).where(MedicalProfile.user_id == current_user.id)
    )
    profile = result.scalar_one_or_none()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medical profile not found"
        )
    
    await db.delete(profile)
    await db.commit()


@router.get("/me/context", response_model=MedicalProfileContext)
async def get_my_profile_context(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get simplified medical profile context for AI
    
    Returns only relevant, non-null information suitable for AI context.
    
    **Required authentication**
    """
    result = await db.execute(
        select(MedicalProfile).where(MedicalProfile.user_id == current_user.id)
    )
    profile = result.scalar_one_or_none()
    
    if not profile:
        return MedicalProfileContext()
    
    return MedicalProfileContext(**profile.to_context_dict())
