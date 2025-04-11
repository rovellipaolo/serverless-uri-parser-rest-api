import logging
from helpers.request_parsers import get_query_string, get_request_body
from helpers.response_factory import build_response, build_error_response
from helpers.uri_parser import UriParser


logger = logging.getLogger("uri-parser-rest-api.parse")
logger.setLevel(logging.INFO)


def handler(event, context):
    logger.debug("Event: %s", event)
    logger.debug("Context: %s", context)

    try:
        force = get_query_string(event=event, name="force", default="false") == "true"
        body = get_request_body(event=event)
        uri = body.get("uri")
        if not uri:
            raise ValueError("Missing 'uri' parameter in request!")

        uri_parser = UriParser(logger=logger)
        if not force and not uri_parser.is_valid(uri):
            raise ValueError(f"Not a valid URI: {uri}")

        info = uri_parser.parse(uri)
        return build_response(status=200, body=info)
    except ValueError as error:
        logger.error("Error: %s", str(error))
        return build_error_response(status=400, message=str(error))
    except Exception as error:
        logger.error("Error: %s", str(error))
        return build_error_response(status=500, message=str(error))
