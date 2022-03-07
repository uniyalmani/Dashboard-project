from typing import Optional

from fastapi import FastAPI
from .controllers import database_initializer
from app.routes import admin, dev, manager

from datetime import datetime, timedelta
print(datetime.utcnow(), datetime.now(), "checking function ")

app = FastAPI()

print("============")
print("inside fastapi.py")
app.include_router(admin.router)
app.include_router(dev.router)
app.include_router(manager.router   )

@app.get("/")
def login():
    return {"heelo"}





