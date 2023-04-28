from typing import Optional, Any, Mapping

from pymongo import MongoClient
from bson.objectid import ObjectId
from pymongo.cursor import Cursor
from bson import json_util
import json

from app.src.models import Car
from app.src.repositories.repository import Repository


class MongoRepository(Repository):

    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['cars']
        self.collection = self.db['cars']

    def create_car(self, car: Car) -> None:
        """
            """
        idcar = self.return_last_id()
        car = car.dict()
        car['_id'] = idcar + 1
        self.collection.insert_one(car)

    def read_all_cars(self) -> Cursor[Mapping[str, Any] | Any]:
        """"""
        cars = self.collection.find()
        return json.loads(json_util.dumps(cars))

    def read_car_by_id(self, car_id: int) -> Optional[Car]:
        """
            """
        car = self.collection.find_one({'_id': car_id})

        return json.loads(json_util.dumps(car))

    def update_car(self, car_id: int, car: Car) -> bool:
        """
            """
        res = self.collection.update_one({'_id': car_id}, {"$set": car.dict()})
        if res.modified_count == 0:
            return False

        return True

    def delete_car(self, car_id: int) -> bool:
        """
            """
        response = self.collection.delete_one({'_id': car_id})

        if response is None:
            return False

        return True

    def return_last_id(self) -> int:
        """
            """
        try:
            idcar = self.collection.find_one(sort=[("_id", -1)])['_id']
        except:
            return 0
        return idcar

    def delete_all_cars(self) -> bool:
        """
            """
        response = self.collection.delete_many({})

        if response is None:
            return False

        return True