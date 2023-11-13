import json
from typing import List, Dict, Any, Optional

from langchain.callbacks.manager import CallbackManagerForChainRun
from langchain.chains.base import Chain
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableParallel

from src.llms import OpenAI4Model
from src.prompts import topic_template


class TopicsChain(Chain):
    llm = OpenAI4Model()

    @property
    def input_keys(self) -> List[str]:
        return ["course_content"]

    @property
    def output_keys(self) -> List[str]:
        return ["topics_content"]

    def _get_topics(self, topics):
        return [topic for topic in topics['topics']]

    def _get_topics_dict(self, topics):
        return {f"key{i + 1}": topic for i, topic in enumerate(topics)}

    def _get_prompts_list(self, topics):
        return {
            f"key{i + 1}": ChatPromptTemplate.from_template(
                topic_template.replace("topics", f"key{i + 1}")
            ) | self.llm for i in range(len(topics))
        }

    def _call(self,
              inputs: Dict[str, Any],
              run_manager: Optional[CallbackManagerForChainRun] = None,
              ):
        topics = self._get_topics(inputs["course_content"])
        topics_dict = self._get_topics_dict(topics)
        prompt_list = self._get_prompts_list(topics)

        response = RunnableParallel(prompt_list).invoke(topics_dict)

        return {
            "topics_content": {key: value.content for key, value in response.items()}
        }
