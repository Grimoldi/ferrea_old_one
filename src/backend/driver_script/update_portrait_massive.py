import requests
import json

if __name__ == "__main__":
    url = "http://127.0.0.1:8000/backend/list/author"
    authors = requests.get(url).json()["response"]["data"]
    url = "http://127.0.0.1:8000/backend/list/preview"
    isbns = requests.get(url).json()["response"]["data"]

    for author in authors:

        for isbn in isbns.keys():
            authors_of_db = isbns[isbn]["author"]
            is_book_of_the_author = author in authors_of_db

            if is_book_of_the_author:
                url_ol = f"http://127.0.0.1:8000/external_api/open_library/{isbn}"
                portrait_req = requests.get(url_ol)
                if portrait_req.status_code != 404 and len(portrait_req.json()) > 0:
                    print(" >>>>>  Found")

                    payload = {
                        'author': author,
                        'field': "portrait",
                        'value': portrait_req.json()[0]["portrait"]
                    }
                    print(payload)
                    url_put = "http://127.0.0.1:8000/backend/update_author"
                    putting = requests.put(url_put, data=payload)
                    print("%s: %s" %
                          (author, portrait_req.json()[0]["portrait"]))
                    print("------")

                    break
                else:
                    # print("Not found")
                    pass
