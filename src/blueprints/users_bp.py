from datetime import timedelta
from flask import Blueprint
from flask import request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from init import db, bcrypt
from models.user import User, UserSchema, UserUpdateSchema
from models.group import Group
from auth import get_group_id


users_bp = Blueprint('users', __name__, url_prefix="/users")


# Create a user (C)
@users_bp.route("/", methods=["POST"])
def create_user():
    # Get User data
    user_data= UserSchema(only=["name", "email", "password", "group_id", "is_admin"]).load(request.json, unknown="exclude")
    # Check if user already exists in database by checking unique email
    if User.query.filter_by(email=user_data["email"]).first() is not None:
        return {"error": "User with this email already exists"}, 400
    # Check group id matches an existing group in the database
    if Group.query.filter_by(id=user_data["group_id"]).first() is None:
        return {"error": "Group does not exist"}, 400
    # Hash password for storing in db
    user_data["password"] = bcrypt.generate_password_hash(user_data["password"]).decode("utf-8")
     # Create user and add to the database
    user = User(**user_data)
    db.session.add(user)
    db.session.commit()
    return UserSchema(exclude=["password", "is_admin", "group_id"]).dump(user_data), 201


# User Login and token generation (C)
@users_bp.route("/login", methods=["POST"])
def login():
    params = UserSchema(only=["email", "password"]).load(request.json, unknown="exclude")
    # Check given email exists in the database
    stmt = db.select(User).where(User.email == params["email"])
    user = db.session.scalar(stmt)
    # If the email does exist, check the given password matches the hashed password in the database
    if user and bcrypt.check_password_hash(user.password, params["password"]):
        token = create_access_token(identity=user.id, expires_delta=timedelta(hours=2))
        return {"token": token}, 200
    else:
        return {"error": "Invalid email or password"}, 401
    

# Get all users (R)
@users_bp.route("/")
@jwt_required()
def get_all_users():
    # Get current_user_group_id to ensure they are only accessing data from their group
    user_group_id = get_group_id()
    # Get all users from the database that have the same group_id as the current user
    stmt = db.select(User).filter(User.group_id == user_group_id)
    users = db.session.scalars(stmt).all()
    # Return all users in the database only showing their name and books in the result
    return UserSchema(only=["name", "books"],many=True).dump(users), 200


# Update User (U)
@users_bp.route("/update/<int:id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_user(id):
    current_user_id = get_jwt_identity()
    if current_user_id!= id:
        return {"error": "You must be the owner of the account to update details"}, 403
    user = db.get_or_404(User, id)
    user_info = UserUpdateSchema(only=["name", "email", "password"]).load(request.json, unknown="exclude")
    user.name = user_info.get("name", user.name)
    user.email = user_info.get("email", user.email)
    new_password = user_info.get("password")
    if new_password:
        user.password = bcrypt.generate_password_hash(new_password).decode("utf-8")

    db.session.commit()
    return {"message": "Details Successfully Updated"}, 200


# Delete User (D)
@users_bp.route("/delete/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_user(id):
    # Check if the user trying to delete is the owner of the account, or an admin
    current_user_id = get_jwt_identity()
    current_user = db.get_or_404(User, current_user_id)
    if current_user_id!= id and not current_user.is_admin:
        return {"error": "You must be the owner of the account, or an admin to delete details"}, 403
    # Now authorised, get corresponding user profile using given ID
    user = db.get_or_404(User, id)
    # Delete the user from the database
    db.session.delete(user)
    db.session.commit()
    return {"message": "User deleted"}, 204
