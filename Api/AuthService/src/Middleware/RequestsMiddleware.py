from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, DispatchFunction, RequestResponseEndpoint

from datetime import datetime, timedelta

from starlette.responses import Response
from starlette.types import ASGIApp


class LimitRequestsMiddleware(BaseHTTPMiddleware):
    
    LimitDuration = timedelta(minutes=1)
    LimitRequests = 6

    def __init__(self, app) -> None:
        super().__init__(app)
        self.requests = {}

    async def dispatch(self, request: Request, call_next) -> Response:
        UserIp = request.client.host

        CountRequests, LastRequest = self.requests.get(UserIp, (0, datetime.min))
        ElapsedTime = datetime.now() - LastRequest

        if ElapsedTime > self.LimitDuration:
            CountRequests = 1
        else:
            if CountRequests >= self.LimitRequests:
                return JSONResponse(
                    status_code = 429,
                    content = {'message': 'wowow, you send requests very fast, rest'}
                )
            CountRequests += 1
        self.requests[UserIp] = (CountRequests, datetime.now())

        response = await call_next(request)
        return response

        
            
