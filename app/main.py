from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
from app.core.config import settings
from app.core.exceptions import FinanceBackendError
from app.schemas.common import ErrorResponse
from app.api.v1.router import api_router

app = FastAPI(
    title=settings.APP_NAME, 
    debug=settings.DEBUG,
    swagger_ui_init_oauth={
        "clientId": "swagger-ui",
        "usePkceWithAuthorizationCodeGrant": False,
    },
    openapi_components={
        "securitySchemes": {
            "ApiKeyAuth": {
                "type": "apiKey",
                "in": "header",
                "name": "Authorization",
                "description": "Enter your API key (access token) here. Use format: 'Bearer <token>' or just '<token>'"
            }
        }
    },
    openapi_security=[{"ApiKeyAuth": []}]
)

# API Key Security Scheme for Swagger
api_key_scheme = APIKeyHeader(name="Authorization", auto_error=False)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception Handler
@app.exception_handler(FinanceBackendError)
async def finance_backend_exception_handler(request: Request, exc: FinanceBackendError):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(detail=exc.message, code=exc.code).model_dump()
    )

app.include_router(api_router, prefix="/api/v1")
