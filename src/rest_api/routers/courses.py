import uuid

from fastapi import APIRouter, BackgroundTasks, HTTPException

from src.chains.course_chain import LlmTypes
from src.configuration import logger
from src.rest_api.controllers import CourseController
from src.rest_api.models import DefaultResponse, ModelRequest

router = APIRouter(
    tags=["Course"],
    prefix="/v1",
)


async def _generate_response(
        request: ModelRequest,
        background_tasks: BackgroundTasks,
        llm_version: LlmTypes
) -> DefaultResponse:
    logger.info(f"Received request text: `{request.text}`")
    course_uuid = uuid.uuid4()

    inputs = {
        "request_uuid": course_uuid,
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
    course_controller = CourseController()
    course_controller.process_request(**inputs)


@router.post(
    "/courses/base_course", response_model=DefaultResponse, response_model_exclude_none=True
)
async def generate_response_base_course(
        request: ModelRequest,
        background_tasks: BackgroundTasks,
):
    return await _generate_response(request, background_tasks, LlmTypes.Gpt_3)


@router.post(
    "/courses/advance_course", response_model=DefaultResponse, response_model_exclude_none=True
)
async def generate_response_advance_course(
        request: ModelRequest,
        background_tasks: BackgroundTasks,
):
    return await _generate_response(request, background_tasks, LlmTypes.Gpt_4)


@router.get("/courses/{course_uuid}")
async def get_course_by_uuid(course_uuid: uuid.UUID):
    logger.info(f"Received request for course UUID: {course_uuid}")

    course_controller = CourseController()
    course_data = course_controller.get_course_by_uuid(course_uuid)

    if course_data is None:
        raise HTTPException(status_code=404, detail="Course not found")

    return course_data
