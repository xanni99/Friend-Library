from datetime import date
from flask import Blueprint
from models.group import Group
from models.user import User
from models.book import Book
from models.loan import Loan
from models.review import Review
from init import app, db, bcrypt


db_commands = Blueprint('db', __name__)


@db_commands.cli.command("create")
def db_create():
    db.drop_all()
    db.create_all()
    print("Created tables")

    groups = [
        Group(code=1234),
        Group(code=5678),
    ]

    db.session.add_all(groups)
    db.session.commit()
    
    users = [
        User(
            email="admin@test.com",
            name = "Gru",
            password=bcrypt.generate_password_hash("stealthemoon").decode("utf8"),
            is_admin=True,
        ),
        User(
            email="user2@test.com",
            name="Kevin",
            password=bcrypt.generate_password_hash("BANANA").decode("utf8"),
        ),
    ]

    db.session.add_all(users)
    db.session.commit()

    books = [
        Book(
            title="Harry Potter and the Philosopher's Stone",
            author="J. K. Rowling",
            genre= "Fantasy",
            description="The first novel in the Harry Potter series and Rowling's debut novel, it follows Harry Potter, a young wizard who discovers his magical heritage on his eleventh birthday, when he receives a letter of acceptance to Hogwarts School of Witchcraft and Wizardry. Harry makes close friends and a few enemies during his first year at the school and with the help of his friends, Ron Weasley and Hermione Granger, he faces an attempted comeback by the dark wizard Lord Voldemort, who killed Harry's parents, but failed to kill Harry when he was just 15 months old.",
            user=users[0],
            is_available=True
        ),
        Book(
            title="The Midnight Library",
            author="Matt Haig",
            genre= "Fantasy",
            description="The Midnight Library by Matt Haig is a novel that follows the life of Nora Seed, who finds herself in a library between life and death, with the opportunity to try out alternate versions of her life and find the one where she truly belongs.",
            user=users[0],
            is_available=True
        ),
    ]

    db.session.add_all(books)
    db.session.commit()




    print("Groups, Users, Books, Reviews and Loans added")