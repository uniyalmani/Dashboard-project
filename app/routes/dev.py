from urllib import response
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Depends, Request, Response, Form
from sqlmodel import Session, select, or_
from typing import Dict
from app.utilities.dependencies import get_decoded_token_data, get_session
from app.utilities.helper import verify_password, create_jwt_token, hash_password
from fastapi.responses import HTMLResponse
from app.models.database_model import *
from fastapi.responses import RedirectResponse
from datetime import datetime
import os
from app.utilities.helper import (
    flash,
    get_flashed_messages,
    verify_password,
    create_jwt_token,
)
from app.utilities.decorators import auth_required
import json
from sqlalchemy import func

router = APIRouter()

templates = Jinja2Templates(directory="app/templates/devloper")
templates.env.globals["get_flashed_messages"] = get_flashed_messages


@router.get("/Devloper/dashboard", tags=["dashboard"], response_class=HTMLResponse)
@auth_required("Devloper")
def devloper_dashboard(
    request: Request,
    decode_existing_token: dict = Depends(get_decoded_token_data),
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
    # data = {"email": email, "role": role}
    return templates.TemplateResponse(
        "dashboard.html", context={"request": request, "data": data, "email": email}
    )


# showing signup form by returning signup template
@router.get("/Devloper/signup", tags=["devsignup"], response_class=HTMLResponse)
async def devloper_signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


# for reciving data form signup form
@router.post("/Devloper/singup/submit", tags=["devloper_singup_submit"])
async def devloper_signup_submit(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    con_password: str = Form(...),
    session: dict = Depends(get_session),
):
    try:
        if password != con_password:
            flash(
                request,
                "password and conf password should be same is incorrect",
                "primary",
            )
            response = RedirectResponse("/Devloper/signup", status_code=303)
            return response
            
        hashed_password: Dict[str] = hash_password(password)
        data = {"email": email, "role": "Devloper"}
        time = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
        token = create_jwt_token(data, time)

        dev_entry = Devloper(name=name, email=email, password=hashed_password)
        session.add(dev_entry)
        session.commit()
        response = RedirectResponse("/Devloper/dashboard", status_code=303)
        response.set_cookie(key="auth-token", value=token)
        return response
    except Exception as e:
        flash(request, "try with diffrent mail", "primary")
        response = RedirectResponse("/Devloper/signup", status_code=303)
        return response


@router.get(
    "/Devloper/dashboard/tasks",
    tags=["devloper_assigned_task"],
    response_class=HTMLResponse,
)
@auth_required("Devloper")
def devloper_tasks(
    request: Request,
    decode_existing_token: Dict = Depends(get_decoded_token_data),
    session: dict = Depends(get_session),
):
    email = decode_existing_token["email"]
    role = decode_existing_token["role"]
    user = select(Devloper).where(Devloper.email == email)
    user_info = session.exec(user).first()
    query = select(Task).where(Task.devloper_id == user_info.id)
    tasks = session.exec(query).all()
    lst_task = ["pending", "not_picked", "completed"]
    return templates.TemplateResponse(
        "task_list.html",
        context={
            "request": request,
            "data": tasks,
            "lst_task": lst_task,
            "email": email,
        },
    )


@router.get(
    "/Devloper/dashboard/tasks/{task_id}/{status}",
    tags=["change_task_status"],
    response_class=HTMLResponse,
)
@auth_required("Devloper")
def change_task_status(
    request: Request,
    task_id,
    status,
    decode_existing_token: Dict = Depends(get_decoded_token_data),
    session: dict = Depends(get_session),
):
    email = decode_existing_token["email"]
    query = select(Task).where(Task.id == task_id)
    task = session.exec(query).first()
    task.status = status
    session.add(task)
    session.commit()
    return RedirectResponse("/Devloper/dashboard/tasks", status_code=303)
