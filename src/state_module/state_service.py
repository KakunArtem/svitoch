from src.configuration import logger
from src.data_storage_module import DataController, DbController, GenerationState, DataStorage
from src.llm_module.chains import CourseChain, LessonsChain


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class StateService(metaclass=SingletonMeta):
    def __init__(self):
        self._data_controller = DataController()
        self._course_chain = CourseChain()
        self._lessons_chain = LessonsChain()
        self._db_controller = DbController()

    def process_course_request(self, request_query, course_uuid, llm_version, language):
        self._db_controller.write_state_data(request_query, course_uuid, llm_version, language)

        try:
            inputs = {"query": request_query, "llm_version": llm_version, "language": language}
            course_chain_response = self._course_chain(inputs=inputs)
            self._db_controller.write_course_records(course_chain_response, course_uuid)

            inputs = {**course_chain_response, "language": language}
            lessons_chain_response = self._lessons_chain(inputs=inputs)
            self._db_controller.write_lesson_content_data(lessons_chain_response, course_uuid)

            self._db_controller.update_generation_state(
                course_uuid=course_uuid,
                new_generation_state=GenerationState.Generated
            )

            self._data_controller.store_data(
                self._db_controller.get_data_by_course_uuid(course_uuid),
                DataStorage.COURSE,
                course_uuid
            )
            logger.info(f"Processed request with query: {request_query}")

        except Exception as e:
            logger.error(e)
            self._db_controller.update_generation_state(
                course_uuid=course_uuid,
                new_generation_state=GenerationState.Failed
            )

    def get_course_by_uuid(self, request_uuid):
        return self._db_controller.check_course_state(request_uuid)

    def get_course_by_name(self, course_name):
        return self._db_controller.get_data_by_course_name(course_name)

    def process_lessons_request(self, request_query, course_uuid, llm_version, language):
        query = request_query.get("course_content").get("course_name")
        self._db_controller.write_state_data(query, course_uuid, llm_version, language)

        try:
            self._db_controller.write_course_records(request_query, course_uuid)

            lessons_chain_response = self._lessons_chain(inputs={**request_query, "llm_version": llm_version})
            self._db_controller.write_lesson_content_data(lessons_chain_response, course_uuid)

            self._db_controller.update_generation_state(
                course_uuid=course_uuid,
                new_generation_state=GenerationState.Generated
            )

            self._data_controller.store_data(
                self._db_controller.get_data_by_course_uuid(course_uuid),
                DataStorage.TOPICS,
                course_uuid
            )
            logger.info(f"Processed request with query: {request_query}")

        except Exception as e:
            logger.error(e)
            self._db_controller.update_generation_state(
                course_uuid=course_uuid,
                new_generation_state=GenerationState.Failed
            )

    def get_lessons_by_uuid(self, request_uuid):
        return self._db_controller.check_course_state(request_uuid)