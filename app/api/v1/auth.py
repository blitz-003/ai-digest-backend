from fastapi import APIRouter, Depends, Response, status, Request
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_user
from app.dependencies.database import get_db
from app.models.profile import Profile
from app.schemas.auth import (
    LoginRequest,
    MessageResponse,
    RegisterRequest,
    LoginResponse,
)
from app.schemas.profile import ProfileResponse
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=MessageResponse,
)
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db),
):
    service = AuthService(db)
    return service.register(data)


@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
)
def login(
    data: LoginRequest,
    response: Response,
    db: Session = Depends(get_db),
):
    service = AuthService(db)

    session = service.login(data)

    response.set_cookie(
        key="access_token",
        value=session.access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=60 * 60,
    )

    response.set_cookie(
        key="refresh_token",
        value=session.refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=60 * 60 * 24 * 30,
    )

    return {
        "message": "Login successful"
    }


@router.post(
    "/logout",
    response_model=MessageResponse,
)
def logout(
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    service = AuthService(db)

    access_token = request.cookies.get("access_token")

    if access_token:
        try:
            service.logout(access_token)
        except Exception:
            # Even if Supabase logout fails,
            # we still clear browser cookies.
            pass

    response.delete_cookie(
        key="access_token"
    )

    response.delete_cookie(
        key="refresh_token"
    )

    return {
        "message": "Logged out successfully"
    }


@router.get(
    "/me",
    response_model=ProfileResponse,
)
def me(
    current_user: Profile = Depends(get_current_user),
):
    return current_user