from src.models.model import ReviewResponse
import json
from langchain.agents.structured_output import ToolStrategy
from src.repository.error_repository import ErrorRepository
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage,SystemMessage
from src.utils.helpers import LLM
from src.agent.prompts import SYSTEM_PROMPT_REVIEW
from src.utils.exceptions.custom_app_exception import AppBaseException,AgentInvocationException
from src.utils.exceptions.error_codes import ErrorCode, ErrorCodeStatus,StatusCode
from src.utils.logger import logger
from src.utils.constants import REVIEW_AGENT_TEMP,REVIEW_AGENT_TOKENS


class ReviewAgent:
    def __init__(self):
        self.error=ErrorRepository()
    async def review_agent(self,quiz_questions,quiz_answers):
        try:
            llm = await LLM(self.error).get_llm(max_tokens=REVIEW_AGENT_TOKENS,temperature= REVIEW_AGENT_TEMP)
            agent=create_agent(
                model=llm,
                response_format=ToolStrategy(ReviewResponse),
                system_prompt=SYSTEM_PROMPT_REVIEW,
            )
            contents=f"""You are evaluating a quiz. There are {len(quiz_questions.questions)} questions in total.The questions are{json.dumps(quiz_questions.model_dump())} and the answer provided by the user is {json.dumps(quiz_answers)} """
            result= await agent.ainvoke({
                "messages":[HumanMessage(content=contents)]
            }
            )
            logger.info("Review Agent Response Generated Successfully")
            response=result.get("structured_response")
            return response
        except AgentInvocationException:
            raise
        except Exception as e:
            logger.error("Error in coder Agent")
            self.error.error(
                file_name="coder_agent.py",
                function_name="coder_agent",
                message=f"Coder Agent running error{e}"
            )
            raise AppBaseException(
                error_code=ErrorCodeStatus.get(ErrorCode.INTERNAL_SERVER_ERROR,"CA_01"),
                message=f"Coder agent error{e}",
                status_code=StatusCode().INTERNAL_SERVER_ERROR_STATUS_CODE
            )