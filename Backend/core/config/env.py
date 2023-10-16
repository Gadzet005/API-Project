import os

from dotenv import load_dotenv


load_dotenv()

STATES = ['DEV', 'PROD']
STATE = os.getenv('STATE', 'DEV').upper()
if STATE not in STATES:
    raise ValueError(f'Параметр STATE указан неверно. Возможные значения: {STATES}')

try:
    _debug = int(os.getenv('DEBUG', 1))
    if _debug != 0 and _debug != 1:
        raise ValueError
    DEBUG = bool(_debug)
except ValueError:
    raise ValueError('Параметр DEBUG может принимать принимать только 0 и 1')

SECRET_KEY = os.getenv('SECRET_KEY', 'no-secret')
if STATE == 'PROD' and (SECRET_KEY == '' or SECRET_KEY == 'no-secret'):
    raise ValueError('SECRET KEY не определён')

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(', ')
