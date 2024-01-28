import uuid

from fastapi import APIRouter, BackgroundTasks, HTTPException

from src.llm_module.chains.course_chain import LlmTypes
from src.configuration import logger
from src.rest_api_module.models import DefaultResponse, ModelRequest
from src.state_module.state_service import StateService

router = APIRouter(
    tags=["Course"],
    prefix="/v1",
)


async def _generate_response(
        request: ModelRequest,
        background_tasks: BackgroundTasks,
        llm_version: LlmTypes
) -> DefaultResponse:
    course_uuid = uuid.uuid4()

    logger.info(f"Received request query: `{request.text}, UUID: {course_uuid}`")

    inputs = {
        "course_uuid": course_uuid,
        "request_query": request.text,
        "llm_version": llm_version,
        "language": request.language
    }

    background_tasks.add_task(process_course_request, inputs)
    return DefaultResponse(
        response={
            "course_uuid": course_uuid
        }
    )


def process_course_request(inputs):
    state_service = StateService()
    state_service.process_course_request(**inputs)


@router.post(
    "/courses/base_course", response_model=DefaultResponse, response_model_exclude_none=True
)
async def generate_base_course(
        request: ModelRequest,
        background_tasks: BackgroundTasks,
):
    return await _generate_response(request, background_tasks, LlmTypes.Gpt_3)


@router.post(
    "/courses/advance_course", response_model=DefaultResponse, response_model_exclude_none=True
)
async def generate_advance_course(
        request: ModelRequest,
        background_tasks: BackgroundTasks,
):
    return await _generate_response(request, background_tasks, LlmTypes.Gpt_4)


@router.get("/courses/uuid/{course_uuid}")
async def get_course_by_uuid(course_uuid: uuid.UUID):
    logger.info(f"Received request for course UUID: {course_uuid}")

    state_service = StateService()
    course_data = state_service.get_course_by_uuid(course_uuid)

    if course_data is None:
        raise HTTPException(status_code=404, detail="Course not found")

    return course_data


@router.get("/courses/name/{course_name}")
async def get_course_by_uuid(course_name: str):
    logger.info(f"Received request for course Name: {course_name}")

    state_service = StateService()
    course_data = state_service.get_course_by_name(course_name)

    if course_data is None:
        raise HTTPException(status_code=404, detail="Course not found")

    return course_data
