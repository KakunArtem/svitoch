from typing import Any, Dict

from langchain.chat_models import ChatOpenAI

from src.configuration import config


class OpenAI3Model(ChatOpenAI):
    request_timeout = 600.0
    temperature = 0.0
    max_retries = 2
    model_name = config.OPENAI_3_5_GENERATION_MODEL_NAME
    openai_api_key = config.OPENAI_API_KEY

    def __init__(self, **kwargs: Dict[str, Any]) -> None:
        super().__init__(**kwargs)
