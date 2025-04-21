from flask import jsonify
from flask_restful import Resource
from data.db_session import create_session
from data.users import User
from utility.aborts import abort_not_found
from utility.parsers import user_parser


class UsersResource(Resource):
    def get(self, id):
        abort_not_found(id, User)
        session = create_session()
        user = session.query(User).get(id)
        session.close()
        return jsonify({'users': user.to_dict()})

    def delete(self, id):
        abort_not_found(id, User)
        session = create_session()
        session.delete(session.query(User).get(id))
        session.commit()
        session.close()
        return jsonify({'success': 'deleted!'})


class UsersListResource(Resource):
    def get(self):
        session = create_session()
        users = session.query(User).all()
        session.close()
        return jsonify({'users': [i.to_dict() for i in users]})

    def post(self):
        args = user_parser.parse_args()
        session = create_session()
        user = User(surname=args['surname'],
                    age=args['age'],
                    position=args['position'],
                    speciality=args['speciality'],
                    address=args['address'],
                    name=args['name'],
                    email=args['email'])
        user.set_password(args['password'])
        session.add(user)
        session.commit()
        session.close()
        return jsonify({'success': 'created!'})
