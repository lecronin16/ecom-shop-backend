from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_cors import CORS, cross_origin

# from flask import Flask,request,jsonify
# app=Flask(__name__)
# CORS(app, support_credentials=True)

#import login funcitonality
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash

# import models
from app.models import User

auth = Blueprint('auth', __name__, template_folder='authtemplates')

from app.models import db

# API
# supports_credentials=True
@auth.route('/api/signup', methods=["POST"])
@cross_origin()
def apiSignMeUp():
    data = request.json
     
    username = data['username']
    email = data['email']
    password = data['password']

    # add user to database
    user = User(username, email, password)

    # add instance to our db
    db.session.add(user)
    db.session.commit()
    return {
        'status': 'ok',
        'message': f"User created {username}"
    }


from app.apiauthhelper import basic_auth, token_auth

@auth.route('/token', methods=['POST'])
@cross_origin()
@basic_auth.login_required
def getToken():
    user = basic_auth.current_user()
    return {
                'status': 'ok',
                'message': "Login successful",
                'data':  user.to_dict()
            }


@auth.route('/api/login', methods=["POST"])
@cross_origin()
def apiLogMeIn():
    data = request.json

    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()

    if user:
        # check password
        if check_password_hash(user.password, password):
            return {
                'status': 'ok',
                'message': "Login successful",
                'data':  user.to_dict()
            }
        return {
            'status': 'not ok',
            'message': "Incorrect password."
        }
    return {
        'status': 'not ok',
        'message': 'Invalid username.'
    }
