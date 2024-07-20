import requests
import json
from random import (
    randint,
    choice,
)
from datetime import (
    datetime,
    timedelta,
)

if __name__ == "__main__":
    url = "http://127.0.0.1:8000/backend/list/user"
    users = requests.get(url).json()["response"]["data"]

    url = "http://127.0.0.1:8000/backend/list/book"
    books = requests.get(url).json()["response"]["data"]

    url_open_read = "http://127.0.0.1:8000/backend/create_read"
    url_close_read = "http://127.0.0.1:8000/backend/update_read"

    url_reserve = "http://127.0.0.1:8000/backend/create_reserve"

    reading_threshold = 30

    start_date_string = '01/05/2021'
    date_format = '%d/%M/%Y'
    start_date = datetime.strptime(start_date_string, date_format)

    j = 0
    for user in users.keys():
        number_of_readings = randint(0, 10)
        print("%s: %s books" % (user, number_of_readings))

        i = 0
        while i < number_of_readings:
            has_finished_reading = randint(0, 100) > reading_threshold
            book = choice(books)["barcode"]
            current_date = start_date + timedelta(days=i + j)
            data = {
                'username': user,
                'barcode': book,
                'when': current_date.timestamp()
            }
            open_read = requests.post(url_open_read, data=data)
            # open_read = requests.post(url_reserve, data=data)
            print(book)
            print(open_read.status_code)
            print(open_read.json())

            if has_finished_reading:
                print("Finished reading")
                data["when"] = (current_date + timedelta(days=1)).timestamp()
                close_read = requests.put(url_close_read, data=data)
                print(close_read.status_code)
                print(close_read.json())

            print("------")
            # break
            i += 1

        # break
        j += 1 + i
