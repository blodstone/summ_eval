import json
import http
import urllib.parse

from flask import jsonify, request

from . import api
from backend.models import Document, AnnotationProject, AnnotationResult, Dataset, DocStatus, db


@api.route('/project/<project_id>/single_doc', methods=['GET'])
def api_project_single_doc(project_id):
    project = AnnotationProject.query.filter_by(id=project_id).first()
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


@api.route('/project', methods=['POST'])
def api_project_create():
    if request.method == 'POST':
        data = request.get_json()
        project = AnnotationProject.create_project(**data)
        if project:
            return '', http.HTTPStatus.CREATED
        else:
            return '', http.HTTPStatus.CONFLICT


@api.route('/project/<project_id>', methods=['GET'])
def api_project_get(project_id):
    project = AnnotationProject.query.filter_by(id=project_id).first()
    if not project:
        return '', http.HTTPStatus.NO_CONTENT
    else:
        return jsonify(project)


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


@api.route('/project/all_progress', methods=['GET'])
def api_project_progress():
    projects = AnnotationProject.query.filter_by(is_active=True).all()
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
            for doc_status in project.doc_statuses:
                n_results = AnnotationResult.query.filter_by(status_id=doc_status.id).count()
                total_n_results += n_results
                total_total_exp_results += doc_status.total_exp_results
            if project.type == 'Highlight':
                form = 'annotation'
            elif project.type == 'Informativeness':
                form = 'inf_eval'
            project_json['progress'] = total_n_results/total_total_exp_results
            project_json['no'] = len(result_json['projects']) + 1

            project_json['link'] = urllib.parse.urljoin(
                request.host_url,
                '#/{form}/{id}'.format(id=project_json['id'], form=form))
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
