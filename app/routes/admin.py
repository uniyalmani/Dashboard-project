from fastapi import APIRouter
from pydantic import BaseModel
from app.utilities import helper
router = APIRouter()

class AdminLogIn(BaseModel):
    email:str
    password:int

@router.get("/adminlogin",tags=["adminlogin"])
async def adminlogin(adminlogin:AdminLogIn):
    return adminlogin
