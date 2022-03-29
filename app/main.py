from subprocess import call
from typing import Optional
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi import FastAPI
from .controllers import database_initializer
from app.routes import admin, dev, manager, common
from fastapi.responses import HTMLResponse
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, Request
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware


templates = Jinja2Templates(directory="app/templates")


middleware = [Middleware(SessionMiddleware, secret_key="ashu")]

app = FastAPI(middleware=middleware)


app.mount("/static/", StaticFiles(directory="app/static", html=True), name="static")



app.include_router(admin.router)
app.include_router(dev.router)
app.include_router(manager.router)
app.include_router(common.router)


@app.get("/", tags=["main page"], response_class=HTMLResponse)
def home_page(
    request: Request,
):
    return templates.TemplateResponse("home.html", {"request": request})
