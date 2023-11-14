import json

from src.chains import CourseChain, TopicsChain
from src.data_storage import DataController, DataStorage


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class CourseController(metaclass=SingletonMeta):
    def __init__(self):
        self._data_controller = DataController()
        self._course_chain = CourseChain()
        self._topics_chain = TopicsChain()

    def process_request(self, request_query, request_uuid, llm_version):
        course_chain_response = self._get_course_chain_response(request_query, llm_version)
        topics_chain_response = self._get_topics_chain_response(course_chain_response)

        response = json.dumps({
            **course_chain_response, **topics_chain_response
        })

        self._data_controller.store_data(response, DataStorage.COURSE, request_uuid)

    def _get_course_chain_response(self, request_query, llm_version):
        return self._course_chain(inputs={
            "query": request_query,
            "llm_version": llm_version
        })

    def _get_topics_chain_response(self, course_chain_response):
        return self._topics_chain(inputs=course_chain_response)

    def get_course_by_uuid(self, request_uuid):
        return self._data_controller.get_data(request_uuid)
