from typing import Optional
from sqlmodel import Field, SQLModel
print("-----------------")
print("inside database_model.py")


class Admin(SQLModel, table = True):
    id:Optional[int] = Field(primary_key=True)
    name:str
    email:str
    password:str

class Manager(SQLModel, table=True):
    id:Optional[int] = Field(primary_key=True)
    name:str
    email:str
    password:str
    admin_id:Optional[int] = Field(default = None, foreign_key = "admin.id")

class Devloper(SQLModel, table = True):
    id: Optional[int] = Field(primary_key=True)
    name: str
    email: str
    password: str
    manager_id: Optional[int] = Field(default = None, foreign_key = "manager.id")

class Task(SQLModel, table = True):
    id: Optional[int] = Field(primary_key=True)
    name: str
    description: str
    status: str
    devloper_id: Optional[int] = Field(default = None, foreign_key = "devloper.id")
  
