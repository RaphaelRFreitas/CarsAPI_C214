"""
"""

import requests


def main() -> None:
    """"""
    add_five_cars()


def add_five_cars() -> None:
    """"""
    url = "http://127.0.0.1:8000/cars"

    car_1 = {
        "brand": "Fiat",
        "model": "Cronos",
        "year": 2023,
        "color": "Black",
    }

    car_2 = {
        "brand": "Tesla",
        "model": "S Plaid",
        "year": 2023,
        "color": "White",
    }

    car_3 = {
        "brand": "Jeep",
        "model": "Compass",
        "year": 2021,
        "color": "White",
    }

    car_4 = {
        "brand": "Santa Fe",
        "model": "Hyundai",
        "year": 2020,
        "color": "Black",
    }

    car_5 = {
        "brand": "WolksWagen",
        "model": "Jetta",
        "year": 2022,
        "color": "Black",
    }

    cars = [car_1, car_2, car_3, car_4, car_5]

    for car_json in cars:
        requests.post(url, json=car_json)


if __name__ == "__main__":
    main()
