from fastapi import APIRouter
from api import test

api_router = APIRouter(prefix='/api')
api_router.include_router(test.router1)
