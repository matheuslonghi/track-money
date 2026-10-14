from fastapi import APIRouter

from track_money.app.authentication._create_token import create_token
from track_money.app.authentication._get_user_profile import (
    UserProfileResponse,
    get_user_profile,
)
from track_money.app.authentication._register_user import register_user

user_router = APIRouter()

user_router.add_api_route(
    "/",
    endpoint=register_user,
    methods=["POST"],
    response_model=None,
    tags=["users"],
    summary="Create a new user",
)

user_router.add_api_route(
    "/token",
    endpoint=create_token,
    methods=["POST"],
    response_model=None,
    tags=["users"],
    summary="Create a JWT token for the user",
)

user_router.add_api_route(
    "/profile",
    endpoint=get_user_profile,
    methods=["GET"],
    response_model=UserProfileResponse,
    tags=["users"],
    summary="Get the user profile based on the JWT token",
)