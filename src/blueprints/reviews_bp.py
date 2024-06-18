from flask import Blueprint, request
from datetime import date
from flask_jwt_extended import jwt_required, get_jwt_identity
from init import db
from models.review import Review, ReviewSchema
from models.user import User
from models.book import Book


reviews_bp = Blueprint("reviews", __name__, url_prefix='/reviews')


# Review a Book (C)
@reviews_bp.route("/add/<int:book_id>", methods=["POST"])
@jwt_required()
def add_review(book_id):
    # Get current user ID to link to added review
    current_user_id = get_jwt_identity()
    # Get book attempting to be reviewed from the database, or throw an error if book does not exist
    book = db.get_or_404(Book, book_id)
    # Get review info from request
    review_info = ReviewSchema(only = ["rating", "review"], unknown = "exclude").load(request.json)
    # Create a new instance of Review with data provoded from request
    review = Review(
        rating = review_info["rating"],
        review = review_info["review"],
        user_id = current_user_id,
        book_id = book.id,
        date = date.today()
    )
    # Add the review to the database
    db.session.add(review)
    db.session.commit()
    return ReviewSchema(only=["rating", "review"]).dump(review), 201




# View All Book Reviews (R)


# View A Book Review (R)


# Update a Book Review (U)


# Delete a Book Review (D)