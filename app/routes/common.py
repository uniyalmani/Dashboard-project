from urllib import response
from fastapi import APIRouter, Depends, Request, Response, Form
from sqlmodel import Session, select
from typing import Dict
from app.utilities.dependencies import get_decoded_token_data, get_session
from app.utilities.helper import (
    flash,
    get_flashed_messages,
    verify_password,
    create_jwt_token,
)
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.models import database_model
from fastapi.responses import RedirectResponse
from datetime import datetime
import json


router = APIRouter()

templates = Jinja2Templates(directory="app/templates")
templates.env.globals["get_flashed_messages"] = get_flashed_messages


@router.get("/error", tags=["login"], response_class=HTMLResponse)
async def error_page(request: Request):
    """Render Invalid html page, if there is an error"""
    print(request.cookies)
    return templates.TemplateResponse("invalid.html", {"request": request})


@router.get("/login", tags=["login"], response_class=HTMLResponse)
async def login(
    request: Request,
    decode_existing_token: dict = Depends(get_decoded_token_data),
    session: dict = Depends(get_session),
):
    if decode_existing_token and decode_existing_token.get("valid_token"):
        email = decode_existing_token["email"]
        role = decode_existing_token["role"]
        model = getattr(database_model, role)
        query = select(model).where(model.email == email)
        user = session.exec(query).first()
        if user is None:
            response = templates.TemplateResponse("login.html", {"request": request})
            response.delete_cookie("auth-token")
            return response
        return RedirectResponse(f"/{role}/dashboard", status_code=303)

    return templates.TemplateResponse("login.html", {"request": request})


# for reciving data form admin login form
@router.post("/login-submit", tags=["login_submit"])
async def login_submit(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    role: str = Form(...),
    decode_existing_token: Dict = Depends(get_decoded_token_data),
    session: dict = Depends(get_session),
):
    data = {"email": email, "role": role}

    token = create_jwt_token(data, 120)
    model = getattr(database_model, role)
    query = select(model).where(model.email == email)
    user = session.exec(query).first()
    if user is None:
        url = router.url_path_for("login")
        flash(request, "Email or Password is incorrect", "primary")
        return RedirectResponse(url, status_code=303)
    if verify_password(password, user.password):
        print("verified")
        response = RedirectResponse(f"/{role}/dashboard", status_code=303)
        response.set_cookie(key="auth-token", value=token)
        return response
    return router.url_path_for("login")


@router.get("/logout", tags=["loginsubmit"])
async def logout(request: Request):
    response = templates.TemplateResponse("login.html", {"request": request})
    response.delete_cookie("auth-token")
    return response
