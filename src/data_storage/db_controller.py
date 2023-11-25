from src.configuration import logger
from src.data_storage import StateDb, DbClient
from src.data_storage.db_tables import GenerationState, LessonDb, CourseDb, LessonContentDb


class DbController:
    def __init__(self):
        self._db_controller = DbClient()

    def update_generation_state(self, course_uuid, new_generation_state):
        session = self._db_controller.get_session()

        state = session.query(StateDb).filter_by(course_uuid=course_uuid).first()
        if state:
            state.generation_state = new_generation_state
            session.commit()
            logger.info(f"Updating course: {course_uuid} with new generation state: {new_generation_state}")
        else:
            raise ValueError(f"No State object found with UUID {course_uuid}")

    def write_state_data(self, request_query, course_uuid, llm_version, language):
        state_data_db = StateDb(
            text=request_query,
            course_uuid=course_uuid,
            llm_version=llm_version,
            language=language,
            generation_state=GenerationState.Processing
        )
        self._db_controller.add_to_db(state_data_db)

    def write_course_data(self, course_chain_response, course_uuid):
        course_table_data_db: CourseDb = self._prepare_course_data(course_chain_response, course_uuid)
        self._db_controller.add_to_db(course_table_data_db)

        lesson_table_data_db = self._prepare_lesson_data(course_chain_response, course_table_data_db)
        for lesson_data in lesson_table_data_db:
            self._db_controller.add_to_db(lesson_data)

    def write_lesson_content_data(self, lesson_content, course_uuid):
        lessons = self._map_lesson_ids_to_lesson_content(lesson_content, course_uuid)
        for lesson in lessons:
            self._db_controller.add_to_db(lesson)

    def check_course_state(self, course_uuid):
        session = self._db_controller.get_session()

        state = session.query(StateDb).filter_by(course_uuid=course_uuid).first()

        if state is None:
            return None

        if state.generation_state == GenerationState.Generated:
            return self.get_data_by_course_uuid(course_uuid)
        elif state.generation_state == GenerationState.Failed:
            return {"message": "Error: Course generation failed"}
        elif state.generation_state == GenerationState.Processing:
            return {"message": "Course generation is in progress"}

    def get_data_by_course_uuid(self, course_uuid):
        session = self._db_controller.get_session()

        state = session.query(StateDb).filter_by(course_uuid=course_uuid).first()
        course = session.query(CourseDb).filter_by(course_uuid=course_uuid).first()

        if course:
            lessons = session.query(LessonDb).filter_by(course_id=course.course_uuid).all()
            lesson_ids = [lesson.id for lesson in lessons]
            lesson_contents = session.query(LessonContentDb).filter(LessonContentDb.lesson_id.in_(lesson_ids)).all()
            modified_lessons_contents = {f"Key{i + 1}": content.to_dict() for i, content in enumerate(lesson_contents)}

            result = {
                "query": state.text,
                "llm_version": state.llm_version,
                "language": state.language,
                "course_name": course.course_name,
                "course_content": {
                    "course_name": course.course_name,
                    "lessons": [lesson.to_dict() for lesson in lessons]
                },
                "lessons_content": modified_lessons_contents

            }

            return result
        else:
            raise ValueError(f"No Course object found with UUID {course_uuid}")

    def _get_lesson_ids_by_course_uuid(self, course_uuid):
        course = self._db_controller.get_session().query(CourseDb).filter_by(course_uuid=course_uuid).first()

        if course:
            lessons = self._db_controller.get_session().query(LessonDb).filter_by(course_id=course.course_uuid).all()

            lesson_ids = [lesson.id for lesson in lessons]

            return lesson_ids
        else:
            raise ValueError(f"No Course object found with UUID {course_uuid}")

    def _map_lesson_ids_to_lesson_content(self, lesson_content, course_uuid):
        lesson_ids = self._get_lesson_ids_by_course_uuid(course_uuid=course_uuid)
        lessons_content = list(lesson_content.get("lessons_content").values())
        return [
            LessonContentDb(content=content, lesson_id=lesson_id)
            for content, lesson_id in zip(lessons_content, lesson_ids)
        ]

    def _prepare_course_data(self, course_chain_response, course_uuid):
        return CourseDb(course_name=course_chain_response.get("course_content").get("course_name"),
                        course_uuid=course_uuid)

    def _prepare_lesson_data(self, course_chain_response, course_data):
        return self._prepare_lessons(
            course_chain_response.get("course_content").get("lessons"),
            course_data.course_uuid)

    def _prepare_lessons(self, lessons: [dict], course_id):
        lessons_list = [
            LessonDb(
                lesson_name=lesson.get("title"),
                topics=lesson.get("topics"),
                course_id=course_id
            )
            for lesson in lessons
        ]
        return lessons_list
