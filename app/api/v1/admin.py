from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.dependencies.role import require_role
from app.models.profile import Profile
from app.schemas.profile import (
    ProfileResponse,
    UpdateRoleRequest,
)

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


@router.patch(
    "/users/{user_id}/role",
    response_model=ProfileResponse,
    dependencies=[Depends(require_role("admin"))],
)
def update_role(
    user_id: UUID,
    data: UpdateRoleRequest,
    db: Session = Depends(get_db),
):
    user = db.query(Profile).filter(Profile.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    user.role = data.role

    db.commit()
    db.refresh(user)

    return user