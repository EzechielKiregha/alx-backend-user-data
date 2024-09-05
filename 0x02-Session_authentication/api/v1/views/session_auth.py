#!/usr/bin/env python3
"""
session auth routes
"""


from api.v1.views import app_views
from flask import request, jsonify, abort
from models.user import User
import os


@app_views.route("/auth_session/login", methods=['POST'], strict_slashes=False)
def login():
    """
    for login a specific user
    """
    email = request.form.get("email")
    passwd = request.form.get("password")

    # if email is None:
    #     return jsonify({"error": "email missing"}), 400
    if email is None or len(email.strip()) == 0:
        return jsonify({"error": "email missing"}), 400
    if passwd is None or len(passwd.strip()) == 0:
        return jsonify({"error": "password missing"}), 400
    try:
        users = User.search({"email": email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404
    if len(users) <= 0:
        return jsonify({"error": "no user found for this email"}), 404
    if users[0].is_valid_password(passwd):
        from api.v1.app import auth
        session_id = auth.create_session(getattr(users[0], 'id'))
        user = jsonify(users[0].to_json())
        user.set_cookie(os.getenv("SESSION_NAME"), session_id)
        return user
    return jsonify({"error": "wrong password"}), 401


@app_views.route("/auth_session/logout",
                 methods=['DELETE'],
                 strict_slashes=False
                 )
def logout():
    """
    a logout function
    that destroys a session for the user
    loggin
    """
    from api.v1.app import auth
    flag = auth.destroy_session(request)
    if flag is None:
        abort(404)
    return jsonify({}), 200
