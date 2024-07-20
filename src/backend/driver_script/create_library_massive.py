import requests
import json
from geopy.geocoders import Nominatim

if __name__ == "__main__":
    libraries = [
        ("Biblioteca Civica", "Via Padre Reginaldo Giuliani 1/a, Monza", "039 382272"),
        ("Biblioteca Cederna", "Via Cederna 19, Monza", "039 2020237"),
        ("Biblioteca Ragazzi", "Piazza Trento e Trieste, 6, Monza", "039 324197"),
        ("Biblioteca San Rocco", "Via Zara, 9, Monza", "039 2007882"),
        ("Biblioteca San Gerardo", "Via Lecco, 12, Monza", "039 326376"),
        ("Biblioteca Triante", "Via Monte Amiata, 60, Monza", "039 731269"),
    ]
    geolocator = Nominatim(user_agent="my_geo_coder")

    for library in libraries:
        name = library[0]
        address = library[1]
        phone = library[2]

        location = geolocator.geocode(address)
        print(name)
        print(location.address)
        print(location.latitude, location.longitude)
        print(phone)

        payload = {
            'name': name,
            'address': address,
            'phone': phone,
            'lat': location.latitude,
            'lon': location.longitude
        }
        url = "http://127.0.0.1:8000/backend/create_library"
        posting = requests.post(url, data=payload)
        print(posting.status_code)
        print("------")
