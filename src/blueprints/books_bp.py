from datetime import date
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from auth import authorize_owner
from init import db
from models.book import Book, BookSchema


books_bp = Blueprint("books", __name__, url_prefix='/books')


# Add a new book (C)
@books_bp.route("/", methods=["POST"])
@jwt_required()
def add_book():
    current_user_id = get_jwt_identity()
    book_info = BookSchema(only = ["title", "author", "description", "genre","is_available"], unknown = "exclude").load(request.json)
    book = Book(
        title = book_info["title"],
        author = book_info["author"],
        genre = book_info["genre"],
        description = book_info["description"],
        is_available = book_info.get("is_available", True),
        user_id = current_user_id
    )
    db.session.add(book)
    db.session.commit()
    return BookSchema().dump(book), 201


# View all books (R)
@books_bp.route("/")
def all_books():
    stmt = db.select(Book)
    books = db.session.scalars(stmt).all()
    return BookSchema(many=True, only=["title", "author", "description", "genre","is_available", "reviews"]).dump(books)


# View one book (R)
@books_bp.route("/<int:id>")
def one_book(id):
    book = db.get_or_404(Book, id)
    return BookSchema(only=["title", "author", "description", "genre","is_available", "reviews"]).dump(book)


# View all AVAILABLE books (R)
@books_bp.route("/available")
def available_books():
    stmt = db.select(Book).where(Book.is_available == True)
    books = db.session.scalars(stmt).all()
    return BookSchema(many=True, only=["title", "author", "description", "genre","is_available", "reviews"]).dump(books)