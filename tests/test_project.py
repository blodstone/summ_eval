import json
from backend.models import Project
from tests.fixture import init_db, test_client


def test_project_create(test_client, init_db):
    response = test_client.post('/project',
                                data=json.dumps(dict(
                                    name='Test_Create',
                                    dataset_name='Sample_BBC',
                                    type='highlight',
                                    total_exp_results=3
                                    )
                                ),
                                content_type='application/json'
                                )
    assert response.status_code == 201
    project = Project.query.filter_by(name='Test_Create').first()
    assert project is not None


def test_project_get_progress(test_client, init_db):
    response = test_client.get('/project/all_progress')
    assert response.status_code == 200
    assert len(response.get_json()['projects']) > 0
    assert response.get_json()['projects'][0]['dataset_name'] == 'Sample_BBC'
    assert 'progress' in response.get_json()['projects'][0]


def test_project_get_single_unfinished_doc(test_client, init_db):
    response = test_client.post('/project',
                                data=json.dumps(dict(
                                    name='Test_Single',
                                    dataset_name='Sample_BBC',
                                    type='highlight',
                                    total_exp_results=3
                                )
                                ),
                                content_type='application/json'
                                )
    project = Project.query.filter_by(name='Test_Create').first()
    assert response.status_code == 201
    print('Project ID'+str(project.id))
    response = test_client.get(
        '/project/{project_id}/single_doc'.format(project_id=project.id))
    assert response.status_code == 200
