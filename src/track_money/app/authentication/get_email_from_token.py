import os

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt


def get_email_from_token(token: str = Depends(OAuth2PasswordBearer(tokenUrl="users/token"))) -> str:
    """Decode the JWT token and return the email"""
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        email: str = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        return email
    except Exception:
        raise HTTPException(status_code=401, detail="Could not validate credentials")