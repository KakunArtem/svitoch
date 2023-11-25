from sqlalchemy import Column, Integer, String, Text, ForeignKey, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class GenerationState:
    Processing = "Processing"
    Generated = "Generated"
    Failed = "Failed"


class StateDb(Base):
    __tablename__ = "state"

    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)
    llm_version = Column(Text, nullable=False)
    language = Column(String(10), nullable=False)
    course_uuid = Column(UUID(as_uuid=True), unique=True, nullable=False)
    generation_state = Column(String(20), nullable=False)

    def to_dict(self):
        return {
            "query": self.text,
            "course_uuid": self.course_uuid,
            "llm_version": self.llm_version,
            "language": self.language
        }


class CourseDb(Base):
    __tablename__ = "course"

    course_name = Column(String(255), nullable=False)
    course_uuid = Column(UUID(as_uuid=True), ForeignKey("state.course_uuid"), primary_key=True, unique=True,
                         nullable=False)

    state = relationship("StateDb", backref="course", uselist=False)

    def to_dict(self):
        return {
            "course_name": self.course_name,
            "course_uuid": self.course_uuid
        }


class LessonDb(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True)
    lesson_name = Column(String(255), nullable=False)
    topics = Column(ARRAY(String(255)))
    course_id = Column(UUID(as_uuid=True), ForeignKey("course.course_uuid"), nullable=False)

    course = relationship("CourseDb", backref="lessons")
    lesson_contents = relationship("LessonContentDb", back_populates="lesson")

    def to_dict(self):
        return {
            "title": self.lesson_name,
            "topics": self.topics,
        }


class LessonContentDb(Base):
    __tablename__ = "lessons_content"

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)

    lesson = relationship("LessonDb", back_populates="lesson_contents")

    def to_dict(self):
        return {
            "content": self.content,
        }
