from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

def add_exception_handlers(app: FastAPI):
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        errors = []
        for error in exc.errors():
            field = " -> ".join(str(loc) for loc in error['loc'])
            errors.append({
                "field": field,
                "message": error['msg'],
                "type": error['type']
            })
        
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "detail": "Data validation error",
                "errors": errors
            }
        )
    
    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": str(exc)}
        )