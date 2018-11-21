import json
from backend.models import AnnotationProject, EvaluationProject,\
    ProjectCategory, ProjectType
from tests.fixture import init_db, test_client


def create_proj_resp(test_client, project_type, name):
    if project_type == ProjectType.ANNOTATION.value:
        return test_client.post('/project/%s' % ProjectType.ANNOTATION.value,
                                data=json.dumps(dict(
                                    name=name,
                                    dataset_name='Sample_BBC',
                                    category=ProjectCategory.HIGHLIGHT.value,
                                    total_exp_results=3
                                    )
                                ),
                                content_type='application/json'
                                )
    elif project_type == ProjectType.EVALUATION.value:
        return test_client.post('/project/%s' % ProjectType.EVALUATION.value,
                                data=json.dumps(dict(
                                    name=name,
                                    dataset_name='Sample_BBC',
                                    category=ProjectCategory.INFORMATIVENESS.value,
                                    total_exp_results=3,
                                    summ_group_name='lead'
                                )),
                                content_type='application/json'
                                )


def test_project_create_annotation(test_client, init_db):
    # Test Annotation Project
    response = create_proj_resp(
        test_client,
        ProjectType.ANNOTATION.value,
        name='Test_Create_Annotation'
    )
    assert response.status_code == 201
    project = AnnotationProject.query.filter_by(name='Test_Create_Annotation').first()
    assert project is not None


def test_project_create_evaluation(test_client, init_db):
    # Test Evaluation Project
    response = create_proj_resp(
        test_client,
        ProjectType.EVALUATION.value,
        name='Test_Create_Evaluation'
    )
    assert response.status_code == 201
    project = EvaluationProject.query.filter_by(name='Test_Create_Evaluation').first()
    assert project is not None


def test_project_get_progress_annotation(test_client, init_db):
    create_proj_resp(test_client, ProjectType.ANNOTATION.value, 'Test_Progress_Annotation')
    response = test_client.get('/project/all_progress/annotation')
    assert response.status_code == 200
    assert len(response.get_json()['projects']) > 0
    assert response.get_json()['projects'][0]['dataset_name'] == 'Sample_BBC'
    assert 'progress' in response.get_json()['projects'][0]


def test_project_get_progress_evaluation(test_client, init_db):
    create_proj_resp(test_client, ProjectType.EVALUATION.value, 'Test_Progress_Evaluation')
    response = test_client.get('/project/all_progress/evaluation')
    assert response.status_code == 200
    assert len(response.get_json()['projects']) > 0
    assert response.get_json()['projects'][0]['dataset_name'] == 'Sample_BBC'
    assert 'progress' in response.get_json()['projects'][0]


def test_project_get_single_unfinished_doc_annotation(test_client, init_db):
    create_proj_resp(test_client, ProjectType.ANNOTATION.value, 'Test_Single_Annotation')
    project = AnnotationProject.query.filter_by(name='Test_Single_Annotation').first()
    response = test_client.get(
        '/project/%s/%s/single_doc' % (ProjectType.ANNOTATION.value, project.id))
    assert response.status_code == 200


def test_project_get_single_unfinished_summ_evaluation(test_client, init_db):
    create_proj_resp(test_client, ProjectType.EVALUATION.value, 'Test_Single_Evaluation')
    project = EvaluationProject.query.filter_by(name='Test_Single_Evaluation').first()
    response = test_client.get(
        '/project/%s/%s/single_doc' % (ProjectType.EVALUATION.value, project.id)
    )
    assert response.status_code == 200
