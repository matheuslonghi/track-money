from fastapi import Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from track_money.app.authentication._user import User
from track_money.app.authentication._user_repository import (
    UserRepository,
    get_user_repository,
)


class UserCreate(BaseModel):
    email: str
    name: str
    password: str


def register_user(body: UserCreate, user_repository: UserRepository = Depends(get_user_repository)):
    """Create a new user."""
    if user_repository.get_by_email(body.email):
        return JSONResponse(
        status_code=400,
        content={"message": "User with this email already exists."},
    )
    
    user = User(name=body.name, email=body.email, password=body.password)
    user_repository.create(user)

    return JSONResponse(
        status_code=201,
        content=None,
        headers={"Location": f"/users/{user.id}"},
    )