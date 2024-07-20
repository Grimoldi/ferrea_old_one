import requests
import random

if __name__ == "__main__":
    libraries = [
        "Biblioteca Civica",
        "Biblioteca Cederna",
        "Biblioteca Ragazzi",
        "Biblioteca San Rocco",
        "Biblioteca San Gerardo",
        "Biblioteca Triante",
    ]

    url = "http://127.0.0.1:8000/backend/list/book"
    books = requests.get(url).json()["response"]["data"]

    for book in books:
        isbn = book["isbn"]
        random_library = random.choice(libraries)

        payload = {
            'isbn': isbn,
            'library': random_library,
        }

        print(isbn)
        print(random_library)

        url = "http://127.0.0.1:8000/backend/create_hosts"
        posting = requests.post(url, data=payload)

        print(posting.status_code)
        print("------")
