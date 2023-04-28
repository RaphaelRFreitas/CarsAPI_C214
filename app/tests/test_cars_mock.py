from unittest.mock import MagicMock
from fastapi.testclient import TestClient

from app.src.main import app
from app.src.models import Car
from app.src.repositories import repository

'''
def test_get_all_cars_mock():
    repository_mock = MagicMock()
    repository_mock.read_all_cars.return_value = [
        {"id": "1", "brand": "Ford", "model": "Mustang", "year": 1964, "color": "red"},
        {"id": "2", "brand": "Chevrolet", "model": "Corvette", "year": 1953, "color": "white"}
    ]

    app.dependency_overrides[repository] = lambda: repository_mock

    APIclient = TestClient(app)

    response = APIclient.get("/cars")

    assert response.status_code == 200
    assert response.json() == {"cars": [
        {"id": "1", "brand": "Ford", "model": "Mustang", "year": 1964, "color": "red"},
        {"id": "2", "brand": "Chevrolet", "model": "Corvette", "year": 1953, "color": "white"}
    ]}


def test_get_car_by_id_mock():
    repository_mock = MagicMock()
    repository_mock.read_car_by_id.return_value = {"id": "1", "brand": "Ford", "model": "Mustang", "year": 1964, "color": "red"}

    app.dependency_overrides[repository] = lambda: repository_mock

    APIclient = TestClient(app)

    response = APIclient.get("/cars/1")

    assert response.status_code == 200
    assert response.json() == {"car": {"id": "1", "brand": "Ford", "model": "Mustang", "year": 1964, "color": "red"}}


def test_insert_car_mock():
    repository_mock = MagicMock()

    app.dependency_overrides[repository] = lambda: repository_mock

    APIclient = TestClient(app)

    response = APIclient.post("/cars", json={"brand": "Ford", "model": "Mustang", "year": 1964, "color": "red"})

    assert response.status_code == 200
    assert response.json() == {"response": "Car added into database"}

    repository_mock.create_car.assert_called_once_with(
        Car(brand="Ford", model="Mustang", year=1964, color="red"))


def test_update_car_mock():
    repository_mock = MagicMock()
    repository_mock.update_car.return_value = True

    app.dependency_overrides[repository] = lambda: repository_mock

    APIclient = TestClient(app)

    response = APIclient.put("/cars/1", json={"brand": "Ford", "model": "Mustang", "year": 1964, "color": "red"})

    assert response.status_code == 200
    assert response.json() == {"response": "Car with id $1 updated in database."}

    repository_mock.update_car.assert_called_once_with("1", Car(brand="Ford", model="Mustang", year=1964, color="red"))

def test_delete_car_mock():
    repository_mock = MagicMock()
    repository_mock.delete_car.return_value = True

    app.dependency_overrides[repository] = lambda: repository_mock

    APIclient = TestClient(app)

    response = APIclient.delete("/cars/1")

    assert response.status_code == 200
    assert response.json() == {"response": "Car with id 1 deleted in database."}

    repository_mock.delete_car.assert_called_once_with("1")
'''