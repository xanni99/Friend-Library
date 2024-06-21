from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from init import db
from models.book import Book, BookSchema, UpdateBookSchema
from models.user import User
from auth import get_group_id


books_bp = Blueprint("books", __name__, url_prefix='/books')


# Add a new book (C)
@books_bp.route("/", methods=["POST"])
@jwt_required()
def add_book():
    # Get current user ID to link to added book
    current_user_id = get_jwt_identity()
    # Get book info from request
    book_info = BookSchema(only = ["title", "author", "description", "genre","is_available"], unknown = "exclude").load(request.json)
    # Create a new instance of Book with data provoded from request
    book = Book(
        title = book_info["title"],
        author = book_info["author"],
        genre = book_info["genre"],
        description = book_info["description"],
        is_available = book_info.get("is_available", True),
        user_id = current_user_id
    )
    # Add the book to the database
    db.session.add(book)
    db.session.commit()
    return BookSchema().dump(book), 201


# View all books (R)
@books_bp.route("/")
@jwt_required()
def all_books():
    user_group_id = get_group_id()
    # Get all of the books from the database where the books belong to user's with the same group id
    stmt = db.select(Book).join(User).filter(User.group_id == user_group_id)
    # Return all books from the database where the user_group_id exists within the books' user_id
    books = db.session.scalars(stmt).all()
    return BookSchema(many=True, only=["title", "author", "description", "genre","is_available", "reviews"]).dump(books)


# View one book (R)
@books_bp.route("/<int:id>")
@jwt_required()
def one_book(id):
    # Get group_id of curent user by calling auth function
    user_group_id = get_group_id()
    # Get the specified book from the database, using the parsed book id where the book_id exists within the group id
    book = db.session.query(Book).join(User).filter(User.group_id == user_group_id, Book.id == id).first_or_404()
    return BookSchema(only=["title", "author", "description", "genre","is_available", "reviews"]).dump(book)


# View all AVAILABLE books (R)
@books_bp.route("/available")
@jwt_required()
def available_books():
    user_group_id = get_group_id()
    # Get all books from the database where is_available = True, and the user_group_id exists within the books' user_id
    stmt = db.select(Book).where(Book.is_available == True).join(User).filter(User.group_id == user_group_id)
    books = db.session.scalars(stmt).all()
    # Return all books that meet the above criteria and display the following attributes in the response
    return BookSchema(many=True, only=["title", "author", "description", "genre","is_available", "reviews"]).dump(books)


# Update a book (U)
@books_bp.route("/update/<int:id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_book(id):
    # Get current user id and group_id and ensure the book attempting to be updated from the database exists
    current_user_id = get_jwt_identity()
    user_group_id = get_group_id()
    book = db.session.query(Book).join(User).filter(User.group_id == user_group_id, Book.id == id).first_or_404()
    # Check the current user is the owner of the book attempting to be updated
    if book.user_id != current_user_id:
        return {"error": "You must be the owner of the book to update details"}, 403
    # Get updated book information from the rquest
    book_info = UpdateBookSchema(only=["title", "author", "description", "genre","is_available"], unknown="exclude").load(request.json)
    book.title = book_info.get("title", book.title)
    book.author = book_info.get("author", book.author)
    book.genre = book_info.get("genre", book.genre)
    book.description = book_info.get("description", book.description)
    book.is_available = book_info.get("is_available", book.is_available)
    # Save new changes to the database
    db.session.commit()
    # Return book with updated information
    return UpdateBookSchema().dump(book), 200


# Delete a book (D)
@books_bp.route("/delete/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_book(id):
    # Get current user ID and the book attempting to be deleted from the database
    current_user_id = get_jwt_identity()
    current_user = db.get_or_404(User, current_user_id)
    user_group_id = get_group_id()
    book = db.session.query(Book).join(User).filter(User.group_id == user_group_id, Book.id == id).first_or_404()
    # Check the current user is the owner of the book attempting to be deleted, or an admin
    if current_user_id != book.user_id and not current_user.is_admin:
        return {"error": "You must be the owner of the account, or an admin to delete a book"}, 403
    # Delete the book from the database
    db.session.delete(book)
    db.session.commit()
    # Return message that book has been deleted
    return {"message": "Book deleted"}, 200