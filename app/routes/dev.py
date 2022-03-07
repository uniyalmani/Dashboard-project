from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class DevSignUp(BaseModel):
    email:str
    password:int
    con_password:int

class DevLogIn(BaseModel):
    email:str
    password:int



@router.post("/devsignup",tags=["devsignup"])
async def devsignup(devsignup:DevSignUp):
    return devsignup


@router.get("/devlogin", tags=["devlogin"])
async def devlogin(devlogin:DevLogIn):
    return devsignup