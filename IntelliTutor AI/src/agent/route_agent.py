from src.models.model import State
from typing import Union
from langchain.agents import create_agent
from langgraph.types import Command
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain_core.messages import HumanMessage,SystemMessage
from src.utils.helpers import LLM
from src.models.model import ChatResponse,NormalResponse
from src.agent.prompts import SYSTEM_PROMPT_ROUTE_AGENT
from src.utils.exceptions.custom_app_exception import AppBaseException,AgentInvocationException
from src.utils.exceptions.error_codes import ErrorCode, ErrorCodeStatus,StatusCode
from src.utils.helpers import logger
from src.utils.constants import ROUTE_AGENT_TEMP,ROUTE_AGENT_TOKENS
from src.tools.tools import quiz_tool,review_tool
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
from typing import Callable

tools=[quiz_tool,review_tool]
STEP_CONFIG = {
    "quiz_agent":{
        "tools":[quiz_tool]
    },
    "solution_agent": {
        "tools": [review_tool],
    }
}

@wrap_model_call
async def apply_step_config(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse],
) -> ModelResponse:
    """Read current_step from state and apply matching tools."""
    current_step = request.state.get("current_step", "quiz_agent")
    step_cfg = STEP_CONFIG[current_step]
    request = request.override(
        tools=step_cfg["tools"],
    )
    return await handler(request)




class RouteAgent:
    def __init__(self,error):
        self.error=error
    async def route_agent(self,config,query,difficulty_level,no_of_questions,checkpointer)->dict:
        try:
            llm = await LLM(self.error).get_llm(max_tokens=ROUTE_AGENT_TOKENS,temperature= ROUTE_AGENT_TEMP)
            logger.info("LLM Client created for route_agent")
            hitl=HumanInTheLoopMiddleware(description_prefix="I need your approval to verify the answer",interrupt_on={"review_tool":True})
            agent=create_agent(
                model=llm,
                tools=tools,
                state_schema=State,
                checkpointer=checkpointer,
                response_format=NormalResponse,
                middleware=[apply_step_config,hitl],
                system_prompt=SystemMessage(content=SYSTEM_PROMPT_ROUTE_AGENT),
            )
            logger.info("Router Agent created successfully")
            contents=f"User query is {query} and the no of questions is {no_of_questions} and the difficulty level is {difficulty_level}"
            result= await agent.ainvoke({
                "messages":[HumanMessage(content=contents)]
            },config
            )
            logger.info("Route Agent Response Generated Successfully")
            if "__interrupt__" in result:
                print("Quiz question generated are \n")
                answers=[]
                logger.info(f"Total questions generated is  {len(result['quiz_questions'].questions)}")
                for i in range(0,len(result['quiz_questions'].questions)):
                    print("="*60)
                    q=result['quiz_questions'].questions[i]
                    print(f"Question no : {q.question_no}")
                    print(f"Question is: {q.question_text}")
                    print("Options are: ")
                    for option in q.options:
                        print(option)
                    print("\n ")  
                    answer=input("Type the options for the questions \n").strip().lower()
                    if answer=="a" or answer == "b" or answer=="c" or answer=="d":
                        answers.append(answer)
                    else:
                        answer=input("You must enter any one option \n").strip().lower()
                        answers.append(answer)
                    print("="*60)
                results=await agent.ainvoke(
                Command(
                    resume={"decisions":[{"type":"approve"}]},
                    update={
                        "quiz_answers":answers
                    })
                    ,config)
                response=results.get('final_response')
                quiz_data=results.get('quiz_questions')
                return {
                    "user_answer_per_question":answers,
                    "review":response.model_dump(),
                    "quiz":quiz_data.model_dump()}
            response=result.get('structured_response')
            return {"reply":response.model_dump()}

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


