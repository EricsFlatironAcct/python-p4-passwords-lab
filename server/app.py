#!/usr/bin/env python3

from flask import request, session, make_response
from flask_restful import Resource

from config import app, db, api
from models import User

class ClearSession(Resource):

    def delete(self):
    
        session['page_views'] = None
        session['user_id'] = None

        return {}, 204

class Signup(Resource):
    
    def post(self):
        json = request.get_json()
        user = User(username=json['username'],)
        user.password_hash=json['password']
        db.session.add(user)
        db.session.commit()
        return user.to_dict(), 201

class CheckSession(Resource):
    def get(self):
        user = User.query.filter_by(id=session['user_id']).first()
        if user:
            resp = make_response(
                user.to_dict(),
                200
            )
            return resp
        else:
            resp = make_response(
                {},
                204
            )
            return resp

class Login(Resource):
    def post(self):
        json = request.get_json()
        user = User.query.filter_by(username=json['username']).first()
        password = json['password']

        if user.authenticate(password):
            session['user_id'] = user.id
            resp = make_response(
                user.to_dict(),
                200
            )
            return resp
        resp = make_response(
            {"error": "Invalid username or password"},
            401
        )
        return resp
    
class Logout(Resource):
    def delete(self):
        session['user_id'] = None
        resp = make_response(
            {'message': '204: No Content'},
            204
        )
        return resp

api.add_resource(CheckSession, '/check_session', endpoint='check_session')    
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(ClearSession, '/clear', endpoint='clear')
api.add_resource(Signup, '/signup', endpoint='signup')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
