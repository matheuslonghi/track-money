import logging

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from track_money.app.authentication import user_router
from track_money.app.domain_exception import DomainException
from track_money.app.infra.database import create_tables, init_database
from track_money.app.movement import movement_router
from track_money.app.subscription import subscription_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()  # Load environment variables from .env file  
init_database()  # Initialize the database connection
create_tables()  # Create the necessary tables in the database

app = FastAPI(
    title="Track Money",
    description="A simple app to track your money",
    version="0.1.0",
)

app.include_router(
    user_router, 
    prefix="/users",
)

app.include_router(
    subscription_router,
    prefix="/subscriptions",
)

app.include_router(
    movement_router,
    prefix="/movements",
)

@app.exception_handler(DomainException)
async def domain_exception_handler(request: Request, exc: DomainException):
    logger.warning(f"DomainException occurred: {exc.message}")

    return JSONResponse(
        status_code=400,
        content={"message": exc.message},
    )


@app.get("/health")
async def health_check():
    return JSONResponse(content={"status": "ok"})


if __name__ == '__main__':
    import uvicorn
    
    uvicorn.run(app, host="0.0.0.0", port=8000)