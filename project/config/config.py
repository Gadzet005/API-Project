import os

from dotenv import load_dotenv


load_dotenv()


class ProjectConfig:
    STATE = 'DEV'
    DEBUG = True
    SECRET_KEY = 'no-secret-key'
    ALLOWED_HOSTS = ['*']

    def __init__(self):
        self.STATE = os.getenv('STATE', self.STATE)
        self.DEBUG = self.STATE != 'PROD'
        self.SECRET_KEY = os.getenv('SECRET_KEY', self.SECRET_KEY)

        raw_allowed_hosts = os.getenv('ALLOWED_HOSTS', '*')
        self.ALLOWED_HOSTS = raw_allowed_hosts.split(', ')
