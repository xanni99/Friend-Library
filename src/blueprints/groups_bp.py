from flask import Blueprint
import random
from init import db
from models.group import Group, GroupSchema


groups_bp = Blueprint('groups', __name__, url_prefix="/groups")


@groups_bp.route("/")
def create_group():
    while True:
        new_code = random.randint(1000,999999)
        if Group.query.filter_by(code=new_code).first() is None:
            break
    group = Group(code=new_code)
    db.session.add(group)
    db.session.commit()
    return GroupSchema().dump(group), 201