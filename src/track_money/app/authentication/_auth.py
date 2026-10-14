import os
from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from track_money.app.authentication._user import User


def generate_jwt_token(user: User) -> str:
     """Generate a JWT token for the user"""
     if not os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"):
         raise ValueError("ACCESS_TOKEN_EXPIRE_MINUTES environment variable is not set")

     expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
     expire = datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)

     if not os.getenv("SECRET_KEY"):
         raise ValueError("SECRET_KEY environment variable is not set")
     if not os.getenv("ALGORITHM"):
         raise ValueError("ALGORITHM environment variable is not set")

     payload = {
         "sub": user.email,
         "name": user.name,
         "exp": expire
     }
     token = jwt.encode(payload, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))
     return token