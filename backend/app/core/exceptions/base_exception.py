class AppException(Exception):
    def __int__(
            self,
            message: str,
            status_code: int = 400,
            error_code: str = "APP_ERROR",
            data = None
            ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.data = data

        super().__init__(message)