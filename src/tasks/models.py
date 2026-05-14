from sqlalchemy import Column,INTEGER,String,Boolean,ForeignKey
from src.utils.db import Base

# base is responsible to connect out models to actual databse

class TaskModel(Base):
    __tablename__="user_tasks"

    id=Column(INTEGER,primary_key=True)
    title=Column(String)
    description=Column(String)
    is_completed=Column(Boolean,default=False)
    user_id=Column(INTEGER,ForeignKey("user_table.id",ondelete="CASCADE"))
# we need to connect this file to our main.py file to get it executed
# if we dont import this file into main.py table will not be created
