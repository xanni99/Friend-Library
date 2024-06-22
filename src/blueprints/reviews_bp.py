from flask import Blueprint, request
from datetime import date
from flask_jwt_extended import jwt_required, get_jwt_identity
from init import db
from models.review import Review, ReviewSchema, UpdateReviewSchema
from models.user import User
from models.book import Book
from auth import get_group_id


reviews_bp = Blueprint("reviews", __name__, url_prefix='/reviews')


# Review a Book (C)
@reviews_bp.route("/add/<int:book_id>", methods=["POST"])
@jwt_required()
def add_review(book_id):
    # Get current user ID to link to added review
    current_user_id = get_jwt_identity()
    # Get the current_user_group_id to ensure they are only accessing data from their group
    user_group_id = get_group_id()
    # Get the instance of book attempting to be reviewed where the user_group_id exists within the book's user_id and where the book_id is =the given id
    book = db.session.query(Book).join(User).filter(User.group_id == user_group_id, Book.id == book_id).first_or_404()
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
    # Get current_user_group_id to ensure they are only accessing data from their group
    user_group_id = get_group_id()
    # Get all reviews from the database
    stmt = db.select(Review).join(User).filter(User.group_id == user_group_id)
    # Return all reviews from the database
    reviews = db.session.scalars(stmt).all()
    if not reviews:
        return {"message": "No Reviews Available"}, 200
    return ReviewSchema(many=True, only=["rating", "review", "date", "user", "book"]).dump(reviews)


# View Reviews for a Book (R)
@reviews_bp.route("/<int:book_id>")
@jwt_required()
def book_reviews(book_id):
    # Get current_user_group_id to ensure they are only accessing data from their group
    user_group_id = get_group_id()
    book = db.session.query(Book).join(User).filter(User.group_id == user_group_id, Book.id == book_id).first_or_404()
    if not book:
        return {"error": "Book does not exist"}, 404
    # Get all reviews from the database where book = id of book requested
    stmt = db.select(Review).where(Review.book_id == book_id)
    # Return all reviews from the database with this book id
    reviews = db.session.scalars(stmt).all()
    if not reviews:
        return {"message": "No Reviews for this book"}, 200
    return ReviewSchema(many=True, only=["rating", "review", "date", "user", "book"]).dump(reviews)


# Update a Book Review (U)
@reviews_bp.route("/update/<int:id>", methods=["PUT","PATCH"])
@jwt_required()
def update_review(id):
    # Get current_user_group_id to ensure they are only accessing data from their group
    user_group_id = get_group_id()
    # Get current user ID and the review attempting to be updated from the database, error if review does not exist
    current_user_id = get_jwt_identity()
    review = db.session.query(Review).join(User).filter(Review.id == id, User.group_id == user_group_id).first_or_404()
    # Check the current user is the creator of the review attempting to be updated
    if review.user_id != current_user_id:
        return {"error": "You must be the creator of the review to update"}, 403
    # Get updated review information from the request
    review_info = UpdateReviewSchema(only = ["rating", "review"], unknown = "exclude").load(request.json)
    review.rating = review_info.get("rating", review.rating)
    review.review = review_info.get("review", review.review)
    # Save new changes to the database
    db.session.commit()
    # Return book with updated information
    return UpdateReviewSchema(exclude=["id"]).dump(review), 200

# Delete a Book Review (D)
@reviews_bp.route("/delete/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_review(id):
    # Get current_user_group_id to ensure they are only accessing data from their group
    user_group_id = get_group_id()
    # Get current user ID and the review attempting to be deleted from the database, error if review does not exist
    current_user_id = get_jwt_identity()
    current_user = db.get_or_404(User, current_user_id)
    review = db.session.query(Review).join(User).filter(Review.id == id, User.group_id == user_group_id).first_or_404()
    # Check the current user is the owner of the review attempting to be deleted, or an admin
    if current_user_id != review.user_id and not current_user.is_admin:
        return {"error": "You must be the creator of the review, or an admin to delete it"}, 403
    # Delete the review from the database
    db.session.delete(review)
    db.session.commit()
    # Return message that review has been deleted
    return {"message": "Review deleted"}, 200