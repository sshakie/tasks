from flask_restful import abort
from data.db_session import create_session
from data.users import User
from data.jobs import Job


def user_abort_not_found(id):
    session = create_session()
    if not session.query(User).get(id):
        abort(404, message=f'User {id} not found')
    session.close()

def job_abort_not_found(id):
    session = create_session()
    if not session.query(Job).get(id):
        abort(404, message=f'Job {id} not found')
    session.close()
