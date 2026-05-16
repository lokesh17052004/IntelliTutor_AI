class ErrorCode:
    DB_CONNECTION_FAILED = "DatabaseConnectionFailedErrorCode"
    INTERNAL_SERVER_ERROR = "InternalServerErrorCode"
    CHAT_PROCESSING_FAILED = "ChatProcessingFailedErrorCode"
    AGENT_INVOKE_FAILED = "AgentInvokeFailedErrorCode"
    BUILD_GRAPH_FAILED="BuildGraphFailedErrorcode"
    INVALID_REQUEST = "InvalidRequestErrorCode"


ErrorCodeStatus = {
    ErrorCode.DB_CONNECTION_FAILED: "HA_DB_001",
    ErrorCode.INTERNAL_SERVER_ERROR: "HA_SYS_001",
    ErrorCode.CHAT_PROCESSING_FAILED: "HA_CHAT_001",
    ErrorCode.AGENT_INVOKE_FAILED: "HA_AGENT_001",
    ErrorCode.INVALID_REQUEST: "HA_REQ_001",
    ErrorCode.BUILD_GRAPH_FAILED:"HA_BG_001"
}

class StatusCode:
    INTERNAL_SERVER_ERROR_STATUS_CODE=500
    RESPONSE_GENERATED_STATUS_CODE=200
    BAD_REQUEST = 400
    UNPROCESSABLE_ENTITY = 422