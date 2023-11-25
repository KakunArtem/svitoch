import json

from src.chains import CourseChain, LessonChain
from src.configuration import logger
from src.data_storage import DataController, DataStorage, DbController, GenerationState


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
        self._db_controller = DbController()

    def process_request(self, request_query, course_uuid, llm_version, language):
        self._db_controller.write_state_data(request_query, course_uuid, llm_version, language)

        try:
            inputs = {"query": request_query, "llm_version": llm_version, "language": language}
            course_chain_response = self._course_chain(inputs=inputs)
            self._db_controller.write_course_data(course_chain_response, course_uuid)

            inputs = {**course_chain_response, "language": language}
            lessons_chain_response = self._lessons_chain(inputs=inputs)
            self._db_controller.write_lesson_content_data(lessons_chain_response, course_uuid)

            response = json.dumps({**course_chain_response, **lessons_chain_response})

            self._db_controller.update_generation_state(
                course_uuid=course_uuid,
                new_generation_state=GenerationState.Generated
            )

            self._data_controller.store_data(response, DataStorage.COURSE, course_uuid)
            logger.info(f"Processed request with query: {request_query}")

        except Exception as e:
            logger.error(e)
            self._db_controller.update_generation_state(
                course_uuid=course_uuid,
                new_generation_state=GenerationState.Failed
            )

    def get_course_by_uuid(self, request_uuid):
        return self._db_controller.check_course_state(request_uuid)
