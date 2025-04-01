from flask import Flask
from flask_restful import reqparse, abort, Api
from data.db_session import create_session, global_init
from data.users import User
from data.jobs import Job
from api.users_resource import UsersResource, UsersListResource
from api.jobs_resource import JobsResource, JobsListResource

app = Flask(__name__)
api = Api(app)

global_init('db/table.db')
api.add_resource(UsersListResource, '/api/v2/users')
api.add_resource(UsersResource, '/api/v2/users/<int:id>')
api.add_resource(JobsListResource, '/api/v2/jobs')
api.add_resource(JobsResource, '/api/v2/jobs/<int:id>')

if __name__ == '__main__':
    app.run()
