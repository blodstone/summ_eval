import json
from tests.fixture import init_db, test_client


def test_get_json(test_client, init_db):
    response = test_client.get('/dataset/Sample_BBC')
    assert response.status_code == 200
    assert response.get_json()['name'] == 'Sample_BBC'


def test_get_dataset_list(test_client, init_db):
    response = test_client.get('/dataset')
    assert response.status_code == 200
    assert response.get_json()['names'] == ['Sample_BBC']
