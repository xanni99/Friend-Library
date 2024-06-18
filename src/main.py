from init import app
from blueprints.cli_bp import db_commands
from blueprints.groups_bp import groups_bp
from blueprints.users_bp import users_bp


app.register_blueprint(db_commands)
app.register_blueprint(groups_bp)
app.register_blueprint(users_bp)

@app.route('/')
def hello_world():
    return 'Hello, World!'