from fastapi import APIRouter

from src.chains import TopicsChain
from src.chains.course_chain import CourseChain, LlmTypes
from src.configuration import logger
from src.rest_api.models import DefaultResponse, ModelRequest

router = APIRouter(
    tags=["Course"],
    prefix="/v1",
)


@router.post(
    "/base_course", response_model=DefaultResponse, response_model_exclude_none=True
)
def generate_response_base_course(request: ModelRequest) -> DefaultResponse:
    logger.info(f"Received request text: `{request.text}`")

    chain = CourseChain()

    generated_text = chain(inputs={
        "query": request.text,
        "llm_version": LlmTypes.Gpt_3
    })

    return DefaultResponse(
        generated=generated_text
    )


@router.post(
    "/advance_course", response_model=DefaultResponse, response_model_exclude_none=True
)
async def generate_response_base_course(request: ModelRequest) -> DefaultResponse:
    logger.info(f"Received request text: `{request.text}`")

    course_chain = CourseChain()
    topics_chain = TopicsChain()

    course_chain_response = course_chain(inputs={
        "query": request.text,
        "llm_version": LlmTypes.Gpt_4
    })

    topics_chain_response = topics_chain(inputs=course_chain_response)

    response = {}
    response.update(course_chain_response)
    response.update(topics_chain_response)

    return DefaultResponse(
        response=response
    )
