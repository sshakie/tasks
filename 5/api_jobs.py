import json
from flask import request, jsonify, make_response, Blueprint
from data.db_session import create_session
from data.jobs import Jobs

blueprint = Blueprint('api_jobs', __name__, template_folder='templates')


@blueprint.route('/api/jobs', methods=['GET'])
def print_jobs():
    db_sess = create_session()
    return jsonify({'jobs': [i.to_dict() for i in db_sess.query(Jobs).all()]})


@blueprint.route('/api/jobs/<int:job_id>')
def give_job(job_id):
    db_sess = create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == job_id).first()
    if job:
        return jsonify({'jobs': job.to_dict()})
    return make_response(jsonify({'error': 'Not found in db'}), 404)


@blueprint.route('/api/jobs', methods=['POST'])
def create_job():
    if len([i for i in request.json.keys() if
            i not in ['job', 'work_size', 'collaborators', 'is_finished', 'end_date']]) != 0:
        return make_response(jsonify({'error': 'Unknown parameter(s)'}), 400)
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in ['job', 'work_size', 'collaborators']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = create_session()
    jobs = Jobs()
    jobs.job = request.json['job']
    jobs.work_size = request.json['work_size']
    jobs.collaborators = request.json['collaborators']
    if 'end_date' in request.json.keys():
        jobs.end_date = request.json['end_date']
    if 'is_finished' in request.json.keys():
        jobs.is_finished = request.json['is_finished']
    db_sess.add(jobs)
    db_sess.commit()
    return jsonify('created!')


@blueprint.route('/api/jobs/delete/<int:job_id>')
def delete_job(job_id):
    db_sess = create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == job_id).first()
    if job:
        db_sess.delete(job)
        db_sess.commit()
        db_sess.close()
        return jsonify('deleted!')
    return make_response(jsonify({'error': 'Not found in db'}), 404)


@blueprint.route('/api/jobs/edit/<int:job_id>', methods=['POST'])
def edit_job(job_id):
    db_sess = create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.id == job_id).first()
    if not jobs:
        return make_response(jsonify({'error': 'Not found in db'}), 404)

    if len([i for i in request.json.keys() if
            i not in ['job', 'work_size', 'collaborators', 'is_finished', 'end_date']]) != 0:
        return make_response(jsonify({'error': 'Unknown parameter(s)'}), 400)
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)

    for i in request.json.keys():
        if i == 'job':
            jobs.job = request.json['job']
        if i == 'work_size':
            jobs.job = request.json['work_size']
        if i == 'collaborators':
            jobs.job = request.json['collaborators']
        if i == 'end_date':
            jobs.job = request.json['end_date']
        if i == 'is_finished':
            jobs.job = request.json['is_finished']
    db_sess.commit()
    db_sess.close()
    return jsonify('edited!')
