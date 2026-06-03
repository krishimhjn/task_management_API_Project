from pydantic_settings import BaseSettings,SettingsConfigDict

# 2STEP
class Settings(BaseSettings):
    # here we are declaring ki hum kya configure karne wale hai  humare settings me jo value 
    # aegi vo kon si file se aegi
    model_config=SettingsConfigDict(env_file=".env",extra="ignore")
    
    DB_CONNECTION:str
    SECRET_KEY:str
    ALGORITHM:str
    EXP_TIME:int
    MAIL_USERNAME:str
    MAIL_PASSWORD:str

settings=Settings()
# jab bhi humko DB conncection ki requierment ho we will simply use 
# settings object and use it 
# like settings.DB_CONNECTION