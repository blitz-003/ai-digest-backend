from fastapi import Depends, HTTPException, status

from app.dependencies.auth import get_current_user
from app.models.profile import Profile


def require_role(*roles: str):
    def role_checker(
        current_user: Profile = Depends(get_current_user),
    ) -> Profile:

        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action.",
            )

        return current_user

    return role_checker