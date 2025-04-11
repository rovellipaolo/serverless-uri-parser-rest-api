import json
from json import JSONDecodeError


def get_path_parameter(event: dict | None, name: str, default: str | None = None) -> str | None:
    parameters = event.get("pathParameters", {}) if event is not None else {}
    return parameters.get(name, default) if parameters is not None else default


def get_query_string(event: dict | None, name: str, default: str | None = None) -> str | None:
    parameters = event.get("queryStringParameters", {}) if event is not None else {}
    return parameters.get(name, default) if parameters is not None else default


def get_request_body(event: dict | None, default: str = "{}") -> dict:
    try:
        body = event.get("body", default) if event is not None else default
        return json.loads(body) if body is not None else {}
    except JSONDecodeError as error:
        raise ValueError(f"Failed to parse '{event}' body from request!") from error
