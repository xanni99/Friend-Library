from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)
from init import db
from models.user import User
from flask import abort, jsonify, make_response


# Route decorator - ensure JWT user is an admin
def admin_only(fn):
    @jwt_required()
    def inner():
        user_id = get_jwt_identity()
        stmt = db.select(User).where(User.id == user_id, User.is_admin)
        user = db.session.scalar(stmt)
        if user:
            return fn()
        else:
            return {"error": "You must be an admin to access this resource"}, 403

    return inner


# Ensure that the JWT user is owner of profile
def authorize_owner(user):
    user_id = get_jwt_identity()
    if user_id != user.user_id:
        abort(make_response(jsonify(error="You must be the owner of the account to update details"),403))