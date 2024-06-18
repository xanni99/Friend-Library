from init import app
from blueprints.cli_bp import db_commands


app.register_blueprint(db_commands)

@app.route('/')
def hello_world():
    return 'Hello, World!'