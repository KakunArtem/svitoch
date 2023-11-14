from typing import List
from pydantic import BaseModel


class Topic(BaseModel):
    title: str
    steps: List[str]


class CourseContent(BaseModel):
    topics: List[Topic]


class Course(BaseModel):
    course_content: CourseContent
