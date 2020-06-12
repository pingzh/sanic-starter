import sys
import os
import pytest
import sqlalchemy
from uuid import uuid4
from databases import Database
# set the root dir
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

os.environ['SANIC_ENV'] = 'test'
os.environ['DATABASE_URL'] = 'sqlite:////tmp/test-server.db'

from models.tables import metadata


@pytest.fixture()
async def db_with_schema():
    test_name = os.environ["PYTEST_CURRENT_TEST"].split('::')[-1].split(' ')[0]
    uuid = f'{test_name}-{uuid4()}'
    db_file = f'/tmp/test-{uuid}.db'
    url = f'sqlite:///{db_file}'
    db = Database(url)
    await db.connect()

    engine = sqlalchemy.create_engine(url)
    metadata.create_all(engine)

    yield db

    metadata.drop_all(engine)
    await db.disconnect()
    os.remove(db_file)

