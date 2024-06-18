from flask import Blueprint, request
import random
from init import db
from models.group import Group, GroupSchema


groups_bp = Blueprint('groups', __name__, url_prefix="/groups")


# Create a group (C)
@groups_bp.route("/", methods=["POST"])
def create_group():
    # Get group name 
    group_name = GroupSchema(only = ["name"], unknown="exclude").load(request.json)
    # Create a new group with a random id
    while True:
        new_id = random.randint(1000,999999)
        if Group.query.filter_by(id=new_id).first() is None:
            break
    group = Group(
        id=new_id,
        name=group_name["name"]
        )
    db.session.add(group)
    db.session.commit()
    return GroupSchema().dump(group), 201