from fastapi import Request
from sqlmodel import Session
from .helper import is_valid_token
from app.controllers.database_initializer import engine


def get_decoded_token_data(request: Request):
    """return token data with key valid_token for validation"""
    auth_token = request.cookies.get("auth-token")
    decoded_data = is_valid_token(auth_token)
    return decoded_data


def get_session():
    with Session(engine) as session:
        yield session
