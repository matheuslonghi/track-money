from fastapi import APIRouter

from track_money.app.subscription.user._get_user import get_user
from track_money.app.subscription.user._select_plan import select_plan

subscription_router = APIRouter()

subscription_router.add_api_route(
    "/select-plan",
    endpoint=select_plan,
    methods=["POST"],
    response_model=None,
    tags=["subscription"],
    summary="Select a plan for the user",
)

subscription_router.add_api_route(
    "/user",
    endpoint=get_user,
    methods=["GET"],
    response_model=None,
    tags=["subscription"],
    summary="Get the current user's subscription details",
)
