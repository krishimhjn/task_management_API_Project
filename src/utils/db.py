from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from src.utils.settings import settings

# 3rd step
# configration of DB
 
Base=declarative_base()
# to create engine we need URL that is in settings.db_connection
engine=create_engine(url=settings.DB_CONNECTION)

# we will need a session to use DB and session  makerclass needs to bind with a engine

LocalSession= sessionmaker(bind=engine)


# now we need a DB provider whenever we need any session we can use it
# like to do some querirs we just need this session ka ek aboject milna chahiye


# this is DB provider we can use get_db any where inside our application
def get_db():
    session=LocalSession()
    try:
        yield session
    finally:
        session.close()


# now we need to connect this Base to our main application
