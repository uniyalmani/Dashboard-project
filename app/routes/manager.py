from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class ManagerLogIn(BaseModel):
    email:str
    password:int

@router.get("/managerlogin",tags=["managerlogin "])
async def managerlogin(managerlogin:ManagerLogIn):
    return managerlogin