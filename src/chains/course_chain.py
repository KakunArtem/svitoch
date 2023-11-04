from typing import List, Dict, Any, Optional

from langchain.callbacks.manager import CallbackManagerForChainRun
from langchain.chains.base import Chain

from src.configuration import logger
from src.llms import OpenAIChatGeneration
from src.prompts import base_course_prompt, advance_course_prompt


class CourseTypes:
    BASE_COURSE = 'base_course'
    ADVANCE_COURSE = 'advance_course'


class CourseChain(Chain):
    llm = OpenAIChatGeneration()

    @property
    def input_keys(self) -> List[str]:
        return ["query"]

    @property
    def output_keys(self) -> List[str]:
        return ["response_text"]

    def _define_prompt(self, course_type):
        if course_type == CourseTypes.BASE_COURSE:
            return base_course_prompt
        elif course_type == CourseTypes.ADVANCE_COURSE:
            return advance_course_prompt

    def _call(
            self,
            inputs: Dict[str, Any],
            run_manager: Optional[CallbackManagerForChainRun] = None,
    ) -> dict:
        query = inputs["query"]
        course_type = inputs["course_type"]

        prompt_value = self._define_prompt(course_type).format_prompt(
            query=query
        )

        logger.info(f"Full prompt: `{prompt_value}`")

        response = self.llm.generate_prompt(
            [prompt_value],
            callbacks=run_manager.get_child() if run_manager else None,
        )

        response_text = response.generations[0][0].text

        result = {
            "response_text": response_text
        }

        return result
