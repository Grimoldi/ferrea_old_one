from neomodel import db

query = (
    "MATCH (u:User)"
    "RETURN "
    "u.username, u.name, u.surname"
)
users = db.cypher_query(query)[0]
users_dict = dict()

for user in users:
    email = user[0]
    name = user[1]
    surname = user[2]

    users_dict[email] = {"name": name, "surname": surname}

USERS = users_dict
