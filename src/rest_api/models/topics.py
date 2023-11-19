from typing import List, Optional
from pydantic import BaseModel, Field


class Topic(BaseModel):
    title: str
    steps: List[str]


class CourseContent(BaseModel):
    topics: List[Topic]


class Course(BaseModel):
    course_content: CourseContent
    language: Optional[str] = Field(min_length=1, alias="language", default="English")
