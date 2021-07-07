from flask import Blueprint

authors_bd = Blueprint('authors', __name__)

from book_library_app.authors import authors