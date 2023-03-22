from flask import Flask, jsonify, request
from flask_restful import abort, Api, Resource
from sqlalchemy import delete, select

from data import db_session
from data.user_request_parser import parser
from data.users import User

app = Flask(__name__)
api = Api(app)


class UserResource(Resource):
    def get(self, user_id):
        self.abort_if_user_not_found(user_id)
        session = db_session.create_session()
        users = session.query(User).get(user_id)
        return jsonify({'user': users.to_dict(
            only=('name', 'surname', 'age', 'address', 'email', 'position', 'speciality'))})

    def delete(self, user_id):
        self.abort_if_user_not_found(user_id)
        session = db_session.create_session()
        session.execute(
            delete(User)
            .where(User.id == user_id)
        )
        return jsonify({'success': 'OK'})

    def abort_if_user_not_found(self, user_id):
        session = db_session.create_session()
        users = session.query(User).get(user_id)
        if not users:
            abort(404, message=f"User {user_id} not found")


class UserListResource(Resource):
    def get(self):
        session = db_session.create_session()
        result = session.execute(
            select(User)
        )
        users = result.all()
        return jsonify({'news': [user.to_dict(
            only=('name', 'surname', 'age', 'address', 'email', 'position', 'speciality')) for user, in users]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User(
            name=request.json['name'],
            surname=request.json['surname'],
            age=request.json['age'],
            address=request.json['address'],
            email=request.json['email'],
            position=request.json['position'],
            speciality=request.json['speciality'],
        )
        user.set_password(args['password'])
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})
