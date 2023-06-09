from sqlite3 import IntegrityError

import flask
from flask import jsonify, request
from sqlalchemy import select

from data import db_session
from data.jobs import Jobs

blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    result = db_sess.execute(select(Jobs))
    jobs = result.all()
    fields = ('id', 'job', 'team_leader', 'work_size', 'collaborators',
              'start_date', 'end_date', 'is_finished', 'category')
    print(jobs[0][0].to_dict())
    jobs_dict = [job.to_dict(only=fields) for job, in jobs]
    return jsonify({
        'jobs': jobs_dict,
    })


@blueprint.route('/api/jobs/<int:job_id>')
def get_job(job_id: int):
    db_sess = db_session.create_session()
    result = db_sess.execute(
        select(Jobs)
        .where(Jobs.id == job_id)
    )
    job = result.scalar()
    if job is None:
        return jsonify({'error': 'Not found'}), 404
    fields = ('id', 'job', 'team_leader', 'work_size', 'collaborators',
              'start_date', 'end_date', 'is_finished', 'category')
    return jsonify({
        'job': job.to_dict(only=fields),
    })


@blueprint.route('/api/jobs', methods=['POST'])
def create_job():
    if not request.json:
        return jsonify({'error': 'Empty request'}), 400
    elif not all(key in request.json for key in
                 ['job', 'team_leader', 'work_size', 'collaborators']):
        fields_str = ', '.join(['job', 'team_leader', 'work_size', 'collaborators'])
        return jsonify({'error': f'required fields: {fields_str}'}), 400

    db_sess = db_session.create_session()
    job = Jobs(
        id=request.json['id'],
        job=request.json['job'],
        team_leader=request.json['team_leader'],
        work_size=request.json['work_size'],
        collaborators=request.json['collaborators'],
        is_finished=request.json['is_finished'],
    )
    db_sess.add(job)
    try:
        db_sess.commit()
    except IntegrityError as error:
        if 'UNIQUE constraint failed: jobs.id' not in str(error):
            raise
        return jsonify({'error': 'Id already exists'}), 400
    return jsonify({'success': 'OK'}), 201

