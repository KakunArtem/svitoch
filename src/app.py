from fastapi import FastAPI, Request, status
from requests import Timeout
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from src.data_storage_module import DbClient, Base
from src.rest_api_module.controllers import course_controller, lessons_controller

DbClient().create_tables(Base)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(course_controller.router)
app.include_router(lessons_controller.router)


@app.exception_handler(Timeout)
async def openai_timeout(request: Request, exc: Timeout) -> JSONResponse:
    """
    Handles Timeout exception from OpenAI
    """
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"message": "OpenAI Service Temporary Unavailable."},
    )

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8000)
