from langchain.agents.structured_output import ToolStrategy
from src.models.model import Quizquestions
from src.repository.error_repository import ErrorRepository
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage,SystemMessage
from src.utils.helpers import LLM
from src.agent.prompts import SYSTEM_PROMPT_QUIZ
from src.utils.exceptions.custom_app_exception import AppBaseException,AgentInvocationException
from src.utils.exceptions.error_codes import ErrorCode, ErrorCodeStatus,StatusCode
from src.utils.logger import logger
from langchain.tools import tool
from src.utils.constants import QUIZ_AGENT_TEMP,QUIZ_AGENT_TOKENS


class QuizAgent:
    def __init__(self):
        self.error=ErrorRepository()
    async def quiz_agent(self,query,difficulty_level,no_of_questions):
        try:
            llm = await LLM(self.error).get_llm(max_tokens=QUIZ_AGENT_TOKENS,temperature= QUIZ_AGENT_TEMP)
            agent=create_agent(
                model=llm,
                system_prompt=SystemMessage(content=SYSTEM_PROMPT_QUIZ),
                response_format=ToolStrategy(Quizquestions)
            )
            contents=f"User query is {query} and the no of questions to genrate {no_of_questions} and the difficulty level is {difficulty_level}"
            result= await agent.ainvoke({
                "messages":[HumanMessage(content=contents)]
            }
            )
            response=result.get("structured_response")
            logger.info("Quiz Agent Response Generated Successfully")
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