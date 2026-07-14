from sqlalchemy.orm import Session

from app.integrations.supabase import supabase
from app.models.profile import Profile
from app.schemas.auth import RegisterRequest, LoginRequest


class AuthService:
    def __init__(self, db: Session):
        self.db = db


    def register(self, data: RegisterRequest):

        # Create user in Supabase Auth
        response = supabase.auth.sign_up(
            {
                "email": data.email,
                "password": data.password,
            }
        )

        user = response.user

        if not user:
            raise Exception("Registration failed")


        # Create profile in our database
        profile = Profile(
            id=user.id,
            email=data.email,
            username=data.username,
            full_name=data.full_name,
            role=None,
            is_premium=False,
        )

        self.db.add(profile)
        self.db.commit()
        self.db.refresh(profile)


        return {
           "access_token": response.session.access_token,
           "refresh_token": response.session.refresh_token,
           "token_type": "bearer",
           "message": "User created"
       }



    def login(self, data: LoginRequest):
        response = supabase.auth.sign_in_with_password(
            {
                "email": data.email,
                "password": data.password,
            }
        )

        session = response.session

        if not session:
            raise Exception("Invalid credentials")

        return session

       