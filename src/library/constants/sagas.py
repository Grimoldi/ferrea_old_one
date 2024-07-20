from neomodel import db

query = (
    "MATCH (s:Saga)"
    "RETURN s.series AS title"
)
sagas = db.cypher_query(query)[0]

SAGAS = sorted([saga[0] for saga in sagas])
