# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://user:pass@localhost/jobsdb')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LINKEDIN_EMAIL = os.getenv('LINKEDIN_EMAIL')
    LINKEDIN_PASSWORD = os.getenv('LINKEDIN_PASSWORD')
    GLASSDOOR_EMAIL = os.getenv('GLASSDOOR_EMAIL')
    GLASSDOOR_PASSWORD = os.getenv('GLASSDOOR_PASSWORD')
