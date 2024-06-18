from datetime import date
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from auth import authorize_owner
from init import db
from models.book import Book, BookSchema


books_bp = Blueprint("books", __name__, url_prefix='/books')


# Get all books (R)
@books_bp.route("/")
def all_books():
    stmt = db.select(Book)
    books = db.session.scalars(stmt).all()
    return BookSchema(many=True, only=["title", "author", "description", "genre","is_available", "reviews"]).dump(books)


# Get one book (R)
@books_bp.route("/<int:id>")
def one_book(id):
    book = db.get_or_404(Book, id)
    return BookSchema(only=["title", "author", "description", "genre","is_available", "reviews"]).dump(book)