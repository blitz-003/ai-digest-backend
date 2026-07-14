from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_user
from app.dependencies.database import get_db
from app.models.profile import Profile
from app.schemas.profile import ProfileResponse, UpdateProfileRequest
from app.services.profile_service import ProfileService

router = APIRouter(prefix="/profiles", tags=["Profiles"])


@router.get(
    "/me",
    response_model=ProfileResponse,
)
def get_my_profile(
    current_user: Profile = Depends(get_current_user),
):
    return ProfileService.get_current_profile(current_user)


@router.patch(
    "/me",
    response_model=ProfileResponse,
)
def update_my_profile(
    profile_data: UpdateProfileRequest,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user),
):
    return ProfileService.update_profile(
        db=db,
        current_user=current_user,
        profile_data=profile_data,
    )