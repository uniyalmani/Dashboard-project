from sqlmodel import  Session, create_engine, SQLModel
from  app.models import database_model
URL = "mysql://fynd_acad:fynd123@mysql_db:3306/fynd_acad"

engine = create_engine(URL)

SQLModel.metadata.create_all(engine)
print("inside database_initializer.py")
print("engin created")


