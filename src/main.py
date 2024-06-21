from init import app
from marshmallow.exceptions import ValidationError
from blueprints.cli_bp import db_commands
from blueprints.groups_bp import groups_bp
from blueprints.users_bp import users_bp
from blueprints.books_bp import books_bp
from blueprints.reviews_bp import reviews_bp
from blueprints.loans_bp import loans_bp


app.register_blueprint(db_commands)
app.register_blueprint(groups_bp)
app.register_blueprint(users_bp)
app.register_blueprint(books_bp)
app.register_blueprint(reviews_bp)
app.register_blueprint(loans_bp)


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.errorhandler(ValidationError)
def invalid_request(err):
    return ({"error": err.messages}), 400