from flask import jsonify
from flask_restful import Resource
from data.db_session import create_session
from data.jobs import Job
from utility.aborts import abort_not_found
from utility.parsers import job_parser, put_job_parser


class JobsResource(Resource):
    def get(self, id):
        abort_not_found(id, Job)
        session = create_session()
        job = session.query(Job).get(id)
        return jsonify({'jobs': job.to_dict()})

    def delete(self, id):
        abort_not_found(id, Job)
        session = create_session()
        session.delete(session.query(Job).get(id))
        session.commit()
        session.close()
        return jsonify({'success': 'deleted!'})

    def put(self, id):
        abort_not_found(id, Job)
        args = put_job_parser.parse_args()
        session = create_session()
        job = session.query(Job).get(id)
        if 'team_leader' in args:
            job.team_leader = args.team_leader
        if 'job' in args:
            job.team_leader = args.team_leader
        if 'work_size' in args:
            job.team_leader = args.team_leader
        if 'collaborators' in args:
            job.team_leader = args.team_leader
        if 'is_finished' in args:
            job.team_leader = args.team_leader
        if 'team_leader' in args:
            job.team_leader = args.team_leader
        session.close()
        return jsonify({'success': 'edited!'})


class JobsListResource(Resource):
    def get(self):
        session = create_session()
        jobs = session.query(Job).all()
        session.close()
        return jsonify({'jobs': [i.to_dict() for i in jobs]})

    def post(self):
        args = job_parser.parse_args()
        session = create_session()
        job = Job(team_leader=args['team_leader'],
                  job=args['job'],
                  work_size=args['work_size'],
                  collaborators=args['collaborators'],
                  is_finished=args['is_finished'])
        session.add(job)
        session.commit()
        session.close()
        return jsonify({'success': 'created!'})
