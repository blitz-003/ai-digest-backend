from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.dependencies.auth import get_current_user
from app.models.profile import Profile
from app.schemas.profile import (
    UpdateRoleRequest,
    ProfileResponse,
)
from app.services.profile_service import ProfileService


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.patch(
    "/me/role",
    response_model=ProfileResponse,
)
def update_role(
    data: UpdateRoleRequest,
    current_user: Profile = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    service = ProfileService(db)

    return service.update_role(
        current_user,
        data.role
    )