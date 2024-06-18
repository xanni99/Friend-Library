from datetime import timedelta
from flask import Blueprint
from flask import request
from flask_jwt_extended import create_access_token
from init import db, bcrypt
from models.user import User, UserSchema


users_bp = Blueprint('users', __name__, url_prefix="/users")


@users_bp.route("/", methods=["POST"])
def create_user():
    # Get User data
    user_data= UserSchema(only=["name", "email", "password", "group_id", "is_admin"]).load(request.json, unknown="exclude")
    # Check if user already exists in database 
    if User.query.filter_by(email=user_data["email"]).first() is not None:
        return {"error": "User with this email already exists"}, 400
    # Check group id matches an existing group in the database
    if User.query.filter_by(group_id=user_data["group_id"]).first() is None:
        return {"error": "Group does not exist"}, 400
    # Hash password for storing in db
    user_data["password"] = bcrypt.generate_password_hash(user_data["password"]).decode("utf-8")
     # Create user
    user = User(**user_data)
    db.session.add(user)
    db.session.commit()
    return UserSchema().dump(user_data), 201
