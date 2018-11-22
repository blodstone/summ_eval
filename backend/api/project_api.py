import json
import http
import urllib.parse

from flask import jsonify, request

from . import api
from backend.models import \
    Document, AnnotationProject, AnnotationResult, \
    Dataset, DocStatus, ProjectType, EvaluationResult, \
    EvaluationProject, Summary, ProjectCategory


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
                if summ_status.total_exp_results == n_results:
                    continue
                else:
                    system_text = Summary.query.get(summ_status.summary_id).text
                    if project_category.lower() == ProjectCategory.INFORMATIVENESS_REF.value.lower():
                        ref_text = Summary.query.filter_by(id=summ_status.ref_summary_id).first().text
                        return jsonify(dict(system_text=system_text, ref_text=ref_text))
                    elif project_category.lower() == ProjectCategory.INFORMATIVENESS_DOC.value.lower():
                        return jsonify(dict(system_text=system_text))
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


# @api.route('/project/<project_id>', methods=['GET'])
# def api_project_get(project_id):
#     project = AnnotationProject.query.filter_by(id=project_id).first()
#     if not project:
#         return '', http.HTTPStatus.NO_CONTENT
#     else:
#         return jsonify(project)


@api.route('/project/save_annotation', methods=['POST'])
def api_project_save_annotation():
    data = request.get_json()
    result = AnnotationResult.create_result(**data)
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
def api_project_progress(project_type):
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

            project_json['link'] = urllib.parse.urljoin(
                request.host_url,
                '#/{form}/{id}'.format(id=project_json['id'], form=project.category))
            result_json['projects'].append(project_json)
        return jsonify(result_json)


@api.route('/doc_status/progress/<doc_status_id>', methods=['GET'])
def api_doc_status_progress(doc_status_id):
    doc_status = DocStatus.query.filter_by(id=doc_status_id).first()
    if not doc_status:
        return '', http.HTTPStatus.NO_CONTENT
    n_results = len(AnnotationResult.query.filter_by(id=doc_status.id).all())
    progress = "{0:.2f}".format(n_results/doc_status.total_exp_results)
    return jsonify(dict(progress=progress))
