import unittest
from parameterized import parameterized

from src.layers.python.helpers.request_parsers import get_path_parameter, get_query_string, get_request_body


class TestRequestParsers(unittest.TestCase):
    @parameterized.expand([
        [None, "any-key", None],
        [{}, "any-key", None],
        [{"any-key": "any-value"}, "any-key", None],
        [{"pathParameters": None}, "any-key", None],
        [{"pathParameters": {}}, "any-key", None],
        [{"pathParameters": {"any-key": "any-value"}}, "any-key", "any-value"],
        [
            {
                "pathParameters": {
                    "any-string-key": "any-string-value",
                    "any-number-key": 1,
                    "any-boolean-key": True,
                    "any-null-key": None
                }
            },
            "any-string-key",
            "any-string-value"
        ]
    ])
    def test_get_path_parameter(self, event, name, expected_path_parameter):
        path_parameter = get_path_parameter(event=event, name=name)

        self.assertEqual(expected_path_parameter, path_parameter)

    @parameterized.expand([
        [None, "any-key"],
        [{}, "any-key"],
        [{"any-key": "any-value"}, "any-key"]
    ])
    def test_get_path_parameter_with_default(self, event, name):
        path_parameter = get_path_parameter(event=event, name=name, default="any-default-value")

        self.assertEqual("any-default-value", path_parameter)

    @parameterized.expand([
        [None, "any-key", None],
        [{}, "any-key", None],
        [{"any-key": "any-value"}, "any-key", None],
        [{"queryStringParameters": None}, "any-key", None],
        [{"queryStringParameters": {}}, "any-key", None],
        [{"queryStringParameters": {"any-key": "any-value"}}, "any-key", "any-value"],
        [
            {
                "queryStringParameters": {
                    "any-string-key": "any-string-value",
                    "any-number-key": 1,
                    "any-boolean-key": True,
                    "any-null-key": None
                }
            },
            "any-string-key",
            "any-string-value"
        ]
    ])
    def test_get_query_string(self, event, name, expected_query_string):
        query_string = get_query_string(event=event, name=name)

        self.assertEqual(expected_query_string, query_string)

    @parameterized.expand([
        [None, "any-key"],
        [{}, "any-key"],
        [{"any-key": "any-value"}, "any-key"]
    ])
    def test_get_query_string_with_default(self, event, name):
        query_string = get_query_string(event=event, name=name, default="any-default-value")

        self.assertEqual("any-default-value", query_string)

    @parameterized.expand([
        [None, {}],
        [{}, {}],
        [{"any-key": "any-value"}, {}],
        [{"body": None}, {}],
        [{"body": '{}'}, {}],
        [{"body": '{"any-key": "any-value"}'}, {"any-key": "any-value"}],
        [
            {
                "body": '{'
                        '"any-string-key": "any-string-value", '
                        '"any-number-key": 1, '
                        '"any-object-key": {}, '
                        '"any-array-key": [], '
                        '"any-boolean-key": true, '
                        '"any-null-key": null'
                        '}'
            },
            {
                "any-string-key": "any-string-value",
                "any-number-key": 1,
                "any-object-key": {},
                "any-array-key": [],
                "any-boolean-key": True,
                "any-null-key": None
            }
        ]
    ])
    def test_get_request_body(self, event, expected_body):
        body = get_request_body(event=event)

        self.assertEqual(expected_body, body)

    @parameterized.expand([
        [None],
        [{}],
        [{"any-key": "any-value"}]
    ])
    def test_get_request_body_with_default(self, event):
        body = get_request_body(event=event, default='{"any-default-key": "any-default-value"}')

        self.assertEqual({"any-default-key": "any-default-value"}, body)

    def test_get_request_body_when_parse_fails(self):
        invalid_event = {"body": "not-a-json"}

        with self.assertRaises(Exception) as error:
            get_request_body(event=invalid_event)

        self.assertEqual(f"Failed to parse '{invalid_event}' body from request!", str(error.exception))


if __name__ == '__main__':
    unittest.main()
