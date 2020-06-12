import yaml
import os

sanic_env = os.environ.get('SANIC_ENV', 'dev').upper()


def read_db_url_in_prod_env():
    config_path = '/config/secrets.yml'
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    return config['DATABASE_URL']


if sanic_env == 'PRODUCTION':
    WORKERS = int(os.environ.get('WEB_WORKERS', 2))
    PORT = int(os.environ.get('WEB_PORT', 8000))
    DEBUG = False
    DATABASE_URL = read_db_url_in_prod_env()
elif sanic_env == 'STAGING':
    WORKERS = int(os.environ.get('WEB_WORKERS', 2))
    PORT = int(os.environ.get('WEB_PORT', 8000))
    DEBUG = False
    DATABASE_URL = read_db_url_in_prod_env()
elif sanic_env == 'TEST':
    DATABASE_URL = os.environ.get('DATABASE_URL')
    WORKERS = 1
    PORT = 8000
    DEBUG = False
else:
    DATABASE_URL = 'mysql://root@localhost/market_maker?min_size=5&max_size=20'
    WORKERS = 2
    PORT = 8000
    DEBUG = True
