import uuid

from fastapi import APIRouter, HTTPException
from starlette.background import BackgroundTasks

from src.configuration import logger
from src.rest_api.controllers.lessons_controller import LessonsController
from src.rest_api.models import DefaultResponse, Course

router = APIRouter(
    tags=["Lessons"],
    prefix="/v1",
)


async def _generate_response(
        request: Course,
        background_tasks: BackgroundTasks
) -> DefaultResponse:
    logger.info(f"Received request text: `{request.course_content}`")
    course_uuid = uuid.uuid4()
    print(request.dict())

    inputs = {
        "request_uuid": course_uuid,
        "request_query": request.dict()
    }

    background_tasks.add_task(process_lessons_request, inputs)
    return DefaultResponse(
        response={
            "course_uuid": course_uuid
        }
    )


def process_lessons_request(inputs):
    lessons_controller = LessonsController()
    lessons_controller.process_request(**inputs)


@router.post(
    "/lessons/generate_lessons", response_model=DefaultResponse, response_model_exclude_none=True
)
async def response_generate_lessons(
        request: Course,
        background_tasks: BackgroundTasks,
):
    return await _generate_response(request, background_tasks)


@router.get("/topics/{course_uuid}")
async def get_course_by_uuid(course_uuid: uuid.UUID):
    logger.info(f"Received request for course UUID: {course_uuid}")

    topics_controller = LessonsController()
    topics_data = topics_controller.get_lessons_by_uuid(course_uuid)

    if topics_data is None:
        raise HTTPException(status_code=404, detail="Course not found")

    return topics_data
