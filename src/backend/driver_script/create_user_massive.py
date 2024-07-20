import requests
import json
from geopy import Point
from geopy import Nominatim
from geopy.distance import great_circle
import geopy.distance
from random import (
    random,
    choice,
    randint,
)
from random_italian_person import RandomItalianPerson
import pprint

if __name__ == "__main__":
    geolocator = Nominatim(user_agent="test")
    origin = (45.583611, 9.273611)  # Monza (by wikipedia)
    my_distance = great_circle(0.5)  # 0.5 Km radius
    my_point = Point(origin)

    email_domains = [
        "@hotmail.it",
        "@outlook.it",
        "@mail.polimi.it",
        "@gmail.com",
        "@tim.it",
        "@fastweb.com"
    ]
    separators = [
        "",
        ".",
        "_",
        "-"
    ]
    url = "http://127.0.0.1:8000/backend/create_user"

    for i in range(79):
        pt = my_distance.destination(point=my_point, bearing=random()*360)
        coordinates = f"{pt[0]}, {pt[1]}"
        location = geolocator.reverse(coordinates)

        person = RandomItalianPerson()

        user = dict()
        user["name"] = person.name
        user["surname"] = person.surname
        user["city"] = "Monza"
        user["role"] = "User"
        user["address"] = location.address
        user["username"] = (
            person.name + person.surname +
            str(randint(1, 9)) + str(randint(1, 9)) + str(randint(1, 9))
        ).lower().replace(" ", "")
        user["email"] = f"{user['name'].replace(' ','')}{choice(separators)}{user['surname'].replace(' ', '')}{choice(email_domains)}"
        user["email"] = user["email"].lower()
        user["phone"] = "99999999999"

        posting = requests.post(url, data=user)

        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(user)

        print(posting.status_code)
        print(posting.json())
        print("------")
