from fastapi import APIRouter

from src.chains.course_chain import CourseChain
from src.configuration import logger
from src.rest_api.models import DefaultResponse, ModelRequest

router = APIRouter(
    tags=["Course"],
    prefix="/v1",
)


@router.post(
    "/base_course", response_model=DefaultResponse, response_model_exclude_none=True
)
async def generate_response_base_course(request: ModelRequest) -> DefaultResponse:
    logger.info(f"Received request text: `{request.text}`")

    chain = CourseChain()

    generated_text = chain(inputs={
        "query": request.text,
        "course_type": "base_course"
    })

    return DefaultResponse(
        generated=generated_text
    )


@router.post(
    "/advance_course", response_model=DefaultResponse, response_model_exclude_none=True
)
async def generate_response_base_course(request: ModelRequest) -> DefaultResponse:
    logger.info(f"Received request text: `{request.text}`")

    chain = CourseChain()

    generated_text = chain(inputs={
        "query": request.text,
        "course_type": "advance_course"
    })

    return DefaultResponse(
        generated=generated_text
    )
