from fastapi import HTTPException, status


class Errors:
    not_found_error = HTTPException(
        detail="Not found",
        status_code=status.HTTP_404_NOT_FOUND
    )