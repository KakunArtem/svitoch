from src.configuration import logger
from src.data_storage_module import StateDb, DbClient
from src.data_storage_module.db_tables import GenerationState, LessonDb, CourseDb, LessonContentDb


class DbController:
    def __init__(self):
        self._db_controller = DbClient()

    def _get_session_and_state(self, course_uuid):
        session = self._db_controller.get_session()
        state = session.query(StateDb).filter_by(course_uuid=course_uuid).first()
        return session, state

    def update_generation_state(self, course_uuid, new_generation_state):
        session, state = self._get_session_and_state(course_uuid)
        if state:
            state.generation_state = new_generation_state
            session.commit()
            logger.info(f"Updating course: {course_uuid} with new generation state: {new_generation_state}")
        else:
            raise ValueError(f"No State object found with UUID {course_uuid}")

    def write_state_data(self, request_query, course_uuid, llm_version, language):
        state_data_db = StateDb(text=request_query,
                                course_uuid=course_uuid,
                                llm_version=llm_version,
                                language=language,
                                generation_state=GenerationState.Processing)
        self._db_controller.add_to_db(state_data_db)

    def write_course_records(self, course_chain_response, course_uuid):
        course_table_data_db = CourseDb(course_name=course_chain_response['course_content']['course_name'],
                                        course_uuid=course_uuid)

        self._db_controller.add_to_db(course_table_data_db)

        lessons = course_chain_response['course_content']['lessons']
        lesson_table_data_db = self._prepare_lessons(lessons, course_uuid)
        for lesson_data in lesson_table_data_db:
            self._db_controller.add_to_db(lesson_data)

    def _prepare_lessons(self, lessons: [dict], course_id):
        return [
            LessonDb(
                lesson_name=lesson.get("title"),
                topics=lesson.get("topics"),
                course_id=course_id
            )
            for lesson in lessons
        ]

    def write_lesson_content_data(self, lesson_content, course_uuid):
        lessons = self._map_lesson_ids_to_lesson_content(lesson_content, course_uuid)
        for lesson in lessons:
            self._db_controller.add_to_db(lesson)

    def _map_lesson_ids_to_lesson_content(self, lesson_content, course_uuid):
        lesson_ids = self._get_lesson_ids_by_course_uuid(course_uuid)
        lessons_content = list(lesson_content["lessons_content"].values())
        return [LessonContentDb(content=content, lesson_id=lesson_id)
                for content, lesson_id in zip(lessons_content, lesson_ids)]

    def _get_lesson_ids_by_course_uuid(self, course_uuid):
        session = self._db_controller.get_session()
        course = session.query(CourseDb).filter_by(course_uuid=course_uuid).first()
        return [lesson.id for lesson in session.query(LessonDb).filter_by(course_id=course.course_uuid).all()]

    def get_data_by_course_uuid(self, course_uuid):
        session = self._db_controller.get_session()

        state, course = (session.query(StateDb, CourseDb)
                         .join(CourseDb, StateDb.course_uuid == CourseDb.course_uuid)
                         .filter(StateDb.course_uuid == course_uuid).first())

        if not (course and state):
            raise ValueError(f"No Course or State object found with UUID {course_uuid}")

        lessons = session.query(LessonDb).filter_by(course_id=course.course_uuid).all()
        lessons_dict = [lesson.to_dict() for lesson in lessons]

        if not lessons:
            raise ValueError(f"No Lesson objects found for course with UUID {course_uuid}")

        lesson_ids = [lesson.id for lesson in lessons]

        lesson_contents = session.query(LessonContentDb).filter(LessonContentDb.lesson_id.in_(lesson_ids)).all()
        modified_lessons_contents = {lesson.get('title'): content.to_dict() for lesson, content in
                                     zip(lessons_dict, lesson_contents)}

        result = {
            "query": state.text,
            "llm_version": state.llm_version,
            "language": state.language,
            "course_content": {
                "course_name": course.course_name,
                "lessons": lessons_dict,
                "content": modified_lessons_contents
            }
        }

        return result

    def get_data_by_course_name(self, course_name):
        session = self._db_controller.get_session()
        courses = session.query(CourseDb).filter_by(course_name=course_name).all()

        return [course.to_dict() for course in courses]

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
