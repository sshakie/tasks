from flask_restful import abort
from data.db_session import create_session
from data.users import User
from data.jobs import Job


def abort_not_found(id, item):
    session = create_session()
    if not session.query(item).get(id):
        abort(404, message=f'{item.__name__} {id} not found')
    session.close()
