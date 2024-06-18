from init import app
from blueprints.cli_bp import db_commands
from blueprints.groups_bp import groups_bp
from blueprints.users_bp import users_bp
from blueprints.books_bp import books_bp
from blueprints.reviews_bp import reviews_bp


app.register_blueprint(db_commands)
app.register_blueprint(groups_bp)
app.register_blueprint(users_bp)
app.register_blueprint(books_bp)
app.register_blueprint(reviews_bp)


@app.route("/")
def hello_world():
    return "Hello, World!"
