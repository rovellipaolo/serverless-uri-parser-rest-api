import json


def build_response(status: int = 200, body: dict | None = None) -> dict:
    if body is None:
        body = {}
    return {
        "statusCode": status,
        "body": json.dumps(body, indent=4),
    }


def build_error_response(status: int = 500, message: str = "") -> dict:
    error = "Unknown"
    match status:
        case 400:
            error = "Bad Request"
        case 404:
            error = "Not Found"
        case 500:
            error = "Internal Server Error"
    return build_response(
        status=status,
        body={
            "error": error,
            "message": message
        }
    )
