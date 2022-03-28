import email
from urllib import response
from fastapi import APIRouter, Depends, Request, Response, Form
from sqlmodel import Session, select, or_
from typing import Dict
from app.utilities.dependencies import get_decoded_token_data, get_session
from app.utilities.helper import verify_password, create_jwt_token
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.models.database_model import *
from fastapi.responses import RedirectResponse
from datetime import datetime
from app.utilities.decorators import auth_required
from sqlalchemy import func
import json


router = APIRouter()

templates = Jinja2Templates(directory="app/templates/admin")


@router.get("/Admin/dashboard", tags=["admin_dashboard"], response_class=HTMLResponse)
# @auth_required("Admin")
def admin_dashboard(
    request: Request,
    decode_existing_token: Dict = Depends(get_decoded_token_data),
    session: dict = Depends(get_session),
):
    email = decode_existing_token["email"]
    query = select(func.count(Devloper.id))
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

    print(devloper_count, manager_count, task_count)
    return templates.TemplateResponse(
        "dashboard.html", context={"request": request, "data": data, "email": email}
    )


@router.get(
    "/Admin/dashboard/tasks",
    tags=["admin_dashboard_tasks"],
    response_class=HTMLResponse,
)
@auth_required("Admin")
def admin_dashboard_tasks(
    request: Request,
    decode_existing_token: Dict = Depends(get_decoded_token_data),
    session: dict = Depends(get_session),
):
    email = decode_existing_token["email"]
    query = select(Task)
    query_res = session.exec(query).all()
    return templates.TemplateResponse(
        "task_list.html",
        context={"request": request, "data": query_res, "email": email},
    )


@router.post("/task/add", tags=["add_task"])
@auth_required("Admin")
def add_task(
    request: Request,
    name: str = Form(...),
    description: str = Form(...),
    decode_existing_token: Dict = Depends(get_decoded_token_data),
    session: dict = Depends(get_session),
):
    email = decode_existing_token["email"]
    task_entry = Task(name=name, description=description, status="not_picked")
    session.add(task_entry)
    session.commit()
    print(task_entry)
    return RedirectResponse("/Admin/dashboard/tasks", status_code=303)


@router.get("/Admin/dashboard/task/{task_id}")
@auth_required("Admin")
def delete_task(
    request: Request,
    task_id,
    decode_existing_token: Dict = Depends(get_decoded_token_data),
    session: dict = Depends(get_session),
):
    email = decode_existing_token["email"]
    query = select(Task).where(Task.id == task_id)
    task_to_delete = session.exec(query).first()
    print(task_to_delete)
    session.delete(task_to_delete)
    session.commit()
    return RedirectResponse("/Admin/dashboard/tasks", status_code=303)


@router.get(
    "/Admin/dashboard/devlopers",
    tags=["admin_dashboard_devloper_list"],
    response_class=HTMLResponse,
)
@auth_required("Admin")
def admin_dashboard_devlopers(
    request: Request,
    decode_existing_token: Dict = Depends(get_decoded_token_data),
    session: dict = Depends(get_session),
):
    query = (
        select(Devloper, Manager)
        .join(Manager, isouter=True)
        .where(or_(Devloper.manager_id == None, Devloper.manager_id == Manager.id))
    )
    manager_info = session.exec(query).all()
    email = decode_existing_token["email"]
    print(manager_info, " *******************/")
    # query = select(Manager)
    # managers = session.exec(query).all()
    query = select(Manager)
    managers = session.exec(query).all()
    # print(managers, "//////")
    # print(devlopers)
    return templates.TemplateResponse(
        "devloper_list.html",
        context={
            "request": request,
            "data": manager_info,
            "managers": managers,
            "email": email,
        },
    )


@router.get("/Admin/dashboard/devlopers/{devloper_id}")
@auth_required("Admin")
def upgrade_devloper(
    request: Request,
    devloper_id,
    decode_existing_token: Dict = Depends(get_decoded_token_data),
    session: dict = Depends(get_session),
):
    email = decode_existing_token["email"]
    query = select(Devloper).where(Devloper.id == devloper_id)
    upgrading_devloper = session.exec(query).first()
    tasks_assigned = select(Task).where(devloper_id == Task.devloper_id)
    tasks = session.exec(tasks_assigned).all()
    print(tasks)
    for task in tasks:
        task.devloper_id = None
        session.add(task)
    session.delete(upgrading_devloper)
    upgrading_devloper = dict(upgrading_devloper)
    new_manager = Manager(**upgrading_devloper)
    session.add(new_manager)

    session.commit()
    return RedirectResponse("/Admin/dashboard/devlopers", status_code=303)


@router.get(
    "/Admin/dashboard/managers",
    tags=["dashboard/managers"],
    response_class=HTMLResponse,
)
@auth_required("Admin")
def admin_dashboard_managers(
    request: Request,
    decode_existing_token: Dict = Depends(get_decoded_token_data),
    session: dict = Depends(get_session),
):
    email = decode_existing_token["email"]
    query = select(Manager)
    query_res = session.exec(query).all()
    # return {"asd":"Yes"}
    return templates.TemplateResponse(
        "managers_list.html",
        context={"request": request, "data": query_res, "email": email},
    )


@router.get("/Admin/dashboard/managers/{manager_id}")
@auth_required("Admin")
def upgrade_manager(
    request: Request,
    manager_id,
    decode_existing_token: Dict = Depends(get_decoded_token_data),
    session: dict = Depends(get_session),
):
    email = decode_existing_token["email"]
    query = select(Manager).where(Manager.id == manager_id)
    user = session.exec(query).first()
    session.delete(user)
    user = dict(user)
    dev_entry = Admin(**user)
    session.add(dev_entry)
    session.commit()
    return RedirectResponse("/Admin/dashboard/managers", status_code=303)


@router.get("/Admin/dashboard/devlopers/{manager_id}/{devloper_id}", tags=["assign_to"])
@auth_required("Admin")
def assign_devloper_to(
    request: Request,
    manager_id,
    devloper_id,
    decode_existing_token: Dict = Depends(get_decoded_token_data),
    session: dict = Depends(get_session),
):
    email = decode_existing_token["email"]
    query = select(Devloper).where(Devloper.id == devloper_id)
    user = session.exec(query).first()
    user.manager_id = manager_id
    session.add(user)
    session.commit()
    return RedirectResponse("/Admin/dashboard/devlopers", status_code=303)
