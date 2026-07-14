from datetime import datetime
from uuid import UUID
from typing import Literal

from pydantic import BaseModel, ConfigDict


class ProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: str
    username: str
    full_name: str | None = None
    avatar_url: str | None = None
    bio: str | None = None
    role: str | None = None
    is_premium: bool
    created_at: datetime
    updated_at: datetime


class UpdateProfileRequest(BaseModel):
    username: str | None = None
    full_name: str | None = None
    avatar_url: str | None = None
    bio: str | None = None


class UpdateRoleRequest(BaseModel):
    role: Literal["reader", "author"]