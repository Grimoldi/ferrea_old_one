from neomodel import db

query = (
    "MATCH (b:Book)-[r:BELONGS_TO]->(s:Saga) "
    "MATCH (a:Author)-[t:WROTE]->(b) "
    "OPTIONAL MATCH(p:Publisher)-[u:PUBLISHED]->(b) "

    "return "
    "b.barcode, b.title, b.cover, "
    "s.series, "
    "a.author, "
    "p.publishing"
)
previews = db.cypher_query(query)[0]
previews_dict = dict()

for preview in previews:
    barcode = preview[0]
    isbn = barcode[0:len(barcode) - 3]
    title = preview[1]
    cover = preview[2]
    series = preview[3]
    author = preview[4]
    publishing = preview[5]

    # some books are written by multiple authors
    if isbn in previews_dict.keys():
        is_already_list = isinstance(previews_dict[isbn]["author"], list)

        # if author is a list and author is not already listed, append the current author
        if is_already_list:
            is_author_already_listed = author in previews_dict[isbn]["author"]
            if not is_author_already_listed:
                previews_dict[isbn]["author"].append(author)

        # if author wasn't a list and author is not equals to current author
        # convert the value to a list and append the current author
        else:
            is_author_already_listed = author == previews_dict[isbn]["author"]
            if not is_author_already_listed:
                author_list = list()
                author_list.append(previews_dict[isbn]["author"])
                author_list.append(author)
                previews_dict[isbn]["author"] = author_list

    # isbn is not in keys
    else:
        previews_dict[isbn] = {
            'isbn': isbn,
            'title': title,
            'cover': cover,
            'series': series,
            'author': [author],
            'publishing': publishing,
        }


PREVIEWS = previews_dict
