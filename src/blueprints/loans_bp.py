from flask import Blueprint, request
from datetime import date, timedelta
from flask_jwt_extended import jwt_required, get_jwt_identity
from init import db
from models.loan import Loan, LoanSchema
from models.book import Book, BookSchema
from models.user import User


loans_bp = Blueprint("loans", __name__, url_prefix='/loans')


# Borrow a Book (C)
@loans_bp.route("/<int:book_id>", methods=["POST"])
@jwt_required()
def new_loan(book_id):
    # Get current user ID to link to added loan
    current_user_id = get_jwt_identity()
    # Get book attempting to be loaned from the database, or throw an error if book does not exist
    book = db.get_or_404(Book, book_id)
    # Check the book is available to be loaned
    if not book.is_available:
        return {"error": "Book is not available to be loaned"}, 403
    # Get loan info from request
    loan_info = LoanSchema(only = ["borrow_length"], unknown = "exclude").load(request.json)
    # Create a new instance of Loan with data provided from request
    loan = Loan(
        book_id = book.id,
        user_id = current_user_id,
        borrow_length = loan_info["borrow_length"],
        borrow_date = date.today(),
        return_date = date.today() + timedelta(days = loan_info["borrow_length"])
    )
    # Update availability status of book
    book.is_available = False
    # Add the loan to the database
    db.session.add(loan)
    db.session.commit()
    return LoanSchema().dump(loan), 201