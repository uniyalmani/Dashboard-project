import enum
from typing import Optional
from sqlmodel import Enum, Field, SQLModel
from sqlalchemy import UniqueConstraint, String
from sqlalchemy import Column




class TaskStatuses(enum.Enum):
    completed = "completed"
    pending = "pending"
    not_picked = "not_picked"

    def __str__(self):
        return self.value


class Admin(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    email: str = Field(sa_column=Column("email", String(40), unique=True))
    password: str


class Manager(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    email: str = Field(sa_column=Column("email", String(40), unique=True))
    password: str
    admin_id: Optional[int] = Field(default=None, foreign_key="admin.id")


class Devloper(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    email: str = Field(sa_column=Column("email", String(40), unique=True))
    password: str
    manager_id: Optional[int] = Field(default=None, foreign_key="manager.id")


class Task(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    description: str
    status: TaskStatuses = Field(sa_column=Column(Enum(TaskStatuses)))
    devloper_id: Optional[int] = Field(default=None, foreign_key="devloper.id")
