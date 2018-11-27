import json
import http
import urllib.parse

from flask import jsonify, request

from . import api
from backend.models import \
    Document, AnnotationProject, AnnotationResult, \
    Dataset, DocStatus, ProjectType, EvaluationResult, \
    EvaluationProject, Summary, ProjectCategory, SummaryGroup


@api.route('/project/<project_type>/<project_category>/<project_id>/single_doc', methods=['GET'])
def api_project_single_doc(project_type, project_category, project_id):
    if project_type.lower() == ProjectType.ANNOTATION.value.lower():
        project = AnnotationProject.query.get(project_id)
        if not project:
            return '', http.HTTPStatus.NO_CONTENT
        else:
            for doc_status in project.doc_statuses:
                n_results = len(AnnotationResult.query.filter_by(status_id=doc_status.id).all())
                if doc_status.total_exp_results == n_results:
                    continue
                else:
                    doc_json = json.dumps(Document.get_dict(doc_status.doc_id))
                    return jsonify(dict(doc_json=doc_json,
                                        doc_status_id=doc_status.id))
            return '', http.HTTPStatus.NO_CONTENT
    elif project_type.lower() == ProjectType.EVALUATION.value.lower():
        project = EvaluationProject.query.get(project_id)
        if not project:
            return '', http.HTTPStatus.NO_CONTENT
        else:
            for summ_status in project.summ_statuses:
                n_results = len(EvaluationResult.query.filter_by(status_id=summ_status.id).all())
                if summ_status.total_exp_results != n_results:
                    system_summary = Summary.query.get(summ_status.summary_id)
                    system_text = system_summary.text
                    doc_json = Document.get_dict(system_summary.doc_id)
                    if project_category.lower() == ProjectCategory.INFORMATIVENESS_REF.value.lower():
                        ref_text = Summary.query.filter_by(id=summ_status.ref_summary_id).first().text
                        return jsonify(dict(system_text=system_text,
                                            ref_text=ref_text, summ_status_id=summ_status.id))
                    elif project_category.lower() == ProjectCategory.INFORMATIVENESS_DOC.value.lower():
                        return jsonify(dict(system_text=system_text,
                                            doc_json=doc_json, summ_status_id=summ_status.id))
                    elif project_category.lower() == ProjectCategory.FLUENCY.value.lower():
                        return jsonify(dict(system_text=system_text, summ_status_id=summ_status.id))
            return '', http.HTTPStatus.NO_CONTENT
    else:
        return '', http.HTTPStatus.BAD_REQUEST


@api.route('/project/<project_type>', methods=['POST'])
def api_project_create(project_type):
    if request.method == 'POST':
        data = request.get_json()
        project = None
        if project_type.lower() == ProjectType.ANNOTATION.value.lower():
            project = AnnotationProject.create_project(**data)
        elif project_type.lower() == ProjectType.EVALUATION.value.lower():
            project = EvaluationProject.create_project(**data)
        else:
            return '', http.HTTPStatus.BAD_REQUEST
        if project:
            return '', http.HTTPStatus.CREATED
        else:
            return '', http.HTTPStatus.CONFLICT


@api.route('/project/get/<project_type>/<project_name>', methods=['GET'])
def api_project_get(project_type, project_name):
    if project_type.lower() == ProjectType.ANNOTATION.value.lower():
        projects = AnnotationProject.query.filter_by(name=project_name).all()
    elif project_type.lower() == ProjectType.EVALUATION.value.lower():
        projects = EvaluationProject.query.filter_by(name=project_name).all()
    else:
        return '', http.HTTPStatus.BAD_REQUEST
    if len(projects) == 0:
        return '', http.HTTPStatus.NO_CONTENT
    else:
        result_json = {}
        for project in projects:
            result_json[project.id] = project.get_dict()
        return jsonify(result_json)


@api.route('/project/save_result/<project_type>', methods=['POST'])
def api_project_save_result(project_type):
    data = request.get_json()
    if project_type.lower() == ProjectType.ANNOTATION.value.lower():
        result = AnnotationResult.create_result(**data)
    elif project_type.lower() == ProjectType.EVALUATION.value.lower():
        result = EvaluationResult.create_result(**data)
    if result:
        return '', http.HTTPStatus.CREATED
    else:
        return '', http.HTTPStatus.CONFLICT


@api.route('/project/<project_id>/close', methods=['POST'])
def api_project_close(project_id):
    project = AnnotationProject.query.filter_by(id=project_id).first()
    if not project or project.is_active is False:
        return '', http.HTTPStatus.NOT_MODIFIED
    else:
        for doc_status in project.doc_statuses:
            results = AnnotationResult.query.filter_by(status_id=doc_status.id).all()
            results_json = {}
            for result in results:
                results_json[result.id] = json.loads(result.result_json)
            if len(results_json) != 0:
                Document.add_results(doc_status.doc_id, results_json)
                DocStatus.close(doc_status.id)
        AnnotationProject.deactivate(project_id)
        return '', http.HTTPStatus.OK


