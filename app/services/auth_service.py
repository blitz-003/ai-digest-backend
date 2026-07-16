from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.integrations.supabase import supabase
from app.models.profile import Profile
from app.schemas.auth import RegisterRequest, LoginRequest


class AuthService:
    def __init__(self, db: Session):
        self.db = db


    def register(self, data: RegisterRequest):
        try:
            # Create user in Supabase Auth
            response = supabase.auth.sign_up(
                {
                    "email": data.email,
                    "password": data.password,
                }
            )

            user = response.user

            if not user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Registration failed",
                )

            # Create profile in our database
            profile = Profile(
                id=user.id,
                email=data.email,
                username=data.username,
                full_name=data.full_name,
                role="reader",
                is_premium=False,
            )

            self.db.add(profile)
            self.db.commit()
            self.db.refresh(profile)

            return {
                "access_token": response.session.access_token,
                "refresh_token": response.session.refresh_token,
                "token_type": "bearer",
                "message": "User created",
            }

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e),
            )

    def login(self, data: LoginRequest):
        try:
            response = supabase.auth.sign_in_with_password(
                {
                    "email": data.email,
                    "password": data.password,
                }
            )

            session = response.session

            if not session:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid email or password",
                )

            return session

        except HTTPException:
            raise

        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

    def logout(self, access_token: str):
        supabase.auth.sign_out(access_token)

        return {
            "message": "Logged out successfully"
        }