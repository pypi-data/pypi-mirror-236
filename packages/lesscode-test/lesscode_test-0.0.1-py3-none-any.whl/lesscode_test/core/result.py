from typing import Any


class Result:
    def __init__(self, status_code: int, response: Any = None,
                 error: Any = None, is_success: bool = True):
        self.status_code = status_code
        self.response = response
        self.error = error
        self.is_success = is_success

    def __dict__(self):
        return {"status_code": self.status_code, "response": self.response,
                "error": self.error, "is_success": self.is_success,
                "retry_times": self.retry_times if hasattr(self, "retry_times") else 0,
                "is_skip": self.is_skip if hasattr(self, "is_skip") else False}
