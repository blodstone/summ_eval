import json
from tests.fixture import init_db, test_client


def test_doc_status(test_client, init_db):
    response = test_client.post('/project',
                                data=json.dumps(dict(
                                    name='Test_Doc_Status',
                                    dataset_name='Sample_BBC',
                                    type='highlight',
                                    total_exp_results=3)
                                ),
                                content_type='application/json'
                                )
    response = test_client.get('/doc_status/progress/1')
    assert response.status_code == 200
    assert response.get_json()['progress'] == '0.00'
