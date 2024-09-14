class ApiResponse:
    def __init__(self, status, data=None, message=None, error_code=None, status_code=200, details=None):
        self.status = status
        self.data = data
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details
        return self.to_dict()

    def to_dict(self):
        response = {
            "status": self.status,
            "data": self.data,
            "message": self.message,
            "error_code": self.error_code,
            "status_code": self.status_code,
            "details": self.details
        }
        # Remove None values from the response dictionary
        return {k: v for k, v in response.items() if v is not None}

    def __str__(self):
        return str(self.to_dict())
