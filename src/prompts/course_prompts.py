from langchain.prompts import HumanMessagePromptTemplate

from src.prompts.external_prompt import ExternalChatPromptTemplate

base_course_template = """Please create a learning course for a software engineering program. 
The course should contain all major topics and themes related to the next information: {query}."""
base_course_prompt = ExternalChatPromptTemplate.from_messages(
    [HumanMessagePromptTemplate.from_template(base_course_template)]
)

advance_course_template = """As a person who studies programming. I want to learn the following topics in depth. 
Build a very detailed training course based on the following:{query}.
"""
advance_course_prompt = ExternalChatPromptTemplate.from_messages(
    [HumanMessagePromptTemplate.from_template(advance_course_template)]
)
