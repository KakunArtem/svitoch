import json

from src.chains import CourseChain, LessonChain
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
        self._lessons_chain = LessonChain()

    def process_request(self, request_query, request_uuid, llm_version, language):
        course_chain_response = self._get_course_chain_response(request_query, llm_version, language)
        lessons_chain_response = self._get_lessons_chain_response(course_chain_response, language)

        response = json.dumps({
            **course_chain_response, **lessons_chain_response
        })

        self._data_controller.store_data(response, DataStorage.COURSE, request_uuid)

    def _get_course_chain_response(self, request_query, llm_version, language):
        return self._course_chain(inputs={
            "query": request_query,
            "llm_version": llm_version,
            "language": language
        })

    def _get_lessons_chain_response(self, course_chain_response, language):
        return self._lessons_chain(inputs={
            **course_chain_response,
            "language": language
        })

    def get_course_by_uuid(self, request_uuid):
        return self._data_controller.get_data(request_uuid)
