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


@app.errorhandler(KeyError)
def missing_key(err):
    return {"error": f"Missing field: {str(err)}"}, 400


@app.errorhandler(400)
def bad_request(err):
    return {"error": "All Fields Required for this request"}, 400


@app.errorhandler(404)
def not_found(err):
    return {"error": f"Requested URL does not exist"}, 404