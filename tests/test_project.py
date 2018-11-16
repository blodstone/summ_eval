import pytest
import json
from backend.app import create_app
from backend.app import db
from scripts.insert_dataset import init_dataset


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app('test.cfg.py')
    testing_client = flask_app.test_client()
    ctx = flask_app.app_context()
    ctx.push()
    yield testing_client
    ctx.pop()


@pytest.fixture(scope='module')
def init_db():
    db.create_all()
    init_dataset(db)
    yield db
    db.drop_all()


def test_dataset(test_client, init_db):
    response = test_client.get('/dataset/Sample_BBC')
    assert response.status_code == 200
    assert response.get_json()['name'] == 'Sample_BBC'


def test_project(test_client, init_db):
    response = test_client.post('/project/Sample_BBC/3',
                                data=json.dumps(dict(
                                    title='Test',
                                    type='highlight')
                                    ),
                                content_type='application/json'
                                )
    assert response.status_code == 201
    response = test_client.get('/document/get_one')
    assert response.status_code == 200


def test_doc_status(test_client, init_db):
    response = test_client.get('/doc_status/progress/1')
    assert response.status_code == 200
    assert response.get_json()['progress'] == '0.00'
