from flask import jsonify
from webargs.flaskparser import use_args

from book_library_app import db
from book_library_app.authors import authors_bd
from book_library_app.models import Author, AuthorsSchema, author_schema
from book_library_app.utils import validate_json_content_type, get_schema_args, apply_order, apply_filter, get_pagination, token_required


@authors_bd.route('/authors', methods=['GET'])
def get_authors():
    query = Author.query
    schema_args = get_schema_args(Author)
    query = apply_order(Author, query)
    query = apply_filter(Author, query)
    items, pagination = get_pagination(query, 'authors.get_authors')

    authors = AuthorsSchema(**schema_args).dump(items)
    return jsonify({
        'success': True,
        'data': authors,
        'number_of_records': len(authors),
        'pagination': pagination
    })


@authors_bd.route('/authors/<int:authors_id>', methods=['GET'])
def get_author(authors_id: int):
    author = Author.query.get_or_404(authors_id, description=f"Author with id {authors_id} not found")
    return jsonify({
        'success': True,
        'data': author_schema.dump(author)
    })


@authors_bd.route('/authors', methods=['POST'])
@token_required
@validate_json_content_type
@use_args(author_schema, error_status_code=400)
def create_author(user_id: int, args: dict):
    author = Author(**args)
    db.session.add(author)
    db.session.commit()

    return jsonify({
        'success': True,
        'data': author_schema.dump(author)
    }), 201


@authors_bd.route('/authors/<int:authors_id>', methods=['PUT'])
@token_required
@validate_json_content_type
@use_args(author_schema, error_status_code=400)
def update_author(user_id: int, args: dict, authors_id: int):
    author = Author.query.get_or_404(authors_id, description=f"Author with id {authors_id} not found")

    author.first_name = args['first_name']
    author.last_name = args['last_name']
    author.birth_date = args['birth_date']

    db.session.commit()

    return jsonify({
        'success': True,
        'data': author_schema.dump(author)
    })


@authors_bd.route('/authors/<int:authors_id>', methods=['DELETE'])
@token_required
def delete_author(user_id: int, authors_id: int):
    author = Author.query.get_or_404(authors_id, description=f"Author with id {authors_id} not found")

    db.session.delete(author)
    db.session.commit()

    return jsonify({
        'success': True,
        'data': f'Author with id {authors_id} has been deleted'
    })