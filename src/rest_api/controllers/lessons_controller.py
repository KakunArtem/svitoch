import json

from src.chains import LessonChain
from src.data_storage import DataController, DataStorage


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class LessonsController(metaclass=SingletonMeta):
    def __init__(self):
        self._data_controller = DataController()
        self._lessons_chain = LessonChain()

    def process_request(self, request_query, request_uuid):
        lessons_chain_response = self._get_lessons_chain_response(request_query)

        response = json.dumps({
            **lessons_chain_response
        })

        self._data_controller.store_data(response, DataStorage.TOPICS, request_uuid)

    def _get_lessons_chain_response(self, request_query):
        return self._lessons_chain(inputs=request_query)

    def get_lessons_by_uuid(self, request_uuid):
        return self._data_controller.get_data(request_uuid)
