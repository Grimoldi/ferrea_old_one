from neomodel import db

query = (
    "MATCH (a:Author)"
    "RETURN a.author AS author, a.portrait as portrait"
)
authors = db.cypher_query(query)[0]

AUTHORS = sorted([author[0] for author in authors])
