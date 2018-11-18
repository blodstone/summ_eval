import json
from backend.models import Project
from tests.fixture import init_db, test_client


def test_project_create(test_client, init_db):
    response = test_client.post('/project',
                                data=json.dumps(dict(
                                    name='Test_Create',
                                    dataset_name='Sample_BBC',
                                    type='highlight',
                                    totalExpResults=3
                                    )
                                ),
                                content_type='application/json'
                                )
    assert response.status_code == 201
    project = Project.query.filter_by(name='Test_Create').first()
    assert project is not None


def test_project_get_one(test_client, init_db):
    response = test_client.get('/document/get_one')
    assert response.status_code == 200


