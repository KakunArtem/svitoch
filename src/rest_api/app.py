from fastapi import FastAPI, Request, status
from requests import Timeout
from starlette.responses import JSONResponse

from src.rest_api.routers import courses, topics

app = FastAPI()
app.include_router(courses.router)
app.include_router(topics.router)


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
