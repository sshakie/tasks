from flask_restful import reqparse

user_parser = reqparse.RequestParser()
user_parser.add_argument('name', required=True, type=str)
user_parser.add_argument('surname', required=True, type=str)
user_parser.add_argument('email', required=True, type=str)
user_parser.add_argument('password', required=True, type=str)

job_parser = reqparse.RequestParser()
job_parser.add_argument('team_leader', required=True, type=int)
job_parser.add_argument('job', required=True, type=str)
job_parser.add_argument('work_size', required=True, type=int)
job_parser.add_argument('collaborators', required=True, type=str)
job_parser.add_argument('is_finished', required=True, type=bool)
