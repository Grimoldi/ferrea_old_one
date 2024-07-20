import requests
import json
from itertools import groupby
from operator import itemgetter

if __name__ == "__main__":
    url = "http://127.0.0.1:8000/backend/list/book"
    books = requests.get(url).json()["response"]["data"]

    # sort book by isbn
    books = sorted(books,
                   key=itemgetter('isbn'))

    for key, value in groupby(books,
                              key=itemgetter('isbn')):
        suffix = 1
        for book in value:
            barcode = "%s%s" % (book["isbn"], str(suffix).zfill(3))
            suffix = suffix + 1
            isbn = book["isbn"]

            payload = {
                'isbn': isbn,
                'value': barcode,
                'field': "barcode"
            }
            url = "http://127.0.0.1:8000/backend/update_book"
            putting = requests.put(url, data=payload)
            print(isbn)
            print(putting.json())
            print("------")
