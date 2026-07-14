from sqlalchemy.orm import Session

from app.models.profile import Profile
from app.schemas.profile import UpdateProfileRequest


class ProfileService:
    @staticmethod
    def get_current_profile(current_user: Profile) -> Profile:
        """
        Return the authenticated user's profile.
        """
        return current_user

    @staticmethod
    def update_profile(
        db: Session,
        current_user: Profile,
        profile_data: UpdateProfileRequest,
    ) -> Profile:
        """
        Update the authenticated user's profile.
        """

        update_data = profile_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(current_user, field, value)

        db.commit()
        db.refresh(current_user)

        return current_user