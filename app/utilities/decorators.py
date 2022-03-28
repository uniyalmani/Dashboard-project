from functools import wraps
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from .helper import *
from .dependencies import get_decoded_token_data

import jwt

import os

templates = Jinja2Templates(directory="app/templates")

templates.env.globals["get_flashed_messages"] = get_flashed_messages


def auth_required(post):
    def decorator_factory(func):
        @wraps(func)
        def decorator(request: Request, *args, **kwargs):
            decode_existing_token = get_decoded_token_data(request)
            print(decode_existing_token)

            if (
                decode_existing_token
                and decode_existing_token.get("valid_token")
                and decode_existing_token.get("role") == post
            ):
                pass
            else:
                flash(
                    request,
                    f"please login with {post} account to access this route or token is not valid",
                    "primary",
                )
                return RedirectResponse("/login", status_code=303)

            return func(request, *args, **kwargs)

        return decorator

    return decorator_factory
