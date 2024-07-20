from neomodel import db

query = (
    "MATCH (b:Book)"
    "RETURN b.title AS title, b.barcode AS barcode"
)
books = db.cypher_query(query)[0]

BOOKS = [{'barcode': book[1], 'title':book[0]} for book in books]
