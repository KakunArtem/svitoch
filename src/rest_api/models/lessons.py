from typing import List, Optional
from pydantic import BaseModel, Field


class Lesson(BaseModel):
    title: str
    topics: List[str]


class CourseContent(BaseModel):
    course_name: str
    lessons: List[Lesson]


class Course(BaseModel):
    course_content: CourseContent
    language: Optional[str] = Field(min_length=1, alias="language", default="English")
