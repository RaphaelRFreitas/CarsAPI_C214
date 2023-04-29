"""
Module containing the APITestCase Class.
"""

from typing import Dict, Union

from unittest import TestCase
from unittest.mock import MagicMock, patch

from app.src.main import app as fastapi_app
from app.src.models import Car

from fastapi.testclient import TestClient


@patch("app.src.main.repository")
class APITestCaseMock(TestCase):
    """
    Class to test the API endpoints.
    """

    def setUp(self) -> None:
        self._client = TestClient(fastapi_app)

    def _build_car(self, brand: str, model: str, year: int, color: str) -> Car:
        """
        Private Method to build a car.
        """
        car = Car(
            brand=brand,
            model=model,
            year=year,
            color=color
        )

        return car

    def _car_to_json(self, car: Car) -> Dict[str, Union[str, int]]:
        """
        Private method to convert the car to JSON format.
        """
        json = {
            "brand": car.brand,
            "model": car.model,
            "year": car.year,
            "color": car.color,
        }
        return json

    def test_should_get_all_cars_but_none_is_retrieved(self, mock_repository: MagicMock) -> None:
        """
        Method to assert the api has a get method endpoint to retrieve all cars
        even though there are none in the repository.
        """
        mock_function = mock_repository.read_all_cars
        mock_function.return_value = None

        response = self._client.get("/cars")

        actual_status_code = response.status_code
        expected_status_code = 200

        actual_response_data = response.json()
        expected_response_data = {"error": "No car found in database yet. Try adding some before retrieving any."}

        self.assertEqual(actual_status_code, expected_status_code)
        self.assertEqual(actual_response_data, expected_response_data)

        mock_function.assert_called_once()

    def test_should_get_all_cars_and_retrieve_three_cars(self, mock_repository: MagicMock) -> None:
        """
        Method to assert the api has a get method endpoint to retrieve all cars
        when there are some in the repository.
        """
        test_car_one = self._build_car("Fiat", "Cronos", 2023, "Black")
        test_car_two = self._build_car("Tesla", "S Plaid", 2023, "White")
        test_car_three = self._build_car("Hyundai", "Santa Fe", 2020, "Black")

        mock_function = mock_repository.read_all_cars
        mock_function.return_value = {
            1: test_car_one,
            2: test_car_two,
            3: test_car_three
        }

        response = self._client.get("/cars")

        actual_status_code = response.status_code
        expected_status_code = 200

        actual_response_data = response.json()
        expected_response_data = {
            "cars": {
                "1": self._car_to_json(test_car_one),
                "2": self._car_to_json(test_car_two),
                "3": self._car_to_json(test_car_three),
            }
        }

        self.assertEqual(actual_status_code, expected_status_code)
        self.assertDictEqual(actual_response_data, expected_response_data)

        mock_function.assert_called_once()

    def test_should_return_an_error_when_trying_to_retrieve_car_that_doesnt_exists_by_its_id(self,
                                                                                             mock_repository: MagicMock) -> None:
        """
        Method to assert the api has a get method endpoint that returns an error
        when the actor tries to access a single car data by its id
        but the car doesn't exists in the repository.
        """
        test_car_id = 1

        mock_function = mock_repository.read_car_by_id
        mock_function.return_value = None

        response = self._client.get(f"/cars/{test_car_id}")

        actual_status_code = response.status_code
        expected_status_code = 404

        actual_response_data = response.json()
        expected_response_data = {"detail": f"Car not found for id {test_car_id}"}

        self.assertEqual(actual_status_code, expected_status_code)
        self.assertEqual(actual_response_data, expected_response_data)

        mock_function.assert_called_once_with(test_car_id)

    def test_should_retrieve_car_by_its_id(self, mock_repository: MagicMock) -> None:
        """
        Method to assert the api has a get method endpoint that retrieves a specific car
        from the repository based on its id.
        """
        test_car_id = 1
        test_car = self._build_car("Fiat", "Cronos", 2023, "Black")

        mock_function = mock_repository.read_car_by_id
        mock_function.return_value = test_car

        response = self._client.get(f"/cars/{test_car_id}")

        actual_status_code = response.status_code
        expected_status_code = 200

        actual_response_data = response.json()
        expected_response_data = {"car": self._car_to_json(test_car)}

        self.assertEqual(actual_status_code, expected_status_code)
        self.assertEqual(actual_response_data, expected_response_data)

        mock_function.assert_called_once_with(test_car_id)

    def test_should_insert_new_car(self, mock_repository: MagicMock) -> None:
        """
        Method to assert the api has a post endpoint that inserts a car into the repository.
        """
        test_car = self._build_car("Fiat", "Cronos", 2023, "Black")
        mock_function = mock_repository.create_car

        test_params = self._car_to_json(test_car)

        response = self._client.post(f"/cars", json=test_params)

        actual_status_code = response.status_code
        expected_status_code = 200

        actual_response_data = response.json()
        expected_response_data = {"response": "Car added into database"}

        self.assertEqual(actual_status_code, expected_status_code)
        self.assertEqual(actual_response_data, expected_response_data)

        mock_function.assert_called_once_with(test_car)

    def test_should_return_an_error_when_inserting_new_car_with_wrong_year_type(self,
                                                                                mock_repository: MagicMock) -> None:
        """
        Method to assert the api has a post endpoint that returns an error
        when trying to insert a car into the repository but it receives the year in a wrong type.
        """
        mock_function = mock_repository.create_car

        test_params = {
            "brand": "WolksWagen",
            "model": "Jetta",
            "year": "wrong_parameter",
            "color": "White"
        }

        response = self._client.post(f"/cars", json=test_params)

        actual_status_code = response.status_code
        expected_status_code = 422

        self.assertEqual(actual_status_code, expected_status_code)

        mock_function.assert_not_called()

    def test_should_update_existing_car(self, mock_repository: MagicMock) -> None:
        """
        Method to assert the api has a put endpoint that updates
        a car that already exists in the repository.
        """
        test_car_id = 1
        test_car = self._build_car("WolksWagen", "Jetta", 2023, "White")

        mock_function = mock_repository.update_car
        mock_function.return_value = True

        test_params = self._car_to_json(test_car)

        response = self._client.put(f"/cars/{test_car_id}", json=test_params)

        actual_status_code = response.status_code
        expected_status_code = 200

        actual_response_data = response.json()
        expected_response_data = {"response": f"Car with id ${test_car_id} updated in database."}

        self.assertEqual(actual_status_code, expected_status_code)
        self.assertEqual(actual_response_data, expected_response_data)

        mock_function.assert_called_once_with(test_car_id, test_car)

    def test_should_return_an_error_when_trying_to_update_that_doesnt_exists(self, mock_repository: MagicMock) -> None:
        """
        Method to assert the api has a put endpoint that returns an error
        when trying to update a car that doesn't exists in the repository.
        """
        test_wrong_car_id = 123
        test_car = self._build_car("WolksWagen", "Jetta", 2023, "White")

        mock_function = mock_repository.update_car
        mock_function.return_value = False

        test_params = self._car_to_json(test_car)

        response = self._client.put(f"/cars/{test_wrong_car_id}", json=test_params)

        actual_status_code = response.status_code
        expected_status_code = 404

        actual_response_data = response.json()
        expected_response_data = {"detail": f"Car not found for id {test_wrong_car_id}"}

        self.assertEqual(actual_status_code, expected_status_code)
        self.assertEqual(actual_response_data, expected_response_data)

        mock_function.assert_called_once_with(test_wrong_car_id, test_car)

    def test_should_return_an_error_when_trying_to_update_car_with_wrong_year_type(self,
                                                                                   mock_repository: MagicMock) -> None:
        """
        Method to assert the api has a put endpoint that returns an error
        when trying to update a car when the wrong year type is passed to it.
        """
        test_car_id = 1

        mock_function = mock_repository.update_car
        mock_function.return_value = False

        test_params = {
            "brand": "WolksWagen",
            "model": "Jetta",
            "year": "wrong_parameter",
            "color": "White"
        }

        response = self._client.put(f"/cars/{test_car_id}", json=test_params)

        actual_status_code = response.status_code
        expected_status_code = 422

        self.assertEqual(actual_status_code, expected_status_code)

        mock_function.assert_not_called()

    def test_should_delete_existing_car(self, mock_repository: MagicMock) -> None:
        """
        Method to assert the api has a delete endpoint that deletes a car
        that already exists in the repository.
        """
        test_car_id = 1

        mock_function = mock_repository.delete_car
        mock_function.return_value = True

        response = self._client.delete(f"/cars/{test_car_id}")

        actual_status_code = response.status_code
        expected_status_code = 200

        actual_response_data = response.json()
        expected_response_data = {"response": f"Car with id ${test_car_id} deleted from database."}

        self.assertEqual(actual_status_code, expected_status_code)
        self.assertEqual(actual_response_data, expected_response_data)

        mock_function.assert_called_once_with(test_car_id)

    def test_should_return_an_error_when_deleting_a_car_that_doesnt_exists(self, mock_repository: MagicMock) -> None:
        """
        Method to assert the api has a delete endpoint that returns an error
        when trying to delete a car that doesn't exists in the repository.
        """
        test_wrong_car_id = 123

        mock_function = mock_repository.delete_car
        mock_function.return_value = False

        response = self._client.delete(f"/cars/{test_wrong_car_id}")

        actual_status_code = response.status_code
        expected_status_code = 404

        actual_response_data = response.json()
        expected_response_data = {"detail": f"Car not found for id {test_wrong_car_id}"}

        self.assertEqual(actual_status_code, expected_status_code)
        self.assertEqual(actual_response_data, expected_response_data)

        mock_function.assert_called_once_with(test_wrong_car_id)