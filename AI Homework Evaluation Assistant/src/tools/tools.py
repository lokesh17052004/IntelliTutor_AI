from src.models.model import State
from langgraph.types import Command
from src.repository.error_repository import ErrorRepository
from src.agent.review_agent import ReviewAgent
from langchain_core.messages import ToolMessage
from src.utils.exceptions.custom_app_exception import AppBaseException,AgentInvocationException
from src.utils.exceptions.error_codes import ErrorCode, ErrorCodeStatus,StatusCode
from src.utils.logger import logger
from langchain_core.tools import tool
from langchain.tools import ToolRuntime
from src.agent.quiz_agent import QuizAgent
quiz_agent=QuizAgent()
review_agent=ReviewAgent()
error=ErrorRepository()
@tool
async def quiz_tool(query:str,difficulty_level:str,no_of_questions:int,runtime:ToolRuntime[None,State])->Command:
    """
    This tool will generate quiz questions based on the user topic 
    with number of questions that user has asked along with the 
    difficulty level that user has sent
    """
    try:
        logger.info("Quiz Tool has been triggered Successfully")
        logger.info(f"The user query is {query} and the difficulty level {difficulty_level} and the number of questions required for user is {no_of_questions}")
        quiz_response=await quiz_agent.quiz_agent(query,difficulty_level,no_of_questions)
        return Command(
            update={
                "messages": [
                    ToolMessage(
                        content=f"Quiz question generated successfully.",
                        tool_call_id=runtime.tool_call_id,
                    )
                ],
        
                "quiz_questions": quiz_response,
                "current_step": "solution_agent"
            }
        )
    except AgentInvocationException:
        raise
    except Exception as e:
        logger.error("Error in coder Agent")
        error.error(
            file_name="coder_agent.py",
            function_name="coder_agent",
            message=f"Coder Agent running error{e}"
        )
        raise AppBaseException(
            error_code=ErrorCodeStatus.get(ErrorCode.INTERNAL_SERVER_ERROR,"CA_01"),
            message=f"Coder agent error{e}",
            status_code=StatusCode().INTERNAL_SERVER_ERROR_STATUS_CODE
        )
    
@tool
async def review_tool(runtime:ToolRuntime[None,State])->Command:
    """
    This tool will analyze the questions along with 
    the answers and evalute the answers and sends back to the user
    with a response as score,percentage and suggested improvements
    """
    try:
        logger.info("Review tool has triggered successfully")
        review_response=await review_agent.review_agent(runtime.state["quiz_questions"],runtime.state["quiz_answers"])

        return Command(
        update={
            "messages": [
                ToolMessage(
                    content=f"Final response is{review_response}",
                    tool_call_id=runtime.tool_call_id,
                )
            ],
            "final_response": review_response,
            "current_step":"quiz_agent"
        }
    )
    except AgentInvocationException:
        raise
    except Exception as e:
        logger.error("Error in coder Agent")
        error.error(
            file_name="coder_agent.py",
            function_name="coder_agent",
            message=f"Coder Agent running error{e}"
        )
        raise AppBaseException(
            error_code=ErrorCodeStatus.get(ErrorCode.INTERNAL_SERVER_ERROR,"CA_01"),
            message=f"Coder agent error{e}",
            status_code=StatusCode().INTERNAL_SERVER_ERROR_STATUS_CODE
        )