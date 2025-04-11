import sys
import unittest
from parameterized import parameterized

# Inject helpers packages (in production this is done via Lambda layer):
sys.path.append("src/layers/python/")

# pylint: disable-next=wrong-import-position
from src.parse import handler  # noqa: E402


class TestHandler(unittest.TestCase):
    @parameterized.expand([
        # GENERIC
        [
            "127.0.0.1",
            "false",
            '{\n'
            '    "fragment": null,\n'
            '    "host": null,\n'
            '    "port": null,\n'
            '    "path": "127.0.0.1",\n'
            '    "query": null,\n'
            '    "raw": "127.0.0.1",\n'
            '    "scheme": null,\n'
            '    "userinfo": null\n'
            '}'
        ],
        [
            "domain.tld",
            "true",
            '{\n'
            '    "fragment": null,\n'
            '    "host": null,\n'
            '    "port": null,\n'
            '    "path": "domain.tld",\n'
            '    "query": null,\n'
            '    "raw": "domain.tld",\n'
            '    "scheme": null,\n'
            '    "userinfo": null\n'
            '}'
        ],
        [
            "username@domain.tld",
            "false",
            '{\n'
            '    "fragment": null,\n'
            '    "host": null,\n'
            '    "port": null,\n'
            '    "path": "username@domain.tld",\n'
            '    "query": null,\n'
            '    "raw": "username@domain.tld",\n'
            '    "scheme": null,\n'
            '    "userinfo": null\n'
            '}'
        ],
        # HTTP
        [
            "http://127.0.0.1",
            "false",
            '{\n'
            '    "fragment": null,\n'
            '    "host": "127.0.0.1",\n'
            '    "port": null,\n'
            '    "path": null,\n'
            '    "query": null,\n'
            '    "raw": "http://127.0.0.1",\n'
            '    "scheme": "http",\n'
            '    "userinfo": null\n'
            '}'
        ],
        [
            "http://domain.tld",
            "false",
            '{\n'
            '    "fragment": null,\n'
            '    "host": "domain.tld",\n'
            '    "port": null,\n'
            '    "path": null,\n'
            '    "query": null,\n'
            '    "raw": "http://domain.tld",\n'
            '    "scheme": "http",\n'
            '    "userinfo": null\n'
            '}'
        ],
        [
            "http://user:password@domain.tld:8080/path?key=value#fragment",
            "false",
            '{\n'
            '    "fragment": "fragment",\n'
            '    "host": "domain.tld",\n'
            '    "port": 8080,\n'
            '    "path": "/path",\n'
            '    "query": "key=value",\n'
            '    "raw": "http://user:password@domain.tld:8080/path?key=value#fragment",\n'
            '    "scheme": "http",\n'
            '    "userinfo": "user:password"\n'
            '}'
        ],
        # HTTPS
        [
            "https://127.0.0.1",
            "false",
            '{\n'
            '    "fragment": null,\n'
            '    "host": "127.0.0.1",\n'
            '    "port": null,\n'
            '    "path": null,\n'
            '    "query": null,\n'
            '    "raw": "https://127.0.0.1",\n'
            '    "scheme": "https",\n'
            '    "userinfo": null\n'
            '}'
        ],
        [
            "https://domain.tld",
            "false",
            '{\n'
            '    "fragment": null,\n'
            '    "host": "domain.tld",\n'
            '    "port": null,\n'
            '    "path": null,\n'
            '    "query": null,\n'
            '    "raw": "https://domain.tld",\n'
            '    "scheme": "https",\n'
            '    "userinfo": null\n'
            '}'
        ],
        [
            "https://user:password@domain.tld:8080/path?key=value#fragment",
            "false",
            '{\n'
            '    "fragment": "fragment",\n'
            '    "host": "domain.tld",\n'
            '    "port": 8080,\n'
            '    "path": "/path",\n'
            '    "query": "key=value",\n'
            '    "raw": "https://user:password@domain.tld:8080/path?key=value#fragment",\n'
            '    "scheme": "https",\n'
            '    "userinfo": "user:password"\n'
            '}'
        ],
        # FTP
        [
            "ftp://domain.tld",
            "false",
            '{\n'
            '    "fragment": null,\n'
            '    "host": "domain.tld",\n'
            '    "port": null,\n'
            '    "path": null,\n'
            '    "query": null,\n'
            '    "raw": "ftp://domain.tld",\n'
            '    "scheme": "ftp",\n'
            '    "userinfo": null\n'
            '}'
        ],
        # MAILTO
        [
            "mailto:username@domain.tld",
            "true",
            '{\n'
            '    "fragment": null,\n'
            '    "host": null,\n'
            '    "port": null,\n'
            '    "path": "username@domain.tld",\n'
            '    "query": null,\n'
            '    "raw": "mailto:username@domain.tld",\n'
            '    "scheme": "mailto",\n'
            '    "userinfo": null\n'
            '}'
        ]
    ])
    def test_handler(self, uri, force, expected_response_body):
        response = handler({"body": f'{{"uri": "{uri}"}}', "queryStringParameters": {"force": force}}, None)

        self.assertEqual(
            {
                "statusCode": 200,
                "body": expected_response_body
            },
            response
        )

    def test_handler_when_request_has_invalid_uri(self):
        invalid_uri = "not-a-uri"
        response = handler({"body": f'{{"uri": "{invalid_uri}"}}'}, None)

        self.assertEqual(
            {
                "statusCode": 400,
                "body": '{\n'
                        '    "error": "Bad Request",\n'
                        f'    "message": "Not a valid URI: {invalid_uri}"\n'
                        '}'
            },
            response
        )

    @parameterized.expand([
        [None],
        [{}],
        [{"body": '{}'}],
        [{"body": '{"uri": null}'}],
        [{"body": '{"uri": ""}'}]
    ])
    def test_handler_when_request_has_empty_body(self, event):
        response = handler(event, None)

        self.assertEqual(
            {
                "statusCode": 400,
                "body": '{\n'
                        '    "error": "Bad Request",\n'
                        '    "message": "Missing \'uri\' parameter in request!"\n'
                        '}'
            },
            response
        )

    @parameterized.expand([
        [{"body": {}}, "the JSON object must be str, bytes or bytearray, not dict"],
        [{"body": []}, "the JSON object must be str, bytes or bytearray, not list"]
    ])
    def test_handler_when_request_has_invalid_body(self, event, expected_error_message):
        response = handler(event, None)

        self.assertEqual(
            {
                "statusCode": 500,
                "body": '{\n'
                        '    "error": "Internal Server Error",\n'
                        f'    "message": "{expected_error_message}"\n'
                        '}'
            },
            response
        )


if __name__ == '__main__':
    unittest.main()
