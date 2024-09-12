from fastapi.responses import JSONResponse
from ..models.main import ErrorResponseModel
from starlette.middleware.base import BaseHTTPMiddleware
import logging

logger = logging.getLogger(__name__)

class ChangeResponseMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)

        if response.status_code == 403:
            body = b""
            async for chunk in response.body_iterator:
                body += chunk
            body = body.decode('utf-8').split(":")[1][1:-2] 
            body = ErrorResponseModel("wrong credentials", 403, body)
            return JSONResponse(content=body, status_code=403)
        return response