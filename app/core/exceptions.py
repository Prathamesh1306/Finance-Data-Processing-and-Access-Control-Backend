class FinanceBackendError(Exception):
    def __init__(self, status_code: int, code: str, message: str):
        self.status_code = status_code
        self.code = code
        self.message = message
        super().__init__(self.message)

class NotFoundError(FinanceBackendError):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(status_code=404, code="not_found", message=message)

class ConflictError(FinanceBackendError):
    def __init__(self, message: str = "Resource conflict"):
        super().__init__(status_code=409, code="conflict", message=message)

class ForbiddenError(FinanceBackendError):
    def __init__(self, message: str = "Forbidden access"):
        super().__init__(status_code=403, code="forbidden", message=message)

class UnauthorizedError(FinanceBackendError):
    def __init__(self, message: str = "Unauthorized access"):
        super().__init__(status_code=401, code="unauthorized", message=message)

class ValidationError(FinanceBackendError):
    def __init__(self, message: str = "Validation error"):
        super().__init__(status_code=422, code="validation_error", message=message)
