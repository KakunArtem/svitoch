from typing import List

from pydantic import BaseModel, Field


class Lesson(BaseModel):
    title: str = Field(description="Title of the theme to learn")
    topics: List[str] = Field(description="Topic to learn in scope of the theme")


class Course(BaseModel):
    course_name: str = Field(description="General overview of the course")
    lessons: List[Lesson] = Field(description="List of themes to learn in scope of course")