@api.route('/project/all_progress/<project_type>', methods=['GET'])
def api_project_progress_all(project_type):
    project_type = project_type.lower()
    if project_type == ProjectType.ANNOTATION.value.lower():
        projects = AnnotationProject.query.filter_by(is_active=True).all()
    elif project_type == ProjectType.EVALUATION.value.lower():
        projects = EvaluationProject.query.filter_by(is_active=True).all()
    else:
        return '', http.HTTPStatus.BAD_REQUEST

    if len(projects) == 0:
        return '', http.HTTPStatus.NO_CONTENT
    else:
        result_json = {'projects': []}
        for project in projects:
            project_json = project.to_dict()
            project_json['dataset_name'] = \
                Dataset.query.filter_by(id=project.dataset_id).first().name
            total_n_results = 0
            total_total_exp_results = 0
            if project_type == ProjectType.ANNOTATION.value.lower():
                for doc_status in project.doc_statuses:
                    n_results = AnnotationResult.query\
                        .filter_by(status_id=doc_status.id).count()
                    total_n_results += n_results
                    total_total_exp_results += doc_status.total_exp_results
            elif project_type == ProjectType.EVALUATION.value.lower():
                for summ_status in project.summ_statuses:
                    n_results = EvaluationResult.query\
                        .filter_by(status_id=summ_status.id).count()
                    total_n_results += n_results
                    total_total_exp_results += summ_status.total_exp_results
            project_json['progress'] = total_n_results/total_total_exp_results
            project_json['no'] = len(result_json['projects']) + 1
            if project_type == ProjectType.EVALUATION.value.lower():
                summ_group = SummaryGroup.query.get(project.summ_group_id)
                project_json['summ_group_name'] = summ_group.name
            project_json['link'] = urllib.parse.urljoin(
            request.host_url,
            '#/{type}/{category}/{id}'.format(
                type=project_type,
                category=project.category,
                id=project_json['id']
                ))
            result_json['projects'].append(project_json)
        return jsonify(result_json)


@api.route('/project/progress/<project_type>/<project_id>', methods=['GET'])
def api_project_progress(project_type, project_id):
    project_type = project_type.lower()
    if project_type == ProjectType.ANNOTATION.value.lower():
        project = AnnotationProject.query.get(project_id)
    elif project_type == ProjectType.EVALUATION.value.lower():
        project = EvaluationProject.query.get(project_id)
    else:
        return '', http.HTTPStatus.BAD_REQUEST
    if not project:
        return '', http.HTTPStatus.CONFLICT
    else:
        progress_json = None
        if project_type == ProjectType.ANNOTATION.value.lower():
            progress_json = {'documents': []}
        elif project_type == ProjectType.EVALUATION.value.lower():
            progress_json = {'systems': []}
        if project_type == ProjectType.ANNOTATION.value.lower():
            for doc_status in project.doc_statuses:
                document = Document.query.get(doc_status.doc_id)
                result_jsons = []
                for result in doc_status.results:
                    result_jsons.append(result.result_json)
                exp_results = doc_status.total_exp_results
                progress_json['documents'].append({
                    'no': len(progress_json['documents']) + 1,
                    'name': document.doc_id,
                    'progress': len(doc_status.results)/exp_results,
                    'result_jsons': result_jsons
                })
            return jsonify(progress_json)
        elif project_type == ProjectType.EVALUATION.value.lower():
            for summ_status in project.summ_statuses:
                summary = Summary.query.get(summ_status.summary_id)
                document = Document.query.get(summary.doc_id)
                result_jsons = []
                for result in summ_status.results:
                    result_jsons.append({
                        'precision': result.precision,
                        'recall': result.recall,
                        'clarity': result.clarity,
                        'fluency': result.fluency
                    })
                exp_results = summ_status.total_exp_results
                progress_json['systems'].append({
                    'no': len(progress_json['documents']) + 1,
                    'name': document.doc_id,
                    'progress': len(summ_status.results) / exp_results,
                    'result_jsons': result_jsons
                })
            return jsonify(progress_json)
        else:
            return '', http.HTTPStatus.BAD_REQUEST


@api.route('/doc_status/progress/<doc_status_id>', methods=['GET'])
def api_doc_status_progress(doc_status_id):
    doc_status = DocStatus.query.filter_by(id=doc_status_id).first()
    if not doc_status:
        return '', http.HTTPStatus.NO_CONTENT
    n_results = len(AnnotationResult.query.filter_by(id=doc_status.id).all())
    progress = "{0:.2f}".format(n_results/doc_status.total_exp_results)
    return jsonify(dict(progress=progress))
