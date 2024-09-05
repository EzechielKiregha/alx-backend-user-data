#!/usr/bin/env python3
"""
Route module for the API
"""
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth
from api.v1.auth.session_exp_auth import SessionExpAuth
from api.v1.auth.session_db_auth import SessionDBAuth

from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
auth_method = getenv("AUTH_TYPE")
if auth_method == "auth":
    auth = Auth()
if auth_method == "basic_auth":
    auth = BasicAuth()
if auth_method == 'session_auth':
    auth = SessionAuth()
if auth_method == "session_exp_auth":
    auth = SessionExpAuth()
if auth_method == "session_db_auth":
    auth = SessionDBAuth()


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def Unauthorized(error) -> str:
    """
    Unauthorized error handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """
    error handler for a forbidden
    request
    """
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def before_request():
    """
    this is a function that will be running before each
    requests
    """
    url_path = request.path
    authorized_url = ['/api/v1/status/',
                      '/api/v1/unauthorized/',
                      '/api/v1/forbidden/',
                      '/api/v1/auth_session/login/'
                      ]
    # flag = auth.require_auth(url_path, authorized_url)
    # if flag and auth:
    #     if not auth.authorization_header(request):
    #         abort(401)
    #     request.current_user = auth.current_user(request)
    #     if not request.current_user:
    #         abort(403)
    #     # if auth.authorization_header(request) and \
    #     #     auth.session_cookie(request):
    #     #         abort(401)
    if auth.require_auth(request.path, authorized_url):
        user = auth.current_user(request)
        if auth.authorization_header(request) is None and \
                auth.session_cookie(request) is None:
            abort(401)
        if user is None:
            abort(403)
        request.current_user = user


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
