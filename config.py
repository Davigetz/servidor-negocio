import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATABSE_URI = os.getenv('DATABASE_URL')
