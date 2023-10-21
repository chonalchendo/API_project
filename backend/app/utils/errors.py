from fastapi import HTTPException, status


class HandleErrors:
    @staticmethod
    def error_404(detail: str):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

    @staticmethod
    def error_500(error: Exception, detail: str = "Internal Server Error"):
        print(f"An error has occurred: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
        )


handle_errors = HandleErrors()
