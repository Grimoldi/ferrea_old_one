import requests

if __name__ == "__main__":
    url = "http://127.0.0.1:8000/backend/list/preview"
    books = requests.get(url).json()

    test = books["response"]["data"]
    print(test)
