import requests
import json
import random

if __name__ == "__main__":
    url = "http://127.0.0.1:8000/backend/list/book"
    books = requests.get(url).json()["response"]["data"]

    libraries = [
        "Biblioteca Civica",
        "Biblioteca Cederna",
        "Biblioteca Ragazzi",
        "Biblioteca San Rocco",
        "Biblioteca San Gerardo",
        "Biblioteca Triante",
    ]

    for book in books:
        isbn = book["isbn"]
        number_of_copies = random.randint(0, 5)
        print(number_of_copies)
        i = 0
        while (i < number_of_copies):
            random_library = random.choice(libraries)
            url = "http://127.0.0.1:8000/backend/create_book"
            payload = {"isbn": isbn, 'library': random_library, }

            posting = requests.post(url, data=payload)

            print(isbn)
            print(random_library)
            print(posting.status_code)
            print("------")
            i = i + 1
