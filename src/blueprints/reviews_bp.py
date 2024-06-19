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
@reviews_bp.route("/")
@jwt_required()
def all_reviews():
    # Get all reviews from the database
    stmt = db.select(Review)
    # Return all reviews from the database
    reviews = db.session.scalars(stmt).all()
    return ReviewSchema(many=True, only=["rating", "review", "date", "user", "book"]).dump(reviews)


# View Reviews for a Book (R)
@reviews_bp.route("/<int:book_id>")
@jwt_required()
def book_reviews(book_id):
    book = db.get_or_404(Book, book_id)
    if not book:
        return {"error": "Book does not exist"}, 404
    # Get all reviews from the database where book = id of book requested
    stmt = db.select(Review).where(Review.book_id == book_id)
    # Return all reviews from the database with this book id
    reviews = db.session.scalars(stmt).all()
    return ReviewSchema(many=True, only=["rating", "review", "date", "user", "book"]).dump(reviews)


# Update a Book Review (U)
@reviews_bp.route("/update/<int:id>", methods=["PUT","PATCH"])
@jwt_required()
def update_review(id):
    # Get current user ID and the review attempting to be updated from the database, error if review does not exist
    current_user_id = get_jwt_identity()
    review = db.get_or_404(Review, id)
    # Check the current user is the creator of the review attempting to be updated
    if review.user_id != current_user_id:
        return {"error": "You must be the creator of the review to update"}, 403
    # Get updated review information from the request
    review_info = ReviewSchema(only = ["rating", "review"], unknown = "exclude").load(request.json)
    review.rating = review_info.get("rating", review.rating)
    review.review = review_info.get("review", review.review)
    # Save new changes to the database
    db.session.commit()
    # Return book with updated information
    return ReviewSchema().dump(review), 200

# Delete a Book Review (D)
@reviews_bp.route("/delete/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_review(id):
# Get current user ID and the review attempting to be deleted from the database, error if review does not exist
    current_user_id = get_jwt_identity()
    current_user = db.get_or_404(User, current_user_id)
    review = db.get_or_404(Review, id)
    # Check the current user is the owner of the review attempting to be deleted, or an admin
    if current_user_id != review.user_id and not current_user.is_admin:
        return {"error": "You must be the creator of the review, or an admin to delete it"}, 403
    # Delete the review from the database
    db.session.delete(review)
    db.session.commit()
    # Return message that review has been deleted
    return {"message": "Review deleted"}, 200