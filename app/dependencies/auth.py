from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.models.profile import Profile
from app.utils.jwt import get_jwks


security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):

    token = credentials.credentials

    try:
        jwks = await get_jwks()
        print(jwks)

        header = jwt.get_unverified_header(token)

        rsa_key = None

        for key in jwks["keys"]:
            if key["kid"] == header["kid"]:
                rsa_key = key
                break

        if not rsa_key:
            raise HTTPException(
                status_code=401,
                detail="Unable to find signing key",
            )


        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=["ES256"],
            audience="authenticated",
        )


        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=401,
                detail="Invalid token",
            )


    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
        )


    user = (
        db.query(Profile)
        .filter(Profile.id == UUID(user_id))
        .first()
    )


    if not user:
        raise HTTPException(
            status_code=404,
            detail="Profile not found",
        )


    return user