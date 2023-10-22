from datetime import datetime
from typing import List

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from fastutils_hmarcuzzo.common.custom_error_response import custom_error_response
from fastutils_hmarcuzzo.common.dto.exception_response_dto import (
    DetailResponseDto,
    ExceptionResponseDto,
)
from fastutils_hmarcuzzo.types.exceptions import (
    BadRequestException,
    NotFoundException,
    UnauthorizedException,
    ForbiddenException,
)


class HttpExceptionsHandler:
    def __init__(self, app: FastAPI):
        self.app = app
        self.add_exceptions_handler()
        custom_error_response(app)

    def add_exceptions_handler(self):
        @self.app.exception_handler(StarletteHTTPException)
        async def http_exception_handler(request: Request, exc) -> JSONResponse:
            return JSONResponse(
                status_code=exc.status_code,
                content=self.global_exception_error_message(
                    status_code=exc.status_code,
                    detail=DetailResponseDto(
                        loc=[], msg=exc.detail, type="starlette_http_exception"
                    ),
                    request=request,
                ).model_dump(),
            )

        @self.app.exception_handler(RequestValidationError)
        async def validation_exception_handler(
            request: Request, exc: RequestValidationError
        ) -> JSONResponse:
            return JSONResponse(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                content=self.global_exception_error_message(
                    status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=[DetailResponseDto(**detail) for detail in exc.errors()],
                    request=request,
                ).model_dump(),
            )

        @self.app.exception_handler(BadRequestException)
        @self.app.exception_handler(UnauthorizedException)
        @self.app.exception_handler(ForbiddenException)
        @self.app.exception_handler(NotFoundException)
        async def custom_exceptions_handler(
            request: Request, exc: BadRequestException
        ) -> JSONResponse:
            detail_dict = exc.__dict__
            detail_dict.pop("status_code", None)

            return JSONResponse(
                status_code=exc.status_code,
                content=self.global_exception_error_message(
                    status_code=exc.status_code,
                    detail=DetailResponseDto(**detail_dict),
                    request=request,
                ).model_dump(),
            )

    @staticmethod
    def global_exception_error_message(
        status_code: int,
        detail: DetailResponseDto | List[DetailResponseDto],
        request: Request,
    ) -> ExceptionResponseDto:
        if not isinstance(detail, List):
            detail = [detail]

        return ExceptionResponseDto(
            detail=detail,
            status_code=status_code,
            timestamp=datetime.now().astimezone(),
            path=request.url.path,
            method=request.method,
        )
