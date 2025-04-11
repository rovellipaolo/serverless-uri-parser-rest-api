import unittest
from parameterized import parameterized

from src.layers.python.helpers.response_factory import build_response, build_error_response


class TestResponseFactory(unittest.TestCase):
    @parameterized.expand([
        [200, None, {"statusCode": 200, "body": '{}'}],
        [300, None, {"statusCode": 300, "body": '{}'}],
        [400, None, {"statusCode": 400, "body": '{}'}],
        [500, None, {"statusCode": 500, "body": '{}'}],
        [200, {}, {"statusCode": 200, "body": '{}'}],
        [300, {}, {"statusCode": 300, "body": '{}'}],
        [400, {}, {"statusCode": 400, "body": '{}'}],
        [500, {}, {"statusCode": 500, "body": '{}'}],
        [200, {"any-key": "any-value"}, {"statusCode": 200, "body": '{\n    "any-key": "any-value"\n}'}],
        [300, {"any-key": "any-value"}, {"statusCode": 300, "body": '{\n    "any-key": "any-value"\n}'}],
        [400, {"any-key": "any-value"}, {"statusCode": 400, "body": '{\n    "any-key": "any-value"\n}'}],
        [500, {"any-key": "any-value"}, {"statusCode": 500, "body": '{\n    "any-key": "any-value"\n}'}],
        [
            200,
            {
                "any-string-key": "any-string-value",
                "any-number-key": 1,
                "any-object-key": {},
                "any-array-key": [],
                "any-boolean-key": True,
                "any-null-key": None
            },
            {
                "statusCode": 200,
                "body": '{\n'
                        '    "any-string-key": "any-string-value",\n'
                        '    "any-number-key": 1,\n'
                        '    "any-object-key": {},\n'
                        '    "any-array-key": [],\n'
                        '    "any-boolean-key": true,\n'
                        '    "any-null-key": null\n'
                        '}'
            }
        ]
    ])
    def test_build_response(self, status, body, expected_response):
        response = build_response(status=status, body=body)

        self.assertEqual(expected_response, response)

    @parameterized.expand([
        [
            400,
            "any-error-message",
            {
                "statusCode": 400,
                "body": '{\n    "error": "Bad Request",\n    "message": "any-error-message"\n}'
            }
        ],
        [
            404,
            "any-error-message",
            {
                "statusCode": 404,
                "body": '{\n    "error": "Not Found",\n    "message": "any-error-message"\n}'
            }
        ],
        [
            500,
            "any-error-message",
            {
                "statusCode": 500,
                "body": '{\n    "error": "Internal Server Error",\n    "message": "any-error-message"\n}'
            }
        ],
        [
            600,
            "any-error-message",
            {
                "statusCode": 600,
                "body": '{\n    "error": "Unknown",\n    "message": "any-error-message"\n}'
            }
        ]
    ])
    def test_build_error_response(self, status, message, expected_response):
        response = build_error_response(status=status, message=message)

        self.assertEqual(expected_response, response)


if __name__ == '__main__':
    unittest.main()
