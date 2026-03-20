from fastapi.responses import JSONResponse, Response
from fastapi.requests import Request
from fastapi import status
from starlette.middleware.base import BaseHTTPMiddleware

class ErrorMiddlewareAPI(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as ex:
            mensaje=f"Error: {str(ex)}"
            codigo=status.HTTP_500_INTERNAL_SERVER_ERROR
            return JSONResponse(content=mensaje, status_code=codigo)