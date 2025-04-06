from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter(
    prefix="/admin"
)