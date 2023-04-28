from fastapi.testclient import TestClient

from app.src.main import app

APIclient = TestClient(app)


def test_index():
    response = APIclient.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Cars API"}


def test_insert_car():
    car = {
        "brand": "Ford",
        "model": "Mustang",
        "year": 1964,
        "color": "red"
    }
    response = APIclient.post("/cars", json=car)
    assert response.status_code == 200
    assert response.json().get("response") == "Car added into database"


def test_get_car_by_id():
    car_id = 1
    # obter o carro pelo id
    response_get = APIclient.get(f"/cars/{car_id}")
    assert response_get.status_code == 200
    assert response_get.json().get("car")["_id"] == car_id

    # obter um carro inexistente
    response_get_inexistente = APIclient.get("/cars/999")
    assert response_get_inexistente.status_code == 404
    assert "Car not found for id 999" in response_get_inexistente.json().get("detail")


def test_update_car():
    car_id = 1

    # atualizar o carro
    response_update = APIclient.put(
        f"/cars/{car_id}",
        json={
            "brand": "Volkswagen",
            "model": "Gol",
            "year": 2023,
            "color": "black"
        }
    )
    assert response_update.status_code == 200
    assert response_update.json().get("response") == f"Car with id ${car_id} updated in database."

    # tentar atualizar um carro inexistente
    response_update_inexistente = APIclient.put(
        "/cars/999",
        json={
            "brand": "Volkswagen",
            "model": "Gol",
            "year": 2023,
            "color": "black"
        }
    )
    assert response_update_inexistente.status_code == 404
    assert "Car not found for id 999" in response_update_inexistente.json().get("detail")


def test_delete_car():
    car_id = 1

    # deletar o carro
    response_delete = APIclient.delete(f"/cars/{car_id}")
    assert response_delete.status_code == 200
    assert response_delete.json().get("response") == f"Car with id ${car_id} deleted from database."

    # tentar deletar um carro inexistente
    response_delete_inexistente = APIclient.delete("/cars/999")
    assert response_delete_inexistente.status_code == 404
    assert "Car not found for id 999" in response_delete_inexistente.json().get("detail")
