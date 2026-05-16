from pydantic import BaseModel,Field
from typing import Union,Optional
from uuid import uuid4
from typing_extensions import Literal
from langchain.agents import AgentState
class ChatRequest(BaseModel):
    query:str
    thread_id:Optional[str]=None
    difficulty_level:Literal["easy","medium","hard"]=Field(default="easy")
    no_of_questions:int=Field(default=5)

class Question(BaseModel):
    question_no: int
    question_text: str
    options: list[str]= Field(min_length=4,     max_length=4,description=(
    "REQUIRED: Exactly 4 answer options ... "
    "Each option MUST be prefixed: 'a) ...', 'b) ...', 'c) ...', 'd) ...'. "
    "This list must NEVER be empty."
    )
)

class Quizquestions(BaseModel):
    questions:list[Question]

class ReviewResponse(BaseModel):
    assessment_score:int
    percentage:float
    assessment_feedback_per_question:list[str]

class State(AgentState):
    current_step:list   
    quiz_questions:Quizquestions
    quiz_answers:list[str]
    final_response:ReviewResponse   
class ChatResponse(BaseModel):
    """
    Use this response model
    if the user query is to generate the quiz on a specific educational topic
    """
    user_answer_per_question:list[str]
    review:ReviewResponse
    quiz:Quizquestions

class NormalResponse(BaseModel):
    """
    Use this response model
    if user prompt is out of context(eg.,generate me quiz on movies),the user query is incomplete(eg.,generate me a quiz on) use str
    if user prompt is related to quiz use ChatResponse 
    """
    reply:Union[str,ChatResponse]