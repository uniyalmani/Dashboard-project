from urllib import response
from fastapi import APIRouter, Depends, Request, Response, Form
from sqlmodel import Session, select, or_
from typing import Dict
from app.utilities.dependencies import get_decoded_token_data, get_session
from app.utilities.helper import verify_password, create_jwt_token, decode_token
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.models.database_model import Manager, Devloper, Task
from fastapi.responses import RedirectResponse
from datetime import datetime
from app.utilities.decorators import auth_required
import json
from sqlalchemy import func

templates = Jinja2Templates(directory="app/templates/manager")


router = APIRouter()


@router.get("/Manager/dashboard", tags=["dashboard"], response_class=HTMLResponse)
@auth_required("Manager")
def manager_dashboard(
    request: Request,
    decode_existing_token: dict = Depends(get_decoded_token_data),
    session: dict = Depends(get_session),
):
    email = decode_existing_token["email"]
    role = decode_existing_token["role"]

    query = select(Manager).where(Manager.email == email)
    manager_info = session.exec(query).first()

    query = select(func.count(Devloper.id)).where(
        Devloper.manager_id == manager_info.id
    )
    devloper_count = session.exec(query).all()

    query = select(func.count(Manager.id))
    manager_count = session.exec(query).all()

    query = select(func.count(Task.id))
    task_count = session.exec(query).all()

    data = {
        "devloper_count": devloper_count[0],
        "manager_count": manager_count[0],
        "total_employee": devloper_count[0] + manager_count[0],
        "task_count": task_count[0],
    }

    return templates.TemplateResponse(
        "dashboard.html",
        context={"request": request, "data": data, "manager_info": manager_info},
    )


@router.get("/Manager/dashboard/tasks", tags=["dashboard"], response_class=HTMLResponse)
@auth_required("Manager")
def manager_tasks(
    request: Request,
    decode_existing_token: dict = Depends(get_decoded_token_data),
    session: dict = Depends(get_session),
):
    email = decode_existing_token["email"]
    role = decode_existing_token["role"]

    query = select(Manager).where(Manager.email == email)
    manager_info = session.exec(query).first()

    user = select(Manager).where(Manager.email == email)
    user = session.exec(user).first()

    query = (
        select(Task, Devloper)
        .join(Devloper, isouter=True)
        .where(or_(Task.devloper_id == None, Devloper.manager_id == user.id))
    )
    tasks_info = session.exec(query).all()
    dev = select(Devloper).where(Devloper.manager_id == user.id)
    devlopers = session.exec(dev).all()

    print(tasks_info, devlopers)

   

    return templates.TemplateResponse(
        "task_list.html",
        context={
            "request": request,
            "data": tasks_info,
            "devlopers": devlopers,
            "manager_info": manager_info,
        },
    )


@router.get("/Manager/dashboard/devlopers/{task_id}/{devloper_id}", tags=["assign_to"])
@auth_required("Manager")
def assign_devloper_to(
    request: Request,
    task_id,
    devloper_id,
    decode_existing_token: Dict = Depends(get_decoded_token_data),
    session: dict = Depends(get_session),
):
   
    query_task = select(Task).where(Task.id == task_id)
    task = session.exec(query_task).first()
    task.devloper_id = devloper_id
    session.add(task)
    session.commit()

    return RedirectResponse("/Manager/dashboard/tasks", status_code=303)


@router.get(
    "/Manager/dashboard/devlopers",
    tags=["manager_dashboard_devloper_list"],
    response_class=HTMLResponse,
)
@auth_required("Manager")
def manager_devlopers_list(
    request: Request,
    decode_existing_token: Dict = Depends(get_decoded_token_data),
    session: dict = Depends(get_session),
):
    email = decode_existing_token["email"]
    role = decode_existing_token["role"]

    query = select(Manager).where(Manager.email == email)
    manager_info = session.exec(query).first()

    user = select(Manager).where(Manager.email == email)
    user = session.exec(user).first()
    query = select(Devloper).where(Devloper.manager_id == user.id)
    devlopers = session.exec(query).all()
    print(devlopers, "devlopers")

    return templates.TemplateResponse(
        "devloper_list.html",
        context={
            "request": request,
            "devlopers": devlopers,
            "manager_info": manager_info,
        },
    )
