import requests
import json

if __name__ == "__main__":
    url = "http://127.0.0.1:8000/backend/list/book"
    books = requests.get(url).json()["response"]["data"]

    small_t = "smallThumbnail"
    thumb = "thumbnail"
    small = "small"
    medium = "medium"
    large = "large"
    xl = "exrtaLarge"
    volume_key = "volumeInfo"
    img_key = "imageLinks"

    for book in books:
        isbn = book["isbn"]

        url = f"http://127.0.0.1:8000/external_api/google/?isbn={isbn}"
        google_book = requests.get(url).json()

        if volume_key in google_book.keys():
            google_book = google_book[volume_key]

            if img_key in google_book.keys():
                google_book = google_book[img_key]

                if small_t in google_book.keys():
                    cover = google_book[small_t]
                elif thumb in google_book.keys():
                    cover = google_book[thumb]
                elif small in google_book.keys():
                    cover = google_book[small]
                elif medium in google_book.keys():
                    cover = google_book[medium]
                elif large in google_book.keys():
                    cover = google_book[large]
                elif xl in google_book.keys():
                    cover = google_book[xl]

        else:
            cover = "ND"

        payload = {
            'isbn': isbn,
            'value': cover,
            'field': "cover",
        }
        url = "http://127.0.0.1:8000/backend/update_book"
        putting = requests.post(url, data=payload)
        print(isbn)
        print(putting.json())
        print("------")
