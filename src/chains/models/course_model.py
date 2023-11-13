import os
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.chat_models import ChatOpenAI

from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List


class Topic(BaseModel):
    title: str = Field(description="Title of the theme to learn")
    steps: List[str] = Field(description="Topic to learn in scope of the theme")


class Course(BaseModel):
    overview: str = Field(description="General overview of the course")
    topics: List[Topic] = Field(description="List of themes to learn in scope of course")
