from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import HumanMessagePromptTemplate, ChatPromptTemplate

from src.chains.models.course_model import Course
from src.prompts.external_prompt import ExternalChatPromptTemplate

course_model = PydanticOutputParser(pydantic_object=Course)

base_course_template = """Please create a learning course for a software engineering program. 
The course should contain all major topics and themes related to the next information: {topics}."""
base_course_prompt = ExternalChatPromptTemplate.from_messages(
    [HumanMessagePromptTemplate.from_template(base_course_template)]
)

advance_course_template = """
### Instructions ###
If MUST ONLY generate a step-by-step self-study course based on the above topics".
You MUST give very precise instructions. 
You MUST include Topic-related terms in instructions.
You MUST be specific, do not give general advice.
You MUST follow the RULES within the section if provided.
### Instructions ###

### Format ###
{format_instructions}
### Format ###

Topics: '''{query}'''
"""

course_prompt = ChatPromptTemplate(
    messages=[
        HumanMessagePromptTemplate.from_template(advance_course_template)
    ],
    input_variables=["query"],
    partial_variables={
        "format_instructions": course_model.get_format_instructions()
    }
)

topic_template = """
### Instructions ###
If MUST ONLY generate a comprehensive guide for each of the provided topics.
You MUST provide detailed code examples with explanations.
You MUST provide comparison tables.
You MUST use detailed explanation.
You MUST return response as a formatted Markdown text.
### Instructions ###

Topics: '''{topics}'''
"""

topic_prompt = ChatPromptTemplate(
    messages=[
        HumanMessagePromptTemplate.from_template(topic_template)
    ],
    input_variables=["topics"]
)