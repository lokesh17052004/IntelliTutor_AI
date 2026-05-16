from src.utils.exceptions.custom_app_exception import AppBaseException
from src.utils.exceptions.error_codes import ErrorCode, ErrorCodeStatus,StatusCode
from src.utils.helpers import DBURL
from langchain_core.runnables import RunnableConfig
from src.utils.logger import logger
from src.agent.route_agent import RouteAgent
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

        
class ChatService:
    def __init__(self,error):
        self.error=error
        self.dburi=DBURL()
        self.route_agent=RouteAgent(self.error)
     
    async def homework_assistant(self,query:str,thread_id:str,difficulty_level:str,no_of_questions:int)->dict:
        try:
            async with AsyncPostgresSaver.from_conn_string(self.dburi._get_db_uri()) as checkpointer:
                await checkpointer.setup()
                logger.info(f"Service:Processing info for the thread-id : {thread_id} ")
                config = RunnableConfig(configurable={"thread_id": thread_id})
                result= await self.route_agent.route_agent(config,query,difficulty_level,no_of_questions,checkpointer)
                return result
        except AppBaseException:
            raise
        except Exception as e:
            logger.error("Error in Service file code_generator function")
            self.error.error(
                file_name="code_generator.py",
                function_name="code_generator",
                message=f"Error in generating code{e}"
            )
            raise AppBaseException(
                error_code=ErrorCodeStatus.get(ErrorCode.CHAT_PROCESSING_FAILED),
                message=f"Error in generating code{e}",
                status_code=StatusCode().INTERNAL_SERVER_ERROR_STATUS_CODE
            )


