from neomodel import db

query = (
    "MATCH (l:Library)"
    "RETURN l.name AS libraries"
)
libraries = db.cypher_query(query)[0]

LIBRARIES = sorted([library[0] for library in libraries])
