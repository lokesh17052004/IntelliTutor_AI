from fastapi import APIRouter,Depends
from src.utils.helpers import thread_check
from src.utils.api_response import APIResponse
from src.models.model import ChatRequest
from src.service.homework_service import ChatService
from src.repository.error_repository import ErrorRepository
from src.utils.exceptions.custom_app_exception import AppBaseException
from src.utils.exceptions.error_codes import ErrorCode,ErrorCodeStatus,StatusCode
from src.utils.logger import logger
def depends(error:ErrorRepository = Depends(ErrorRepository)):
    return ChatService(error=error)

router=APIRouter(prefix="/api/v1",tags=["Homework Assistant Agent"])
@router.post("/chat")
async def homework_assistant(request:ChatRequest,service:ChatService=Depends(depends),error:ErrorRepository=Depends(ErrorRepository)):
    try:
        logger.info("In homework assistant Router File")
        thread_id=await thread_check(request)
        query=request.query.strip()
        if query and thread_id:
            logger.info("In homework assistant Router File:Request has been validated ")
            result= await service.homework_assistant(query,thread_id,request.difficulty_level,request.no_of_questions)
            return APIResponse(
                thread_id=str(thread_id),
                message=result,
                status_code=StatusCode().RESPONSE_GENERATED_STATUS_CODE
            )

        else:
            logger.error("User sent an empty values for message ")
            error.error(
                function_name="homework_assistant",
                file_name="router.py",
                message="User query can't be empty"
            )
            raise AppBaseException(
                error_code=ErrorCodeStatus.get(ErrorCode.CHAT_PROCESSING_FAILED),
                status_code= StatusCode().BAD_REQUEST,
                message= f"User message can't be empty"
            )

    except AppBaseException:
        raise
    except Exception as e:
        logger.error("Error in router file")
        error.error(
            function_name="homework_assistant",
            file_name="router.py",
            message=f"Router Error {e}"
        )
        raise AppBaseException(
            error_code=ErrorCodeStatus.get(ErrorCode.CHAT_PROCESSING_FAILED),
            status_code=StatusCode().INTERNAL_SERVER_ERROR_STATUS_CODE,
            message= f"Router error while generating quiz{e}"
        )
        