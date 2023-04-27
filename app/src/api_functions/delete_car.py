"""
"""

import requests


def main() -> None:
    """"""
    delete_car()


def delete_car() -> None:
    """"""
    car_id = 1
    url = f"http://127.0.0.1:8000/cars/{car_id}"

    requests.delete(url)


if __name__ == "__main__":
    main()
