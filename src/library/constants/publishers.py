from neomodel import db

query = (
    "MATCH (p:Publisher)"
    "RETURN p.publishing AS publishing"
)
publishers = db.cypher_query(query)[0]

PUBLISHERS = sorted([publisher[0] for publisher in publishers])
