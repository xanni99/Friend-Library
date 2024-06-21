from flask import Blueprint, request
from datetime import date, timedelta
from flask_jwt_extended import jwt_required, get_jwt_identity
from init import db
from auth import admin_only
from models.loan import Loan, LoanSchema
from models.book import Book
from models.user import User
from auth import get_group_id


loans_bp = Blueprint("loans", __name__, url_prefix='/loans')


# Borrow a Book (C)
@loans_bp.route("/borrow/<int:book_id>", methods=["POST"])
@jwt_required()
def new_loan(book_id):
    # Get the current_user_group_id to ensure they are only accessing data from their group
    user_group_id = get_group_id()
    # Get current user ID to link to added loan
    current_user_id = get_jwt_identity()
    # Get book attempting to be loaned from the database ensuring it exists within user's group, or throw an error if book does not exist
    book = db.session.query(Book).join(User).filter(User.group_id == user_group_id, Book.id == book_id).first_or_404()
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
        due_date = date.today() + timedelta(days = loan_info["borrow_length"])
    )
    # Update availability status of book
    book.is_available = False
    # Add the loan to the database
    db.session.add(loan)
    db.session.commit()
    return LoanSchema().dump(loan), 201


# Return a Book (U)
@loans_bp.route("/return/<int:loan_id>", methods=["PATCH"])
@jwt_required()
def return_book(loan_id):
    # Get the current_user_group_id to ensure they are only accessing data from their group
    user_group_id = get_group_id()
    # Get current user ID to confirm it is their loan
    current_user_id = get_jwt_identity()
    # Get the instance of loan attempting to be completed (book returned) from the database ensuring that user_group_id exists within the user_id of the loan, or throw an error if record does not exist
    loan = db.session.query(Loan).join(User).filter(User.group_id == user_group_id, Loan.id == loan_id).first_or_404()
    # Check the current user is the owner of the loan attempting to be completed
    if loan.user_id!= current_user_id:
        return {"error": "You did not borrow this book"}, 403
    # Get instance of the book being returned from the database
    book = db.get_or_404(Book, loan.book_id)
    # Update availability status of book (allowing it to be borrowed again)
    book.is_available = True
    # Update returned status of loan
    loan.returned_status = True
    # Update returned date of loan
    loan.returned_date = date.today()
    # Commit changes to the database
    db.session.commit()
    return LoanSchema().dump(loan), 200


# View Own User Loans (R)
@loans_bp.route("/")
@jwt_required()
def user_loans():
    # Get current user ID
    current_user_id = get_jwt_identity()
    # Get all loans made by current user from the database
    stmt = db.select(Loan).where(Loan.user_id == current_user_id)
    # Return all loans from the database
    loans = db.session.scalars(stmt).all()
    return LoanSchema(many=True, exclude= ["id"]).dump(loans)



# View entire Loan history (R)
@loans_bp.route("/all")
@admin_only
def all_loans():
    # Get user group_id to ensure only loans from their group can be accessed
    user_group_id = get_group_id()
    # Get all loans from the database where the user_group_id exists within the loans' user_id
    stmt = db.select(Loan).join(User).filter(User.group_id == user_group_id)
    # Return all loans from the database
    loans = db.session.scalars(stmt).all()
    return LoanSchema(many=True, exclude= ["id"]).dump(loans)

