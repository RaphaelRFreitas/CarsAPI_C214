"""
"""

import requests


def main() -> None:
    """"""
    update_car()


def update_car() -> None:
    """"""
    car_id = 2
    url = f"http://127.0.0.1:8000/cars/{car_id}"

    json = {
        "brand": "Nissan",
        "model": "Kicks",
        "year": 2019,
        "color": "White",
    }

    requests.put(url, json=json)


if __name__ == "__main__":
    main()
